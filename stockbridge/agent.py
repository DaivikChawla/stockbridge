"""The Stockbridge route agent.

One cycle: read the twin -> find stock that won't sell -> plan moves -> ask every owner ->
commit what both sides approve -> re-plan around any "no" or "only 3" -> draft the paperwork
-> build the delivery route. Every step is written to a trace, with the reason.

Hard rules the agent never breaks (checked in code, not left to a model):
- every move needs a yes from the shop giving the stock and the shop receiving it;
- no move that would leave the stock less than `min_sell_days` to sell at the receiver;
- no receiver goes over its weekly budget;
- a receiver's offer only mentions its own sales, never another shop's;
- documents are drafts; an accountant posts them.
"""
from __future__ import annotations

import datetime as dt
import math
import time
from dataclasses import dataclass, field

from .catalogue import BY_ID
from .planner import Move, plan
from .twin import RouteTwin

BASE_DATE = dt.date(2026, 12, 7)


def day_str(day: int) -> str:
    return (BASE_DATE + dt.timedelta(days=day)).strftime("%d %b")


@dataclass
class Request:
    id: str
    kind: str  # "give" (to the shop holding the stock) or "take" (to the receiving shop)
    shop_id: str
    lot_id: str
    item_id: str
    qty: int
    mode: str
    unit_price: int
    message: str
    round: int
    status: str = "pending"  # pending | accepted | partial | declined | cancelled
    accepted_qty: int = 0
    move_index: int | None = None

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class RouteAgent:
    twin: RouteTwin
    trace: list[dict] = field(default_factory=list)
    requests: dict[str, Request] = field(default_factory=dict)
    moves: list[Move] = field(default_factory=list)  # proposed in the current round
    committed: list[dict] = field(default_factory=list)
    documents: list[dict] = field(default_factory=list)
    declined: set[tuple[str, str]] = field(default_factory=set)  # memory: (shop, item) said no
    caps: dict[tuple[str, str], int] = field(default_factory=dict)  # memory: (shop, item) said "only n"
    locked_lots: set[str] = field(default_factory=set)  # holder said no to giving this lot
    round: int = 0
    _seq: int = 0
    _t0: float = field(default_factory=time.time)

    # ---------- trace ----------
    def log(self, step: str, msg: str, **data) -> None:
        self.trace.append({"t": round(time.time() - self._t0, 2), "step": step, "msg": msg, **data})

    # ---------- the cycle ----------
    def run_cycle(self) -> list[Request]:
        risk = self.twin.at_risk()
        total = sum(r["value_at_risk"] for r in risk)
        self.log("detect", f"{len(risk)} lots will not sell before expiry, ₹{total:,} at risk.")
        for r in risk:
            if r["mode"] in ("claim", "expired") and not any(d["lot_id"] == r["lot_id"] for d in self.documents if d["type"] == "brand_claim"):
                it = BY_ID[r["item_id"]]
                self.log("refuse", f"Won't move {it.label} at {self.shop(r['shop_id'])}: {r['days_to_expiry']} days left, "
                         f"it would expire on the next shelf too. Drafting a brand claim instead.", lot_id=r["lot_id"])
                self._doc("brand_claim", r["shop_id"], r["item_id"], r["batch"], r["unsold"], it.unit_cost, lot_id=r["lot_id"])
        return self._plan_round()

    def _plan_round(self) -> list[Request]:
        self.round += 1
        t = time.time()
        lots = [r for r in self.twin.at_risk() if r["lot_id"] not in self.locked_lots]
        moves, _ = plan(self.twin, excluded=self.declined, caps=self.caps, lots=lots)
        self.moves = moves
        ms = int((time.time() - t) * 1000)
        if not moves:
            self.log("plan", f"Round {self.round}: nothing more can be moved safely ({ms} ms).")
            return []
        self.log("plan", f"Round {self.round}: {len(moves)} moves planned in {ms} ms "
                 f"(OR-Tools, within each shop's budget and selling speed).",
                 moves=[m.to_dict() for m in moves])
        new: list[Request] = []
        by_lot: dict[str, list[int]] = {}
        for i, m in enumerate(moves):
            by_lot.setdefault(m.lot_id, []).append(i)
        for lot_id, idxs in by_lot.items():
            m0 = moves[idxs[0]]
            total = sum(moves[i].qty for i in idxs)
            give = self._request("give", m0.from_shop, m0, total, None)
            if self._consent_left(lot_id) >= total:
                # The holder already agreed to give this lot earlier; don't ask twice.
                give.status, give.accepted_qty = "accepted", total
                self.log("memory", f"{self.shop(m0.from_shop)} already agreed to give this stock; not asking again.")
            else:
                new.append(give)
            for i in idxs:
                new.append(self._request("take", moves[i].to_shop, moves[i], moves[i].qty, i))
        for r in new:
            self.log("ask", f"Asked {self.shop(r.shop_id)} in the app: {r.message}", request_id=r.id)
        return new

    def _request(self, kind: str, shop_id: str, m: Move, qty: int, move_index: int | None) -> Request:
        self._seq += 1
        rid = f"R{self._seq}"
        req = Request(rid, kind, shop_id, m.lot_id, m.item_id, qty, m.mode, m.unit_price,
                      self._message(kind, shop_id, m, qty), self.round, move_index=move_index)
        self.requests[rid] = req
        return req

    def _message(self, kind: str, shop_id: str, m: Move, qty: int) -> str:
        it = BY_ID[m.item_id]
        exp = day_str(self.twin.today + m.days_to_expiry)
        if kind == "give":
            if m.mode == "take_back":
                return (f"{qty} × {it.label} (batch {m.batch}, expiry {exp}) won't sell here before expiry. "
                        f"Return them on Tuesday's visit? Credit note ₹{qty * it.unit_cost:,}.")
            return (f"{qty} × {it.label} (expiry {exp}) is past the return window. A nearby shop needs it. "
                    f"Sell at ₹{m.unit_price} each (₹{qty * m.unit_price:,})?")
        weekly = self.twin.rate(shop_id, m.item_id) * 7
        # Privacy rule: the receiver only sees its own sales, never the giving shop's.
        if m.mode == "take_back":
            return (f"{qty} × {it.label}, expiry {exp}. You sell about {weekly:.0f} a week. "
                    f"Add to Thursday's order at ₹{m.unit_price} each?")
        return (f"{qty} × {it.label} at clearance price ₹{m.unit_price} (distributor ₹{it.unit_cost}), expiry {exp}. "
                f"You sell about {weekly:.0f} a week. Accept for Thursday?")

    # ---------- answers from owners ----------
    def respond(self, request_id: str, accept_qty: int) -> list[Request]:
        """An owner answered in the app. Returns any new requests from a re-plan."""
        req = self.requests[request_id]
        if req.status != "pending":
            return []
        accept_qty = max(0, min(int(accept_qty), req.qty))
        req.accepted_qty = accept_qty
        req.status = "accepted" if accept_qty == req.qty else ("declined" if accept_qty == 0 else "partial")
        who = self.shop(req.shop_id)
        it = BY_ID[req.item_id]
        if req.kind == "give":
            if req.status == "declined":
                self.locked_lots.add(req.lot_id)
                self.log("decline", f"{who} wants to keep {it.label}. Cancelling its offers.")
                for r in self._round_requests():
                    if r.kind == "take" and r.lot_id == req.lot_id and r.status == "pending":
                        r.status = "cancelled"
            else:
                self.log("approve", f"{who} agreed to give {accept_qty} × {it.label}.")
        else:
            if req.status == "declined":
                self.declined.add((req.shop_id, req.item_id))
                self.log("decline", f"{who} said no to {it.label}. Remembered; will not offer it again this cycle.")
            elif req.status == "partial":
                self.caps[(req.shop_id, req.item_id)] = 0  # took what it wanted; don't re-offer more now
                self.log("partial", f"{who} accepted only {accept_qty} of {req.qty} × {it.label}.")
            else:
                self.log("approve", f"{who} accepted {accept_qty} × {it.label}.")
        self._commit_ready()
        if all(r.status != "pending" for r in self._round_requests()):
            needs_replan = any(r.status in ("declined", "partial") for r in self._round_requests() if r.kind == "take")
            if needs_replan:
                t = time.time()
                new = self._plan_round()
                self.log("replan", f"Re-planned in {time.time() - t:.2f} s around the answers.")
                return new
            self.log("done", "All owners answered. Plan complete.")
        return []

    def _consent_left(self, lot_id: str) -> int:
        """Units the holder agreed to give in earlier rounds that are not yet committed."""
        agreed = sum(r.accepted_qty for r in self.requests.values()
                     if r.kind == "give" and r.lot_id == lot_id and r.round < self.round and r.status in ("accepted", "partial"))
        used = sum(c["qty"] for c in self.committed if c["lot_id"] == lot_id)
        return agreed - used

    def _round_requests(self) -> list[Request]:
        return [r for r in self.requests.values() if r.round == self.round]

    def _commit_ready(self) -> None:
        for take in self._round_requests():
            if take.kind != "take" or take.status not in ("accepted", "partial") or getattr(take, "_done", False):
                continue
            give = next((r for r in self._round_requests() if r.kind == "give" and r.lot_id == take.lot_id), None)
            if not give or give.status not in ("accepted", "partial"):
                continue
            already = sum(c["qty"] for c in self.committed if c["lot_id"] == take.lot_id and c["round"] == self.round)
            qty = min(take.accepted_qty, give.accepted_qty - already)
            if qty <= 0:
                continue
            m = self.moves[take.move_index]
            self.twin.move_units(m.lot_id, m.to_shop, qty)
            self.twin.shops[m.to_shop].spent_this_week += qty * m.unit_price
            c = {"lot_id": m.lot_id, "item_id": m.item_id, "batch": m.batch, "from": m.from_shop, "to": m.to_shop,
                 "qty": qty, "mode": m.mode, "unit_price": m.unit_price, "round": self.round}
            self.committed.append(c)
            take._done = True  # type: ignore[attr-defined]
            it = BY_ID[m.item_id]
            if m.mode == "take_back":
                self._doc("credit_note", m.from_shop, m.item_id, m.batch, qty, it.unit_cost)
                self._doc("invoice", m.to_shop, m.item_id, m.batch, qty, m.unit_price)
            else:
                self._doc("clearance_bill", m.from_shop, m.item_id, m.batch, qty, m.unit_price, buyer=m.to_shop)
            self.log("commit", f"{qty} × {it.label}: {self.shop(m.from_shop)} → {self.shop(m.to_shop)} "
                     f"({'credit note + fresh invoice' if m.mode == 'take_back' else 'clearance sale'}). Added to Thursday's route.")

    # ---------- outputs ----------
    def _doc(self, kind: str, shop_id: str, item_id: str, batch: str, qty: int, unit: int, **extra) -> None:
        prefix = {"credit_note": "CN", "invoice": "INV", "clearance_bill": "CLR", "brand_claim": "CLM"}[kind]
        n = sum(1 for d in self.documents if d["type"] == kind) + 101
        self.documents.append({"type": kind, "no": f"{prefix}-{n}", "shop_id": shop_id, "shop": self.shop(shop_id),
                               "item": BY_ID[item_id].label, "batch": batch, "qty": qty, "unit": unit,
                               "amount": qty * unit, "status": "DRAFT: accountant to post", **extra})

    def route(self) -> list[dict]:
        """Delivery stops: pick-ups first, then drops, each in nearest-next order from the depot."""
        pick, drop = {}, {}
        for c in self.committed:
            pick.setdefault(c["from"], []).append(c)
            drop.setdefault(c["to"], []).append(c)
        stops, pos = [], self.twin.depot
        for kind, group in (("pick up", pick), ("drop", drop)):
            left = set(group)
            while left:
                sid = min(left, key=lambda s: math.hypot(self.twin.shops[s].x - pos[0], self.twin.shops[s].y - pos[1]))
                left.remove(sid)
                pos = (self.twin.shops[sid].x, self.twin.shops[sid].y)
                qty: dict[str, int] = {}
                for c in group[sid]:
                    qty[c["item_id"]] = qty.get(c["item_id"], 0) + c["qty"]
                stops.append({"stop": len(stops) + 1, "shop_id": sid, "shop": self.shop(sid), "action": kind,
                              "items": [f"{q} × {BY_ID[i].label}" for i, q in qty.items()]})
        return stops

    def shop(self, sid: str) -> str:
        return self.twin.shops[sid].name

    def state(self) -> dict:
        return {
            "round": self.round,
            "pending": [r.to_dict() | {"shop": self.shop(r.shop_id)} for r in self.requests.values() if r.status == "pending"],
            "committed": self.committed, "documents": self.documents, "route": self.route(),
            "trace": self.trace[-40:], "memory": {"declined": sorted(map(list, self.declined))},
        }

    def auto_answer(self, decide) -> None:
        """Run the whole cycle with a function standing in for owners: decide(request) -> accepted qty."""
        pending = [r for r in self.requests.values() if r.status == "pending"]
        guard = 0
        while pending and guard < 200:
            guard += 1
            r = pending.pop(0)
            if r.status != "pending":
                continue
            self.respond(r.id, decide(r))
            pending = [x for x in self.requests.values() if x.status == "pending"]
