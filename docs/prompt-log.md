# Prompt log

One line per change: date · run · what changed · why

- 4 Nov · v0.1 · first draft of preflight/prompts; removed two example phrases that hinted at known answers
- 4 Nov · run 02 (404917) · added code: 4 AlarmServer repos at 4 Mar 2026, git history removed · run 01 skipped step 2 (no repos/); test the code check
- 5 Nov · run 03 (404917) · v0.2: single output file (no notes.md); added Code map and Parked sections; each fact appears once · team review of runs 01–02: notes.md and preflight.md overlapped heavily (notes was 2x the agenda size in run 02)
- 5 Nov · 431577 live-01 · v0.2, first headless run (`claude -p`, read/search/write tools only, no shell or web), current ADO snapshot, repos from tags (ihcp, tes) · 3.1 min, 36 turns, $1.39; tokens: output 18,837 (6,344 thinking), cache-write 102,723, cache-read 953,349, fresh input 30 · single file produced, as v0.2 intended · found sibling feature docs (tsp-data-integration) in the repo on its own · published to ADO as a comment and attachment
- 5 Nov · 431577 live-02 · v0.3: summary first (readiness + maturity counts, blockers, next step, who is needed), then a "By role" section (PO/Architect/Dev/Tester/UX, priority order, urgency, depends on), with each section opening on a one-line summary; the renderer folds sections into collapsibles · team feedback on live-01: too dense, no per-role view, hard to skim · 3.7 min, 37 turns, $1.83; tokens: output 22,707 (8,406 thinking), cache-write 134,344, cache-read 1,504,693, fresh input 37 · every agenda item still cites evidence; By role refers to items by ID and does not repeat evidence
