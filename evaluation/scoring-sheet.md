# Scoring sheet (one copy per run)

Copy this file to `runs/<feature>/run-NN-score.md` and fill it in right after the run. Score against the frozen ground truth in `evaluation/ground-truth/`.

## 1. Run facts
| Field | Value |
|---|---|
| Run ID | `<feature>-run-NN` (or `-delivery`) |
| Date / time | |
| Tool + model (+ reasoning setting) | e.g. Claude Code / claude-opus-5-5; Codex / <model> <effort> |
| Prompt version | e.g. `preflight/prompts` v0.3 (must match `docs/prompt-log.md`) |
| Feature + input snapshot | e.g. 404917, `runs/404917/input/` as of 1 Mar 2026 |
| Context given | Ticket only / Ticket + code (repos and commit: ______) |
| Variable changed vs previous run | ONE thing, or "none (repeat)" |
| Tokens in | |
| Tokens out | |
| Cached tokens (if shown) | |
| Wall-clock run time | start to final output |
| Team review time | minutes to score this sheet |
| Reviewers (roles) | |

### Reading tokens
- **Claude Code:** start a fresh session per run. At the end run `/cost` (API billing) or `/usage` (subscription). Record input, output and cache figures as shown.
- **Codex CLI:** start a fresh session per run. Use `/status` at the end of the session, or the token usage summary printed when the session ends or when `codex exec` finishes. Record input, output and cached separately if shown.
- If a tool shows only a total, record the total and write "split n/a". Don't estimate.

## 2. Per-item table
List **every** item the run produced (questions, agenda lines, code notes). One row per item.

| # | Output item (short) | Mark | GT-ID / NF-ID | Note |
|---|---|---|---|---|
| 1 | | Hit / Useful new / Already known / Noise / Wrong | | |

Marks:
- **Hit**: matches a frozen GT item under that file's hit rule. Write the GT-ID. Each GT-ID counts once per run, so a second item hitting it is marked Already known.
- **Useful new**: valid, not in the GT, and worth refinement time. Copy it to "Post-freeze finds" in the GT file (Proposed, then confirmed per that file).
- **Already known**: true, but already stated in the stories or obvious to the team
- **Noise**: generic, irrelevant or duplicate ("consider edge cases")
- **Wrong**: factually incorrect about the ticket or code, e.g. an invented field or a false claim. Always note why.

If two reviewers disagree on a Hit and can't settle it in 1 minute, mark it **not** a hit.

## 3. Summary metrics
| Metric | Formula | Value |
|---|---|---|
| Total items (N) | rows in table | |
| Hits (H) | distinct GT-IDs hit | |
| Recall, ticket-only | H on **T** items / number of T items (404917: 5, 431577: 4) | |
| Recall, in scope | H / GT items in scope for this context (ticket-only = T items; ticket + code = T + C items with available code; C-NA is always excluded) | |
| Precision | (H + Useful new) / N | |
| Noise rate | Noise / N | |
| Wrong | count (target 0) | |
| New finds proposed / confirmed | from the GT file's post-freeze table | / |
| Tokens in + out | | |
| Hits per 10k tokens | H / (tokens in + out) x 10,000 | |

**Ticket-only runs are judged on "Recall, ticket-only".** Don't penalise a run for missing C items it couldn't see.

## 4. Analysis (3 lines max)
- Biggest miss and likely why:
- Biggest noise source:
- The ONE thing to change next (log it in `docs/prompt-log.md`):
