#!/usr/bin/env bash
# Ask Codex (signed in with ChatGPT Plus) for a second opinion. Read-only: it cannot edit files.
#
# Usage:
#   scripts/ask-codex.sh <slug> "<question>"                 # Codex reads the repo itself
#   git diff main | scripts/ask-codex.sh <slug> "<question>" # pipe extra context (a diff, a plan)
#
# The answer is printed and saved to docs/reviews/<date>-<slug>-codex.md
set -euo pipefail

if ! command -v codex >/dev/null 2>&1; then
  echo "codex CLI not installed. See playbook/TOOLS_SETUP.md (Codex CLI)." >&2
  exit 2
fi
[ $# -ge 2 ] || { echo "usage: $0 <slug> \"<question>\"" >&2; exit 1; }

slug="$1"; shift
question="$*"
root="$(git rev-parse --show-toplevel)"
out="$root/docs/reviews/$(date +%Y-%m-%d)-${slug}-codex.md"
mkdir -p "$root/docs/reviews"

preamble="You are a senior reviewer on the Stockbridge repo. Read AGENTS.md first.
Be specific: cite file:line, rank issues by severity, and say what you would change.
Do not rewrite everything; only flag what matters for correctness, quality and the judging criteria in playbook/CRITERIA.md."

cd "$root"
{
  echo "# Codex review: ${slug} ($(date '+%Y-%m-%d %H:%M'))"
  echo
  echo "**Question:** ${question}"
  echo
  # If stdin is piped, Codex treats it as extra context for this instruction.
  codex exec --sandbox read-only "${preamble}

${question}"
} | tee "$out"

echo >&2
echo "Saved: ${out#$root/}" >&2
