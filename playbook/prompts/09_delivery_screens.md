# 09 · Delivery app screens

**Who:** Amogh · **When:** 29–30 Nov.
**Tools:** Stitch for exploration, then Claude Design (`/design`).
**Depends on:** 07.
**Criteria moved:** T3, A3 (acts in external systems), A5 (recovers).

## Stitch brief (3 variants per screen, saved to `design/explore/delivery/`)
```text
Android app, Material 3 Expressive, for a delivery partner on a two-wheeler or van in Patiala.
Used outdoors in sunlight with one hand: high contrast, huge buttons, minimal text, Hindi-first.
Screen: <name>. Real shop names, real items, ₹ amounts. No gradients, glow or decorative pills.
```

## Claude Design
```text
/design
Read AGENTS.md, docs/PRD.md (delivery journeys), design/brand/BRAND.md, design/tokens.json, design/COMPONENTS.md, design/explore/delivery/.
Design the Delivery app for the S24, light and dark (dark is important outdoors at dusk), Hindi primary:
1. Today: route summary (stops, items to pick up and drop, credit notes to hand over), start button.
2. Map + list: MapLibre map with numbered stops in order; the current stop expanded; navigation hand-off to Google Maps.
3. Stop detail:
   - pick-up: count the units, scan or confirm the batch, owner taps to confirm on their phone or by OTP;
   - drop: count, owner confirm.
   - Show the documents to hand over.
4. Live change: the plan changed (a new stop added, or one removed). An animated re-order with a clear explanation ("Bansal Kirana took only 3; route updated").
5. Exceptions: shop closed, count mismatch, owner refuses. Each one sends a report to the distributor.
6. Day end: summary, sync status.
7. Offline: actions queued, "will send when online".
Annotate motion for the live re-order (shared element on stops, spring). Export to design/screens/delivery/ with DESIGN.md sections.
```

## Done when
- [ ] All 7 screens in `design/screens/delivery/`, light and dark, motion annotated.
