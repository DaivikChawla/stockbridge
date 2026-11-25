# 34 · Finale prep (27 Dec, Bangalore Palace, in person)

**Who:** all · **When:** 16–26 Dec. Light during exams; full on 20–26 Dec.
**Tools:**
- ChatGPT (voice mode) and Gemini as hostile judges;
- Claude for the pitch script and the Q&A bank;
- Remotion for any finale-specific clips;
- the S24 for rehearsals.

**Depends on:** 33, and being shortlisted.
**Criteria moved:** all; the jury is "industry leaders and domain experts" and the pitch carries entrepreneurial weight.

## Paste into Claude Code
```text
Read docs/submission/*, docs/DEMO_SCRIPT.md, docs/research/MARKET.md, docs/field/synthesis.md, backend/evals/results/REPORT.md and playbook/CRITERIA.md.
Create docs/finale/:
1. PITCH.md: a 5-minute pitch + live demo script (who says what, and when the demo starts and stops), plus a 2-minute and a 1-minute version.
2. QA_BANK.md: 40 likely jury questions with crisp answers backed by evidence. Cover tech (why native, accuracy in noisy shops, privacy, what's simulated, cost per shop), business (who pays, why now, competitors, CAC, distributor sales cycle, GST/credit-note correctness), impact (jobs, JanAI fit), and the hard ones ("why won't Udaan do this?", "what if the owner says no to the mic?").
3. RISK_PLAYBOOK.md: what we do if the venue Wi-Fi fails (phone hotspot; outbox; recorded backup video), the S24 dies (second phone with APKs installed), the backend fails (local backend on the laptop with the same seed), or UPI doesn't arrive (labelled simulated payment).
4. A printed one-pager (PDF via /design) to hand to judges.
Update PROGRESS.md, push.
```

## Rehearsal loop (humans)
- Each day from 20 Dec: run the full pitch with demo, timed, twice.
- Use ChatGPT voice mode as a hostile judge:
  ```text
  You are a tough judge at an Indian startup hackathon finale (industry leaders, CA and banking backgrounds).
  I'll pitch Stockbridge. Interrupt with hard questions; then score me on technical merit and entrepreneurial potential.
  ```
- Fix weak answers in `QA_BANK.md`.
- Pack: the S24 + a backup phone, chargers, a hotspot, a laptop + HDMI/USB-C adapter, printed one-pagers, the letters of intent (printed), the demo reset command written on a card.

## Done when
- [ ] Three clean timed rehearsals. The Q&A bank has been drilled. Backup plans have been tested once.
