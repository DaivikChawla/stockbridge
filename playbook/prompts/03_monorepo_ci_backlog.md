# 03 · Monorepo restructure, CI, issue backlog

**Who:** Daivik · **When:** 27 Nov · **Account:** Daivik's Claude Pro.
**Tool:** Claude Code, `/model opus`, plan mode, second opinion on the plan; GitHub MCP for issues.
**Depends on:** 02 (merged).
**Criteria moved:** T1.

**Keep the Homingo submission working.** Homingo judges open this repo 4–6 Dec, so the README run steps must still work after the move.

## Paste into Claude Code
```text
Read AGENTS.md (section 3 has the target layout), docs/ARCHITECTURE.md and docs/PRD.md.

Restructure the repo into the target monorepo without breaking what works:
1. Move the Python code into backend/ as a uv project (Python 3.12).
   - Packages: app/ (FastAPI), agent/, planner/, twin/, capture/, evals/, tests/.
   - Keep git history (use git mv).
   - Make `uv run pytest -q` pass (15 tests) and `uv run python -m evals.eval_capture` and `evals.backtest` still run.
   - Keep the current demo UI working at http://localhost:8000.
2. Create the skeletons:
   - android/: an empty Gradle project with a settings file listing the modules from AGENTS.md. Content comes in prompt 18; just make it sync.
   - web/: run `create-next-app` with TypeScript, Tailwind, ESLint and the App Router, using pnpm. It just has to build.
   - video/: leave a README placeholder that says Remotion is set up in prompt 33.
   - design/: add a README that explains what goes there.
3. Update README.md.
   - Keep everything Homingo needs: problem, how it works, results, guardrails, AI tools, team.
   - Fix the "Run it" commands for backend/.
   - Add a short "Repository layout" section.
4. Add CI in .github/workflows/:
   - backend: ruff + pytest;
   - web: lint + typecheck + build;
   - android: assembleDebug.
   Each runs only when its folder changes. Cache dependencies.
5. Add root dev helpers in scripts/: dev-backend.sh, dev-web.sh, gen-api-clients.sh (a stub until prompt 12).
6. Create GitHub issues for prompts 04–34, one per prompt, using the GitHub MCP.
   - Use the title from playbook/MASTER_WORKFLOW.md section 5.
   - Body: a link to the prompt file plus its "Done when" list.
   - Add the labels from prompt 00 and a milestone per phase (A–F).

Plan first. Run the second-opinion skill on the plan:
"Will this restructure break anything that currently works (tests, evals, README steps)? Is the CI right?"
Then show me the plan.

After approval, do it on branch p03-monorepo and verify every point above, pasting the commands and their output. Update PROGRESS.md, push, and open a PR.
```

## Done when
- [ ] On a fresh clone: backend tests pass, evals run, the demo UI loads, web builds, and Android syncs.
- [ ] CI is green on the PR.
- [ ] Issues 04–34 exist with labels and milestones.
- [ ] README run steps work for Homingo.
