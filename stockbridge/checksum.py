"""The amount paid is a checksum on the bill.

Given candidate lines and the UPI amount, find every way to pick one pack per line so the
bill adds up exactly. One answer: save it. Several answers: ask the owner the single
question that tells them apart. None: say so and ask. Never save a bill on a guess.
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass, field

from .capture import Line
from .catalogue import BY_ID


@dataclass
class Result:
    status: str  # "match" | "ask" | "mismatch" | "cash_confirm" | "empty"
    bill: list[dict] = field(default_factory=list)  # [{"item_id", "qty", "price"}] when resolved
    question: dict | None = None  # {"line": i, "heard", "options": [{"item_id","label","price"}]}
    heard_total: int | None = None
    paid: int | None = None
    note: str = ""

    def to_dict(self) -> dict:
        return self.__dict__.copy()


def _bill(lines: list[Line], choice: tuple[str, ...]) -> list[dict]:
    return [{"item_id": c, "qty": ln.qty, "price": BY_ID[c].price, "label": BY_ID[c].label} for ln, c in zip(lines, choice)]


def _total(lines: list[Line], choice: tuple[str, ...]) -> int:
    return sum(BY_ID[c].price * ln.qty for ln, c in zip(lines, choice))


def reconcile(lines: list[Line], paid: int | None, max_combos: int = 5000) -> Result:
    if not lines:
        return Result("empty", paid=paid, note="No items heard. Ask the owner to say them (Manual mode).")

    combos = list(itertools.islice(itertools.product(*[ln.candidates for ln in lines]), max_combos))

    if paid is None:  # cash sale: no amount to check against
        if len(combos) == 1:
            c = combos[0]
            return Result("cash_confirm", bill=_bill(lines, c), heard_total=_total(lines, c),
                          note="Cash sale: no amount to check. Owner confirms the total.")
        return Result("ask", question=_question(lines, combos), note="Cash sale with an unclear pack.")

    fits = [c for c in combos if _total(lines, c) == paid]
    distinct = sorted(set(fits))
    if len(distinct) == 1:
        c = distinct[0]
        return Result("match", bill=_bill(lines, c), heard_total=paid, paid=paid, note="Items add up to the amount paid.")
    if len(distinct) > 1:
        return Result("ask", question=_question(lines, distinct), paid=paid,
                      note="More than one pack size fits the amount. One tap decides.")
    # Nothing fits: report the nearest reading so the owner sees what was heard.
    nearest = min(combos, key=lambda c: abs(_total(lines, c) - paid))
    gap = paid - _total(lines, nearest)
    note = (f"Heard items come to ₹{_total(lines, nearest)}, paid ₹{paid}. "
            + ("Something may be missing." if gap > 0 else "Something may be extra or a wrong pack."))
    return Result("mismatch", bill=_bill(lines, nearest), heard_total=_total(lines, nearest), paid=paid,
                  question=_question(lines, combos) if len(combos) > 1 else None, note=note)


def _question(lines: list[Line], combos: list[tuple[str, ...]]) -> dict:
    """Pick the first line whose choice differs across the remaining combinations."""
    for i, ln in enumerate(lines):
        opts = sorted({c[i] for c in combos})
        if len(opts) > 1:
            return {"line": i, "heard": ln.heard, "qty": ln.qty,
                    "options": [{"item_id": o, "label": BY_ID[o].label, "price": BY_ID[o].price} for o in opts]}
    return {"line": 0, "heard": lines[0].heard, "qty": lines[0].qty, "options": []}


def apply_answer(lines: list[Line], line_index: int, item_id: str) -> list[Line]:
    """The owner's tap pins one line to one pack."""
    out = [Line(ln.qty, list(ln.candidates), ln.heard) for ln in lines]
    out[line_index].candidates = [item_id]
    return out
