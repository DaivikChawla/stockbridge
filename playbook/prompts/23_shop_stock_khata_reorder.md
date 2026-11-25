# 23 · Shop app: stock, expiry alerts, khata, reorder within budget, weekly report

**Who:** Daivik · **When:** 7 Dec · **Account:** Daivik's Claude Pro.
**Tools:** Claude Code `/model opus`, plan mode; compose + m3-expressive skills; mobile-mcp.
**Depends on:** 22.
**Criteria moved:** T3, C4, PS 5.1 boundaries ("purchases stay within a cash budget the owner sets, and the owner approves every order").

## Paste into Claude Code
```text
Read AGENTS.md, PROGRESS.md, design/specs/shop/ (stock, khata, reorder, weekly report), docs/PRD.md journey (j), and backend reorder and khata endpoints.
On branch p23-stock-khata-reorder:
1. Stock: items sorted by urgency (expiring soon, low cover); days-of-cover bars; expiry badges; batch detail; a weekly stock check flow for a JanAI helper (count items, post StockCount).
2. Expiry alerts: a daily local notification summary; tapping opens the at-risk items with "what Stockbridge is doing about it" (link to requests).
3. Khata: customers, dues, add entry by voice ("Sharma ji 120 udhaar") or tap; settle; simple history.
4. Reorder: the weekly suggestion within the owner's budget (budget bar), with take-back stock from nearby shops preferred and marked. The owner edits quantities and approves, and the order goes to the distributor. Budget can't be exceeded without an explicit override.
5. Weekly report: sales, top movers, slow movers, money saved from moves and clearance (labelled if synthetic), and one suggestion. Shareable as an image.
6. Tests: budget enforcement, khata math, stock check post.
7. Screenshots on the S24, then compare to the designs and fix differences.
Plan first, build, run the gates, update PROGRESS.md, push, open a PR.
```

## Done when
- [ ] Reorder can't exceed the budget. Khata works by voice. The stock check posts. The report renders.
