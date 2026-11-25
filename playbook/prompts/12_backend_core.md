# 12 · Backend v2 core: database, auth, tenants, catalogue, lots, consent

**Who:** Parv · **When:** 29 Nov · **Account:** Parv's Claude trial.
**Tools:** Claude Code `/model opus`, plan mode, second opinion on the plan; Supabase MCP (read-only); context7 (FastAPI, SQLModel, Alembic).
**Depends on:** 03.
**Criteria moved:** T1, C5 (consent, minimal data), E4.

## Paste into Claude Code
```text
Read AGENTS.md, PROGRESS.md, docs/ARCHITECTURE.md, docs/DATA_MODEL.md, backend/openapi.draft.yaml and the existing backend/ code.

Build the backend core in backend/ on branch p12-backend-core:
1. Database. SQLModel models for every entity in DATA_MODEL.md, plus Alembic migrations, on Postgres (Supabase; DATABASE_URL from .env).
   - Local dev uses Docker Postgres or the Supabase CLI: document both in backend/README.md.
2. Auth.
   - Phone + OTP. The OTP is simulated in demo mode (fixed code, clearly labelled); a JWT carries user, role and distributor_id.
   - Role-based access per ARCHITECTURE.md: shop_owner, helper, distributor_admin, accountant, delivery_partner.
   - Row-level tenancy by distributor.
3. Core endpoints from the contract:
   - distributors, routes, shops, users;
   - catalogue items with aliases and local names (Hindi, Punjabi, English);
   - batches and lots;
   - consent records (grant and revoke, with timestamps);
   - stock counts.
4. Privacy.
   - Enforce that a shop can never read another shop's sales or stock.
   - Write tests that try to and must fail.
5. Simulated Tally/Busy import: an endpoint that accepts a CSV in a documented format and creates batches and lots, labelled "simulated import" in responses.
6. Seed script: the Patiala demo route.
   - 1 distributor, 1 route, 8–12 shops with realistic names and positions, a catalogue of 40+ real SKUs with MRPs and aliases, and lots with batches and expiry dates shaped like docs/DEMO_SCRIPT.md needs.
   - Everything synthetic is labelled in the data.
7. The twin, planner, checksum and agent modules keep working on top of the database. Adapt the twin to load from and persist to the database; keep the pure logic testable without a database.
8. Generate backend/openapi.json from FastAPI. Finish scripts/gen-api-clients.sh: TypeScript types for web/ and kotlinx models for android/core/model. Delete openapi.draft.yaml once the generated file covers it.
9. Tests: model and permission tests, tenancy tests, the existing 15 tests, and an API test for each endpoint.

Plan first, then run the second-opinion skill on the plan:
"Security and data-model review: tenancy leaks, missing indexes, migration risks, anything that blocks real-time in prompt 13."

After approval, build. Run the gates. Update PROGRESS.md, push, open a PR.
```

## Done when
- [ ] Migrations run on Supabase. Seed loads the demo route.
- [ ] Privacy and tenancy tests pass. `openapi.json` and the generated clients are committed.
