# Playbook: start here

The team's operating manual for the Tech4Bharat GAVS prototype round. It covers 25 Nov to 15 Dec 2026, then the finale on 27 Dec.

| File | What it is |
|---|---|
| [MASTER_WORKFLOW.md](MASTER_WORKFLOW.md) | Roles, the daily calendar, how to run a prompt, tools, risks, definition of done |
| [CRITERIA.md](CRITERIA.md) | What the judges score, and the evidence we must show for each line |
| [TOOLS_SETUP.md](TOOLS_SETUP.md) | Accounts, installs, MCP servers, skills, design tools |
| [BUDGET.md](BUDGET.md) | Free resources, the ≤ ₹2,000 spend plan, what not to buy |
| [prompts/](prompts/) | 35 numbered prompts (00–34), one focused session each |

Also at the repo root:
- [`AGENTS.md`](../AGENTS.md): rules for every agent;
- [`CLAUDE.md`](../CLAUDE.md): Claude-specific notes;
- [`PROGRESS.md`](../PROGRESS.md): the hand-off log;
- [`.mcp.json`](../.mcp.json);
- [`scripts/`](../scripts/);
- [`.claude/skills/second-opinion`](../.claude/skills/second-opinion/SKILL.md).

## Quick start for a new session (any teammate, any account)
1. `git pull`. Read the top entry of `PROGRESS.md`.
2. Find your next prompt in `MASTER_WORKFLOW.md` section 4.
3. Start Claude Code, run `/model opus`, switch to plan mode, then paste the prompt's block.
4. Before stopping: update `PROGRESS.md`, commit, push.
