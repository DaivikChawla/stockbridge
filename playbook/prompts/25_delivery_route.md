# 25 · Delivery app: today's route, map, stops

**Who:** Amogh · **When:** 3 Dec · **Account:** Amogh's Claude trial.
**Tools:** Claude Code `/model opus`, plan mode, second opinion on the plan; compose + m3-expressive skills; context7 (MapLibre Android); mobile-mcp.
**Depends on:** 18, 13.
**Criteria moved:** T3, A3.

## Paste into Claude Code
```text
Read AGENTS.md, PROGRESS.md, docs/ARCHITECTURE.md, design/specs/delivery/ and design/screens/delivery/, and the backend route/stop API and route WebSocket events.
Map tiles must be free: use MapLibre with a free OSM-based style (e.g. OpenFreeMap; check its current terms) and credit OSM on the map.

Build :app-delivery on branch p25-delivery-route, matching the designs:
1. Sign-in as delivery_partner (simulated OTP).
2. Today: route summary (stops, pick-ups, drops, documents to hand over), Start.
3. Map + list:
   - MapLibre map with numbered stop markers in order and the current location (location permission with an explainer);
   - a bottom sheet list synced with the map;
   - "Navigate" hands off to Google Maps with an intent.
4. Stop detail (read-only in this prompt): what to pick up or drop, batch, counts, documents.
5. Live connection to /ws/route/{id}, with resume. Shows the connection state subtly.
6. Dark theme first-class (dusk), high contrast, one-hand reach.
7. Tests: route view model, marker ordering, WebSocket reconnect.
8. Run on a device or emulator with seeded demo data. Screenshot to docs/screens/android/delivery/.
Plan first. Run the second-opinion skill on the plan, build, run the gates, update PROGRESS.md, push, open a PR.
```

## Done when
- [ ] The seeded route shows on the map and the list. Stops are ordered. Navigation hand-off works. Live connection is shown.
