# 20 · Shop app: Auto counter mode (foreground mic + UPI listener), the hero feature

**Who:** Daivik · **When:** 3–4 Dec (two sessions) · **Account:** Daivik's Claude Pro.
**Tools:**
- Claude Code `/model opus`, plan mode, second opinion on the plan;
- Android skills, compose and m3-expressive skills;
- context7 (Android foreground services, NotificationListenerService, SpeechRecognizer, AudioRecord);
- mobile-mcp on the S24.

**Depends on:** 19, 14.
**Criteria moved:** T2, T3, T4 (payment-as-checksum), C1, A5.

## Paste into Claude Code
```text
Read AGENTS.md, PROGRESS.md, docs/PRD.md journeys (a, c, d), design/specs/shop/ (home, counter-auto, outcomes), backend capture API (prompt 14) and docs/ARCHITECTURE.md.
Use context7 for the current Android 15/16 rules on foreground service types (microphone), notification-listener permissions and SpeechRecognizer.

Build Auto mode on branch p20-auto-counter:
1. Foreground "counter" service (type microphone).
   - Persistent notification with pause/stop.
   - Voice activity detection: on-device VAD (e.g. Silero ONNX or WebRTC VAD), so only speech is processed.
   - Two engines behind one interface:
     a. Android SpeechRecognizer (hi-IN / pa-IN / en-IN, prefer on-device);
     b. Sarvam streaming through our /ws/speech proxy (16 kHz PCM).
   - The engine is switchable in settings and the debug menu. Never write audio to disk.
2. UPI listener: NotificationListenerService.
   - Parses "received ₹X" notifications from PhonePe, Google Pay, Paytm and BHIM (English and Hindi), ignoring debits and OTPs.
   - Unit-tested against a fixtures file of real notification strings (ask me for samples from our phones; label any synthetic ones).
   - Posts the payment event to the backend.
3. Counter screen (Auto):
   - live listening indicator;
   - the running list of heard items, animating in as they're recognised;
   - partial transcript;
   - the amount arriving.
   Then the three outcomes, with motion and haptics per the spec:
   - saved (success morph);
   - one-tap question (chips with shape-morph selection);
   - doesn't add up (clear choices: fix items, mark cash, switch to Manual).
4. Demo-mode "simulate payment ₹X" button, clearly labelled "Simulated", for stages where a real UPI payment isn't possible.
5. Outbox: if offline, the sale is saved locally with an idempotency key and sent later; the UI shows "will send when online".
6. Performance: no jank on the S24 (check with the Android profiler skill / Perfetto); battery-friendly VAD; the service survives screen-off.
7. Tests:
   - UPI parser fixtures;
   - session ↔ payment matching (unit);
   - Compose UI tests for the three outcomes with fakes.
8. On the S24: run a real spoken sale + a real ₹1 UPI payment between our phones; record a screen video (scrcpy) to docs/screens/android/shop/auto_demo.mp4 (git LFS or a link if large).

Plan first. Run the second-opinion skill on the plan:
"Review this Android design for foreground mic + notification listener on Android 15/16 (Samsung One UI): permission pitfalls, background limits, battery, privacy."
Revise, build, run the gates, update PROGRESS.md, push, open a PR.
```

## Done when
- [ ] On the S24, a spoken order plus a real UPI ₹ payment saves the right bill in under 3 s.
- [ ] Ambiguous and mismatch outcomes work. The offline sale syncs. No jank.
