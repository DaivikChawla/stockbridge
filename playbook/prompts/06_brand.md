# 06 · Brand: identity, colour, type, voice, motion principles

**Who:** Daivik · **When:** 28 Nov · **Account:** Daivik's Claude Pro.
**Tool:** Claude Code `/design` (Claude Design). Optional: Stitch for quick colour and type explorations.
**Depends on:** 01.
**Criteria moved:** T3 (a product that looks real), and the pitch.

## Context for the designer
- Who sees this:
  - kirana owners on Android (often older; Hindi or Punjabi first);
  - delivery partners outdoors in sunlight;
  - distributors on a laptop;
  - judges, who are industry leaders, on an S24 and a projector.
- The feeling: trustworthy, warm, local, precise; like a good ledger, not a tech toy.
- The earlier deck used a warm paper palette with Fraunces headings and Inter body text, and the team liked it.
- Avoid every "AI slop" item in AGENTS.md section 6.

## Paste into Claude Code
```text
/design
Read AGENTS.md (sections 1, 5, 6), docs/PRD.md (users), and research/ notes if present.
Create the Stockbridge brand, as design/brand/BRAND.md plus assets:
1. Three distinct brand directions, each with:
   - a moodboard description;
   - a palette with roles (primary, surface, success, warning, danger, info) that works in light and dark on Android M3 Expressive;
   - a type pairing that supports Latin, Devanagari and Gurmukhi (check Google Fonts coverage: e.g. Noto Sans Devanagari / Gurmukhi pairings);
   - an icon style;
   - an example screen: Shop app home with a pending approval.
   Show them to me side by side. I pick one.
2. For the chosen direction:
   - a logo mark + wordmark (SVG, simple, works at 24 px and on an app icon);
   - an Android adaptive app icon for Shop and Delivery (same family, distinguishable);
   - a favicon;
   - an OG image.
3. Voice and tone: how the app speaks to an owner in Hindi, Punjabi and English. Short, respectful, no jargon. 10 example strings each (approve request, bill doesn't add up, stock expiring, network lost).
4. Motion principles: what moves, why, with which spring. Map them to M3 Expressive MotionScheme (spatial vs effects springs) and to Motion (web) spring values.
5. Colour contrast check (AA) for every text and background pair.
Export to design/brand/. Then update PROGRESS.md, commit on p06-brand, push, open a PR.
```

## Done when
- [ ] One direction chosen. Logo, app icons, palette, type, voice and motion are documented in `design/brand/`.
- [ ] Contrast checked. No slop patterns.
