# 31 · Integration, demo seed, failure drills, deployment

**Who:** Daivik (Parv and Amogh test on devices) · **When:** 10–11 Dec · **Account:** Daivik's Claude Pro.
**Tools:** Claude Code `/model opus`, plan mode; mobile-mcp (S24 + emulator); Playwright MCP; Supabase MCP (read-only checks); second-opinion skill.
**Depends on:** 24, 26, 30 (and everything before).
**Criteria moved:** T3 (working prototype), A5 (recovery), C3, C6, T1 (deployed).

## Paste into Claude Code
```text
Read AGENTS.md, PROGRESS.md (all entries since 01), docs/DEMO_SCRIPT.md, docs/PRD.md and playbook/CRITERIA.md section C (demo moments).
On branch p31-integration:
1. Deploy:
   - backend to Azure (container + Postgres on Supabase + env vars), with health checks and a warm instance so there are no cold starts;
   - web to Vercel on the .tech domain;
   - point both apps' release builds at production.
   Write docs/DEPLOY.md.
2. Demo seed v2.
   - The Patiala route exactly as DEMO_SCRIPT.md needs, so every demo moment happens on cue: Horlicks at Sharma, Bansal taking only 3, bread too short-dated (brand claim), Good Day past the return window (clearance), Arora declining.
   - A one-command reset: `scripts/demo-reset.sh` (backend endpoint + script).
3. Run DEMO_SCRIPT.md end to end on real devices:
   - S24 = shop (Auto mode, real UPI ₹1);
   - second phone or emulator = second shop;
   - a third device or emulator = delivery;
   - laptop = dashboard.
   Fix every break. Time each beat and fit it to 3 and 5 minutes.
4. Failure drills (each must recover visibly, and appear in the trace):
   a. airplane mode during a sale → outbox → sync;
   b. owner declines → re-plan;
   c. bill doesn't add up → one-tap fix;
   d. Sarvam unavailable → on-device speech;
   e. LLM unavailable → rule parser;
   f. WebSocket drop on the dashboard → resume without gaps;
   g. delivery exception (shop closed) → re-plan for the next day.
   Write docs/FAILURE_DRILLS.md with the results.
5. "Simulated" audit: every simulated integration shows the tag in the UI and is listed in the README.
6. Run the second-opinion skill on the full diff since main:
   "What could crash or embarrass us during a live 5-minute demo?"
   Fix the findings.
Update PROGRESS.md, push, open a PR.
```

## Done when
- [ ] The demo script runs three times in a row without a crash, on production.
- [ ] All drills pass. Reset takes one command.
