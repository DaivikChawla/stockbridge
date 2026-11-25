@AGENTS.md

# Claude Code notes (in addition to AGENTS.md)

## Model and mode
- Use the newest Opus for everything in this repo: run `/model opus` at the start of a session. The alias always picks the newest Opus, so a new release is used automatically.
- Start every playbook prompt in **plan mode** (Shift+Tab until it says plan mode). Write the plan, get approval, then build.
- Use subagents generously:
  - `Explore` for searching the codebase;
  - parallel subagents for independent pieces (for example, three screens, or backend + web client);
  - a fresh subagent to review your own diff before you finish.

## Saving usage without losing quality
- One playbook prompt per session. Run `/clear` between prompts; the repo (PROGRESS.md, docs/) carries the context, not the chat.
- Read only the files you need. Don't paste large logs; summarise them.
- Hand reviews, test scaffolds, proofreading and research to the second-opinion tools (below), not to Opus.
- At 80% of the 5-hour limit, stop starting new work. Finish the current step, write the PROGRESS entry, commit and push.

## Second opinions (ChatGPT Plus and Google AI Pro, from the terminal)
Use the `second-opinion` skill (`.claude/skills/second-opinion/`). It runs:
- `scripts/ask-codex.sh`: Codex CLI, signed in with ChatGPT Plus, read-only sandbox;
- `scripts/ask-gemini.sh`: Antigravity CLI `agy -p`, signed in with Google AI Pro.

Both write to `docs/reviews/`. Use them:
- on every plan before approval in prompts 01, 02 and 03;
- on every PR before merge;
- after two failed attempts at the same bug;
- for design critique.

Weigh their answers yourself; never apply them blindly. If a CLI isn't installed or signed in, say so and continue.

Fallback for jobs the CLIs can't do (Deep Research, image generation): ask the human, or use Claude in Chrome on chatgpt.com or gemini.google.com when the human has it set up.

## Which tool for which job
| Job | Use |
|---|---|
| Current library and API docs (Compose, Next.js, FastAPI, OR-Tools, Ktor) | Context7 MCP ("use context7") |
| Android build, emulator, device, Compose previews, Journeys tests | Android CLI (`android …`) and the Android skills |
| M3 Expressive components and Compose correctness | `m3-expressive-compose` skill and `compose-skill` |
| Drive the emulator or the S24, take screenshots, tap through flows | mobile-mcp |
| Brand, design system, screen mock-ups, deck | Claude Design: `/design`; `/design-sync` keeps tokens in step |
| Read or write Figma frames, hand-off specs | Figma MCP (official plugin) |
| Web components | shadcn MCP first, then 21st.dev MCP for richer pieces; restyle with our tokens |
| Web look and polish | `frontend-design`, then Taste Skill (`design-taste-frontend`), then Impeccable (`/impeccable critique`, `polish`, `audit`); Vercel `web-design-guidelines` to review |
| Web animation | Motion skill + Motion MCP (docs, best practices); Emil Kowalski skills to review motion |
| Web QA and screenshots | Playwright MCP |
| Database | Supabase MCP (read-only by default; schema changes go through Alembic migrations in code) |
| Demo and pitch video | Remotion skills in `video/` |
| GitHub issues and PRs | GitHub MCP or `gh` |

## Don'ts
- Don't change the stack or the API contract without a `docs/DECISIONS.md` entry.
- Don't mark work done without the AGENTS.md quality gates.
- Don't end a session without a PROGRESS.md entry, a commit and a push.
