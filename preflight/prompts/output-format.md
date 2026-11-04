# Output format: `output/preflight.md` (v0.1)

```markdown
# Pre-Flight: <feature id> <title>
Prompt version: v0.1 · Code check: done (<repos>) / skipped · Readiness: <0–4> (<one-line reason>)

## Top 3 before anything else
1. <item id>: <one line>
2. ...

## DECIDE
| ID | Decision needed | Options | Evidence | Owner | Conf. | Min |
|---|---|---|---|---|---|---|
| D-01 | ... | A: ... / B: ... | #story "quote" or file:line | Architect | high | 2 |

## SPIKE
| ID | Question the spike answers | Evidence | Owner | Timebox | Conf. |
|---|---|---|---|---|---|

## ASK THE PO
| ID | Question | Evidence | Why it matters | Conf. |
|---|---|---|---|---|

## ALREADY ANSWERED (by code)
| ID | Question | Answer | file:line |
|---|---|---|---|

## Not checked
- <components or repos needed but not available>
```

Rules:
- Use stable item IDs: `D-`, `S-`, `P-`, `A-` plus a number. Reviewers score against these IDs.
- One question per row, with no compound questions.
- Each row is at most 2 lines.
