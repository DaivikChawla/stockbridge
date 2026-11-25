# 10 · Distributor dashboard screens (web)

**Who:** Amogh · **When:** 30 Nov–1 Dec.
**Tools:** Claude Design (`/design`) with the Taste Skill's art direction; Stitch optional.
**Depends on:** 07.
**Criteria moved:** T2 (AI quality made visible), T3, A1–A5 (agent visible), E3 (impact).

## Paste into Claude Code (or Claude Design)
```text
/design
Read AGENTS.md (section 6), docs/PRD.md (distributor journeys), design/brand/BRAND.md, design/tokens.json, design/COMPONENTS.md.
Use the design-taste-frontend skill for art direction: an operations tool that feels calm and precise, like a great ledger. Not a generic SaaS admin.
Design the dashboard at 1440 px and 1280 px (and a 390 px glance view of Overview), light and dark:
1. Overview: the route on a map with shops coloured by risk; KPIs (stock at risk ₹, moved this week, expiry avoided (synthetic, labelled), approvals pending, stock-outs flagged); "Run agent" primary action.
2. Route twin: shops × items grid with days of cover, expiry heat; a shop drawer with lots by batch and expiry and its selling rate over time.
3. At-risk lots: table with treatment (take back / clearance / brand claim / too far out), why, and value.
4. Agent run, the hero screen: the plan as a flow (lots → receiving shops), and owner answers arriving live (Approve, Only N, Decline). A re-plan animates. A trace timeline shows each step (detect, refuse, plan, ask, remember, re-plan, commit) in plain English.
5. Approvals tracker: who has been asked, who answered, reminders, the WhatsApp fallback (simulated, labelled).
6. Documents: credit notes, invoices, clearance bills, brand claims as drafts; preview; "export for accountant" (simulated Tally, labelled).
7. Delivery: today's route, live driver progress, stop status.
8. What-if: sliders (demand change, delayed delivery, shop closed) → units and ₹ expiring if nothing moves.
9. Impact and evals: capture accuracy (F1, silent-wrong rate with and without checksum), backtest results, latency. Every number shows its source (measured / synthetic).
10. Settings: policy (return window, min sell days, clearance discount), consent records, users and roles.
Annotate Motion choreography (list re-order, number count-up, plan re-flow) and reduced-motion fallbacks.
Export to design/screens/web/ with DESIGN.md sections.
```

## Done when
- [ ] All 10 screens at 1440 and 1280 px (plus the 390 px Overview), light and dark, in `design/screens/web/`.
