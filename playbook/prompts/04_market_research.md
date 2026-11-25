# 04 · Market sizing, distributor economics, competitors (cited)

**Who:** Parv · **When:** 25–27 Nov.
**Tools:**
- Gemini Deep Research (Google AI Pro) and ChatGPT deep research (Plus), run in parallel on the web;
- then Claude (chat or Claude Code) to fact-check and merge.

**Depends on:** 00.
**Criteria moved:** E2 Market, E3 Business model, E4 Scalability, E5 Job creation, T4 Innovation (the gap no competitor fills).

## Step 1: paste the same brief into Gemini Deep Research AND ChatGPT deep research
```text
Research brief for an Indian student startup (prototype stage). Cite every number with a link and date. Mark estimates clearly. Prefer government data, company filings, reputable industry reports, and trade-body statements over blogs.

Product: Stockbridge. Kirana shops capture item-level sales by voice, checked against the UPI amount. A distributor's agent uses those sales plus batch and expiry data to move near-expiry FMCG stock to nearby shops that will sell it, on the existing delivery route. Shops free; the distributor pays per active shop per month.

Answer:
1. How many kirana / general stores are there in India, and in Punjab? How many FMCG distributors and stockists? Typical shops per distributor route and routes per distributor.
2. Expiry and damage losses in Indian FMCG general trade: as a % of sales, who bears them (brand, distributor, retailer), and how claims and returns work. Any statements from AICPDF or other distributor federations.
3. Kirana working capital tied in dead stock; stock-out losses; share of kiranas using billing software; UPI adoption among kiranas, with recent numbers.
4. Distributor margins and what distributors currently pay for software (Tally, Busy, Marg, Bizom, Salesforce-type DMS). Price ranges per user or per outlet.
5. Competitors and adjacent products, with a table (what they capture, who pays, price, whether they move stock between shops):
   - voice billing: VoiceKhata, Dukaan AI, etc.;
   - UPI alert apps: AlertPay by Khatabook, AlertBox;
   - retail and DMS software: Marg, Bizom, ShelfLifePro and similar;
   - B2B ordering: Udaan, Jumbotail, ElasticRun, Reliance JioMart Partner;
   - quick-commerce pressure on kiranas.
6. Government and ecosystem hooks: ONDC, Digital India, MSME schemes; and JanAI (janai.ai) cafés and their model.
7. A bottom-up market size: Punjab first, then India (shops × distributors × price), with stated assumptions.
8. Job creation: what a helper or onboarding-agent model could pay per shop, with comparable gig rates.

Output: a structured report with a sources list.
```

## Step 2: merge and fact-check (Claude)
Save both reports to `docs/research/raw/gemini_dr.md` and `chatgpt_dr.md`. Then in Claude Code:
```text
Read docs/research/raw/*.md. Write docs/research/MARKET.md:
- Merge the two reports.
- For every number, keep the source link. If the two reports disagree, show both and pick the more credible with a reason.
- Open each cited source that matters for a deck number (use web fetch) and check the number is actually there. Mark it "verified", "not found at source" or "estimate".
- Add a one-page "deck numbers" section: the 8–10 numbers we will put on slides, each verified or labelled.
- Add a competitor table and a "why nobody does this yet" paragraph.
Update PROGRESS.md. Commit on p04-market-research, push, open a PR.
```

## Done when
- [ ] `docs/research/MARKET.md` has deck numbers that are all verified or labelled.
- [ ] Competitor table done.
- [ ] Bottom-up market size with stated assumptions.
