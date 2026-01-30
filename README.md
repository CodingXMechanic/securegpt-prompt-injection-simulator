# SecureGPT — Prompt Injection Simulator (Smart)

## What changed
This enhanced version includes:
- Context-aware simulated LLM (keeps chat history)
- Intent detection (definitions, examples, data requests, how-to)
- Fuzzy similarity checks to detect paraphrased system prompts
- Mode toggle: `vulnerable` (demo leaks) and `hardened` (blocks & explains)
- Polished frontend with example payloads and mode control

## Quick run
1. `pip install flask`
2. `python app.py`
3. Open `http://127.0.0.1:5000`

## Demo flow suggestions
- Start in `vulnerable` mode: show a benign question, then run `direct_injection` — observe leak/partial leak.
- Toggle to `hardened` mode: resend same payload — observe block & explanation.
- Try `role_play_injection` and `indirect_injection` to illustrate different vectors.
- Discuss defenses (blacklist, fuzzy similarity, instruction isolation, output filtering) and their pros/cons.

## Files
- `app.py`, `simulator.py`, `attacks.py`, `defenses.py`, `system_prompt.txt`, `templates/index.html`

## Ethics
Educational tool only. Do not use to attack real LLM deployments.