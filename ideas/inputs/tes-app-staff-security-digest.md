# Digest: Feature 404917, TES App staff security step 2

Source: ADO IHCP, fetched 4 Nov 2026 via `az boards` (feature, 7 children, plus comments on 3 stories). Personal names are omitted.
Repos listed by the team: `AlarmServer.Swamp` (about 94 MB), `AlarmServer.Database`, `AlarmServer.Koala`, `AlarmServer.Web` (all small, branch `master`).

## Status
- Feature **Closed** (created 13 Nov 2025, last changed 21 Sep 2026). All 7 stories are Closed. None have acceptance criteria or story points.
- Feature text: the description is filled in, but **Problem statement, Business value and Dependencies are empty**.
- This makes it a **hindsight case**: the outcome is known, so we can check whether the tool would have predicted it.

## What the feature says
- Show staff security alarms in the normal alarm list but visibly marked as **prio 0**, then reuse today's staff security view with **embedded Google Maps** showing the position.
- Stories: the Android app sends GPS on an interval (414476), DM90i sends the interval at login with a default of 30 s (414477), DM90i fans GPS out to all apps that received the alarm, "follow me" (414478), app features for acknowledging (414479), Insight can take the alarm (414480), the TES app follows the position on a map (414481), and DM90i Insight prio 0 v2 (422194, added later).

## What happened (ground truth from comments, Mar–Jun 2026)
- **Fan-out bug** (7 May): position updates reached **only one app** even when several had accepted the alarm.
- **Map update bug** (7–13 May): after accepting, the position didn't update; reopening showed one extra point, and leaving the alarm lost the earlier positions.
- **Late scope cut** (19 May): "In version 1 we won't have alarm position history." The feature was removed and the flow had to be retested.
- **Missed cross-component dependency** (1 Jun): Insight treated prio 0 like a regular alarm ("X has already taken the alarm"). It needed the TES app's requests **plus Swamp and Database changes**, which led to a new story, 422194, added late.
- API design was worked out in comments during development (a `PUT /emergency/{alarmId}` position update and `POST .../emergency/done`).

## Hindsight hypothesis
A pre-refinement analysis could plausibly have flagged:
- the multi-receiver state model
- position history as an undecided scope question
- the prio 0 lifecycle in `/alarms/all` and Insight's different alarm-taking flow
- missing acceptance criteria
- GPS battery and privacy questions, and Google Maps licensing (not discussed at all)

## Gap in our own input
The Android TES app and the Insight app are **not in the listed repos**, yet 3 of 7 stories live there. Ask the team for them, or record it as a limit.

## Caveat for a fair test
The stories were edited during development. For a blind test, use the **ADO revision as it was before development started** (around Mar 2026), not today's text, and hide the comments from the tool.
