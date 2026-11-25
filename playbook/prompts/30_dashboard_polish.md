# 30 · Dashboard polish: taste, Impeccable, motion review, accessibility, performance

**Who:** Amogh · **When:** 8–9 Dec (two sessions) · **Account:** Amogh's Claude trial.
**Tools:**
- Claude Code `/model opus`;
- **Impeccable** (`/impeccable critique`, `audit`, `polish`), **design-taste-frontend**, Vercel **web-design-guidelines**;
- Emil Kowalski `review-animations` and `animation-performance`; Motion AI Kit;
- Playwright MCP; second-opinion skill with screenshots.

**Depends on:** 27–29.
**Criteria moved:** T3.

## Paste into Claude Code
```text
Read AGENTS.md section 6, design/brand/BRAND.md, design/REVIEW.md and all web specs.
Polish web/ on branch p30-dashboard-polish. Keep before/after screenshots in docs/screens/web/polish/.
1. Run /impeccable audit and /impeccable critique on every page; fix everything rated important. Run /impeccable polish on the Overview and Agent run pages.
2. Run the web-design-guidelines review: focus states, labels, keyboard navigation, touch targets, motion with a reduced-motion fallback. Fix the findings.
3. Motion: review-animations + animation-performance skills; one coherent choreography (the same springs everywhere, from tokens); no layout thrash; 60 fps on a mid-range laptop and smooth on a projector.
4. Typography and numbers: Indian number formatting, tabular numerals in tables, Devanagari and Gurmukhi rendering.
5. Performance: Lighthouse at 90+ on Overview (Playwright runs it); bundle analysis; lazy-load the map; Suspense streaming.
6. Run the second-opinion skill with screenshots:
   "You are a design-literate industry judge seeing this on a projector. Rank the 10 things that look generic, AI-generated or unfinished."
   Fix them.
7. Final screenshots at 1440, 1280 and 390 px, light and dark.
Run the gates, update PROGRESS.md, push, open a PR.
```

## Done when
- [ ] Impeccable important issues are zero. Lighthouse 90+. Reviewers' top-10 fixed. It looks hand-made, not generated.
