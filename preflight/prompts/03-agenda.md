# Step 3: Refinement agenda (prompt v0.1)

Turn the notes from steps 1 and 2 into a 15-minute refinement agenda for a developer-heavy team, with a PO facilitating.

1. **Filter.** Drop:
   - anything already answered clearly in the stories
   - generic advice
   - duplicates, by merging items that are really the same question
   - low-confidence items with no evidence

   Keep **at most 25 items**, and prefer fewer.
2. **Classify** each remaining item into exactly one bucket:
   - **DECIDE**: a technical or scope choice the team must make before development. Give the options, ideally as A or B.
   - **SPIKE**: needs investigation before it can be decided or estimated. Give the question the spike answers and a rough timebox.
   - **ASK THE PO**: needs a business or user answer.
   - **ALREADY ANSWERED**: answered by the code in step 2. Include it, so the team can skip it and trust the answer.
3. **Prioritise** within each bucket. The things that would hurt most if discovered mid-sprint come first: cross-component work, data model changes, or behaviour shared by several users or devices.
4. Give each item an **owner role** (Dev / Architect / Tester / PO / UX) and a time slot, so the total fits 15 minutes.
5. Set a **readiness level** for the whole feature:
   - 0: idea
   - 1: shaped
   - 2: refined, but has open decisions
   - 3: ready for dev
   - 4: ready, with decisions recorded

   Give a one-line reason.
