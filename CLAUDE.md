# Tunstall AI Hackathon workspace (3–5 Nov 2026)

We are a team at the TTN & TTG AI Hackathon. The goal is to pick one real problem, then explore and solve it with AI, and to give the **process** (methodology, workflows, context and memory management) as much weight as the result. Full brief: @docs/hackathon-brief.md

## Our workflow (draft, evolve it as we go)
1. **Ideate**: run n rounds of team + agent iteration (`/ideate`). Each round is saved in `ideas/round-NN.md`.
2. **Converge**: shortlist, then pick one problem. Record the decision in `decisions/`.
3. **Define**: `product-owner` agent covers users, value, scope and the success measures (before/after).
4. **Architect**: `architect` agent produces the high-level plan that guides design and build.
5. **Build, test, document**: `developer`, `tester` and `ux-designer` agents, guided by the plan.
6. **Evidence**: log anything demo- or checklist-worthy with `/evidence` as it happens.

## Agents
- `ideation-facilitator`: divergent ideation, provocation and convergence (project level)
- `product-owner`, `architect`, `developer`, `tester`, `ux-designer`: global personas

## Conventions
- Keep context lean: write conclusions to files and reference them instead of re-pasting history.
- Every decision gets a short record in `decisions/NNN-title.md` (Context / Options / Decision / Why).
- Record token usage for comparable tasks (`/cost` or `/usage`) because the Token diet achievement needs tool-reported numbers.
- Write prompts/context that improved results to `docs/prompt-log.md` (Prompt mechanic evidence).

## Current status
Day 1: setting the scene and ideating. No problem chosen yet.
