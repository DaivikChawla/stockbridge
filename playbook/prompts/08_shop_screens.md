# 08 · Shop app screens

**Who:** Amogh · **When:** 28–29 Nov.
**Account:** Amogh's Claude (free plan includes Claude Design) + Google Stitch (free) for exploration.
**Depends on:** 07 (tokens; a draft is enough to start exploring).
**Criteria moved:** T3, C1 (voice-first, vernacular), C2 (limited literacy), A6 (approvals).

## Step 1: explore in Google Stitch (fast, many variants)
For each screen below, generate 3 variants in Stitch using this brief, and keep the best ideas as PNGs in `design/explore/shop/`:
```text
Android app, Material 3 Expressive, for an Indian kirana shop owner (Hindi-first, may have limited literacy).
Warm, trustworthy, precise; large touch targets; icons + short words; numbers big and clear.
Screen: <name>. Content: <from the list below>. Use real Indian products and ₹ prices.
No gradients, no glow, no decorative pills, no emoji icons.
```

## Step 2: final screens in Claude Design
```text
/design
Read AGENTS.md (sections 5, 6), docs/PRD.md (Shop app journeys), design/brand/BRAND.md, design/tokens.json, design/COMPONENTS.md, and the explorations in design/explore/shop/.
Design the Shop app for a Samsung Galaxy S24 (1080×2340, 120 Hz), light and dark, in Hindi (primary), with English and Punjabi variants of 3 key screens.
Screens and states:
1. Onboarding: language pick (spoken prompt), consent (mic, notifications, data use; plain words + icons), shop setup by a JanAI Café helper (catalogue import from a distributor bill photo: simulated, labelled).
2. Home: today's sales, money in, 1–2 urgent items (approval waiting, stock expiring), mode switch Auto / Manual.
3. Counter, Auto mode:
   - live listening indicator;
   - running list of heard items as they're said;
   - the UPI amount arriving;
   - three outcomes: bill saved (match), one-tap question (ambiguous), doesn't add up (mismatch).
4. Manual mode: speak or tap items; quick-pick of frequent items; amount; save.
5. Bills: list + detail; cash sale confirm.
6. Requests inbox: give / take / clearance offers with Approve, Only N, Decline; detail with what the owner gets (credit note or clearance price) and why; privacy: never other shops' sales.
7. Stock: items with days of cover and expiry badges; batch detail.
8. Khata: customers and dues.
9. Reorder: suggestion within the weekly budget; owner edits and approves.
10. Weekly report.
11. Settings: language, Auto/Manual, consent, helper mode.
12. Network-lost banner and the "sent when online" state on a bill and an approval.
For each screen, show the motion intent (what animates on enter, on select, on success) as annotations.
Export PNGs to design/screens/shop/ and a DESIGN.md section per screen (layout, components used, states, strings).
```

## Done when
- [ ] All 12 screens are in `design/screens/shop/`, light and dark, with annotations.
- [ ] Strings are listed per screen, in Hindi and English.
