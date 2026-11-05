# Output format: `output/preflight.md` (v0.3: summary first, then by role)

This is the **only** file you write. Do your step 1 and step 2 analysis in your own working process, then write one consolidated document. Don't write `notes.md` or any other file.

The document is read in layers. Someone who reads only **Summary** knows the state of the feature and what happens next. Each section below it opens with a **one-line summary** (the `> ` line) and folds out into detail, so a reader can stop at any layer. The renderer turns every `##` section after Summary into a collapsible block, with the `> ` line visible when it's closed.

```markdown
# Pre-Flight: <feature id> <title>
Prompt v0.3 · Code check: done (<repos>) / skipped

## Summary
**Readiness: <0–4> <label>** · <one-line reason>
**Maturity:** <n>/<m> stories with acceptance criteria · <n>/<m> estimated · <n> decisions open · <n> spikes · <n> PO questions
<2–3 plain sentences for everyone (PO, dev, UX, test, manager): what the feature is, the main risk, and the state in one breath. No file paths, no IDs.>

**Blockers**
1. <ID>: <one line, plain language>
2. ...
(at most 3)

**Next step:** <one sentence: the single thing that moves the feature forward>
**Who is needed:** <roles, plus any outside team or system owner (e.g. Keycloak owner, TSP vendor)>

## By role
> <one line: which roles have the most to do>

### <Role> · <n> items
> <one line: what this role must do, in plain words>

| # | ID | Action | Urgency | Depends on |
|---|---|---|---|---|
| 1 | D-05 | <verb-first action, at most 12 words> | Now / Before sprint / In sprint | <IDs, or an outside party, or –> |

(Repeat for each role that has items, in this order: PO, Architect, Developer, Tester, UX. Skip roles with no items.)

## Refinement agenda (15 min)
> <one line: how many items, and the time budget per bucket>

### DECIDE
| ID | Decision needed | Options | Evidence | Owner | Conf. | Min |
|---|---|---|---|---|---|---|

### ASK THE PO
| ID | Question | Evidence | Why it matters | Conf. |
|---|---|---|---|---|

## Spikes
> <one line: how many, total timebox, which one blocks most>

| ID | Question the spike answers | Evidence | Owner | Timebox | Conf. |
|---|---|---|---|---|---|

## Already answered by the code
> <one line: what the team can stop worrying about>

| ID | Question | Answer | file:line |
|---|---|---|---|

## Code map
> <one line: the main components touched>

| Component / file | What changes or why it matters | Agenda IDs |
|---|---|---|
At most 12 rows. Group files by component when you can. Omit the whole section if the code check was skipped.

## Parked
> <one line>

- <role>: <item> (<evidence>)
At most 10.

## Not checked
> <one line>

- <components or repos needed but not available, and assumptions about mapping names to code>
```

Rules:
- Use stable item IDs: `D-`, `S-`, `P-`, `A-` plus a number.
- One question per row. Each row is at most 3 lines.
- **Each fact appears once with its evidence**: in the agenda, spikes or already answered. The **By role** and **Summary** sections are the action view. They refer to items by ID with a short action and never repeat evidence.
- Every DECIDE, SPIKE and ASK THE PO item appears in **By role** under its owner, and under any other role that must act on it (for example, a tester who must rewrite Gherkin once P-04 is answered).
- In **By role**, rows are ordered by priority (most important first). **Urgency** means: `Now` = before or in the refinement meeting; `Before sprint` = must be done before the stories can be estimated; `In sprint` = can be handled during development. **Depends on** names what must happen first.
- Plain language in Summary and in the `> ` lines: no file paths and no code identifiers.
- A code finding with no agenda item goes in DECIDE or SPIKE if it carries risk, otherwise in Parked. It's never dropped silently.
