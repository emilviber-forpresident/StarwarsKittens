# Step 1: Ask (prompt v0.1)

Read `input/feature.md` in full. Then go through it once for **each lens** below, as that person preparing for refinement. Write down what they would need answered before they could start or estimate the work.

| Lens | Looks for |
|---|---|
| **Developer** | Unclear behaviour, missing states and transitions, error and retry paths, what happens with several users or devices at once, the data that has to exist, ordering and timing |
| **Architect** | Which components or systems are involved and who owns each change, integration contracts (APIs, messages, payloads), sync direction and source of truth, consistency, migration of existing data, security and authorisation, non-functional needs (performance, scale, battery, privacy, licensing) |
| **Tester** | Acceptance criteria that can't be tested or are missing, unstated preconditions, negative and boundary cases, what must be tested together across components |
| **PO / UX** (keep short) | Scope boundaries ("is X in v1?"), unstated user goals, conflicting statements, empty fields in the ticket (problem statement, value, dependencies) |

Also check across the whole feature:
- **Assumptions**: things the text takes for granted but never states.
- **Open decisions**: places where a choice clearly has to be made (A or B) but isn't recorded.
- **Gaps between stories**: behaviour that falls between two stories, or that no story owns.
- **Contradictions** between the feature and a story, or between two stories.
- **Readiness**: missing acceptance criteria, estimates or dependencies.

For each finding, record:
- the lens
- the question, phrased so it can be answered
- the evidence (story number and quote)
- why it matters (what goes wrong if it's unanswered)
- confidence (high / medium / low)

Aim for completeness here, not brevity. Step 3 does the filtering.
