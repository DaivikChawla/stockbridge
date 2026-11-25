# 11 · Design critique and hand-off

**Who:** Daivik · **When:** 1 Dec · **Account:** Daivik's Claude Pro.
**Tools:** Claude Code + Impeccable (`/impeccable critique`) + Taste Skill + the `second-opinion` skill (Codex + Gemini look at the PNGs) + Figma MCP.
**Depends on:** 08, 09, 10.
**Criteria moved:** T3.

## Paste into Claude Code
```text
Read AGENTS.md section 6, design/brand/BRAND.md, design/COMPONENTS.md, and every screen in design/screens/{shop,delivery,web}/ with its DESIGN.md section.
Run a hard design review before anyone builds:
1. Use /impeccable critique and the design-taste-frontend checks on every screen. For Android also apply the m3-expressive-compose review checklist.
   Look for:
   - consistency across the three surfaces;
   - hierarchy;
   - touch target sizes;
   - Hindi and Punjabi text length (Devanagari and Gurmukhi run longer);
   - empty, error and loading states;
   - contrast;
   - motion intent;
   - every AI-slop item in AGENTS.md.
2. Run the second-opinion skill with the screen paths:
   "Rank the 10 biggest design problems across these screens for a judge watching a live demo on a Galaxy S24 and a projector."
3. Write design/REVIEW.md: the issues ranked, with a fix for each.
4. Fix them in /design, re-export the changed screens, and note "fixed" in REVIEW.md.
5. Hand-off: put the final screens into the Figma file "Stockbridge – Hand-off", one page per surface, using the Figma MCP lightly. Write design/specs/<surface>/<screen>.md with:
   - layout grid;
   - components (from COMPONENTS.md);
   - tokens used;
   - strings (string resource keys);
   - states;
   - motion spec (which spring, which shared element);
   - analytics or events if any.
   These specs are what the build prompts read.
Update PROGRESS.md, commit on p11-design-review, push, open a PR.
```

## Done when
- [ ] `REVIEW.md` issues all fixed or consciously waived.
- [ ] Specs exist for every screen. Figma hand-off file updated.
