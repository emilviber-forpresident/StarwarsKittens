---
name: ideate
description: Run one iteration round of team + AI ideation for the hackathon. Reads previous rounds, takes the team's new input, diverges or converges, and saves the round to ideas/round-NN.md. Use when the user says "/ideate", "next idea round", or wants to brainstorm or shortlist hackathon ideas.
argument-hint: "[diverge|converge] [team input or focus]"
---

# Ideation round

Act in the style of the `ideation-facilitator` persona (`.claude/agents/ideation-facilitator.md`).

1. **Load context cheaply**: read `ideas/index.md` (create it if missing). Only open the latest round file in full. Don't re-read every round.
2. **Determine mode** from the arguments: `diverge` (default for early rounds) or `converge`. Treat any remaining text as the team's input for this round, and give it priority over your own ideas.
3. **Run the round**: Frame, then Diverge or Converge, then Provoke (see the persona). When converging, score against the criteria in `docs/hackathon-brief.md`: real problem, data access, starting areas touched, measurable before/after, team contribution and reuse potential.
4. **Save** `ideas/round-NN.md` (next number) with these sections: Focus, Team input, Ideas (new/evolved), Killed (with reason), Scores (converge only), Open questions, Next round.
5. **Update** `ideas/index.md` with one line per round (number, mode, one-sentence outcome) and a running "Live shortlist" section.
6. Finish with a short chat summary and the provocative questions for the team to discuss offline before the next round.

This log is also the evidence for the **Idea generator** and **Problem detective** achievements, so keep the team's own contributions visibly attributed.
