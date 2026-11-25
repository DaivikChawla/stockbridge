# 22 · Shop app: approvals inbox, push, clearance offers

**Who:** Daivik · **When:** 6 Dec · **Account:** Daivik's Claude Pro.
**Tools:** Claude Code `/model opus`, plan mode; compose + m3-expressive skills; mobile-mcp (two devices if available: the S24 + an emulator as the second shop).
**Depends on:** 18, 13, 15 (16 for voice and messages, if ready).
**Criteria moved:** A3, A4, A6 (human approval), T3, T4 (clearance).

## Paste into Claude Code
```text
Read AGENTS.md, PROGRESS.md, design/specs/shop/ (requests inbox, request detail), docs/PRD.md journeys (e, f), and the backend agent API and events.
On branch p22-approvals:
1. Push: FCM data messages deep-link to the request; the notification shows the summary in the owner's language, with Approve and Decline actions that work from the notification shade (with an auth check).
2. Inbox: give / take / clearance requests with clear consequences:
   - "you get a credit note of ₹2,160";
   - "you pay ₹10 each instead of ₹17";
   - expiry date;
   - why.
   A receiver never sees the giver's sales.
3. Answer: Approve, Only N (number stepper), Decline (optional reason chips). Optimistic UI; outbox when offline; idempotency key.
4. Listen button: reads the request aloud (TTS from prompt 16).
5. Live updates over the shop WebSocket: a new request slides in, a withdrawn request animates out, and a "plan changed" note appears.
6. History: past requests, answers and resulting documents (view the credit note / clearance bill PDF).
7. Tests: answer flows, offline answer, notification action, privacy (no giver data in the receiver's view model).
8. Two-device test: the S24 as Bansal Kirana and an emulator as Sharma General Store. Run the agent from the dashboard (or curl). Both receive requests; answers re-plan live. Record a short video.
Plan first, build, run the gates, update PROGRESS.md, push, open a PR.
```

## Done when
- [ ] The end-to-end agent cycle works across two devices, live, including "Only 3" and Decline leading to a re-plan.
