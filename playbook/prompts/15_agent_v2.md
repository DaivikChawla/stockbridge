# 15 · Agent v2: memory, recovery, approvals, documents, reorder, khata

**Who:** Parv · **When:** 3 Dec · **Account:** Parv's Claude trial.
**Tools:** Claude Code `/model opus`, plan mode, second opinion on the plan.
**Depends on:** 13.
**Criteria moved:** A1–A7 (the booklet's agentic definition), T2, T4.

## Paste into Claude Code
```text
Read AGENTS.md, PROGRESS.md, playbook/CRITERIA.md (section A), docs/PRD.md (agent journeys) and backend/agent, planner, twin.

Upgrade the agent on branch p15-agent-v2. It must visibly satisfy each verb in CRITERIA.md lines A1–A7.
1. Persistent agent cycles.
   - AgentCycle, Proposal, Request, Answer and Move are stored in the database.
   - Each step emits an agent.step event with a plain-English message for the trace.
   - A cycle can be resumed after a server restart.
2. Memory per shop: declines (with expiry, e.g. "don't offer Horlicks for 14 days"), caps ("only 3"), typical answer times, preferred contact channel. It is used in planning and shown in the trace ("remembered: Arora said no to Bournvita on 3 Dec").
3. Recovery:
   - re-plan on decline or partial without asking the giver again;
   - reminders after N hours, then a WhatsApp fallback (simulated, labelled);
   - expire unanswered requests and re-plan;
   - handle a stop that failed on delivery (the shop was closed) by re-planning for the next route day.
4. Approvals:
   - nothing commits without both owners' yes;
   - documents are drafts;
   - the accountant approves export;
   - log who approved what and when (AuditEvent).
5. Documents.
   - Generate PDF drafts: credit note, invoice, clearance bill, brand claim. Include GST fields where they apply, with a disclaimer that it is a draft for the accountant.
   - Ask me to check the GST fields with our CA parent before the demo.
6. Reorder agent.
   - Weekly suggestion per shop from its selling rate and days of cover, within the owner's weekly budget, preferring take-back stock from nearby shops before fresh stock.
   - The owner edits and approves; the order goes to the distributor.
7. Khata: a simple ledger of customer credit, voice-addable ("Sharma ji 120 udhaar").
8. Planner tuning: confirm CP-SAT stays under 2 s for 40 shops × 200 lots; add a benchmark test.
9. Tests: one per verb A1–A6 (a scenario test that asserts the trace), plus reorder budget, khata and documents.

Plan first. Run the second-opinion skill on the plan:
"Does this agent clearly meet the booklet definition (plans, acts in external systems, memory, recovers, human approval)? What would a skeptical AI judge poke at?"
Revise, build, run the gates, update PROGRESS.md, push, open a PR.
```

## Done when
- [ ] Scenario tests pass for A1–A6. The trace reads well to a non-engineer.
- [ ] Document PDFs render. Reorder respects the budget.
