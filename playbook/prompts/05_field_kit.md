# 05 · Field kit and interviews (the strongest entrepreneurial evidence)

**Who:** Parv (Daivik joins the distributor calls).
**When:** kit on 25 Nov; interviews 27 Nov–9 Dec.
**Tool:** Claude chat or Claude Code for the kit; humans in the field.
**Depends on:** 01 (open questions in PRD section 7).
**Criteria moved:** E1 Problem relevance, E3 Business model, E5 Job creation, C1–C4.

The booklet says teams should "take a statement into the field … and only then define the solution". Judges reward real evidence. Use the CA parents' network for introductions to kirana owners and 1–2 FMCG distributors in Patiala.

## Paste into Claude Code
```text
Read docs/PRD.md (open questions), playbook/CRITERIA.md, and the PS 5.1 questions quoted in AGENTS.md.
Create docs/field/ with:
1. interview_kirana.md: a 15-minute script in simple Hindi with an English gloss.
   - Covers: how they decide reorders; what expired last month and why; what runs out (festivals); records they keep (UPI alerts, khata, distributor bills); credit to customers; would they sell near-expiry stock to a neighbouring shop at a discount; would they let a phone listen at the counter (privacy), and what would make them trust it; Auto vs Manual preference; budget for extra stock.
   - Neutral questions, no leading.
   - End with: "May we quote you anonymously? May we photograph the shelf, not people?"
2. interview_distributor.md: a 20-minute script.
   - Covers: expiry losses and claims process; return window; brand claim approval rates; software used (Tally/Busy/Marg); routes, shops per route, delivery days; would they pay ₹150–250 per active shop per month, and what would make that a yes; who approves; letter of intent ask.
3. consent_form.md: a short bilingual consent for interviews and quotes.
4. loi_template.md: a one-page non-binding letter of intent for a distributor pilot of one route (10–15 shops), in plain English. Parents can review it.
5. notes_template.md: one file per interview: date, shop type, location area (no names unless consented), answers, quotes, surprises, "what we change because of this".
6. synthesis.md (empty structure): patterns, quotes for the deck, numbers heard (labelled as interview data), changes to the PRD.
Update PROGRESS.md, commit on p05-field-kit, push, open a PR.
```

## In the field (human)
- Aim for **10+ kiranas** (mix of sizes) and **2+ distributors**. Record notes the same day.
- Photograph shelves and expired stock only with consent; no faces.
- With consent, record 20–30 short counter-style audio clips (owner reading typical orders in Hindi, Punjabi and code-mixed) for the speech eval in prompt 17. Store them in a private drive, not in git.
- After the interviews, ask Claude to fill `synthesis.md` from the notes and propose PRD changes. Daivik approves the changes.

## Done when
- [ ] 10+ kirana and 2+ distributor notes in `docs/field/notes/`.
- [ ] Synthesis written, with deck quotes.
- [ ] At least one letter of intent (a signed photo kept privately; mention it in the deck).
