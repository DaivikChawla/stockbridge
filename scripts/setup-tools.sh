#!/usr/bin/env bash
# One-time setup of the agent skills this repo expects. Safe to re-run (it updates).
# Run from the repo root on each teammate's laptop: bash scripts/setup-tools.sh
#
# Installs skills into the project (.claude/skills, .agents/skills) through the open `skills` CLI,
# so Claude Code, Codex and Antigravity all see them.
#
# Claude Code plugins and the MCP sign-ins can't be scripted; the script prints them at the end.
set -uo pipefail

ok()   { printf '  \033[32mok\033[0m   %s\n' "$1"; }
warn() { printf '  \033[33mskip\033[0m %s\n' "$1"; }
step() { printf '\n\033[1m%s\033[0m\n' "$1"; }

need() { command -v "$1" >/dev/null 2>&1; }

step "1. Checking prerequisites"
for c in git node npx python3; do need "$c" && ok "$c" || warn "$c missing (see playbook/TOOLS_SETUP.md)"; done
node -e 'process.exit(+process.versions.node.split(".")[0] >= 22 ? 0 : 1)' 2>/dev/null \
  && ok "node >= 22" || warn "node 22+ recommended (Taste Skill and Context7 need it)"
for c in claude codex agy android uv pnpm; do need "$c" && ok "$c" || warn "$c not installed yet"; done

step "2. Web design and animation skills"
npx -y skills@latest add github.com/Leonxlnx/taste-skill --skill "design-taste-frontend" && ok "Taste Skill" || warn "Taste Skill"
npx -y skills@latest add vercel-labs/agent-skills --skill web-design-guidelines && ok "Vercel web-design-guidelines" || warn "web-design-guidelines"
npx -y skills@latest add emilkowalski/skills && ok "Emil Kowalski animation skills" || warn "Emil Kowalski skills"
npx -y impeccable install --providers=claude,codex --scope=project && ok "Impeccable" || warn "Impeccable (run: npx impeccable install)"

step "3. Android skills"
npx -y skills@latest add aldefy/compose-skill && ok "compose-skill" || warn "compose-skill"
npx -y skills@latest add sanikantv/m3-expressive-skill && ok "m3-expressive-skill" || warn "m3-expressive-skill (install as a Claude plugin, see TOOLS_SETUP)"
if need android; then
  android init && ok "Android CLI skill" || warn "android init"
  android skills add --all --project=. && ok "Android skills (all)" || warn "android skills add --all"
else
  warn "Android CLI not installed: skipping Android skills"
fi

step "4. Video"
npx -y skills@latest add remotion-dev/skills && ok "Remotion skills" || warn "Remotion skills"

step "5. MCP servers that ship their own installers"
echo "  Run these once (they edit your Claude Code config):"
echo "    npx @21st-dev/cli@latest init --client claude      # 21st.dev components (free tier)"
echo "    npx ctx7 setup --claude                             # Context7 sign-in (or /mcp -> context7 -> Authenticate)"
echo "    Motion AI Kit: follow https://motion.dev/docs/ai-kit-install (free docs + best practices)"

step "6. Inside Claude Code, paste these slash commands once"
cat <<'EOF'
    /plugin install frontend-design@claude-plugins-official
    /plugin install figma@claude-plugins-official
    /plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
    /plugin install ui-ux-pro-max@ui-ux-pro-max-skill
    /plugin marketplace add android/skills
    /plugin install android-skills@android-skills
    /plugin marketplace add mobile-next/mobile-mcp
    /plugin install mobile-mcp@mobile-mcp
    /mcp            -> authenticate figma, supabase, context7 (browser sign-in)
EOF

step "7. Second-opinion CLIs (sign in once, interactively)"
echo "    codex            # choose 'Sign in with ChatGPT' (Plus)"
echo "    agy              # sign in with the Google AI Pro account"
echo "    export GITHUB_PAT=...   # fine-grained token, repo access to DaivikChawla/stockbridge only"

printf '\nDone. Re-run any time to update skills.\n'
