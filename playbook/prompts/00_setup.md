# 00 · Setup (everyone, about 2 hours)

**Who:** Daivik, Amogh and Parv, each on their own laptop.
**When:** Wed 25 Nov.
**Tool:** none (human checklist). Claude helps only if something breaks.
**Criteria moved:** none directly; everything depends on it.

## Steps
1. Work through `playbook/TOOLS_SETUP.md` sections 1–5.
2. Clone the repo, then run the setup script:
   ```bash
   git clone https://github.com/DaivikChawla/stockbridge && cd stockbridge
   ```
   ```bash
   bash scripts/setup-tools.sh
   ```
3. Start Claude Code in the repo and paste the plugin commands that the script printed.
4. Go through the checklist in `TOOLS_SETUP.md` section 6.
5. **Daivik only:**
   - Paste the prototype-round email or form text into `docs/round2_requirements.md`: video length, deck, APK, links, fields.
   - Create GitHub labels: `backend`, `android-shop`, `android-delivery`, `web`, `design`, `research`, `field`, `bug`, `blocked`.
   - Turn on branch protection for `main`: PR required, no force-push.
6. Put the S24 in developer mode with USB debugging on, then check it appears in `adb devices`.

## If something fails, paste into Claude Code
```text
I'm setting up this repo following playbook/TOOLS_SETUP.md. This step failed:
<paste the command and the error>
My OS is <macOS / Windows / Linux>. Find the current official install method (use context7 or the linked page),
fix it, and update TOOLS_SETUP.md if the documented command is wrong. Don't install anything system-wide without asking.
```

## Done when
- [ ] Everyone's `TOOLS_SETUP.md` section 6 checklist is green, or failures are listed in PROGRESS.md with an owner.
- [ ] `docs/round2_requirements.md` exists, even if it only says "email not received yet".
