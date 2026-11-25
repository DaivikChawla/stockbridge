# 16 · Owner messaging agent (Lyzr), vernacular messages, voice replies

**Who:** Parv · **When:** 4 Dec · **Account:** Parv's Claude trial.
**Tools:** Claude Code `/model opus`, plan mode; Lyzr docs (when credits arrive); Sarvam Bulbul TTS docs.
**Depends on:** 15.
**Criteria moved:** A3 (acts in external systems), C1 (vernacular), T2. Lyzr is the hackathon's AI partner, so using it visibly can help.

## Paste into Claude Code
```text
Read AGENTS.md, PROGRESS.md, backend/agent and the voice and tone guide in design/brand/BRAND.md.

On branch p16-messaging:
1. Message templates. Every request and notification the agent sends has an English, Hindi and Punjabi version in a templates file.
   - Short, respectful, in the brand's voice.
   - Numbers and product names are filled in safely.
   - No other shop's sales ever appear in a receiver's message (add a test).
   Ask me to have a native speaker check the Hindi and Punjabi. Mark them "needs native review" until then.
2. Owner messaging agent (Lyzr). If LYZR_API_KEY is set:
   - Route the "explain this request to the owner and answer follow-up questions" conversation through a Lyzr agent.
   - Examples: "kyun bhejna hai?", "credit note kab milega?". The agent is grounded only on that request's data and the policy, with no access to other shops.
   - If the key isn't set, or Lyzr fails, use the NIM LLM with the same prompt and guardrails.
   - Log which one answered in the trace.
   - Document it in docs/ARCHITECTURE.md and the README.
3. Voice replies. Sarvam Bulbul TTS reads requests and bill outcomes aloud in the owner's language (an "listen" button in the app; auto-read optional). Cache audio per message, never user audio.
4. WhatsApp fallback: a simulated sender that logs the message it would send, clearly labelled. Keep the interface ready for the WhatsApp Business Platform later.
5. Tests for templates, the privacy rule, and the fallback order (Lyzr → NIM → template only).
Plan first, build, run the gates, update PROGRESS.md, push, open a PR.
```

## Done when
- [ ] Requests read naturally in three languages; native check pending or done.
- [ ] The Lyzr path works if a key exists; the fallback works if not. Listen audio plays.
