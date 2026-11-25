# 19 · Shop app: onboarding, consent, language, helper mode, catalogue import

**Who:** Daivik · **When:** 2 Dec · **Account:** Daivik's Claude Pro.
**Tools:** Claude Code `/model opus`, plan mode; m3-expressive + compose skills; Figma MCP (read the screen frames); mobile-mcp.
**Depends on:** 18, 12.
**Criteria moved:** C4 (JanAI Café assisted path), C5 (consent), A6, C1.

## Paste into Claude Code
```text
Read AGENTS.md, PROGRESS.md, design/specs/shop/ (onboarding, settings) and the matching PNGs in design/screens/shop/, docs/PRD.md journey (h).
Build in :app-shop on branch p19-shop-onboarding, matching the designs exactly (layout, tokens, motion annotations):
1. Language pick: big options with spoken prompts (TTS from prompt 16 if ready, else Android TTS); sets the per-app locale.
2. Consent flow: microphone, notification access (deep link to the Notification Listener settings with a clear explainer), data use. Plain words and icons; every consent stored through the API with a timestamp; revocable in Settings.
3. Sign-in: phone + OTP (simulated in demo mode, labelled).
4. Helper mode (JanAI Café): a helper signs in, onboards a shop, imports the catalogue from a distributor-bill photo (simulated OCR, labelled; it posts the CSV import from prompt 12), sets the weekly reorder budget, and hands the phone to the owner.
5. Settings: language, Auto/Manual default, consent status, helper hand-off, about (with the "Simulated" list).
6. Motion: M3 Expressive springs; shape-morph on selection; shared-element from the language tile to the header.
7. Tests: ViewModel unit tests; a Compose UI test for consent gating (no mic or notification use before consent).
8. Run on the S24 via mobile-mcp. Screenshot every screen (light, dark, hi, en) into docs/screens/android/shop/. Compare each to the design PNG and fix differences.
Plan first, build, run the gates, update PROGRESS.md, push, open a PR.
```

## Done when
- [ ] A new owner can be onboarded by a helper in under 2 minutes on the S24. Consent is enforced and stored.
- [ ] Screens match the designs.
