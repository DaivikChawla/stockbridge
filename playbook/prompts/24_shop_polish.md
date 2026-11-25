# 24 · Shop app polish: motion, transitions, haptics, states, accessibility, performance

**Who:** Daivik · **When:** 8–9 Dec (two sessions) · **Account:** Daivik's Claude Pro.
**Tools:**
- Claude Code `/model opus`;
- m3-expressive skill (review mode), compose-skill (performance), Android skills (Perfetto / profiler, baseline profiles);
- mobile-mcp for screenshots;
- second-opinion skill with screenshots.

**Depends on:** 19–23.
**Criteria moved:** T3 (the product feels real and premium on the S24).

## Paste into Claude Code
```text
Read AGENTS.md section 6, design/brand/BRAND.md (motion principles), design/REVIEW.md and every spec in design/specs/shop/.
Polish :app-shop on branch p24-shop-polish. Work screen by screen, with before/after screenshots in docs/screens/android/shop/polish/.
1. Motion:
   - M3 Expressive MotionScheme springs everywhere;
   - shared-element transitions (bill row → bill detail, request card → detail, item → stock detail);
   - predictive back with a preview;
   - shape morph on selection;
   - list item placement animations;
   - success moments (bill saved, request approved) with restrained, delightful motion and haptics.
   Use the m3-expressive skill's review checklist.
2. States: every screen has designed empty, loading (LoadingIndicator / wavy progress), error (with retry) and offline states.
3. Copy: all strings come from resources; Hindi and Punjabi fit without truncation; numbers are formatted Indian-style (₹1,23,456).
4. Accessibility:
   - TalkBack labels;
   - 48 dp targets;
   - font scale at 200% doesn't break layouts;
   - contrast AA;
   - reduced motion respected.
5. Performance:
   - generate and include a baseline profile;
   - check recomposition counts on the counter screen and the inbox;
   - Perfetto trace for cold start and the counter screen;
   - target smooth 120 Hz.
6. Run the second-opinion skill with the screenshots:
   "Rank the 10 things that still look unpolished or inconsistent for a judge on a Galaxy S24."
   Fix them.
7. Run /impeccable-style checks only as guidance (that skill is web-oriented); Android rules come from the m3-expressive skill.
Plan first, then work through it. Run the gates, update PROGRESS.md, push, open a PR.
```

## Done when
- [ ] No placeholder states anywhere. Baseline profile included. No dropped frames on the main flows.
- [ ] Reviewers' top-10 fixed.
