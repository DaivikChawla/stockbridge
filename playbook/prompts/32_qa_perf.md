# 32 · QA, performance, crash sweep, code review (demo freeze at the end)

**Who:** all (Daivik's Claude fixes; Parv and Amogh test and file issues; Codex and Gemini review).
**When:** 11–12 Dec. **Demo freeze: Sat 12 Dec, 11 PM.**
**Tools:** Claude Code `/model opus`; Android CLI Journeys (natural-language end-to-end tests); Playwright; mobile-mcp; Codex CLI and `agy` for full-repo review.
**Depends on:** 31.
**Criteria moved:** T3, T1.

## Human test pass (Parv and Amogh, 2 hours)
Walk through `docs/DEMO_SCRIPT.md` and every journey in `docs/PRD.md` on the devices, in Hindi and English. File each problem as a GitHub issue labelled `bug`, with steps, a screenshot and severity (blocker / major / minor).

## Paste into Claude Code (Daivik)
```text
Read AGENTS.md, PROGRESS.md and the open GitHub issues labelled bug (GitHub MCP).
On branch p32-qa:
1. Full-repo review in parallel:
   scripts/ask-codex.sh qa-backend "Review backend/ for bugs, security and privacy issues, ranked."
   scripts/ask-gemini.sh qa-android "Review android/ for crashes, lifecycle bugs, permission handling, leaks, ranked."
   scripts/ask-codex.sh qa-web "Review web/ for bugs, accessibility and real-time edge cases, ranked."
   Merge these into docs/reviews/qa-decision.md together with the bug issues. Fix all blockers and majors.
2. Automated end-to-end:
   - Android Journeys (Android CLI) for the shop sale, approvals and delivery confirm flows;
   - Playwright for the dashboard agent run;
   - both run in CI where possible.
3. Crash sweep: StrictMode in debug; LeakCanary; run monkey for 10 minutes on each app; fix every crash.
4. Performance: cold start under 1.5 s on the S24 (with the baseline profile); counter screen and inbox at a steady 120 Hz; backend p95 under 300 ms for app endpoints; plan under 2 s.
5. Release builds: signed APKs (keystore kept out of git), R8 on, tested on the S24. Attach the APKs to a GitHub Release "prototype-round".
6. Freeze: tag v0.9-demo-freeze. After this, only blocker fixes.
Update PROGRESS.md, push, open a PR.
```

## Done when
- [ ] Zero open blockers or majors. Signed APKs on a GitHub Release. Journeys and Playwright are green.
- [ ] Tagged `v0.9-demo-freeze`.
