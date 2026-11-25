# 01 · Plan master: PRD, user journeys, demo storyboard

**Who:** Daivik · **When:** 25–26 Nov · **Account:** Daivik's Claude Pro.
**Tool:** Claude Code, `/model opus`, **plan mode**, with the second-opinion skill on the plan.
**Depends on:** 00.
**Criteria moved:** all of them. This sets what we build.

## Read first
- `AGENTS.md`, `PROGRESS.md`
- `playbook/CRITERIA.md`, `docs/round2_requirements.md`
- `README.md` (the current agent)
- `stockbridge/*.py`, `evals/*.py`

## Paste into Claude Code
```text
We are building the prototype of Stockbridge for the Tech4Bharat GAVS prototype round (due 15 Dec, finale 27 Dec, live demo on a Samsung Galaxy S24).
Read AGENTS.md, CLAUDE.md, playbook/CRITERIA.md, docs/round2_requirements.md, README.md, and skim stockbridge/*.py and evals/*.py so you know what already works.

Write docs/PRD.md, the product requirements, as the single source of truth for what we ship by 14 Dec. It must contain:
1. Problem and users. Kirana owner, counter helper, distributor owner, distributor accountant, delivery partner, JanAI Café helper. For each: goal, context (phone, literacy, language) and top 3 jobs.
2. Scope.
   - MUST (demo-critical), SHOULD, COULD, and OUT, for the Shop app, Delivery app, Dashboard and Agent. Keep MUST small enough to be excellent.
   - The cut order in playbook/MASTER_WORKFLOW.md section 7 must stay consistent.
3. User journeys, step by step, with the screen and system event at each step:
   a. a sale in Auto mode;
   b. a sale in Manual mode;
   c. an ambiguous bill answered in one tap;
   d. a cash sale;
   e. the agent cycle: detect, refuse, plan, ask, partial yes, decline, re-plan, commit;
   f. clearance shop-to-shop;
   g. the delivery day with a live re-plan;
   h. onboarding a shop through a JanAI Café helper;
   i. network drop and recovery (outbox);
   j. reorder within the owner's budget.
4. A criteria map. For every line in playbook/CRITERIA.md: which feature and which demo moment proves it. Flag any line with weak evidence.
5. Non-functional targets:
   - latency: sale to saved bill under 3 s on Wi-Fi; plan in under 2 s for 40 shops;
   - smoothness: 120 Hz, no jank on the S24;
   - languages: en, hi, pa;
   - accessibility; privacy and consent.
6. Simulated vs real. List every integration (UPI notifications: real; Tally import: simulated file; WhatsApp: simulated; etc.) and how the UI labels it.
7. Open questions for the field interviews (feed into prompt 05).

Also write docs/DEMO_SCRIPT.md: the 3-minute live demo and the 5-minute finale demo, beat by beat. Include who holds which phone, what is said, what appears on screen, and which criteria line each beat proves. Use the demo moments in CRITERIA.md section C.

Plan first. Before I approve, run the second-opinion skill on your plan with the question:
"Does this PRD scope give the strongest possible score on playbook/CRITERIA.md within 14 days for 3 builders using AI agents? What is missing, what is over-scoped, and which demo moments are weak?"
Reconcile the answers in docs/reviews/, revise the plan, then show it to me.

After approval, write the files, update PROGRESS.md, commit on branch p01-plan-master, push, and open a PR.
```

## Done when
- [ ] `docs/PRD.md` and `docs/DEMO_SCRIPT.md` exist. Every CRITERIA line maps to a feature and a demo beat.
- [ ] Review files are in `docs/reviews/`. A PROGRESS entry is written.
- [ ] Daivik has read the MUST list and agrees it is achievable.
