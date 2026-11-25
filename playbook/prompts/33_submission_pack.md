# 33 · Submission pack: Remotion demo video, deck, README, criteria self-check

**Who:** all. Daivik's Claude builds; Amogh records phone footage; Parv writes and checks copy.
**When:** 13–14 Dec. **Submit Mon 14 Dec.**
**Tools:**
- Claude Code `/model opus`;
- **Remotion skills** (`/remotion-best-practices`, `/remotion-captions`, `/remotion-maps`, `/remotion-render`);
- **Claude Design** (`/design`) for the deck;
- scrcpy for S24 screen recording;
- ChatGPT and Gemini as hostile reviewers.

**Depends on:** 32. Also needs `docs/round2_requirements.md` (exact video length and fields).
**Criteria moved:** all; this is how judges first see the work.

## Step 1: footage (Amogh, human)
Record each demo beat from `DEMO_SCRIPT.md`:
- S24 screen via scrcpy (`scrcpy --record shop.mp4`);
- the dashboard via screen capture;
- a short real-world clip of a counter (with consent).

Put the clips in a shared drive and list them in `video/FOOTAGE.md`.

## Step 2: paste into Claude Code (Daivik)
```text
Read AGENTS.md, docs/round2_requirements.md, docs/DEMO_SCRIPT.md, playbook/CRITERIA.md, docs/research/MARKET.md, docs/field/synthesis.md, backend/evals/results/REPORT.md and video/FOOTAGE.md.

1. Video (video/, Remotion). Set up the project with the Remotion skills (check the licence with /remotion-license; we are a team of 3 students).
   - Composition "PrototypeDemo", at the required length (default 3:00, 1080p, 30 fps):
     problem (with 1–2 field quotes) → the hero sale on the S24 (footage + animated callouts) → the agent cycle on the dashboard (footage + an animated trace overlay) → delivery live re-plan → evals and impact (animated numbers, each labelled measured or synthetic) → business model → team.
   - Captions throughout (/remotion-captions), in English with Hindi phrases subtitled. Use the brand tokens for every overlay. No stock-AI look.
   - An optional animated route map with /remotion-maps (MapLibre).
   - Render to out/stockbridge_prototype.mp4. Voiceover: leave a track for a team member's recorded voice; give me the script in video/VOICEOVER.md, timed to the cut.
2. Deck: run /design to build the prototype-round deck (10–12 slides) from the brand.
   - Problem (field evidence), solution, live demo stills, architecture, AI quality (evals), agentic proof (the trace), innovation, market (verified numbers), business model and unit economics, scalability, job creation, roadmap, team.
   - Export PDF and PPTX to docs/submission/.
   - Every number cited or labelled.
3. README: update for judges. One-paragraph pitch, demo video link, APK links, live dashboard URL, architecture diagram, how to run, evals summary, guardrails, "Simulated integrations" list, AI tools used (Claude, Codex, Gemini/Antigravity, NIM, Sarvam, Lyzr), team.
4. Self-check: score every line in playbook/CRITERIA.md 0/1/2 in docs/submission/SELF_SCORE.md with evidence links. Fix anything at 0 that can be fixed today.
5. Hostile review:
   scripts/ask-codex.sh judge "You are a tough industry judge. Watch-read the deck PDF text and README. Score 1-10 on each criterion in playbook/CRITERIA.md and list the 5 weakest points."
   scripts/ask-gemini.sh judge "<same>"
   Fix what's fixable.
6. docs/submission/CHECKLIST.md: every form field from round2_requirements.md with the exact text or link to paste.
Update PROGRESS.md, push, open a PR. Tag v1.0-prototype-submission after merge.
```

## Step 3: submit (Daivik, human)
Fill in the HackCulture form from `CHECKLIST.md`. Save a screenshot of the confirmation in `docs/submission/`. Tell the team.

## Done when
- [ ] Video, deck, README, APKs and live URL are all linked in the form.
- [ ] Self-score has no 0s. Submitted on 14 Dec, with the confirmation saved.
