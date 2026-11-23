"""The route twin: a live model of one distributor route.

It holds every shop's stock by batch and expiry (from the distributor's books) and each
shop's selling rate per item (learned from the sales the shop app captures). Every sale
event updates it straight away. From it the agent reads days of cover, which lots will
not sell before they expire, and what happens under "what if" scenarios.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from .catalogue import BY_ID


def _cover(v: float) -> float | None:
    return None if math.isinf(v) else round(v, 1)


@dataclass
class Shop:
    id: str
    name: str
    x: float  # position on the route map (km from the depot)
    y: float
    weekly_budget: int  # the owner's cap for extra stock in a week (₹)
    spent_this_week: int = 0
    consent_share_sales: bool = True

    @property
    def budget_left(self) -> int:
        return max(0, self.weekly_budget - self.spent_this_week)


@dataclass
class Lot:
    id: str
    shop_id: str
    item_id: str
    batch: str
    qty: int
    expiry_day: int  # days from "today" (day 0)

    def days_to_expiry(self, today: int) -> int:
        return self.expiry_day - today


@dataclass
class Policy:
    return_window_days: int = 30  # distributor takes stock back only until this many days before expiry
    min_sell_days: int = 7  # never send stock that has less than this many days to sell at the receiver
    lead_days: int = 2  # next delivery day on this route
    clearance_discount: float = 0.5  # shop-to-shop clearance price as a share of distributor price
    rate_window_days: int = 14  # a sale moves the 14-day rolling rate
    horizon_days: int = 90  # only act on stock that expires within this many days


@dataclass
class RouteTwin:
    route_name: str
    depot: tuple[float, float]
    shops: dict[str, Shop]
    lots: list[Lot]
    rates: dict[tuple[str, str], float]  # (shop_id, item_id) -> units per day
    today: int = 0
    policy: Policy = field(default_factory=Policy)
    events: list[dict] = field(default_factory=list)
    _lot_seq: int = 0

    # ---------- reads ----------
    def rate(self, shop_id: str, item_id: str) -> float:
        return self.rates.get((shop_id, item_id), 0.0)

    def stock(self, shop_id: str, item_id: str) -> int:
        return sum(l.qty for l in self.lots if l.shop_id == shop_id and l.item_id == item_id and l.qty > 0)

    def days_of_cover(self, shop_id: str, item_id: str) -> float:
        r = self.rate(shop_id, item_id)
        s = self.stock(shop_id, item_id)
        return math.inf if r <= 0 else s / r

    def shop_lots(self, shop_id: str, item_id: str) -> list[Lot]:
        return sorted((l for l in self.lots if l.shop_id == shop_id and l.item_id == item_id and l.qty > 0),
                      key=lambda l: l.expiry_day)

    def unsold_before_expiry(self, lot: Lot, rate_multiplier: float = 1.0) -> int:
        """Units of this lot that will still be on the shelf when it expires (first-expiry-first-out)."""
        r = self.rate(lot.shop_id, lot.item_id) * rate_multiplier
        ahead = 0
        for l in self.shop_lots(lot.shop_id, lot.item_id):
            if l.id == lot.id:
                break
            ahead += l.qty
        can_sell = max(0.0, r * max(0, lot.days_to_expiry(self.today)) - ahead)
        return max(0, lot.qty - int(math.floor(can_sell)))

    def extra_capacity(self, shop_id: str, item_id: str, sell_days: int) -> int:
        """How many more units this shop can sell within sell_days, on top of what it holds."""
        r = self.rate(shop_id, item_id)
        if r <= 0 or sell_days <= 0:
            return 0
        return max(0, int(math.floor(r * sell_days - self.stock(shop_id, item_id))))

    def at_risk(self) -> list[dict]:
        out = []
        for lot in self.lots:
            if lot.qty <= 0:
                continue
            dte = lot.days_to_expiry(self.today)
            if dte > self.policy.horizon_days:
                continue  # too far out to act on; selling rates will change before then
            unsold = self.unsold_before_expiry(lot)
            if unsold <= 0:
                continue
            it = BY_ID[lot.item_id]
            if dte <= 0:
                mode = "expired"
            elif dte - self.policy.lead_days < self.policy.min_sell_days:
                mode = "claim"  # too late to move without it expiring on the next shelf
            elif dte >= self.policy.return_window_days:
                mode = "take_back"  # distributor credit note + fresh invoice
            else:
                mode = "clearance"  # past the return window: shop-to-shop at a discount
            out.append({
                "lot_id": lot.id, "shop_id": lot.shop_id, "item_id": lot.item_id, "batch": lot.batch,
                "qty": lot.qty, "unsold": unsold, "days_to_expiry": dte,
                "days_of_cover": _cover(self.days_of_cover(lot.shop_id, lot.item_id)),
                "value_at_risk": unsold * it.unit_cost, "mode": mode,
            })
        return sorted(out, key=lambda d: -d["value_at_risk"])

    # ---------- writes (real-time sync from the shop app and the delivery app) ----------
    def record_sale(self, shop_id: str, item_id: str, qty: int, source: str = "shop app") -> None:
        """A captured sale: take stock first-expiry-first-out and nudge the rolling rate up."""
        left = qty
        for lot in self.shop_lots(shop_id, item_id):
            take = min(lot.qty, left)
            lot.qty -= take
            left -= take
            if left == 0:
                break
        w = self.policy.rate_window_days
        old = self.rate(shop_id, item_id)
        self.rates[(shop_id, item_id)] = old + qty / w
        self.events.append({"type": "sale", "shop_id": shop_id, "item_id": item_id, "qty": qty, "source": source,
                            "rate_before": round(old, 3), "rate_after": round(self.rates[(shop_id, item_id)], 3)})

    def move_units(self, lot_id: str, to_shop: str, qty: int) -> Lot:
        lot = next(l for l in self.lots if l.id == lot_id)
        qty = min(qty, lot.qty)
        lot.qty -= qty
        self._lot_seq += 1
        new = Lot(f"{lot.id}-m{self._lot_seq}", to_shop, lot.item_id, lot.batch, qty, lot.expiry_day)
        self.lots.append(new)
        self.events.append({"type": "move", "from": lot.shop_id, "to": to_shop, "item_id": lot.item_id,
                            "batch": lot.batch, "qty": qty})
        return new

    # ---------- what-if ----------
    def simulate_expiry(self, days: int, demand_multiplier: float = 1.0) -> dict:
        """Expected stock that expires within `days` if nothing is moved (deterministic, FEFO)."""
        expired_units = 0
        expired_value = 0
        for lot in self.lots:
            if lot.qty <= 0:
                continue
            dte = lot.days_to_expiry(self.today)
            if dte > days:
                continue
            unsold = self.unsold_before_expiry(lot, demand_multiplier)
            expired_units += unsold
            expired_value += unsold * BY_ID[lot.item_id].unit_cost
        return {"days": days, "demand_multiplier": demand_multiplier,
                "expired_units": expired_units, "expired_value": expired_value}

    def snapshot(self) -> dict:
        return {
            "route": self.route_name, "today": self.today,
            "shops": [s.__dict__ | {"budget_left": s.budget_left} for s in self.shops.values()],
            "at_risk": self.at_risk(),
            "events": self.events[-20:],
        }
