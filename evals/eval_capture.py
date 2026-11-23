"""Evaluate sale capture + the amount checksum on synthetic counter conversations.

Generates N noisy, code-mixed transcripts with known answers (seeded), runs the parser and
the checksum, and simulates the owner answering any one-tap question correctly.

Reports:
- saved automatically and correct
- saved silently WRONG (the number that must stay near zero)
- needed one tap / flagged as not adding up
- item-level precision, recall, F1 of the final bills
- the same bills WITHOUT the checksum (always take the first pack), as a baseline

Usage: python -m evals.eval_capture [--n 300] [--seed 7] [--llm]
"""
from __future__ import annotations

import argparse
import json
import random
from collections import Counter
from pathlib import Path

from stockbridge import capture, checksum
from stockbridge.catalogue import ITEMS, BY_ID

NUM_WORDS = {1: ["ek", "1", ""], 2: ["do", "2"], 3: ["teen", "3"], 4: ["char", "4"], 5: ["paanch", "5"]}
PREFIX = ["", "bhaiya ", "veerji ", "uncle ", "bhai sahab ", "sun na "]
JOIN = [" ", " aur ", " te ", ", ", " fir "]
SUFFIX = ["", " dena", " de do", " dedo ji", " please", " jaldi"]
NOISE = ["haan ji haan", "breaking news aaj ka mausam", "kitne hue", "change hai?", "arre suno"]
SELLABLE = [it for it in ITEMS if it.id != "bread_400"]


def make_sale(rng: random.Random) -> tuple[str, list[tuple[str, int]], int | None]:
    n_items = rng.choice([1, 1, 2, 2, 2, 3])
    items = rng.sample(SELLABLE, n_items)
    truth, parts = [], []
    for it in items:
        q = rng.choice([1, 1, 1, 2, 2, 3, 4, 5])
        alias = rng.choice(it.aliases)
        if rng.random() < 0.08 and len(alias) > 4:  # mis-heard word: one letter dropped
            k = rng.randrange(1, len(alias) - 1)
            alias = alias[:k] + alias[k + 1:]
        qw = rng.choice(NUM_WORDS[q])
        parts.append((qw + " " + alias).strip())
        if rng.random() < 0.15:
            parts.append(rng.choice(NOISE))
        truth.append((it.id, q))
    text = rng.choice(PREFIX) + rng.choice(JOIN).join(parts) + rng.choice(SUFFIX)
    paid = None if rng.random() < 0.2 else sum(BY_ID[i].price * q for i, q in truth)
    return text, truth, paid


def bill_counter(bill: list[dict]) -> Counter:
    return Counter({b["item_id"]: b["qty"] for b in bill})


def run(n: int, seed: int, use_llm: bool) -> dict:
    rng = random.Random(seed)
    stats = Counter()
    tp = fp = fn = 0
    base_wrong = 0
    examples = []
    for _ in range(n):
        text, truth, paid = make_sale(rng)
        t = Counter(dict(truth))
        lines, parser = capture.parse(text, use_llm=use_llm)
        stats[f"parser_{parser}"] += 1
        res = checksum.reconcile(lines, paid)
        taps = 0
        # Simulate the owner: answer each question with the true pack, at most 3 taps.
        while res.status == "ask" and res.question and res.question["options"] and taps < 3:
            opts = [o["item_id"] for o in res.question["options"]]
            pick = next((o for o in opts if o in t), opts[0])
            lines = checksum.apply_answer(lines, res.question["line"], pick)
            res = checksum.reconcile(lines, paid)
            taps += 1
        final = bill_counter(res.bill)
        correct = final == t
        if paid is None:
            stats["cash"] += 1
        if res.status == "match" and taps == 0:
            stats["auto_correct" if correct else "silent_wrong"] += 1
        elif res.status == "match":
            stats["one_tap_correct" if correct else "tap_wrong"] += 1
        elif res.status == "cash_confirm":
            stats["cash_confirm_correct" if correct else "cash_confirm_wrong"] += 1
        else:
            stats["flagged_" + res.status] += 1
        if res.status in ("match", "cash_confirm"):
            for k in set(final) | set(t):
                tp += min(final[k], t[k])
                fp += max(0, final[k] - t[k])
                fn += max(0, t[k] - final[k])
        else:  # flagged: nothing saved; everything still needs the owner
            fn += sum(t.values())
        # Baseline: no checksum, always take the first candidate pack.
        first = Counter()
        for ln in capture.parse(text, use_llm=False)[0]:
            first[ln.candidates[0]] += ln.qty
        if paid is not None and first != t:
            base_wrong += 1
        if len(examples) < 8:
            examples.append({"heard": text, "paid": paid, "status": res.status, "taps": taps, "correct": correct})
    upi = n - stats["cash"]
    prec = tp / (tp + fp) if tp + fp else 0
    rec = tp / (tp + fn) if tp + fn else 0
    out = {
        "n": n, "seed": seed, "parser": "llm" if use_llm else "rules", "upi_sales": upi, "cash_sales": stats["cash"],
        "auto_saved_correct": stats["auto_correct"], "saved_after_one_tap": stats["one_tap_correct"],
        "saved_silently_wrong": stats["silent_wrong"] + stats["tap_wrong"],
        "flagged_for_owner": stats["flagged_mismatch"] + stats["flagged_ask"] + stats["flagged_empty"],
        "cash_confirmed_correct": stats["cash_confirm_correct"], "cash_confirmed_wrong": stats["cash_confirm_wrong"],
        "item_precision": round(prec, 3), "item_recall": round(rec, 3),
        "item_f1": round(2 * prec * rec / (prec + rec), 3) if prec + rec else 0,
        "baseline_no_checksum_wrong_bills_upi": base_wrong,
        "examples": examples,
    }
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=300)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--llm", action="store_true", help="use the NVIDIA NIM parser (needs NVIDIA_API_KEY)")
    a = ap.parse_args()
    res = run(a.n, a.seed, a.llm)
    Path("evals/results").mkdir(parents=True, exist_ok=True)
    Path(f"evals/results/capture_{res['parser']}.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps({k: v for k, v in res.items() if k != "examples"}, indent=2))
