# 17 · Evals v2: real speech clips, capture metrics, backtest refresh

**Who:** Parv · **When:** 5 Dec (last trial day; record clips on 6 Dec if needed, then re-run without Claude).
**Tools:** Claude Code `/model opus`, plan mode; Codex for reviewing the metrics code.
**Depends on:** 14, 15.
**Criteria moved:** T2 Quality of AI ("judged on measured performance"), E3.

## Paste into Claude Code
```text
Read AGENTS.md, PROGRESS.md, backend/evals/ (eval_capture.py and backtest.py) and backend/capture.

On branch p17-evals:
1. Real speech eval (evals/eval_speech.py).
   - Input: a folder of consented audio clips (path from .env, NOT committed) plus a CSV of the true items and amounts.
   - Run each clip through (a) on-device text, if we have it recorded from the phone, (b) Sarvam saaras:v4 codemix with keyterms, (c) Sarvam without keyterms.
   - Report: word error rate on item words, item precision / recall / F1, bills saved silently wrong with and without checksum, taps per sale, latency p50/p95.
   - Write results to evals/results/speech_*.json and a markdown summary.
2. Synthetic capture eval: keep the existing one, and add the new LLM-constrained parser as a third column.
3. Backtest refresh: run on the new database-backed twin and agent (synthetic 40-shop route, 90 days, 5 seeds), using the new memory and recovery behaviour. Report expired ₹, stock-outs, moves, owner requests per shop per week.
4. A single command: `uv run python -m evals.report` → evals/results/REPORT.md, plus a JSON file the dashboard's Impact and Evals page reads (prompt 29).
5. Every number says where it came from:
   - "measured on N real clips recorded with consent";
   - "synthetic simulation".
6. Update the README Results section from REPORT.md.

Plan first, build. Then run the second-opinion skill on the eval code:
"Are these metrics computed correctly and honestly? Any leakage between test data and keyterms or catalogue?"
Fix, run the gates, update PROGRESS.md, push, open a PR.
```

## After the trial ends (human, no Claude)
Record clips with shops (prompt 05), then run `uv run python -m evals.report` again and commit the updated results.

## Done when
- [ ] `REPORT.md` has real-clip metrics (or a clear "pending clips" note) and synthetic metrics, all labelled.
- [ ] The README results are updated.
