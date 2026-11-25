# 26 · Delivery app: pick-up/drop confirmation, live re-plan, exceptions, polish

**Who:** Amogh · **When:** 4 Dec · **Account:** Amogh's Claude trial.
**Tools:** Claude Code `/model opus`, plan mode; compose + m3-expressive skills; mobile-mcp (two devices: delivery + shop).
**Depends on:** 25 (and 22 for the owner-confirm side, which can be stubbed if not merged yet).
**Criteria moved:** T3, A3, A5 (recovery).

## Paste into Claude Code
```text
Read AGENTS.md, PROGRESS.md, design/specs/delivery/ (stop detail, live change, exceptions, day end, offline) and docs/PRD.md journey (g).
On branch p26-delivery-confirm:
1. Confirm pick-up or drop:
   - count stepper (units);
   - batch check (scan a barcode with CameraX + ML Kit if quick, else confirm the batch shown);
   - owner confirmation via a push to the owner's phone (Approve) or a 4-digit OTP the owner reads out.
   - Posts stop.confirmed with an idempotency key (outbox if offline).
2. Live re-plan:
   - on route.updated, animate the list re-order (shared elements, springs) and the map markers;
   - show a plain-language reason ("Bansal Kirana took only 3; Stop 5 added");
   - never lose the driver's in-progress stop.
3. Exceptions: shop closed, count mismatch, owner refuses. Each posts an exception that the agent handles (re-plan for the next route day) and appears on the dashboard.
4. Documents to hand over: show the credit note / clearance bill PDF; mark it as handed over.
5. Day end: summary, everything synced, outbox empty.
6. Polish pass: states (empty, loading, error, offline), haptics, TalkBack, sunlight contrast, baseline profile.
7. Two-device test: the delivery app on the S24 + the shop app on an emulator. Run the agent, accept "only 3" on the shop, and watch the delivery route re-order live. Record a video to docs/screens/android/delivery/.
Plan first, build, run the gates, update PROGRESS.md, push, open a PR.
```

## Done when
- [ ] A full delivery day works with confirmations, one live re-plan and one exception.
- [ ] The dashboard reflects every stop event.
