---
name: evidence
description: Log a piece of hackathon evidence (a result, prompt improvement, token measurement, funny AI mistake, outsider feedback) against the achievement checklist in docs/evidence.md. Use when the user says "/evidence", "log this", or something demo-worthy just happened.
argument-hint: "<what happened> [achievement name]"
---

# Log evidence

1. Read `docs/evidence.md` (create it from the achievement table in `docs/hackathon-brief.md` if missing, with columns: Achievement | Status | Evidence refs).
2. Map the user's description to one or more achievements. Ask if it's ambiguous. Check the condition in the brief honestly, and say what is still missing for the claim to hold (for example, "needs verification against source" or "needs tool-reported token counts").
3. Append a dated entry under `## Log` with: what happened, file/link references, which achievements it supports, and the gaps that remain.
4. Update the status column (`idea` → `in progress` → `claimable`).
5. Report the current estimated score and the 1–2 cheapest next achievements.
