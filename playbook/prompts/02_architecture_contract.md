# 02 · Architecture, data model, event model, API contract

**Who:** Daivik · **When:** 26 Nov · **Account:** Daivik's Claude Pro.
**Tool:** Claude Code, `/model opus`, plan mode, second opinion on the plan. Use context7 for FastAPI, SQLModel, Ktor and Next.js docs.
**Depends on:** 01 (merged).
**Criteria moved:** T1 Architecture, E4 Scalability, C3, C5.

## Read first
- `AGENTS.md`
- `docs/PRD.md`, `docs/DEMO_SCRIPT.md`
- `stockbridge/twin.py`, `planner.py`, `agent.py`, `checksum.py`, `capture.py`

## Paste into Claude Code
```text
Read AGENTS.md, docs/PRD.md, docs/DEMO_SCRIPT.md and the current Python modules in stockbridge/.
Design the architecture for the prototype and write it down. Don't write app code yet.

Produce:
1. docs/ARCHITECTURE.md
   - A mermaid diagram of the three clients, the API, the event bus, workers (agent cycle, speech), Postgres, FCM, Sarvam, NIM, Lyzr and the Tally import.
   - The request and event flow for each journey in the PRD.
   - Real-time design: WebSocket channels per route and per shop, the event types, and how clients reconcile. Online-first, plus an outbox on Android for sales, approvals and delivery confirmations, with idempotency keys.
   - Auth: phone + OTP, simulated for the demo and labelled. Roles: shop_owner, helper, distributor_admin, accountant, delivery_partner. Multi-tenant by distributor.
   - Privacy: what each role can read; audio never stored; consent records.
   - Where the existing agent, planner, twin and checksum code moves, and what changes in it.
   - Hosting: Azure for Students for the API and workers, Supabase Postgres, Vercel for web. Cost per shop per month (infra + speech), with its assumptions.
   - Scalability: route as the unit; what changes at 1,000 routes.
2. docs/DATA_MODEL.md: entities with fields and relations.
   - Distributor, Route, Shop, User, Consent, CatalogueItem (aliases and local names), Batch, Lot, Sale, SaleLine, PaymentEvent, StockCount, AgentCycle, Proposal, Request (give/take), Answer, Move, Document (credit note, invoice, clearance bill, brand claim), Stop, Delivery, KhataEntry, ReorderSuggestion, AuditEvent.
   - Note which fields feed the twin.
3. backend/openapi.draft.yaml: the full REST contract (paths, schemas, errors, pagination) plus the WebSocket event schemas.
   - Name everything consistently.
   - This draft becomes the generated openapi.json in prompt 12.
4. docs/DECISIONS.md, ADR-style entries:
   - native Kotlin + Compose;
   - online-first + outbox;
   - FastAPI + Postgres;
   - generated contract;
   - Sarvam + on-device speech;
   - NIM;
   - Lyzr for messaging only;
   - MapLibre + free tiles;
   - FCM.

Plan first. Then run the second-opinion skill on the plan with:
"Find weaknesses in this architecture for a live demo on 3 devices plus a web dashboard: race conditions, missing events, privacy leaks, over-engineering for a 14-day build."
Reconcile, revise and show me the plan.

After approval: write the files, update PROGRESS.md, commit on branch p02-architecture, push, open a PR.
```

## Done when
- [ ] `ARCHITECTURE.md`, `DATA_MODEL.md`, `openapi.draft.yaml` and `DECISIONS.md` are merged.
- [ ] Every PRD journey has a request and event flow.
- [ ] The privacy table shows a receiver can't read another shop's sales.
