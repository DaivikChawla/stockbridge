# 14 · Speech and capture service: on-device + Sarvam, keyterms, LLM parse, checksum

**Who:** Parv · **When:** 1–2 Dec (two sessions) · **Account:** Parv's Claude trial.
**Tools:** Claude Code `/model opus`, plan mode, second opinion on the plan; context7 (Sarvam docs via web, httpx, websockets).
**Depends on:** 12.
**Criteria moved:** T2 Quality of AI, T4, C1, A5.

**Budget note:** use Sarvam's free ₹100 credits for building and A/B testing. Top up about ₹500 only if Sarvam clearly beats on-device speech on our clips (see `BUDGET.md`).

## Paste into Claude Code
```text
Read AGENTS.md, PROGRESS.md, docs/ARCHITECTURE.md, the existing capture/ and checksum code, and evals/eval_capture.py.
Sarvam docs:
- https://docs.sarvam.ai/api/api-guides-tutorials/models/saaras (saaras:v4; modes transcribe / codemix / translit; keyterm prompting, up to 50 terms; REST ≤30 s; streaming WebSocket, PCM 16 kHz)
- https://docs.sarvam.ai/api/getting-started/pricing

Build the capture service on branch p14-speech:
1. Two speech paths behind one interface:
   a. Client-side text. The Android app sends text from the on-device SpeechRecognizer (hi-IN / pa-IN / en-IN). This path is free and the default during development.
   b. Server-side Sarvam. A streaming WebSocket proxy (/ws/speech/{shop_id}): the app streams 16 kHz PCM; the server streams to Sarvam saaras:v4 in codemix mode, with keyterms built from that shop's top catalogue aliases (≤50, refreshed daily). It returns partial and final transcripts.
   - Audio is never stored: process in memory only, and say so in the code and the docs.
   - API key from .env.
2. Parsing.
   - Keep the rule parser.
   - Upgrade the LLM parse (NIM) to constrained JSON output over that shop's catalogue.
   - Guardrails: unknown items dropped, quantities 1–50, local-name mapping (e.g. "namak", "double roti").
3. Auto mode session logic:
   - a running list of heard items for an open counter session;
   - close the bill when a payment event arrives (POST /payments/notification from the app's UPI listener, with parsed amount, app and time);
   - match the payment to the right open session (time window + amount);
   - run the checksum: match → save; ambiguous → sale.needs_answer with one question; mismatch → flagged.
4. Manual mode endpoint: text or items + amount, then the same checksum.
5. UPI notification parser (server-side copy for testing; the app has its own in prompt 20).
   - Patterns for PhonePe, Google Pay, Paytm and BHIM "received ₹X" notifications, in English and Hindi.
   - Fixture-based tests. Ask me for real notification text samples if you have none; label synthetic fixtures.
6. Fallbacks: Sarvam fails → on-device text path; LLM fails → rule parser; nothing heard → Manual mode prompt. Each fallback emits an agent.step event so the trace shows recovery.
7. Latency logging for every stage (STT final → parse → checksum → saved). Target under 3 s on Wi-Fi.
8. Tests for all of the above. The existing capture eval still runs.

Plan first. Run the second-opinion skill on the plan:
"What will break in a noisy kirana with two people talking? How should sessions and payments be matched more robustly?"
Revise, then build. Run the gates, update PROGRESS.md, push, open a PR.
```

## Done when
- [ ] A recorded Hindi order streamed through Sarvam produces a saved bill when a matching payment arrives.
- [ ] The ambiguous and mismatch paths work. Fallbacks show in the event stream. Latency is logged.
