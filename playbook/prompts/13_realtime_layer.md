# 13 · Real-time layer: events, WebSocket/SSE, FCM push

**Who:** Parv · **When:** 30 Nov · **Account:** Parv's Claude trial.
**Tools:** Claude Code `/model opus`, plan mode; context7 (FastAPI WebSockets, Firebase Admin).
**Depends on:** 12.
**Criteria moved:** T1, T3, A3.

## Paste into Claude Code
```text
Read AGENTS.md, PROGRESS.md, docs/ARCHITECTURE.md (real-time section) and the backend.

Build the real-time layer on branch p13-realtime:
1. Event model.
   - An events table (append-only) plus an in-process publisher, with an interface that could later move to Redis.
   - Event types from ARCHITECTURE.md: sale.saved, sale.needs_answer, stock.changed, twin.updated, agent.cycle_started, agent.step (detect / refuse / plan / ask / answer / replan / commit), request.created, request.answered, move.committed, document.drafted, route.updated, stop.confirmed, consent.changed.
2. WebSocket endpoints.
   - /ws/route/{route_id} for the dashboard and delivery app; /ws/shop/{shop_id} for the shop app.
   - Auth by JWT; role filtering, so a shop only gets its own events.
   - Heartbeats; resume from the last event id after reconnect, so no event is missed.
3. SSE fallback for the dashboard (same stream).
4. FCM push (Firebase Admin SDK).
   - Device token registration endpoint; push on request.created, route.updated and sale.needs_answer.
   - Data messages so the app can deep-link.
   - Credentials come from .env and are never committed.
5. Idempotency. All write endpoints accept an Idempotency-Key header, so the Android outbox can retry safely. Store keys for 48 h.
6. Tests: event ordering, resume-after-disconnect, role filtering (a shop can't receive another shop's events), idempotent retries.
7. A small CLI, scripts/tail-events.sh, that prints live events. This helps the demo and debugging.
Regenerate openapi.json and the clients.

Plan first, build, run the gates, update PROGRESS.md, push, open a PR.
```

## Done when
- [ ] Two WebSocket clients and a phone (FCM) receive the right events.
- [ ] Reconnect resumes without gaps. Idempotent retries are proven by tests.
