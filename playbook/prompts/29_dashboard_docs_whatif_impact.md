# 29 · Dashboard: documents, delivery view, what-if, impact and evals

**Who:** Amogh · **When:** 7 Dec · **Account:** Amogh's Claude trial.
**Tools:** Claude Code `/model opus`, plan mode; shadcn MCP; Motion; the `dataviz` skill if installed (chart quality); Playwright MCP.
**Depends on:** 28, 17 (evals JSON).
**Criteria moved:** T2 (measured AI quality made visible), E3 (impact), A3, C6 (simulated labels).

## Paste into Claude Code
```text
Read AGENTS.md, PROGRESS.md, design/specs/web/ (documents, delivery, what-if, impact, settings), backend/evals/results/ (REPORT.md and JSON) and the backend endpoints.
Build on branch p29-docs-whatif-impact:
1. Documents: a list of drafts (credit notes, invoices, clearance bills, brand claims); a PDF preview; status (draft → approved by accountant → exported). "Export for Tally" is simulated, labelled, and downloads a CSV/XML in a documented format.
2. Delivery: today's route with live driver progress (stop.confirmed events), exceptions, and documents handed over.
3. What-if: sliders and toggles (demand ±%, delivery delayed N days, shop closed) → units and ₹ expiring if nothing moves, versus with the agent. Recharts, with our tokens.
4. Impact and evals:
   - capture accuracy (F1, silent-wrong rate with and without checksum), speech results on real clips, latency p50/p95, backtest results;
   - every number shows its source label (measured on N consented clips / synthetic simulation) and links to the eval code.
5. Settings: policy (return window, min sell days, clearance discount, lead days), users and roles, consent records (read-only), "Simulated integrations" list.
6. Playwright tests + screenshots.
Plan first, build, run the gates, update PROGRESS.md, push, open a PR.
```

## Done when
- [ ] Every page in `design/specs/web/` exists and is wired to live data. Every number is labelled with its source.
