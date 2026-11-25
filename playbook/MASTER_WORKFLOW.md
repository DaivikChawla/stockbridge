# Stockbridge prototype round: master workflow

**Team Terra:** Daivik Chawla (lead), Amogh Anand, Parv Dua.

**Round:** Tech4Bharat GAVS prototype development, 25 Nov to **15 Dec 2026, 11:59 PM IST**. Top teams go to the finale on **27 Dec** at Bangalore Palace.

**Internal dates:**
- Demo freeze: Sat 12 Dec.
- **Submit: Mon 14 Dec.**
- Tue 15 Dec is buffer only.

Goal: the best possible product, judged on `playbook/CRITERIA.md`.

---

## 1. How this works in one paragraph
Claude Code with the newest Opus builds everything that ships. All context lives in this repo, not in anyone's chat, so any of our three Claude accounts can pick up any prompt cold:
- `AGENTS.md` / `CLAUDE.md`: the rules;
- `PROGRESS.md`: the hand-off log;
- `docs/`: specs and decisions;
- `playbook/prompts/`: 35 numbered prompts.

ChatGPT Plus (Codex) and Google AI Pro (Antigravity, Gemini Deep Research, Stitch) do the rest:
- research;
- design exploration;
- second-opinion reviews of every plan and PR;
- test scaffolds;
- pitch drills.

One prompt equals one focused Claude session, so quality stays high and usage stays predictable.

## 2. Roles

| Person | Owns | Claude account |
|---|---|---|
| **Daivik** | Lead: architecture, brand and design system, Shop app, integration, final review and merge of every PR, submission | Claude Pro, whole period |
| **Amogh** | Screen designs, Delivery app, web dashboard | Claude free plan (Claude Design) until 2 Dec; **free trial week 3–9 Dec** for code |
| **Parv** | Research, field interviews and letters of intent, backend and agent, speech evals, business model, pitch | **Free trial week 29 Nov–5 Dec** for code |

If a trial week has already started or can't start on these dates, move that person's prompts to match. The order inside each track matters more than the dates.

Second-opinion accounts:
- Daivik uses his ChatGPT Plus (Codex) and Google AI Pro (`agy`).
- Amogh and Parv use their own free Codex (Codex is included on the ChatGPT Free plan) and the free Antigravity tier.
- Never share one person's paid account across laptops.

## 3. How to run any prompt (the loop)
1. `git pull`. Read the newest `PROGRESS.md` entry.
2. Open `playbook/prompts/NN_*.md`. Check its **Depends on** line is done.
3. Start Claude Code in the repo: `claude`, then `/model opus`, then plan mode (Shift+Tab).
4. Paste the block under **Paste into Claude Code**. Let it read, explore and write a plan.
5. For prompts marked **2nd opinion on plan**, Claude runs the `second-opinion` skill on its plan (Codex + Gemini) and revises.
6. Approve the plan. Claude builds on branch `p<NN>-<slug>`, using subagents for independent parts.
7. Claude runs the quality gates (`AGENTS.md` section 7), takes screenshots for UI, and runs a second-opinion review of the diff.
8. Claude appends to `PROGRESS.md`, commits, pushes and opens a PR. Daivik reviews and merges (same day).
9. `/clear` before the next prompt.

When a 5-hour limit is close: finish the step, write the PROGRESS entry, push, stop. The next window, or another account, continues from PROGRESS.

## 4. Calendar

Legend:
- **D** = Daivik's Claude Pro
- **P** = Parv's Claude trial (29 Nov–5 Dec)
- **A** = Amogh's Claude trial (3–9 Dec)
- *human* = no Claude needed

| Day | Daivik | Parv | Amogh |
|---|---|---|---|
| **Wed 25 Nov** | 00 setup · **01** plan master (start) | 00 setup · **04** research: start Gemini + ChatGPT Deep Research runs *(human)* · **05** field kit | 00 setup · Stitch exploration of shop screens; collect references into `design/references/` *(human)* |
| **Thu 26** | **01** finish (2nd opinion) · **02** architecture + API contract | **04** fact-check, book first interviews *(human)* | Stitch exploration: delivery app + dashboard *(human)* |
| **Fri 27** | **03** monorepo restructure + CI + issues | Interviews 1–3 *(human, field)* | Read PRD and journeys; screen inventory *(human)* |
| **Sat 28** | **06** brand · **07** design system (start) | Interviews 4–6 *(human, field)* | **08** shop screens (Claude Design on free plan + Stitch) |
| **Sun 29** | **07** design system (finish, `/design-sync`) | **P** trial starts · **12** backend core | **08** finish · **09** delivery screens |
| **Mon 30** | **18** Android foundation · upload NLDSL note (due today) | **13** real-time layer | **10** dashboard screens |
| **Tue 1 Dec** | **11** design critique + Figma hand-off · **18** finish | **14** speech service (day 1) | **10** finish; fix critique items |
| **Wed 2** | **19** shop onboarding + consent + language | **14** speech service (day 2) | Write per-screen specs in `design/specs/` *(human)* |
| **Thu 3** | **20** Auto counter mode (day 1) | **15** agent v2 | **A** trial starts · **25** delivery: route + stops |
| **Fri 4** | **20** Auto mode (day 2) · submit Homingo (4–6 Dec window) | **16** Lyzr agent + vernacular messages + voice | **26** delivery: confirm + live re-plan |
| **Sat 5** | **21** Manual mode + checksum one-tap + bills | **17** evals v2 (last trial day) | **27** dashboard shell + live twin |
| **Sun 6** | **22** approvals inbox + push + clearance | Record speech clips with shops; interviews 7–10 *(human)* | **28** at-risk, planner, approvals, trace |
| **Mon 7** | **23** stock, expiry, khata, reorder, weekly report | Business model + unit economics from interviews *(human, Codex free)* | **29** documents, what-if, impact, evals |
| **Tue 8** | **24** shop polish (day 1) | Pitch narrative + video storyboard draft *(human)* | **30** dashboard polish |
| **Wed 9** | **24** shop polish (day 2) | Interview synthesis + letters of intent → `docs/field/` | **30** finish; delivery polish leftovers (last trial day) |
| **Thu 10** | **31** integration + demo seed (day 1) | Device testing, bug list *(human)* | Device testing, bug list *(human)* |
| **Fri 11** | **31** finish · **32** QA (start) | Failure drills *(human)* | Playwright and visual checks with Codex free *(reviewed by D)* |
| **Sat 12** | **32** QA · **DEMO FREEZE 11 PM** | Copy for deck and README *(human)* | Record S24 footage (scrcpy) *(human)* |
| **Sun 13** | **33** submission: Remotion video + deck | Proofread, check every number's source | Video review, deck review |
| **Mon 14** | **33** finish · **SUBMIT** | Submit checklist | Submit checklist |
| **Tue 15** | Buffer only. Deadline 11:59 PM | | |
| **16–26 Dec** | **34** finale prep (light during exams), travel 26 Dec | | |

**Load check:**
- Daivik's Claude runs about one prompt a day: about 22 prompts in 20 days.
- Parv's 6 code prompts fit his 7-day trial.
- Amogh's 6 code prompts fit his.

The heaviest Claude week is 7–13 Dec. If Daivik hits the weekly limit, use the reserve in `BUDGET.md` (Claude usage credits).

## 5. Prompt index and dependencies

| # | Prompt | Owner | Depends on | Criteria |
|---|---|---|---|---|
| 00 | Setup | all | none | none |
| 01 | Plan master: PRD, journeys, demo storyboard | D | 00 | all |
| 02 | Architecture + API contract | D | 01 | T1 |
| 03 | Monorepo restructure + CI + backlog | D | 02 | T1 |
| 04 | Market and competitor research | P | 00 | E2–E5 |
| 05 | Field kit + interviews | P | 01 | E1, E3 |
| 06 | Brand | D | 01 | T3 |
| 07 | Design system | D | 06 | T1, T3 |
| 08 | Shop app screens | A | 07 (tokens draft) | T3, C1, C2 |
| 09 | Delivery app screens | A | 07 | T3 |
| 10 | Dashboard screens | A | 07 | T3, T2 |
| 11 | Design critique + hand-off | D | 08–10 | T3 |
| 12 | Backend core | P | 03 | T1, C5 |
| 13 | Real-time layer | P | 12 | T1, A3 |
| 14 | Speech service | P | 12 | T2, C1, A5 |
| 15 | Agent v2 | P | 13 | A1–A6, T4 |
| 16 | Lyzr agent + vernacular messages + voice | P | 15 | A3, C1 |
| 17 | Evals v2 | P | 14, 15 | T2 |
| 18 | Android foundation | D | 03, 07 | T1 |
| 19 | Shop: onboarding, consent, language | D | 18, 12 | C4, C5, A6 |
| 20 | Shop: Auto counter mode | D | 19, 14 | T2–T4, C1 |
| 21 | Shop: Manual mode + checksum + bills | D | 20 | T2, A5, C2 |
| 22 | Shop: approvals inbox + push + clearance | D | 18, 13, 15 | A3, A6 |
| 23 | Shop: stock, expiry, khata, reorder, report | D | 22 | T3, C4 |
| 24 | Shop polish | D | 19–23 | T3 |
| 25 | Delivery: route + stops | A | 18, 13 | T3, A3 |
| 26 | Delivery: confirm + live re-plan + polish | A | 25 | T3, A5 |
| 27 | Dashboard shell + live twin | A | 03, 07, 13 | T1, T3 |
| 28 | Dashboard: at-risk, planner, approvals, trace | A | 27, 15 | A1–A5 |
| 29 | Dashboard: documents, what-if, impact, evals | A | 28, 17 | T2, E3 |
| 30 | Dashboard polish | A | 27–29 | T3 |
| 31 | Integration + demo seed + failure drills | D | 24, 26, 30 | T3, A5, C3 |
| 32 | QA, performance, crash sweep | all | 31 | T3 |
| 33 | Submission pack | all | 32 | all |
| 34 | Finale prep | all | 33 | all |

## 6. How each tool is used

| Tool | Used for |
|---|---|
| **Claude Code (Opus)** | Every line of shipped code and UI; plans; integration |
| **Claude Design** (`/design`) | Brand, design system, final screens, deck. `/design-sync` keeps tokens matched to code |
| **Codex CLI** (ChatGPT Plus) | Second-opinion reviews of plans and PRs; test scaffolds; quick read-only investigations |
| **ChatGPT** (web) | Deep research (market), hostile-judge pitch drills, copy critique |
| **Antigravity `agy`** (Google AI Pro) | Second-opinion reviews (Gemini), alternative implementations to compare when stuck |
| **Gemini** (web) | Deep Research (market, competitors), checking Hindi and Punjabi copy |
| **Google Stitch** | Many quick screen variants before Claude Design finalises |
| **Figma + MCP** | One hand-off file; Claude reads frames when building |
| **Remotion** | Demo video, animated explainers, finale clips |
| **Android CLI + skills, mobile-mcp** | Builds, emulator and device control, Compose previews, Journeys tests |
| **shadcn, 21st.dev, Motion, taste, Impeccable, Emil skills** | Web dashboard quality |
| **Playwright MCP** | Web QA and screenshots |
| **Claude in Chrome** | Optional: ask ChatGPT or Gemini web (Deep Research) from inside a Claude session |

## 7. Risks and what we do

| Risk | Plan |
|---|---|
| Claude 5-hour or weekly limit | Stop cleanly (PROGRESS + push); continue on another account or the next window; last resort: usage credits (BUDGET.md) |
| A prompt runs long | Split it at the PROGRESS entry; push what works behind a flag |
| UPI notification formats vary | Prompt 20 ships parsers for PhonePe, Google Pay, Paytm and BHIM, with tests from real notification samples; demo mode has a labelled simulated payment button |
| Speech accuracy weak in a noisy shop | Manual mode is first-class; checksum catches errors; Sarvam keyterms from the catalogue |
| Exams | Swap days for lighter work (reviews, research, testing); keep the order of each track |
| A feature slips | Cut in this order: weekly report → khata → Lyzr agent → Bulbul voice replies → Punjabi (keep Hindi + English) → what-if polish. **Never cut:** capture + checksum, agent plan/ask/re-plan, approvals on phones, delivery confirm, dashboard twin + trace, evals |

## 8. Definition of done for the submission (14 Dec)
- [ ] Both APKs install and run on the S24 with no crash through the full demo script (`docs/DEMO_SCRIPT.md`).
- [ ] Dashboard live on the `.tech` domain; backend on Azure; seeded Patiala demo route.
- [ ] Demo video (Remotion, ≤ length required) uploaded; deck PDF; README updated with setup, architecture, evals, guardrails, "Simulated" list and AI tools used.
- [ ] `playbook/CRITERIA.md` self-score: no line at 0, most at 2.
- [ ] Field evidence in `docs/field/`; every number in the deck has a source or a "synthetic" or "indicative" label.
- [ ] Form submitted on HackCulture, confirmation screenshot saved.
