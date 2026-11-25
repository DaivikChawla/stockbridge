# TOOLS_SETUP.md: accounts, installs, MCPs and skills

Do this once per laptop (prompt 00). Commands were checked against the official pages on 25 Nov 2026.
If a command fails, open the linked page: install steps change often.

## 1. Accounts (each teammate unless marked)

| Account | Who | Notes |
|---|---|---|
| GitHub + **Student Developer Pack** | all | https://education.github.com/pack. Verify with your Thapar ID. Unlocks `.tech`, Azure, Copilot Student |
| `.tech` domain | Daivik | Claim from the pack; suggest `stockbridge.tech` |
| Azure for Students | Parv | $100, no card. Backend hosting |
| Supabase | Parv | One project: `stockbridge` (region Mumbai) |
| Vercel | Amogh | Import the GitHub repo, root `web/` |
| Firebase | Daivik | One project with two Android apps (shop, delivery) for FCM |
| Sarvam | Parv | https://www.sarvam.ai/apis/speech-to-text; ₹100 free credits |
| NVIDIA NIM | Parv | https://build.nvidia.com; free API key |
| Claude | all | Daivik: Pro. Amogh and Parv: free week (start the trial on the day in MASTER_WORKFLOW) |
| ChatGPT Plus | Daivik | Codex CLI + deep research |
| Google AI Pro | Daivik | Antigravity (`agy`), Gemini Deep Research, Stitch |
| Figma (free) | Daivik, Amogh | For hand-off only |
| Lyzr | Parv | When the organisers' credits arrive |

Keep keys in each folder's `.env` (git-ignored). Never paste keys into chat, prompts or issues.

## 2. Installs

| Tool | Install | Link |
|---|---|---|
| Android Studio (latest stable) + JDK 21 | Installer | https://developer.android.com/studio |
| **Android CLI** | macOS (Apple chip): `curl -fsSL https://dl.google.com/android/cli/latest/darwin_arm64/install.sh \| bash` · Linux: `curl -fsSL https://dl.google.com/android/cli/latest/linux_x86_64/install.sh \| bash` · Windows: download page. Then `android update` and `android init` | https://developer.android.com/tools/agents/android-cli/download |
| Node 22+ and pnpm | `corepack enable` | https://nodejs.org |
| Python 3.12 + uv | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | https://docs.astral.sh/uv |
| **Claude Code** | Native installer | https://code.claude.com |
| **Codex CLI** (ChatGPT Plus) | `curl -fsSL https://chatgpt.com/codex/install.sh \| sh` or `npm i -g @openai/codex`; run `codex` once and pick "Sign in with ChatGPT" | https://developers.openai.com/codex/cli |
| **Antigravity CLI `agy`** (Google AI Pro) | `curl -fsSL https://antigravity.google/cli/install.sh \| bash`; run `agy` once to sign in. Gemini CLI no longer serves AI Pro accounts | https://antigravity.google/docs/cli/headless |
| Antigravity app (optional) | For Gemini-side exploration and review | https://antigravity.google/download |
| Claude in Chrome (optional) | Lets Claude use chatgpt.com and gemini.google.com in your browser, e.g. to start a Deep Research run | Claude settings |
| scrcpy (optional) | Mirror the S24 to the laptop for recording the demo | https://github.com/Genymobile/scrcpy |

### Android Studio with Claude inside it (optional, nice for previews)
Android Studio supports **Bring Your Own Agent**: Settings → AI → choose Claude Agent. Claude then works with Studio's project graph, build diagnostics and emulator.
- https://developer.android.com/ai-tools/guides/quickstart
- https://developer.android.com/blog/posts/build-it-your-way-a-next-era-of-android-development

## 3. MCP servers
`.mcp.json` in the repo already lists these; Claude Code asks you to approve them on first run:

| Server | Purpose | Auth |
|---|---|---|
| figma | Read and write Figma frames, hand-off specs | `/mcp` → figma → Authenticate. Better: install the Figma plugin (section 4), which adds Figma's skills |
| context7 | Current docs for Compose, Next.js, FastAPI, OR-Tools, Ktor | `/mcp` → Authenticate, or `npx ctx7 setup --claude` |
| supabase | Inspect the database (read-only) | `/mcp` → Authenticate |
| github | Issues and PRs | `export GITHUB_PAT=<fine-grained token, this repo only>` before starting Claude |
| shadcn | Search and add shadcn/ui components | none |
| playwright | Drive the dashboard in a real browser, screenshots | none |
| mobile-mcp | Drive the emulator or S24 (USB debugging on), screenshots, taps | needs Android platform-tools |

Installed by their own commands, not in `.mcp.json`:
- **21st.dev MCP:** `npx @21st-dev/cli@latest init --client claude`. https://21st.dev/mcp
- **Motion AI Kit:** follow https://motion.dev/docs/ai-kit-install. Docs search and best practices are free; Motion+ features are not needed.

## 4. Skills and plugins
Run `bash scripts/setup-tools.sh` from the repo root. It installs:

| Skill | For | Source |
|---|---|---|
| Taste Skill (`design-taste-frontend`) | Art direction for the dashboard and landing | https://github.com/Leonxlnx/taste-skill |
| Impeccable | `/impeccable critique`, `polish`, `audit`; catches AI-slop tells | https://github.com/pbakaus/impeccable |
| Vercel `web-design-guidelines` | Pre-merge UI review (accessibility, focus, motion) | https://github.com/vercel-labs/agent-skills |
| Emil Kowalski skills | Animation build and review (`animate`, `review-animations`, `animation-performance`) | https://github.com/emilkowalski/skills |
| compose-skill | Correct Compose (state, recomposition, navigation, animation) | https://github.com/aldefy/compose-skill |
| m3-expressive-skill | Material 3 Expressive APIs that compile | https://github.com/sanikantv/m3-expressive-skill |
| Android skills (all) | Google's official Android agent skills | https://github.com/android/skills |
| Remotion skills | Code-built demo video | https://www.remotion.dev/docs/ai/skills |

Then, inside Claude Code, paste once:
```
/plugin install frontend-design@claude-plugins-official
/plugin install figma@claude-plugins-official
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill
/plugin marketplace add android/skills
/plugin install android-skills@android-skills
/plugin marketplace add mobile-next/mobile-mcp
/plugin install mobile-mcp@mobile-mcp
```

Already in the repo: `.claude/skills/second-opinion/` (Codex + Gemini reviews).

## 5. Design tools

| Tool | Use | Notes |
|---|---|---|
| **Claude Design** | Brand, design system, final screens, deck | Inside Claude Code: `/design`; keep code and design in step with `/design-sync`. The standalone site (claude.ai/design) stays open until 14 Dec 2026 |
| **Google Stitch** | Fast exploration of many Android screen variants; exports `DESIGN.md` | Free with daily credits |
| **Figma** (free) | One hand-off file; Figma MCP reads it | Watch the MCP call limits on free seats |

## 6. Check it all works (5 minutes)
- [ ] `claude` → `/mcp` shows figma, context7, supabase, github, shadcn, playwright and mobile-mcp as connected.
- [ ] `/skills` (or ask "what skills do you have?") lists the skills above.
- [ ] `scripts/ask-codex.sh test "Say hello and name the repo"` prints an answer.
- [ ] `scripts/ask-gemini.sh test "Say hello and name the repo"` prints an answer.
- [ ] `android devices` (or `adb devices`) shows the S24 with USB debugging on.
- [ ] The current agent runs: `pip install -r requirements.txt && uvicorn server:app` → http://localhost:8000.
