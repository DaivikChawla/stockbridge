# PROGRESS.md: the hand-off log

Newest entry at the top. Every session, by any person or any agent, adds one entry before it stops. This file is how a fresh session on another account picks up with zero context.

## Template (copy this)

```
## YYYY-MM-DD HH:MM · p<NN> <prompt name> · <who> (<tool / account>)
**Branch / PR:** p<NN>-slug · #PR
**Done:** what now works (link files, screenshots in docs/screens/)
**Not done / next step:** the exact next action, so the next session can start immediately
**Decisions:** anything new (also add to docs/DECISIONS.md)
**Gates:** backend tests ✓/✗ · android build ✓/✗ · web build ✓/✗ · reviewed by codex/agy ✓/✗
**Blockers / questions for Daivik:**
```

---

## 2026-11-25 · playbook · Claude (lead session)
**Done:**
- Added the build playbook: `playbook/` (master workflow, criteria, tools setup, budget, prompts 00–34).
- Added the agent rules (`AGENTS.md`, `CLAUDE.md`), the committed MCP config (`.mcp.json`), helper scripts (`scripts/`) and the `second-opinion` skill.

The code is unchanged: the Python agent still runs from the root, as in the README.

**Next step:** everyone runs `playbook/prompts/00_setup.md`. Then Daivik runs `01_plan_master.md`.
**Decisions:** stack fixed as in AGENTS.md section 4 (native Kotlin + Compose, Next.js, FastAPI); online-first with an outbox.
**Gates:** backend tests ✓ (15 passed).
