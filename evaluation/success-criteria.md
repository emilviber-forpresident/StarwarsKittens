# Success criteria: Padawan Pre-Flight

Frozen on 4 Nov 2026, before run 1, together with `evaluation/ground-truth/` and `evaluation/scoring-sheet.md`. Any change to these after run 1 must be logged in `docs/prompt-log.md` with a reason, and must not be applied to runs that are already scored.

## 1. The "before" baseline
| Option | What it shows | Weakness |
|---|---|---|
| (a) Run 1 vs run N of the tool | Prompt and context improvement: Prompt mechanic, Token diet | Run 1 is already AI, so it doesn't show value over today's way of working |
| (b) Original human refinement: score the pre-dev stories as written with the same sheet | Value over the status quo: Better than before | On 404917 it's close to 0 by construction (the problems surfaced during dev) |

**Recommendation: use (b) as THE "before" for Better than before.** Score the frozen input snapshot itself: how many GT items the stories already captured, plus *when* humans actually surfaced each item (comment dates: 404917 May to Jun, during dev; 431577 19 Oct and 2 Nov, weeks after the stories were written). "After" is the best run N, measured in minutes, before refinement.
Use (a) only as the **iteration yardstick** (Prompt mechanic, Token diet), not as the headline before/after.
404917's near-zero baseline must be stated openly. 431577 is the fairer comparison, because humans did find those items, just late.

## 2. "Good enough" thresholds (per feature, best run)
| Measure | Target |
|---|---|
| Recall, ticket-only | **at least 60%** (404917: 3 of 5 T items; 431577: 3 of 4, i.e. 75%, the nearest whole item) |
| Recall, in scope (ticket + code runs) | at least 60% |
| Noise rate | **at most 25%** of items |
| Precision | at least 60% (on 431577 read it as a floor only, because the GT is partial) |
| Wrong | 0, or at most 1 if the run flags it as uncertain |
| Size | at most 25 items, so the agenda fits 15 minutes |
| Team review time | at most 15 min per run |
| Confirmed new finds | at least 1 per feature (Second pair of eyes) |
| Token diet | at least 30% fewer tokens (in + out) than the first run that met all the thresholds above, while still meeting them |

## 3. Stopping rule (per feature)
Stop iterating when **any** of these is true:
1. All thresholds are met **and** the next run improves neither recall (+1 GT item) nor noise (−5 points). Then do at most 2 token-diet runs, and stop.
2. Two runs in a row show no gain on recall or noise. The method has levelled off, so record why.
3. 6 runs on this feature, or the timebox (Thu 5 Nov 10:00) is reached, to leave time for the evidence checklist due at 12:00.

## 4. Fairness rules
- **Frozen GT and measures.** Nothing in the frozen tables changes after run 1. New finds go to the post-freeze tables only.
- **Same input revision.** Every scored run on a feature uses the same byte-identical snapshot in `runs/<feature>/input/` (404917 as of **4 Mar 2026**, 431577 as of 18 Oct 2026, UTF-8, comments hidden).
- **One variable per iteration:** prompt, context mode, step order, or model, but never two at once. A pure repeat (no change) is allowed to measure variance.
- **Log every change** in `docs/prompt-log.md`: run ID, what changed, why, and the expected effect.
- **Fresh session per run.** No memory or chat carry-over, and the tool never sees `evaluation/`, the digests or `decisions/001`. Run it from a clean folder.
- **Same scoring.** Use the same sheet and hit rule. If possible, at least one reviewer per run should not have written the prompt change.
- **Report all runs**, including bad ones. No cherry-picking.

## 5. Claude Code vs Codex
- These are **separate tracks**. The tool is not a variable inside one iteration chain.
- Compare head-to-head only at the **same prompt version, same input snapshot and same context mode**. Ticket-only is the main comparison, because Codex has TES app repo access that Claude Code may lack.
- Compare recall (ticket-only), noise, Wrong, item count and review time directly.
- Tokens are **not** directly comparable across tools (different tokenizers and cache reporting). Compare token-diet gains *within* a tool (percentage change), and give cross-tool totals only as indicative.
- Record the model and reasoning setting each time. A Codex ticket + code run that hits C-NA items (Android or Insight code) is reported as extra evidence, outside the shared recall figure.
- What transfers between the tools (same prompts, similar scores) versus what needs adapting goes into Repeatable success.

## Assumptions to confirm with the team
1. **Pre-dev cutoffs:** 404917 uses the ADO revision and repo commit as of **1 Mar 2026**, and 431577 uses **18 Oct 2026**. These assume the first dev comment or human question came after those dates.
   **Resolved 4 Nov, before run 1:** on 1 Mar, 404917 had **no child stories**; all six were created on 4 Mar, and the first was activated on 5 Mar. The cutoff moves to **4 Mar 2026 (end of day)**: after the breakdown, before development. 431577's 18 Oct is confirmed (the feature was last changed 2 Oct, and the first human question came on 19 Oct). Snapshots are in `runs/<feature>/input/feature.md`, built with the ADO REST `asOf` parameter.
2. **Baseline and thresholds:** (b) the human refinement is the headline "before", with targets of at least 60% ticket-only recall and at most 25% noise.
3. Story attribution of the 404917 comments (414478, 414480, 414481) is inferred from topic. Verify it against the raw comments; the wording and count stay frozen.
4. Hindsight-hypothesis items (GPS battery and privacy, Google Maps licensing) and the facilitator's TSP watch list are **not** GT. They can only score as Useful new.
5. GT-SS-02 (map bug) stays out of recall until the Android TES app repo is available. If it becomes available, it counts only in runs that have it.
6. "Readiness" (GT-SS-06, missing AC and empty fields) is a fair GT item even though it's easy to spot. If the team disagrees, drop it **before** run 1, not after.
7. The team can produce the as-of-date ADO snapshots (architect task), so the blind setup is feasible.
