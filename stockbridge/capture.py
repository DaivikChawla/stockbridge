"""Turn what was said at the counter into candidate bill lines.

Two parsers produce the same output shape: a list of Line(qty, candidates).
- llm_parse: an LLM (NVIDIA NIM) constrained to this shop's catalogue ids.
- rule_parse: a deterministic alias matcher with Hindi/Punjabi number words.

Neither parser decides prices or pack sizes on its own when the words are ambiguous:
it returns every candidate, and checksum.reconcile() uses the amount paid to decide,
or asks the owner one question.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from . import llm
from .catalogue import ITEMS, BY_ID, alias_index

NUMBER_WORDS = {
    "ek": 1, "ik": 1, "one": 1, "1": 1,
    "do": 2, "dou": 2, "two": 2, "2": 2,
    "teen": 3, "tin": 3, "three": 3, "3": 3,
    "char": 4, "chaar": 4, "four": 4, "4": 4,
    "paanch": 5, "panch": 5, "five": 5, "5": 5,
    "chhe": 6, "che": 6, "six": 6, "6": 6,
    "saat": 7, "seven": 7, "7": 7,
    "aath": 8, "eight": 8, "8": 8,
    "nau": 9, "nine": 9, "9": 9,
    "das": 10, "ten": 10, "10": 10,
}


@dataclass
class Line:
    qty: int
    candidates: list[str]  # item ids; more than one means "not sure which pack"
    heard: str = ""

    def to_dict(self) -> dict:
        return {"qty": self.qty, "candidates": self.candidates, "heard": self.heard}


def _normalise(text: str) -> list[str]:
    text = text.lower().replace("-", " ")
    text = re.sub(r"[^\w\s₹]", " ", text)
    return text.split()


def rule_parse(transcript: str) -> list[Line]:
    """Greedy longest-alias match over the transcript, with a pending quantity.

    "do" is both the number 2 and "give"; it only counts as a number when an item follows it.
    """
    idx = alias_index()
    max_len = max(len(a.split()) for a in idx)
    toks = _normalise(transcript)
    lines: list[Line] = []
    pending_qty: int | None = None
    last_end = -1  # token index just after the previous match
    i = 0
    while i < len(toks):
        matched = False
        for n in range(min(max_len, len(toks) - i), 0, -1):
            phrase = " ".join(toks[i:i + n])
            if phrase in idx:
                cands = sorted(idx[phrase])
                if lines and i == last_end and pending_qty is None and lines[-1].candidates == cands:
                    # "dairy milk chocolate": two names for the same thing, said back to back.
                    lines[-1].heard += " " + phrase
                else:
                    lines.append(Line(qty=pending_qty or 1, candidates=cands, heard=phrase))
                pending_qty = None
                last_end = i + n
                i += n
                matched = True
                break
        if matched:
            continue
        tok = toks[i]
        if tok in NUMBER_WORDS:
            pending_qty = NUMBER_WORDS[tok]
        i += 1
    return _merge(lines)


def _merge(lines: list[Line]) -> list[Line]:
    """Combine repeated mentions of the same candidate set ("ek parle ... ek parle")."""
    out: list[Line] = []
    for ln in lines:
        for o in out:
            if o.candidates == ln.candidates:
                o.qty += ln.qty
                break
        else:
            out.append(ln)
    return out


SYSTEM_PROMPT = (
    "You read a short transcript of a customer ordering at an Indian kirana counter "
    "(Hindi, Punjabi and English mixed, romanised). Return ONLY JSON: "
    '{"lines": [{"qty": <int>, "candidates": [<item ids>], "heard": "<words>"}]}. '
    "Use ONLY item ids from the catalogue given. If the words could mean more than one "
    "pack size, list every possible id in candidates; never guess a single pack. "
    "Ignore chatter, TV noise and words that are not items. Never invent items or prices."
)


def llm_parse(transcript: str) -> list[Line] | None:
    if not llm.available():
        return None
    cat = "\n".join(f"{it.id}: {it.label}, ₹{it.price}; people say: {', '.join(it.aliases)}" for it in ITEMS)
    data = llm.chat_json(SYSTEM_PROMPT, f"Catalogue:\n{cat}\n\nTranscript: {transcript}")
    if not data or not isinstance(data.get("lines"), list):
        return None
    out: list[Line] = []
    for raw in data["lines"]:
        try:
            qty = int(raw.get("qty", 1))
        except (TypeError, ValueError):
            continue
        # Guardrail: drop anything that is not a real catalogue id.
        cands = sorted({c for c in raw.get("candidates", []) if c in BY_ID})
        if qty < 1 or qty > 50 or not cands:
            continue
        out.append(Line(qty=qty, candidates=cands, heard=str(raw.get("heard", ""))[:60]))
    return _merge(out) if out else None


def parse(transcript: str, use_llm: bool = True) -> tuple[list[Line], str]:
    """Return (lines, parser_used). Falls back to rules if the LLM is off or fails."""
    if use_llm:
        got = llm_parse(transcript)
        if got is not None:
            return got, "llm"
    return rule_parse(transcript), "rules"
