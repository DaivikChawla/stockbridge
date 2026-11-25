# 21 · Shop app: Manual mode, checksum one-tap flow, bill history, cash sales

**Who:** Daivik · **When:** 5 Dec · **Account:** Daivik's Claude Pro.
**Tools:** Claude Code `/model opus`, plan mode; compose + m3-expressive skills; mobile-mcp.
**Depends on:** 20.
**Criteria moved:** T2, A5, C2 (limited literacy).

## Paste into Claude Code
```text
Read AGENTS.md, PROGRESS.md, design/specs/shop/ (manual, bills, cash) and docs/PRD.md journeys (b, c, d).
On branch p21-manual-bills:
1. Manual mode:
   - hold-to-talk (same engines as Auto) or tap items;
   - quick-pick grid of the shop's 12 most frequent items (from sales history);
   - quantity steppers;
   - amount from the UPI notification or typed;
   - Save runs the same checksum flow and UI as Auto.
2. One-tap answer component (shared with Auto): options as large chips with pack-size pictures; spoken question; shape-morph on select; undo for 5 s.
3. Cash sales: the owner confirms the total (big number, spoken back), plus an optional "add to khata" for credit.
4. Bills: list grouped by day with totals; detail with items, payment source, and how it was captured (Auto / Manual / helper); edit within 10 minutes with an audit trail.
5. Smart suggestion: if Auto needed many taps today, suggest Manual mode (and the reverse), as the PRD describes.
6. Tests: checksum UI states, undo, cash confirm, edit audit.
7. Screenshots on the S24 in hi and en, light and dark; compare to the designs and fix differences.
Plan first, build, run the gates, update PROGRESS.md, push, open a PR.
```

## Done when
- [ ] A Manual sale takes 3 taps or fewer for a 2-item order. The one-tap question flow is shared and polished. Bills are complete.
