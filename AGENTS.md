# AGENTS.md: rules for every coding agent on this repo

Claude Code, Codex and Antigravity all read this file. `CLAUDE.md` imports it and adds Claude-only notes.
If something here conflicts with a prompt, this file wins unless the prompt says it overrides a named rule.

## 1. What we are building
**Stockbridge** by **Team Terra** (Daivik Chawla, Amogh Anand, Parv Dua; Thapar Institute, Patiala).
Tech4Bharat GAVS Hackathon 2026, problem statement **5.1** "Kiranas tie up cash in dead stock while running out of what sells", tagged **Agentic AI**.

- **Prototype round:** 25 Nov to **15 Dec 2026, 11:59 PM IST**.
  - Internal demo freeze: **12 Dec**.
  - Internal submit target: **14 Dec**.
- **Finale:** in person, 27 Dec, Bangalore Palace. Live demo on a **Samsung Galaxy S24**.

### Three surfaces, one agent
1. **Shop app (Android).** An old phone on the counter hears what customers ask for (Auto mode), or the owner says or taps the items (Manual mode).
   - The UPI payment notification closes the bill. The items must add up to the amount paid (the checksum); if they don't, the owner answers one tap.
   - The owner also approves offers, sees stock and expiry, keeps khata, and reorders within a budget.
2. **Delivery app (Android).** The day's route in order, pick-ups and drops, and confirmation with count plus owner tap. Updates live when the plan changes.
3. **Distributor dashboard (web).** The route twin (stock by batch and expiry, plus each shop's selling rate), at-risk lots, the planner, owner approvals, documents, what-if, impact, and the agent trace.

### The agent
Its steps: detect at-risk lots → refuse what would expire on the next shelf (draft a brand claim instead) → plan moves (OR-Tools CP-SAT) → ask both owners → remember answers → re-plan → commit (credit note + invoice, or clearance bill) → hand the route to delivery.

**Judging** (see `playbook/CRITERIA.md`):
- Technical: architecture, quality of AI, working prototype, innovation.
- Entrepreneurial: problem relevance, market, business model, scalability, job creation.

Every change should move at least one of these.

## 2. Session protocol (every session, every agent)
1. Read `PROGRESS.md` (latest entry first), then the prompt or issue you were given.
2. For anything over ~30 lines of change, plan first (Claude: plan mode) and get approval.
3. Work on a branch named `p<NN>-<short-slug>` (NN = playbook prompt number). Never commit straight to `main` unless the prompt says so.
4. Run the quality gates (section 7) before you say "done".
5. **Before you stop**, for any reason, including a usage limit:
   - append an entry to `PROGRESS.md` using the template there;
   - commit;
   - push.

   A session that ends without a PROGRESS entry has lost its work for the next person.
6. Open a PR with a summary, screenshots for UI changes, and test output. Daivik (lead) merges.

## 3. Repository layout
Target layout, created by prompt 03. Until then, the Python agent lives at the root (`stockbridge/`, `server.py`, `evals/`, `tests/`, `ui/`).

```
backend/                 FastAPI app, agent, planner, twin, speech, evals, tests (Python 3.12, uv)
  app/  agent/  planner/  twin/  capture/  speech/  docs_gen/  evals/  tests/
  openapi.json           GENERATED from FastAPI. The single API contract.
android/                 One Gradle project
  app-shop/  app-delivery/
  core/designsystem/  core/model/  core/network/  core/data/  core/testing/
  feature/<name>/
web/                     Next.js dashboard (pnpm)
video/                   Remotion project for demo and pitch videos
design/                  Exported tokens, DESIGN.md, screen PNGs, Figma links
docs/                    PRD.md, ARCHITECTURE.md, DECISIONS.md, research/, field/, reviews/
playbook/                The team workflow and the numbered prompts
scripts/                 setup-tools.sh, ask-codex.sh, ask-gemini.sh, dev helpers
```

## 4. Fixed stack (change only through a `docs/DECISIONS.md` entry approved by Daivik)
- **Android:** Kotlin, Jetpack Compose, **Material 3 Expressive** (material3 1.5.x).
  - Hilt, type-safe Navigation Compose, Ktor client + kotlinx.serialization, WebSocket for live updates, Coil, MapLibre Android, Firebase Cloud Messaging, DataStore.
  - Room only as a start-up cache and a small outbox (see below).
  - Min SDK 29, target the latest stable. Demo device: Galaxy S24 (120 Hz).
- **Native capabilities that are core features:**
  - `NotificationListenerService` (UPI alerts from PhonePe, Google Pay, Paytm, BHIM);
  - a foreground microphone service (Auto mode);
  - Android `SpeechRecognizer` (on-device, free) and Sarvam streaming STT;
  - FCM; location for the delivery app.
- **Online-first, not offline-first.** The server is the source of truth and screens are live. Room holds a cache for instant start-up and an **outbox**: a sale, approval or delivery confirmation made with no network is saved and sent on reconnect. Never cut a feature or an animation to support offline use.
- **Web:** Next.js (App Router), TypeScript strict, Tailwind, shadcn/ui, Motion (`motion/react`), TanStack Query, MapLibre GL, Recharts. Deployed on Vercel.
- **Backend:**
  - FastAPI, SQLModel on Postgres (Supabase), Alembic migrations, WebSocket/SSE events, FCM push.
  - Planning with OR-Tools CP-SAT.
  - LLM via NVIDIA NIM (OpenAI-compatible).
  - Speech via Sarvam Saaras v4, with catalogue keyterms.
  - Lyzr agent for owner messaging, when the organisers' credits arrive.
- **Contract:** `backend/openapi.json` is generated from FastAPI and committed. Generated clients:
  - web: `openapi-typescript` into `web/src/lib/api/`;
  - Android: kotlinx.serialization models in `core/model`.

  Never hand-edit generated files; change the backend and regenerate.

## 5. Product rules (from the official problem-statement booklet; judges check these)
- **Human approval before any money, legal or personal-data step.** The owner approves every order, take-back, clearance and route change. Documents are drafts for the accountant.
- **Explicit consent** before capturing audio or reading notifications. Audio is processed and deleted, never stored.
- **Minimal data.** A receiving shop never sees another shop's sales.
- **Voice-first and vernacular.** Every user-facing string comes from resources in English, Hindi and Punjabi (`values/`, `values-hi/`, `values-pa/`; web: `messages/en|hi|pa.json`). No hard-coded UI strings.
- **JanAI Café assisted path:** a helper can onboard a shop and do a weekly stock check from the same apps.
- **Label every simulation.** Any mocked integration (Tally import, WhatsApp, UPI in demo mode) shows a visible "Simulated" tag in the UI and is listed in the README.
- **Never invent numbers.** Statistics in UI, README, deck or video must be cited, measured by our evals, or labelled "synthetic" or "indicative".

## 6. Design rules
- **Tokens only.**
  - Colours, type, shapes, spacing and motion come from `core/designsystem` (Android) and `web/src/styles/tokens.css` plus the Tailwind config (web), both generated from `design/tokens.json`.
  - No raw hex values or magic numbers in feature code.
- **Android:** M3 Expressive components and `MotionScheme` springs, shape morphing for selection, predictive back, shared-element transitions where content moves between screens, haptics on confirm, edge-to-edge. Supports light and dark.
- **Web:** shadcn/ui primitives styled with our tokens. Motion only where it explains a change: a list re-ordering, a plan updating, a number counting. Respect `prefers-reduced-motion`.
- **Banned "AI slop"** (the team's explicit feedback):
  - coloured accent bars on cards;
  - glow or gradient highlights;
  - pill rows of tags as decoration;
  - uppercase eyebrow labels;
  - numbered circles and tick bubbles as decoration;
  - purple or blue gradients;
  - emoji as icons;
  - generic 3-card feature rows;
  - lorem ipsum;
  - placeholder avatars;
  - em dashes in UI copy.
- **Real content:** real Indian product names and MRPs, real Patiala-area shop types, realistic numbers. Every screen designed for its empty, loading, error and success states.
- **Accessibility:** 48 dp touch targets, contrast AA, TalkBack labels, font scaling to 200% without breaking.

## 7. Quality gates (run before saying "done")
- **Backend:**
  ```
  cd backend && uv run ruff check . && uv run pytest -q
  ```
  The evals still run, and `openapi.json` is regenerated if the API changed.
- **Android:**
  ```
  cd android && ./gradlew spotlessCheck lint testDebugUnitTest assembleDebug
  ```
  New screens have `@Preview`s. Run it on a device or emulator and attach screenshots.
- **Web:**
  ```
  cd web && pnpm lint && pnpm typecheck && pnpm test && pnpm build
  ```
  Run Playwright for touched flows; attach screenshots at 1440 px and 390 px.
- **General:** no new TODOs without an issue link; no secrets; no failing tests skipped or deleted to get green.

## 8. Writing and git
- Plain English; short sentences. Cite sources in docs.
- **Conventional commits:** `feat(shop): …`, `fix(agent): …`, `docs: …`.
- Never put AI model identifiers in commits, code comments, docs or the app.
- Secrets live in `.env` files (git-ignored). Keep `.env.example` files current.
