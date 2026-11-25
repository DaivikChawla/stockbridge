# 07 · Design system: one token source for Android and web

**Who:** Daivik · **When:** 28–29 Nov · **Account:** Daivik's Claude Pro.
**Tools:** Claude Code `/design` + `/design-sync`; the `m3-expressive-compose` skill; Figma MCP (hand-off frame, light use).
**Depends on:** 06.
**Criteria moved:** T1, T3.

## Paste into Claude Code
```text
Read AGENTS.md section 6 and design/brand/BRAND.md. Use the m3-expressive-compose skill for Android API names and status in material3 1.5.x. Use context7 for Tailwind v4 and shadcn theming.

Build the Stockbridge design system:
1. design/tokens.json, the single source. It holds:
   - colour roles for light and dark (M3 roles, including surface containers and fixed roles);
   - type scale (display through label, with Devanagari and Gurmukhi fallbacks);
   - shape scale, including M3 Expressive shapes we will use for selection morphs;
   - spacing;
   - elevation;
   - motion: spring presets for spatial and effects, with stiffness and damping; durations for web.
2. A generator script, scripts/gen-tokens.mjs, that writes:
   - android/core/designsystem/src/main/kotlin/.../Theme.kt, Color.kt, Type.kt, Shape.kt, Motion.kt (MaterialExpressiveTheme, MotionScheme);
   - web/src/styles/tokens.css (CSS variables) and the Tailwind theme mapping, plus the shadcn theme variables.
   Don't hand-edit the outputs; they carry a "generated" header.
3. Component inventory, design/COMPONENTS.md. For each component: purpose, states, Android implementation (M3 Expressive component or custom), web implementation (shadcn primitive + our styling), and motion.
   Components:
   - app bar, bottom bar (ShortNavigationBar), FAB / FAB menu, floating toolbar, button group, split button;
   - list items (segmented), cards for request / bill / stop / lot;
   - one-tap answer chips (shape morph on select);
   - amount display, live transcript view, stock row with expiry badge, approval sheet;
   - empty, error and loading states (LoadingIndicator / wavy progress);
   - map stop marker, KPI tile, table, trace timeline.
4. Use /design to render a component sheet (light and dark) and a "kitchen sink" screen for Android and for web, so we can see the system before screens are built.
5. /design-sync so Claude Design and the repo share the tokens.
6. Create a Figma file "Stockbridge – Hand-off" with one page for tokens and one for components (Figma MCP, light use: free seats have low call limits). Put its link in design/README.md.

Plan first, then build. Update PROGRESS.md, commit on p07-design-system, push, open a PR.
```

## Done when
- [ ] `tokens.json` generates Compose theme files and web CSS/Tailwind with one command.
- [ ] Component sheet rendered (light and dark).
- [ ] `COMPONENTS.md` complete. The Figma link is recorded.
