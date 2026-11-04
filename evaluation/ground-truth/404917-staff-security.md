# Ground truth: Feature 404917, TES App staff security step 2 (HINDSIGHT)

**Status: FROZEN on 4 Nov 2026, before run 1.** Do not edit the frozen table. Anything found later goes under "Post-freeze finds" and is reported separately (it never changes the recall denominator).
Source: `ideas/inputs/tes-app-staff-security-digest.md` (ADO comments Mar to Jun 2026). Feature is Closed, so the outcome is known.

## Detectability key
- **T** = visible from ticket text alone (pre-dev revision). A good question about it counts as a hit.
- **C** = needs code to be detectable. Only counts toward recall in ticket + code runs where the repo is available.
- **C-NA** = needs code that the tool cannot access today (Android TES app / Insight app are not in the listed repos). Out of scope for recall until the repo is available.

## Frozen checklist (6 items: 5 T, 0 C, 1 C-NA)

| ID | Known problem (one line) | Source (story, comment date) | Category | Detect |
|---|---|---|---|---|
| GT-SS-01 | Multi-receiver state model undefined: position updates reached only one app when several had accepted the alarm (fan-out bug) | 414478*, 7 May 2026 | bug / state model | T |
| GT-SS-02 | Map did not follow position after accept; reopening showed one extra point; leaving the alarm lost earlier positions | 414481*, 7 to 13 May 2026 | bug | C-NA |
| GT-SS-03 | Position history was an undecided scope question; cut late ("v1 won't have alarm position history"), forcing a retest | 414481*, 19 May 2026 | scope | T |
| GT-SS-04 | Insight treats prio 0 like a regular alarm ("X has already taken the alarm"); needed TES app requests plus Swamp and Database changes, which became late story 422194 | 414480*, 1 Jun 2026 | dependency (cross-component) | T |
| GT-SS-05 | API contract for position updates and ending the emergency was not defined; worked out in comments during dev (`PUT /emergency/{alarmId}`, `POST .../emergency/done`) | comments Mar to Jun 2026, story to verify | open decision / API | T |
| GT-SS-06 | Not ready for refinement: no acceptance criteria or story points on any story; Problem statement, Business value and Dependencies fields empty | feature + all stories (ticket fields) | readiness | T |

\* Story attribution inferred from story topic; the digest does not name the story per comment. Verify against the raw ADO comments before run 1 (lookup only, do not change the wording or the count).
**Verified 4 Nov against the raw ADO comments (lookup only):**
- GT-SS-01 is on 414478 (7 May)
- GT-SS-02 is on 414481 (7 and 13 May)
- GT-SS-03 is on 414481 (19 May)
- GT-SS-04 is on 414480 (1 Jun)
- GT-SS-05: the endpoints are on 414478 (10 Mar)

### Hit rule
A run item is a hit when it would have made refinement discuss **the same area and the same risk**. Examples:
- GT-SS-01 hit: "How is position fan-out tracked when several apps accept? Who stops receiving and when?" Not a hit: "Consider concurrency."
- GT-SS-04 hit: any item that asks how Insight takes or displays a prio 0 alarm differently, or flags a missing Swamp/Database dependency. Not a hit: "Check dependencies."
- GT-SS-03 hit: any item that asks whether position history or a track is in v1.

## Not ground truth (candidates only)
From the digest's hindsight hypothesis. There's no evidence these caused problems, so they are **not** in the denominator. If a run raises one, mark it **Useful new** only if the team confirms it as a valid gap.
- GPS battery drain from interval sending; privacy and consent for staff location
- Google Maps licensing and cost
- Prio 0 lifecycle in `/alarms/all` (overlaps GT-SS-04; if the item names the Insight taking flow, score it as GT-SS-04)

## HIDE from the tool (blind run)
| Hide | Why |
|---|---|
| All comments on the feature and its stories | They contain the answers |
| Every revision after dev start. Use the ADO revision **as of 1 Mar 2026** (before the first comment) | Stories were edited during dev |
| Story **422194** entirely (title, text, link) | Added late as a result of GT-SS-04 |
| State, closed dates, and the "Closed" and "Resolved" history | Signals the outcome |
| Repo code after dev start: check out the last commit **before 1 Mar 2026** for the code step | `master` contains the fixes |
| This file, `evaluation/`, `ideas/inputs/*digest.md`, `decisions/001` | They contain the ground truth |

Practical rule: run the tool from a clean folder that holds only the prompts and the frozen input snapshot (`runs/404917/input/`), not from the repo root.

## Post-freeze finds (separate, never added to the table above)
| ID | Finding | Found in run | Confirmed by (role) | Source checked | Status |
|---|---|---|---|---|---|
| NF-SS-01 | | | | | Proposed / Confirmed / Rejected |
