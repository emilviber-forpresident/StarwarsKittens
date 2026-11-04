# Ground truth: Feature 431577, TSP Client Integration (LIVE)

**Status: FROZEN on 4 Nov 2026, before run 1.** Do not edit the frozen table. New finds go under "Post-freeze finds".
Source: `ideas/inputs/tsp-client-integration-digest.md` (human comments on 19 Oct and 2 Nov 2026).

> **This ground truth is PARTIAL.** The case is live: stories are New and refinement hasn't happened yet. The 6 items below are only what humans have raised so far. A low precision score here may just mean we don't know yet. That's why confirming new finds (below) matters more here than for 404917.

## Detectability key
- **T** = visible from ticket text alone (revision before the questions were asked)
- **C** = needs code or system knowledge (`ihcp`, `tes` repos) to be detectable

## Frozen checklist (6 items: 4 T, 2 C)

| ID | Human-raised open question (one line) | Source (story, comment date) | Category | Detect |
|---|---|---|---|---|
| GT-TSP-01 | Navigil watch with **no service agreement**: can updates reach TSP at all? | 433196, 19 Oct 2026 | edge case / data model | T |
| GT-TSP-02 | How are alarm codes added or updated in the **new TES web**? (flow not defined) | 433225, 19 Oct 2026 | scope / flow | T |
| GT-TSP-03 | Should **all** alarm codes go to TSP, or only some? | 433225, 19 Oct 2026 | scope / data model | T |
| GT-TSP-04 | Does deleting an alarm code belong in 433225 or in delete story 433197? | 433225, 19 Oct 2026 | scope (story boundary) | T |
| GT-TSP-05 | TSP **soft-deletes** service agreements, but TES has no soft-delete concept: delete semantics don't match | 433225, 19 Oct 2026 | state model | C |
| GT-TSP-06 | Is syncing "Medicinsk information" acceptable for **legal, audit and GDPR**? Could "Viktig information" be reused instead? | 433196, 2 Nov 2026 | NFR / compliance | C (GDPR part is T, see hit rule) |

### Hit rule
Same area and same risk, as for 404917. Clarifications:
- GT-TSP-05: in a ticket-only run, an item about "delete in TES vs delete in TSP may mean different things" counts as a hit.
- GT-TSP-06: any item that flags sensitive or medical data sent to TSP (GDPR, legal basis, audit) is a hit. Suggesting reuse of "Viktig information" is not required.
- GT-TSP-03 and GT-TSP-04 are separate. One item can hit only one GT ID, so pick the closest.

## Watch list (not ground truth, unverified)
The facilitator's first read of the text. These are **not** in the denominator. If a run raises one, mark it **Useful new (pending)** and send it for confirmation.
- Error handling, retry and offline behaviour when TSP is down
- Sync direction and conflicts (edits made directly in TSP)
- Uniqueness of "TSP Användarkod": who guarantees it, and is there a race?
- Migrating existing clients who are already in both systems
- Auth and credentials (only "endpoint information" today)
- Organisation sync frequency, and what happens to clients when an organisation is "flagged"
- "Potential dependency to TSP and DM90" is still undecided

## HIDE from the tool (blind measurement runs)
| Hide | Why |
|---|---|
| All comments (19 Oct and 2 Nov) | They are the ground truth |
| Revisions after **18 Oct 2026**. Use the ADO revision as of 18 Oct | Stories may have been edited after the questions |
| This file, `evaluation/`, `ideas/inputs/*digest.md`, `decisions/001` | They contain the ground truth |

- Input must be fetched as UTF-8 (no "Anv�ndarkod"). Fix it once, snapshot it into `runs/431577/input/`, and reuse it byte-for-byte.
- **Delivery run:** the version handed to the real refinement may use the current text and comments. It is labelled "delivery" and is **not** scored for recall.

## How new finds get confirmed
1. A reviewer marks the item **Useful new (pending)** on the scoring sheet and copies it to the table below.
2. Confirmation by **role**:
   - technical items: a dev or the architect, checked against code (file or path) or the story text (quote)
   - business or scope items: the **PO**, by decision or in refinement
3. The status is **Confirmed** only with a source reference. Without one it stays Proposed and doesn't count.
4. Confirmed finds are reported as "new finds confirmed" (Second pair of eyes). They are **never** added to the frozen table, so recall stays comparable across runs.

## Post-freeze finds
| ID | Finding | Found in run | Confirmed by (role) | Source checked (quote / path / decision) | Status |
|---|---|---|---|---|---|
| NF-TSP-01 | | | | | Proposed / Confirmed / Rejected |
