# 001: Padawan Pre-Flight: AI pre-refinement analysis of features

Date: 4 Nov 2026 · Status: **Accepted** · Source: [ideas/round-01](../ideas/round-01.md), [round-02](../ideas/round-02.md)

## Context
When a feature arrives, complexity, hidden dependencies and open technical decisions are often found **during development** instead of before it. Evidence from Feature 404917 (staff security):
- a fan-out bug found in test
- a late scope cut (position history)
- a missed Insight → Swamp/Database dependency that became story 422194

We want these found *before* the feature team's refinement meeting. The audience is mainly **developers** (plus an architect), and the **PO facilitates** the meeting.

## Options considered
1. **#4 Question Storm**: questions from each persona about the ticket. Score 26/30.
2. **#5 Code-Aware Complexity Map**: link the ticket to the code it touches and its risky areas. Score 24/30.
3. **#8 Refinement Agenda**: turn the findings into a meeting plan. Score 23/30.
4. Ready-or-Not Radar, Decision Debt Finder, Maturity Ladder and others (round 01). These were folded into the steps above or parked.

## Decision
Build **one tool, Padawan Pre-Flight** (`/preflight <feature-id>`), that runs three steps on **one feature at a time**:

1. **Ask (#4):** unclear points, assumptions and open decisions, weighted toward dev, architect and tester. PO and UX questions go in an "ask the PO" bucket.
2. **Check against the code (#5, optional):** answer, sharpen or add questions using only the code the feature touches. If there's no repo access, skip this step and say so in the output.
3. **Agenda (#8):** a 15-minute refinement plan: **Decide / Spike / Ask the PO / Already answered**, each with an owner role and a readiness level.

### Way of working: iterate per feature, measure each run
For each feature, the team repeats:
1. **Run** Pre-Flight and save the output in `runs/<feature>/run-NN.md`, together with the prompt version used and the tokens in and out.
2. **Measure** the run against the feature's ground truth and the team's judgement (see below).
3. **Analyse** as a team: what it missed, what was noise, and why.
4. **Adjust** one thing (prompt, context, steps) and note it in `docs/prompt-log.md`, then run again.

The same feature is rerun until the improvement levels off, then we move to the next feature. Comparing run 1 with run N on the same feature gives the before/after.

### Measures per run (to be refined by `product-owner`)
| Measure | How |
|---|---|
| **Recall** | Share of known ground-truth problems the run predicted. Staff security: the late bugs, scope cut and dependency. TSP: the open questions humans raised on 19 Oct and 2 Nov. |
| **Precision / noise** | Team marks each item useful, already-known or noise |
| **New finds** | Valid items humans hadn't raised. Each one must be confirmed against the source. |
| **Tokens** | In and out, as reported by `/cost` or `/usage` |
| **Time** | Wall clock for the run, plus the team's review time |

### Cases
| Feature | Role | Code step |
|---|---|---|
| 404917 TES App staff security step 2 | **Hindsight**: pre-development ADO revision, comments hidden | AlarmServer repos. The TES app/Insight repos are pending a PAT. |
| 431577 TSP Client Integration | **Live**: output goes to the real refinement (devs + PO) | `ihcp`, `tes` (large, so read only the targeted parts) |
| "Bonnus" feature | Optional third case | App repo not accessible yet |

## Why
- It's a real, recurring pain, and both cases have **ground truth** to measure against.
- Each step on its own is weak (a long list, facts without meaning, an empty agenda). Chained, they're useful.
- The optional code step makes it robust to missing repo access.
- The per-feature iteration loop produces the evidence on its own:
  - **Prompt mechanic** and **Better than before**: comparing runs
  - **Token diet**: tokens per run at equal quality
  - **Beyond the happy path**: the hindsight case
  - **Useful beyond our team**: the TSP refinement feedback
  - **Repeatable success**: two different kinds of feature
  - **Second pair of eyes**: confirmed new finds

## Consequences / next steps
- `product-owner`: sharpen the measures and the success threshold, and define a fair "before" baseline.
- `architect`: design the skill layout, prompt versioning, the `runs/` structure, and how to fetch an ADO revision as of a date (with the UTF-8 fix).
- Team: get the PAT for the app repos, and agree when the TSP refinement happens.
