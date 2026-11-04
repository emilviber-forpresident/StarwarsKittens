# Round 01 (diverge)

## Focus
How might we find a feature's complexity, open technical decisions and "not ready" signals *before* the team starts the refinement discussion?

Constraints: 3 days, a small team, Claude Code plus our own tickets/repos. The output has to work on real tickets.

## Team input (verbatim summary, original in Swedish)
- A feature/ticket arrives.
- It needs analysing, and the areas of complexity need identifying.
- Complexity or problems in the solution need thinking through, and technical decisions get made.
- Those decisions should be made **as early as possible**, before development starts.
- A tool or method for analysing the feature *before* developers/the team discuss it would help.
- **Maturity / ready for dev**: is the feature ready, or are there problems we can spot early that need resolving?

## Ideas (new)
1. **Ready-or-Not Radar**: an agent scores a ticket against a Definition-of-Ready rubric (goal, acceptance criteria, data, dependencies, NFRs, UX). It returns a traffic light plus the reasons. *Cheap to test.*
2. **Pre-mortem Bot**: "It's 3 sprints later and this feature failed. Why?" It produces failure stories that point at hidden complexity.
3. **Decision Debt Finder**: pulls out the implicit technical decisions in a ticket ("sync or async?", "which service owns X?") and drafts ADR stubs to settle in refinement.
4. **Question Storm**: generates the 10 questions a senior dev, a tester, a UX designer and an ops person would each ask. It's persona switching via our existing agents. *Cheap.*
5. **Code-Aware Complexity Map**: reads the ticket plus the repo, finds the components it touches, and flags hotspots (churn, no tests, old bugs). It marries the ticket to reality.
6. **Ghost of Tickets Past**: finds similar historical tickets and bugs: "last time we touched this, it took 3× longer because…"
7. **Assumption Ledger**: lists every unstated assumption in the ticket, each marked verified, unverified or contradicted.
8. **Refinement Agenda Generator**: the output isn't a score, it's a 15-minute agenda for the team meeting: what to decide, who needs to be there, and what to spike.
9. **Inversion: the Saboteur**: an agent tries to misread the ticket on purpose and build the wrong thing. Every successful misreading is an ambiguity. (Fun, and a candidate for 404 dignity points.)
10. **Maturity Ladder**: levels 0–4 (idea → shaped → refined → ready → ready + decisions recorded), with the evidence each level needs. It works as a team-wide method, not just a tool.

## Killed
None yet (diverge round).

## Starting areas touched
Mainly 1 (needs and defining work). Also 3 (testability questions), 4 (#5/#6 use bug history and tech debt) and 5 (#6 uses product knowledge). There's good Bridge builder potential.

## Open questions
- Which ticket source can we actually reach in 3 days (Jira/ADO export, or pasted text)? Can we also get the code repo?
- Do we have **historical tickets that went wrong**, where we know the hidden problem afterwards? That would be our before/after and difficult-case evidence.
- Who decides "ready" today, and how long does refinement take per ticket? That's our baseline.
- Output for whom: the PO (before handing over) or the devs (before discussing)?
  - **Answered (team, 4 Nov):** the feature team: developers and an architect, sometimes a PO or UX stakeholder. This holds for all our examples.

## Team preference (4 Nov)
Team likes **4 (Question Storm), 5 (Code-Aware Complexity Map) and 8 (Refinement Agenda Generator)**, so the converge round will focus on these. The team is collecting real ADO features and repo context first.

## Next round
Collect 2–3 real tickets (one known to have blown up). Then run a converge round on ideas 1, 3, 4, 5, 8 and 10, scored against the brief.
