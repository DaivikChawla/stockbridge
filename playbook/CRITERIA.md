# CRITERIA.md: what the judges score, and how we prove each point

Every prompt names the criteria lines it moves. Before submission (prompt 33), score each line honestly: 0 (missing), 1 (claimed), 2 (shown with evidence).

## Sources
- **Tech4Bharat 2026 official problem-statement booklet** (Oct 2026): https://thegavshackathon.com/docs/Tech4Bharat-2026-Problem-Statements.pdf
- **Challenges page:** https://thegavshackathon.com/challenges
- **HackCulture page:** https://hackculture.io/hackathons/tech4bharat-gavs-hackathon

The booklet says: "Submissions are judged on two dimensions. The technical dimension covers architecture, quality of AI, a working prototype and innovation, while the entrepreneurial dimension covers problem relevance, market, business model, scalability and job creation. Final criteria and weightages are published with the registration details."
**Action:** paste the prototype-round email or form text into `docs/round2_requirements.md` the day you get it, and adjust this file.

## A. Technical dimension

| # | Criterion | What "2 points" looks like for Stockbridge | Prompts |
|---|---|---|---|
| T1 | **Architecture** | Clean monorepo; one generated API contract; event-driven twin with live updates to 3 surfaces; online-first apps with an outbox; documented in `docs/ARCHITECTURE.md` with a diagram; deployed (dashboard URL on the `.tech` domain) | 02, 03, 12, 13, 18, 27 |
| T2 | **Quality of AI** | Speech (Sarvam with catalogue keyterms) → LLM parse → **amount checksum**; CP-SAT planner; agent memory and re-planning. **Measured:** item F1, silent-wrong rate with and without checksum, latency, speech eval on real recorded clips, 90-day backtest. An eval page in the dashboard | 14, 15, 17, 29 |
| T3 | **Working prototype** | Live on the S24: a spoken sale becomes a saved bill; the twin updates; the agent plans; two phones approve; the delivery app gets the route; documents appear on the dashboard. No crashes. A 3-minute video of the same flow | 20–31, 33 |
| T4 | **Innovation** | Payment-as-checksum (no product found that checks spoken items against the UPI amount); batch-level route twin; refusal logic (won't move stock that would expire on the next shelf); shop-to-shop clearance | 01, 14, 15, 33 |

### The booklet's definition of "Agentic AI" (judges will look for each verb)

| # | The agent must… | Our evidence, visible in the trace | Prompts |
|---|---|---|---|
| A1 | pursue a goal over many steps on behalf of its user | One cycle: detect → refuse → plan → ask → re-plan → commit → route | 15, 28 |
| A2 | plan | CP-SAT plan with budgets, selling speed, expiry | 15 |
| A3 | act in external systems | Push to owners' phones, route to the delivery app, draft documents for the accountant, Tally import (labelled simulated where mocked), Lyzr messaging agent | 13, 15, 16, 26, 29 |
| A4 | keep memory of the case | Per-shop memory: declines, caps, past answers, consent | 15 |
| A5 | recover when something fails | Owner says no → re-plan; bill doesn't add up → one-tap question; network drops → outbox; STT fails → Manual mode; LLM down → rule parser | 14, 15, 31 |
| A6 | seek human approval before money, legal or personal data | Every move needs both owners' yes; documents are drafts; consent screens | 19, 22 |
| A7 | "well beyond answering questions" | It acts, with a person approving | all |

### Conditions every solution works within (booklet)

| # | Condition | Our evidence | Prompts |
|---|---|---|---|
| C1 | Voice-first, vernacular, code-mixed | Hindi, Punjabi and English UI; code-mixed speech; voice prompts | 14, 16, 19–23 |
| C2 | Limited literacy | Icons + voice + one-tap answers; numbers spoken back | 08, 20–23 |
| C3 | Entry-level Android, patchy connectivity | Runs well on the S24 and degrades gracefully: outbox for sales, approvals and confirmations; small payloads. Only claim low-end support if tested | 18, 31 |
| C4 | Assisted path through a JanAI Café | Helper mode: onboard a shop, import catalogue, weekly stock check | 19, 23 |
| C5 | Explicit consent, limited data | Consent screens; audio never stored; receivers never see other shops' sales | 12, 19 |
| C6 | Mock integrations clearly labelled | "Simulated" tag in the UI + README list | 12, 31, 33 |

## B. Entrepreneurial dimension

| # | Criterion | What "2 points" looks like | Prompts |
|---|---|---|---|
| E1 | **Problem relevance** | 10+ kirana interviews and 2+ distributor interviews in Patiala, with quotes, photos (with consent) and what we changed because of them. Letters of intent if possible | 05 |
| E2 | **Market** | Bottom-up: kiranas per distributor route × routes × distributors in Punjab, then India. Every number cited | 04 |
| E3 | **Business model** | Distributor pays ₹150–250 per active shop a month (validated or adjusted in interviews); shops free; unit economics and payback | 04, 05, 33 |
| E4 | **Scalability** | Route as the unit; cost per shop per month (infra + speech); onboarding through JanAI Cafés | 02, 04, 33 |
| E5 | **Job creation** | JanAI Café helpers paid per shop for onboarding and weekly stock checks; delivery partners get more stops | 04, 33 |

## C. Demo moments (each one proves several lines)
1. A customer speaks at the counter, the UPI notification arrives, and the bill saves itself. (T2, T3, T4, C1)
2. An ambiguous bill ("Surf ₹10 ya ₹20?") is answered in one tap. (T2, A5, C2)
3. The agent refuses to move bread with 2 days left and drafts a brand claim instead. (A1, A5, T4)
4. Bansal Kirana accepts "only 3"; the agent re-plans in under a second without asking Sharma again. (A4, A5)
5. The delivery app re-orders live; the driver confirms a drop and the dashboard updates. (T1, T3, A3)
6. Airplane mode on the shop phone, a sale is made, airplane mode off, and it syncs. (C3, A5)
7. The impact page: rupees of expiry avoided on the route this week (synthetic, labelled), and eval results. (T2, E3)
