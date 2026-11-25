# 27 · Dashboard: shell, auth, route overview, live twin

**Who:** Amogh · **When:** 5 Dec · **Account:** Amogh's Claude trial.
**Tools:**
- Claude Code `/model opus`, plan mode, second opinion on the plan;
- **frontend-design** + **design-taste-frontend** skills;
- **shadcn MCP**, **21st.dev MCP**, **Motion** skill/MCP;
- context7 (Next.js App Router, TanStack Query, MapLibre GL);
- Playwright MCP.

**Depends on:** 03, 07 (web tokens), 13, 10/11 (specs).
**Criteria moved:** T1, T3.

## Paste into Claude Code
```text
Read AGENTS.md (sections 4, 6, 7), PROGRESS.md, design/specs/web/ and design/screens/web/, web/src/styles/tokens.css, and the generated API types in web/src/lib/api/.
Use frontend-design and design-taste-frontend for direction; the shadcn MCP for primitives; the 21st.dev MCP only for pieces shadcn lacks (restyle with our tokens, no default looks); Motion (motion/react) for animation, following the Motion skill's best practices.

Build on branch p27-dashboard-shell:
1. App structure:
   - Next.js App Router with server components where useful;
   - TanStack Query for data; a typed API client from openapi-typescript;
   - an auth flow (simulated OTP for distributor_admin and accountant, labelled);
   - i18n (en, hi, pa) with next-intl or similar.
2. Shell: sidebar + top bar per the specs; route switcher; command palette (cmdk); light and dark; responsive down to 390 px for Overview.
3. Real-time: a hook that subscribes to /ws/route/{id} (SSE fallback), resumes from the last event id, and updates the TanStack Query caches. A subtle live indicator.
4. Overview page: MapLibre map of shops coloured by risk (free OSM style, OSM credit); KPI tiles with count-up on change; "Run agent" button (POST, then follow events).
5. Twin page: the shops × items grid (virtualised), days of cover, expiry heat; a shop drawer with lots by batch and the selling-rate sparkline.
6. Loading skeletons, empty and error states as designed.
7. Playwright: smoke tests for login → overview → twin, plus screenshots at 1440 and 390 px into docs/screens/web/.
8. Deploy a preview to Vercel (root web/). The production domain is the .tech domain when Daivik sets it.
Plan first. Run the second-opinion skill on the plan, build, run the gates, update PROGRESS.md, push, open a PR.
```

## Done when
- [ ] Overview and Twin show live seeded data and update when a sale is saved from the shop app.
- [ ] Vercel preview works. Playwright smoke tests pass.
