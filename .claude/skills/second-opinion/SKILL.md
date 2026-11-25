---
name: second-opinion
description: Get independent reviews of a plan, diff, bug or design from Codex (ChatGPT Plus) and Gemini (Antigravity CLI, Google AI Pro), then reconcile them. Use before approving a plan in prompts 01-03, before every merge, after two failed fixes of the same bug, and for design critique.
---

# Second opinion

Two other strong models review the work. You decide what to do with their answers.

## When
- A plan is written and about to be approved (always for prompts 01, 02, 03, 12, 18, 27).
- A PR is ready to merge.
- The same bug survived two fix attempts.
- A screen or page needs design critique (attach screenshots by path).

## How
1. Build the context.
   - For a plan: the plan file path.
   - For code: `git diff main...HEAD`.
   - For a bug: failing test output plus suspect files.
   - For design: screenshot paths plus `design/DESIGN.md`.
2. Ask both models in parallel, with the same specific question:
   ```bash
   git diff main...HEAD | scripts/ask-codex.sh  <slug> "<question>" &
   git diff main...HEAD | scripts/ask-gemini.sh <slug> "<question>" &
   wait
   ```
   Good questions are narrow:
   - "Find correctness bugs and missing states in this diff."
   - "Does this plan meet playbook/CRITERIA.md lines 1-5? What is missing?"
   - "Rank the top 5 visual problems in these screens against AGENTS.md section 6."
3. Reconcile. Write `docs/reviews/<date>-<slug>-decision.md` with:
   - points both agree on (usually act on these);
   - points only one raised (judge each on its merits);
   - what you will change, and what you reject and why.
4. Apply the accepted changes, then re-run the quality gates.

## Rules
- Never paste secrets or `.env` contents into the context.
- If a CLI is missing or signed out, note it in the decision file and continue with the other one.
- The reviewers run read-only. They never edit the repo.
- Don't loop: one round of review per plan or PR, plus at most one re-check after big changes.
