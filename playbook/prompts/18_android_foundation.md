# 18 · Android foundation: modules, DI, navigation, network, design system

**Who:** Daivik · **When:** 30 Nov–1 Dec · **Account:** Daivik's Claude Pro.
**Tools:**
- Claude Code `/model opus`, plan mode, second opinion on the plan;
- **Android CLI + Android skills**, `compose-skill`, `m3-expressive-compose` skill;
- context7 (Compose, Hilt, Ktor, Navigation);
- mobile-mcp to run on the S24.

**Depends on:** 03, 07 (`tokens.json` + generated theme), 12 (generated models).
**Criteria moved:** T1, T3.

## Paste into Claude Code
```text
Read AGENTS.md (section 4 is the fixed stack), PROGRESS.md, docs/ARCHITECTURE.md, design/COMPONENTS.md and design/tokens.json.
Use the Android CLI (`android` commands) and the Android skills; use the compose-skill and m3-expressive-compose skills for API correctness; use context7 for current library versions.

Set up android/ on branch p18-android-foundation:
1. Gradle.
   - Version catalog with current stable versions: Kotlin, AGP, Compose BOM, material3 1.5.x (M3 Expressive), Hilt, Navigation (type-safe), Ktor, kotlinx.serialization, Room, DataStore, WorkManager, Coil, MapLibre Android, Firebase Messaging, Lottie (only if needed).
   - Convention plugins in build-logic/ for android-app, android-library, compose, hilt.
   - Spotless (ktlint) and lint configs. Baseline profile module scaffold.
2. Modules:
   - :app-shop and :app-delivery;
   - :core:designsystem (generated theme + our components from COMPONENTS.md as reusable composables with @Previews in light and dark, en and hi);
   - :core:model (generated from openapi.json);
   - :core:network (Ktor client, auth interceptor, JWT storage in EncryptedSharedPreferences or DataStore + Keystore, WebSocket client with resume-from-last-event, error mapping);
   - :core:data (repositories; Room cache; the outbox with idempotency keys and WorkManager retry);
   - :core:testing.
3. App shells: single activity, edge-to-edge, predictive back, type-safe navigation graph with placeholder destinations for every screen in design/specs/, splash, dark theme, dynamic colour OFF (brand colours).
4. Localisation scaffolding: values/, values-hi/, values-pa/; per-app language picker (AppCompat per-app locales); Devanagari and Gurmukhi fonts bundled or downloadable.
5. A debug menu, in debug builds only: environment switch (local / Azure), demo-mode toggle (simulated payments, labelled), event log viewer.
6. CI: assembleDebug, lint, unit tests.
7. Run both apps on the S24 with mobile-mcp. Screenshot the component catalogue screen in light and dark into docs/screens/android/.

Plan first. Run the second-opinion skill on the plan:
"Is this module structure and library set right for two premium Compose apps built in 10 days? Any version conflicts or over-engineering?"
Build, run the gates, update PROGRESS.md, push, open a PR.
```

## Done when
- [ ] Both apps install on the S24, show the catalogue screen, switch language and theme, and connect to the backend WebSocket.
- [ ] CI is green.
