# Step 2: Check against the code (prompt v0.1, optional)

Only run this step if `repos/` contains code. Keep the token cost down: **search first, then read only the matches**. Never read whole repositories.

1. **Locate.** From the feature and the step 1 questions, pull out the key terms: domain words, entity names, endpoints, settings, UI names. The ticket may be in Swedish or English, so search for both forms. Search the repos and list the 5–15 files or components that are most likely to change.
2. **Answer or sharpen.** For each step 1 question the code can inform:
   - **Answered by code**: the code already decides it. Cite `file:line` and say what it does.
   - **Sharpened**: the code shows the concrete constraint (for example "this field is nullable" or "this setting is read once at startup"). Rewrite the question to match, and cite `file:line`.
   - **Not visible in the code**: leave the question as it is.
3. **Add code-only findings.** Look for things the ticket text can't reveal:
   - other clients or components that call the same code path, and may break or need the same change
   - existing behaviour or data the feature changes that other parts of the code rely on
   - places where the database or schema has to change
   - code with no tests, or code that has been changed a lot recently, in the touched area
   - existing settings or feature flags that already cover part of the feature
4. Record each item with its `file:line` evidence and a confidence level. If a component the feature clearly needs isn't in `repos/`, say so explicitly ("Not checked: <component>, code not available").
