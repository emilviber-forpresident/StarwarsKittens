# 002: Run 1 is exploratory; formal scoring comes later

Date: 4 Nov 2026 · Status: **Accepted** (team)

## Context
The product owner agent produced a full evaluation framework: frozen ground truth, a per-item scoring sheet, thresholds and a stopping rule (`evaluation/`). The team found it **overwhelming** as a starting point, and wanted to see what Pre-Flight actually produces before deciding how to judge it.

## Options
1. Score run 1 with the full sheet.
2. **Run 1 as an open team conversation (5 questions), and bring in the formal scoring later, if and where it helps.**
3. Drop the evaluation framework.

## Decision
Option 2. Run 1 (404917, ticket only) is discussed using `runs/404917/run-01-notes.md`. `evaluation/` stays untouched as **reference material**: we can score any saved run against it later, because the ground truth was frozen before run 1.

## Why
- Talking about real output first builds a shared understanding faster than a framework does.
- Nothing is lost. The frozen ground truth and saved outputs mean we can still score run 1 formally afterwards, for the evidence.
- We keep only two rules: the same input every run, and one written-down change per run.

## Learning (for the demo)
AI tends to over-engineer the process. The team pushed back and simplified it. That's a human-in-the-loop example worth telling.
