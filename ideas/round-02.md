# Round 02 (converge)

## Focus
Which of the team's picks (#4 Question Storm, #5 Code-Aware Complexity Map, #8 Refinement Agenda Generator) should we build, tested on two real features?

## Team input
- **Team picks (4 Nov):** ideas 4, 5 and 8.
- **Who the output is for (team):** the feature team: devs and an architect, sometimes a PO or UX.
- **Cases supplied by the team:** Feature 431577 *TSP Client Integration* (repos `ihcp`, `tes`) and Feature 404917 *TES App staff security step 2* (repos `AlarmServer.Swamp/.Database/.Koala/.Web`). A third folder, "Bonnus feature usecases not accessible", is empty.

Digests (later rounds read only these):
- [tsp-client-integration-digest.md](inputs/tsp-client-integration-digest.md)
- [tes-app-staff-security-digest.md](inputs/tes-app-staff-security-digest.md)

**Context-size evidence (Token diet / Prompt mechanic):** the input files held 642 bytes of pointers. The raw ADO data fetched was about 224 KB of JSON across 31 files. The two digests come to **5.7 KB (about 2.5% of the raw data)**.

## What the cases tell us
| | TSP Client Integration | Staff security step 2 |
|---|---|---|
| Type | **Live**: Implementing, 7 stories New, no points | **Hindsight**: Closed, outcome known |
| Ticket quality | Rich description, Gherkin acceptance criteria | Empty problem statement and value fields, **no acceptance criteria** |
| Ground truth | Open questions humans raised on 19 Oct and 2 Nov (soft delete mismatch, watch with no service agreement, GDPR on medical info) | Late bugs (fan-out to one app, map updates), a late scope cut (position history), a missed Insight→Swamp/DB dependency that led to a new story |
| Domain | Data sync / integration | Real-time alarms / mobile / GPS |

These are two different products and kinds of task, which is good material for **Repeatable success**.

## Scores (1–5)
| Criterion | #4 Question Storm | #5 Complexity Map | #8 Agenda |
|---|---|---|---|
| Real problem, concrete case | 5 | 5 | 4 |
| Data access in 3 days | 5 (ticket text only) | 3 (repos readable but `tes` is 1 GB; staff security app repos missing) | 5 |
| Starting areas touched | 3 (1, 3) | 4 (1, 3, 4, 5) | 2 (1) |
| Measurable before/after | 4 (recall against comments) | 5 (would it have caught the Insight/Swamp dependency?) | 3 (needs a live meeting) |
| Team contribution | 4 | 4 (dev and architect heavy) | 4 (UX shapes the format) |
| Reuse by others | 5 | 3 (needs per-product repo mapping) | 5 |
| **Total /30** | **26** | **24** | **23** |

## Decision proposal: don't pick one, chain them
The three ideas form one pipeline, with each step adding a layer:

```
ADO feature + children → [#4 Question Storm: dev / architect / tester / PO / UX personas]
                       → [#5 Complexity Map: optional code layer, only the files the feature touches]
                       → [#8 Refinement Agenda: decide / spike / ask, by role, a 15-minute meeting]
```
- **MVP (today/tomorrow morning):** #4 → #8 from ticket text alone. This is the highest score and the lowest risk.
- **Depth layer (Thursday):** #5 on one case. Staff security is the better candidate because its repos are small, and it tests the "missed dependency" story.
- **Test protocol:**
  - *Hindsight* (staff security): give the tool the pre-development ADO revision with comments hidden, then score how many of the known late problems it predicted. This is **Beyond the happy path** and **Better than before**.
  - *Live* (TSP): run it before the team's refinement, then compare with the questions humans already raised. Hand it to the TSP team for feedback. This is **Useful beyond our team** and **Second pair of eyes**.

## Evolved ideas
- #4 takes in #7 (Assumption Ledger) and #3 (Decision Debt Finder): unstated assumptions and open decisions become question types in the Storm.
- #10 Maturity Ladder becomes a single "readiness level" line at the top of the agenda. It isn't a separate tool.

## Killed or parked
- **#1 Ready-or-Not Radar**: folded into #8. A bare traffic light invites arguing with the score instead of the content.
- **#2 Pre-mortem, #6 Ghost of Tickets Past**: parked. Good later, but #6 needs a history search we don't have time to build.
- **#9 Saboteur**: parked as a fun prompt variant. It may earn the "404: dignity not found" point.

## Open questions
- Can we get the **Android TES app and Insight repos**? 3 of the 7 staff security stories live there.
- Is it OK to send internal ticket text and code to Claude under the hackathon rules? (Still not confirmed.)
- Who in the TSP team could receive our output *before* their next refinement, and when is it?
- What did you mean to put in the empty "Bonnus" folder?
- Fun points: candidate names are **"Jedi Pre-cog"**, **"These Aren't the Requirements You're Looking For"** and **"Padawan Pre-Flight"**.

### Team answers (4 Nov)
1. App repos: maybe reachable with a PAT, since some team members have access.
2. Sending internal tickets and code to Claude: **OK**.
3. TSP output audience: **developers**, plus the PO who facilitates refinement. It's mainly a developer audience.
4. "Bonnus" folder: another feature, but it has the same problem (the TES app / iOS app repo isn't accessible). Possibly resolved later.
5. Project name: **Padawan Pre-Flight**.
6. The team questions the case for chaining #4, #5 and #8. The facilitator explained it in chat (one tool with three stages, not three tools). Decision still pending.

## Next round
Write the decision record `decisions/001-chosen-problem.md`, then hand it to `product-owner` for the before/after success measures and to `architect` for the pipeline sketch.
