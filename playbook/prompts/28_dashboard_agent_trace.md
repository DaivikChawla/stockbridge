# 28 · Dashboard: at-risk lots, agent run (plan, live answers, re-plan), approvals, trace

**Who:** Amogh · **When:** 6 Dec · **Account:** Amogh's Claude trial.
**Tools:** Claude Code `/model opus`, plan mode; Motion skill; Emil Kowalski `animate` skill; shadcn MCP; Playwright MCP.
**Depends on:** 27, 15.
**Criteria moved:** A1–A6 (this page is where judges *see* the agent), T2, T4.

## Paste into Claude Code
```text
Read AGENTS.md, PROGRESS.md, playbook/CRITERIA.md section A, design/specs/web/ (at-risk, agent run, approvals) and the backend agent API and events.
Build on branch p28-agent-views:
1. At-risk lots table: treatment (take back / clearance / brand claim / too far out), why (plain English), value at risk; filters; row → lot drawer.
2. Agent run, the hero page:
   - "Run agent" starts a cycle;
   - the plan is drawn as a flow from giving shops' lots to receiving shops, with quantities;
   - each owner's answer arrives live (Approve / Only N / Decline) and the flow re-flows with Motion layout animations;
   - refused lots (brand claim) are shown separately with the reason.
   Plan timing shows ("planned in 640 ms").
3. Trace timeline: every agent.step event as a readable line, grouped by step type (detect, refuse, plan, ask, remember, re-plan, commit, route), with icons, timestamps and expandable details. This must read well to a non-technical judge.
4. Approvals tracker: who was asked, the channel (app push, WhatsApp fallback (simulated, labelled)), reminders, answers, times.
5. Controls for the demo: a "simulate owner answers" panel, visible only in demo mode and labelled, for when a second phone isn't available.
6. Motion: restrained and purposeful (number count-ups, list re-order, re-flow), with reduced-motion fallbacks. Review with the Emil Kowalski review-animations skill.
7. Playwright: run a full cycle against the seeded backend with simulated answers; assert the trace contains every step type; screenshot.
Plan first, build, run the gates, update PROGRESS.md, push, open a PR.
```

## Done when
- [ ] A judge can watch a full agent cycle on one screen and understand each step without explanation.
