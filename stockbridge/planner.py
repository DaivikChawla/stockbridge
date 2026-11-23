"""Plan which at-risk stock goes to which shop.

For every lot that will not sell before it expires, find shops on the same route that sell
the item fast enough to finish it before expiry, can absorb it within their weekly budget,
and have not declined this kind of offer before. Solved as a small integer program with
Google OR-Tools CP-SAT; a greedy fallback gives the same structure if OR-Tools is missing.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from .catalogue import BY_ID
from .twin import RouteTwin

try:
    from ortools.sat.python import cp_model
except ImportError:  # pragma: no cover
    cp_model = None


@dataclass
class Move:
    lot_id: str
    item_id: str
    batch: str
    from_shop: str
    to_shop: str
    qty: int
    mode: str  # "take_back" (credit note + fresh invoice) or "clearance" (shop-to-shop at a discount)
    unit_price: int  # what the receiving shop pays per unit
    days_to_expiry: int

    def to_dict(self) -> dict:
        return self.__dict__.copy()


def _dist(twin: RouteTwin, a: str, b: str) -> float:
    sa, sb = twin.shops[a], twin.shops[b]
    return math.hypot(sa.x - sb.x, sa.y - sb.y)


def unit_price(twin: RouteTwin, item_id: str, mode: str) -> int:
    it = BY_ID[item_id]
    if mode == "clearance":
        return max(1, int(round(it.unit_cost * twin.policy.clearance_discount)))
    return it.unit_cost


def plan(twin: RouteTwin, excluded: set[tuple[str, str]] | None = None,
         caps: dict[tuple[str, str], int] | None = None, lots: list[dict] | None = None) -> tuple[list[Move], list[dict]]:
    """Return (moves, refusals).

    excluded: (shop_id, item_id) pairs the agent must not offer to (they declined).
    caps: (shop_id, item_id) -> max units this shop agreed to take ("only 3").
    """
    excluded = excluded or set()
    caps = caps or {}
    risk = lots if lots is not None else twin.at_risk()
    refusals = [r for r in risk if r["mode"] in ("claim", "expired")]
    movable = [r for r in risk if r["mode"] in ("take_back", "clearance")]

    # Candidate (lot, receiver) pairs with their per-pair limit.
    pairs: list[tuple[int, str, int]] = []
    for li, r in enumerate(movable):
        sell_days = r["days_to_expiry"] - twin.policy.lead_days
        for sid in twin.shops:
            if sid == r["shop_id"] or (sid, r["item_id"]) in excluded:
                continue
            cap = twin.extra_capacity(sid, r["item_id"], sell_days)
            if (sid, r["item_id"]) in caps:
                cap = min(cap, caps[(sid, r["item_id"])])
            cap = min(cap, r["unsold"])
            if cap > 0:
                pairs.append((li, sid, cap))

    if not pairs:
        return [], refusals

    x = _solve(twin, movable, pairs) if cp_model else _greedy(twin, movable, pairs)
    moves = []
    for (li, sid, _), q in zip(pairs, x):
        if q <= 0:
            continue
        r = movable[li]
        moves.append(Move(r["lot_id"], r["item_id"], r["batch"], r["shop_id"], sid, int(q), r["mode"],
                          unit_price(twin, r["item_id"], r["mode"]), r["days_to_expiry"]))
    return moves, refusals


def _solve(twin: RouteTwin, movable: list[dict], pairs: list[tuple[int, str, int]]) -> list[int]:
    m = cp_model.CpModel()
    xs = [m.NewIntVar(0, cap, f"x{k}") for k, (_, _, cap) in enumerate(pairs)]
    # A lot cannot give more than its unsold units.
    for li, r in enumerate(movable):
        m.Add(sum(xs[k] for k, p in enumerate(pairs) if p[0] == li) <= r["unsold"])
    # A receiver cannot take more of an item than it can sell, or spend beyond its weekly budget.
    for sid, shop in twin.shops.items():
        ks = [k for k, p in enumerate(pairs) if p[1] == sid]
        if not ks:
            continue
        m.Add(sum(xs[k] * unit_price(twin, movable[pairs[k][0]]["item_id"], movable[pairs[k][0]]["mode"]) for k in ks)
              <= shop.budget_left)
        for item in {movable[pairs[k][0]]["item_id"] for k in ks}:
            kk = [k for k in ks if movable[pairs[k][0]]["item_id"] == item]
            sell_days = min(movable[pairs[k][0]]["days_to_expiry"] for k in kk) - twin.policy.lead_days
            m.Add(sum(xs[k] for k in kk) <= twin.extra_capacity(sid, item, sell_days))
    # Maximise value saved; prefer nearby shops; small penalty per receiver keeps trips few.
    uses = [m.NewBoolVar(f"u{k}") for k in range(len(pairs))]
    for k, (_, _, cap) in enumerate(pairs):
        m.Add(xs[k] <= cap * uses[k])
    value = sum(xs[k] * BY_ID[movable[li]["item_id"]].unit_cost * 10 for k, (li, _, _) in enumerate(pairs))
    trip = sum(uses[k] * int(20 + 10 * _dist(twin, movable[li]["shop_id"], sid)) for k, (li, sid, _) in enumerate(pairs))
    # Prefer the shop that sells it faster: the stock is gone sooner and safer.
    speed = sum(xs[k] * int(100 * twin.rate(sid, movable[li]["item_id"])) for k, (li, sid, _) in enumerate(pairs))
    m.Maximize(value + speed - trip)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 2.0
    solver.parameters.num_workers = 4
    status = solver.Solve(m)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return _greedy(twin, movable, pairs)
    return [solver.Value(v) for v in xs]


def _greedy(twin: RouteTwin, movable: list[dict], pairs: list[tuple[int, str, int]]) -> list[int]:
    left = {li: r["unsold"] for li, r in enumerate(movable)}
    budget = {sid: s.budget_left for sid, s in twin.shops.items()}
    taken: dict[tuple[str, str], int] = {}
    order = sorted(range(len(pairs)), key=lambda k: (-BY_ID[movable[pairs[k][0]]["item_id"]].unit_cost,
                                                     _dist(twin, movable[pairs[k][0]]["shop_id"], pairs[k][1])))
    x = [0] * len(pairs)
    for k in order:
        li, sid, cap = pairs[k]
        r = movable[li]
        price = unit_price(twin, r["item_id"], r["mode"])
        room = twin.extra_capacity(sid, r["item_id"], r["days_to_expiry"] - twin.policy.lead_days) - taken.get((sid, r["item_id"]), 0)
        q = max(0, min(cap, left[li], room, budget[sid] // price))
        x[k] = q
        left[li] -= q
        budget[sid] -= q * price
        taken[(sid, r["item_id"])] = taken.get((sid, r["item_id"]), 0) + q
    return x
