"""Backtest on a SYNTHETIC route: 40 shops, 90 days. Does the agent cut expired stock?

Every number here comes from simulated data, not from real shops. The point is to test the
agent's logic end to end under messy conditions, not to claim real-world savings.

World:
- Each shop sells each item at its own true daily rate (Poisson demand). Some shops don't stock some items.
- The distributor restocks weekly in whole cases (24 biscuits, 6 health drinks...). Slow shops end up
  holding a full case they can't finish: that's how stock gets stranded in real life.
- The shop app has captured 28 days of sales before day 0; the twin's rate is the last 28 days.
- Opening stock and restocks arrive part-aged (distributor stock is 20-50% through its shelf life).
- The agent only acts on lots expiring within 90 days.
- On day 30, demand shifts: about 15% of shop-items drop by 60% and 10% rise by 80% (a school closes,
  a competitor opens). The twin only sees this through captured sales (rolling average).

Two policies on the same seeded world:
- baseline: no movement between shops; stock that expires is written off.
- stockbridge: every route day the agent runs a full cycle. Simulated owners answer each request:
  holders agree 90% of the time; receivers accept 70%, accept half 15%, decline 15%.
  Each week's budget resets.

Usage: python -m evals.backtest [--seeds 5]
"""
from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

from stockbridge.agent import RouteAgent
from stockbridge.catalogue import BY_ID, ITEMS
from stockbridge.twin import Lot, Policy, RouteTwin, Shop

CASE = {"biscuits": 24, "home care": 24, "noodles": 24, "health drinks": 6, "staples": 10, "personal care": 12,
        "snacks": 24, "chocolates": 24, "spreads": 6}
ITEMSET = [it for it in ITEMS if it.category != "bakery"]
DAYS, N_SHOPS, ROUTE_EVERY, WARMUP = 90, 40, 7, 28


def poisson(rng: random.Random, lam: float) -> int:
    if lam <= 0:
        return 0
    l, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= rng.random()
        if p <= l:
            return k
        k += 1


def build_world(seed: int):
    rng = random.Random(seed)
    shops = {}
    for i in range(N_SHOPS):
        sid = f"s{i:02d}"
        shops[sid] = Shop(sid, f"Shop {i + 1}", rng.uniform(0, 8), rng.uniform(0, 8), rng.choice([4000, 6000, 8000]))
    true_rate = {}
    for sid in shops:
        for it in ITEMSET:
            if rng.random() < 0.55:  # this shop stocks the item
                base = {"health drinks": 0.15, "spreads": 0.12, "personal care": 0.3, "staples": 0.5}.get(it.category, 1.2)
                true_rate[(sid, it.id)] = base * rng.lognormvariate(0, 0.8)
    shift = {}
    for k in true_rate:
        u = rng.random()
        shift[k] = 0.4 if u < 0.15 else (1.8 if u < 0.25 else 1.0)
    # Opening stock: one or two cases at random ages.
    lots, n = [], 0
    for (sid, iid), r in true_rate.items():
        it = BY_ID[iid]
        for _ in range(rng.choice([1, 1, 2])):
            n += 1
            age = rng.randint(0, int(it.shelf_life_days * 0.85))
            lots.append(Lot(f"O{n}", sid, iid, f"B{n:04d}", CASE[it.category], it.shelf_life_days - age))
    return shops, true_rate, shift, lots


def run(seed: int, use_agent: bool) -> dict:
    shops, true_rate, shift, lots = build_world(seed)
    rng = random.Random(seed * 1000 + 1)
    owner = random.Random(seed * 7 + 3)
    twin = RouteTwin("Synthetic route", (4.0, 4.0), shops, lots,
                     {k: 0.0 for k in true_rate}, policy=Policy(clearance_discount=0.6))
    # Warm-up: the shop app has already captured 28 days of sales before day 0.
    history: dict[tuple[str, str], list[int]] = {k: [poisson(rng, r) for _ in range(WARMUP)] for k, r in true_rate.items()}
    for k, h in history.items():
        twin.rates[k] = sum(h) / len(h)
    agent = RouteAgent(twin) if use_agent else None
    out = {"expired_units": 0, "expired_value": 0, "lost_units": 0, "lost_value": 0, "sold_units": 0,
           "moved_units": 0, "moves": 0, "claims": 0, "owner_requests": 0, "lot_seq": 0}

    def decide(req) -> int:
        out["owner_requests"] += 1
        if req.kind == "give":
            return req.qty if owner.random() < 0.9 else 0
        u = owner.random()
        return req.qty if u < 0.7 else (req.qty // 2 if u < 0.85 else 0)

    for day in range(DAYS):
        twin.today = day
        # 1) Sales (true demand, FEFO). Rates the twin sees = last 14 days of captured sales.
        for k, r in true_rate.items():
            lam = r * (shift[k] if day >= 30 else 1.0)
            want = poisson(rng, lam)
            have = twin.stock(*k)
            sold = min(want, have)
            left = sold
            for lot in twin.shop_lots(*k):
                if lot.expiry_day <= day:
                    continue
                t = min(lot.qty, left)
                lot.qty -= t
                left -= t
                if not left:
                    break
            sold -= left
            out["sold_units"] += sold
            lost = want - sold
            out["lost_units"] += lost
            out["lost_value"] += lost * BY_ID[k[1]].price
            history[k].append(sold)
            h = history[k][-WARMUP:]
            twin.rates[k] = sum(h) / len(h)
        # 2) Write off anything that expires today.
        for lot in twin.lots:
            if lot.qty > 0 and lot.expiry_day <= day:
                out["expired_units"] += lot.qty
                out["expired_value"] += lot.qty * BY_ID[lot.item_id].unit_cost
                lot.qty = 0
        twin.lots = [l for l in twin.lots if l.qty > 0]
        # 3) Route day: agent cycle (stockbridge only), then the usual restock in whole cases.
        if day % ROUTE_EVERY == 0 and day > 0:
            for s in twin.shops.values():
                s.spent_this_week = 0
            if agent:
                before = len(agent.committed)
                agent.run_cycle()
                agent.auto_answer(decide)
                new = agent.committed[before:]
                out["moves"] += len(new)
                out["moved_units"] += sum(c["qty"] for c in new)
                out["claims"] = sum(1 for d in agent.documents if d["type"] == "brand_claim")
            for k, r in true_rate.items():
                obs = twin.rates[k]
                if obs <= 0 and twin.stock(*k) > 0:
                    continue
                if twin.stock(*k) < max(1.0, obs * 10):
                    it = BY_ID[k[1]]
                    case = CASE[it.category]
                    qty = case * max(1, math.ceil(obs * 21 / case))
                    out["lot_seq"] += 1
                    twin.lots.append(Lot(f"R{out['lot_seq']}", k[0], k[1], f"N{out['lot_seq']:04d}", qty,
                                         day + int(it.shelf_life_days * rng.uniform(0.5, 0.8))))
    out.pop("lot_seq")
    return out


def main(seeds: int) -> dict:
    rows = []
    for s in range(1, seeds + 1):
        b, a = run(s, False), run(s, True)
        rows.append({"seed": s, "baseline": b, "stockbridge": a})
        print(f"seed {s}: expired ₹{b['expired_value']:,} -> ₹{a['expired_value']:,} | "
              f"lost sales ₹{b['lost_value']:,} -> ₹{a['lost_value']:,} | moves {a['moves']} ({a['moved_units']} units), "
              f"owner requests {a['owner_requests']}, claims drafted {a['claims']}")

    def mean(policy, key):
        return round(sum(r[policy][key] for r in rows) / len(rows))

    keys = ["expired_units", "expired_value", "lost_units", "lost_value", "sold_units", "moved_units", "moves",
            "owner_requests", "claims"]
    summary = {p: {k: mean(p, k) for k in keys} for p in ("baseline", "stockbridge")}
    b, a = summary["baseline"], summary["stockbridge"]
    summary["change"] = {
        "expired_value_pct": round(100 * (a["expired_value"] - b["expired_value"]) / max(1, b["expired_value"]), 1),
        "lost_sales_value_pct": round(100 * (a["lost_value"] - b["lost_value"]) / max(1, b["lost_value"]), 1),
    }
    summary["note"] = "SYNTHETIC data: 40 simulated shops, 90 simulated days, simulated owner answers."
    return {"seeds": seeds, "summary": summary, "runs": rows}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=5)
    res = main(ap.parse_args().seeds)
    Path("evals/results").mkdir(parents=True, exist_ok=True)
    Path("evals/results/backtest.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps(res["summary"], indent=2, ensure_ascii=False))
