# Padawan Pre-Flight: how to run it (any tool)

The prompts in `prompts/` are tool-neutral, so the same files are used in Claude Code, Codex and ChatGPT.

## 1. Make a clean run workspace (needed for a fair blind run)
Create it **outside** the `StarwarsKittens` repo, so the tool can't see `evaluation/`, `ideas/` or `decisions/`:
```
preflight-runs/<feature>-run-NN/
  prompts/   ← copy of preflight/prompts (this exact version)
  input/feature.md   ← frozen snapshot (as-of date, UTF-8, no comments)
  repos/     ← optional: clones checked out at a commit from before development
  output/
```

## 2. Start it (fresh session, from inside the workspace)
- **Claude Code:** `claude` → `Read prompts/00-runner.md and run Pre-Flight.` → at the end, `/cost` or `/usage`
- **Codex CLI:** `codex exec "Read prompts/00-runner.md and run Pre-Flight."`, or run it interactively and use `/status` for tokens
- **ChatGPT:** upload the `prompts/*.md` files and `feature.md`, and paste the content of `00-runner.md`. It runs ticket-only, and no token report is available.

## 3. Score it
Copy `../evaluation/scoring-sheet.md` to `runs/<feature>/run-NN-score.md` in the team repo, fill it in, and log any prompt change in `docs/prompt-log.md`.

## Versions
| Version | Date | Change |
|---|---|---|
| v0.1 | 4 Nov 2026 | First draft. Written by someone who has seen the ground truth: generic examples only, and wording checked for leaked hints. |
