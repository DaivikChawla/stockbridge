#!/usr/bin/env bash
# Ask Gemini through the Antigravity CLI (agy, signed in with Google AI Pro) for a second opinion.
# Runs headless in plan mode, so it should not edit files.
#
# Usage:
#   scripts/ask-gemini.sh <slug> "<question>"
#   git diff main | scripts/ask-gemini.sh <slug> "<question>"
#
# The answer is printed and saved to docs/reviews/<date>-<slug>-gemini.md
set -euo pipefail

if ! command -v agy >/dev/null 2>&1; then
  echo "agy (Antigravity CLI) not installed. See playbook/TOOLS_SETUP.md (Antigravity CLI)." >&2
  exit 2
fi
[ $# -ge 2 ] || { echo "usage: $0 <slug> \"<question>\"" >&2; exit 1; }

slug="$1"; shift
question="$*"
root="$(git rev-parse --show-toplevel)"
out="$root/docs/reviews/$(date +%Y-%m-%d)-${slug}-gemini.md"
mkdir -p "$root/docs/reviews"

preamble="You are a senior reviewer on the Stockbridge repo. Read AGENTS.md first. Do not edit any files.
Be specific: cite file:line, rank issues by severity, and say what you would change.
Only flag what matters for correctness, quality and the judging criteria in playbook/CRITERIA.md."

context=""
if [ ! -t 0 ]; then
  context="$(cat)"
fi

cd "$root"
{
  echo "# Gemini review: ${slug} ($(date '+%Y-%m-%d %H:%M'))"
  echo
  echo "**Question:** ${question}"
  echo
  agy --mode=plan -p "${preamble}

${question}

${context:+Context:
${context}}"
} | tee "$out"

echo >&2
echo "Saved: ${out#$root/}" >&2
