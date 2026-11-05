# Pre-Flight: 404917 TES App staff security step 2
Prompt version: v0.1 · Code check: skipped · Readiness: 1 (shaped: feature is "Ready" but no story has AC or points, and the core contracts and stop conditions are undefined)

Time plan (15 min): DECIDE 7 · SPIKE 2.5 · ASK THE PO 4.5 · wrap-up 1

## Top 3 before anything else
1. D-01: Agree on the GPS update message contract across the Android app, DM90i and Insight. No story defines it.
2. D-02: Define the event that stops GPS tracking. "Until the alarm has been handled" has no owner or signal.
3. P-02: No story covers the alarm list highlight or the Google Maps embedding, which are the visible core of the feature.

## DECIDE
| ID | Decision needed | Options | Evidence | Owner | Conf. | Min |
|---|---|---|---|---|---|---|
| D-01 | How are GPS updates carried app→DM90i and DM90i→apps? | A: new dedicated GPS-update message (alarm id, lat, lon, accuracy, timestamp) / B: repeat or extend the existing alarm message | #414476 "send in the GPS position to the DM90i"; #414478 "should be send out to all tes apps" (no payload given) | Architect | high | 2 |
| D-02 | What stops the app sending GPS updates? | A: DM90i sends an explicit stop when the alarm is closed / B: app stops locally on "Sign as handled" | #414476 "until the alarm has been handled"; #414479 "Sign as handled" | Architect | high | 1.5 |
| D-03 | Who sends GPS when a W9 triggers the alarm? | A: the TES app paired with the W9 user / B: none, so W9 alarms get no tracking in v1 | #414476 "triggered either by W9 or by TES app" vs #414481 "the TES App that has started the alarm" | Architect | high | 1 |
| D-04 | Who receives forwarded GPS updates? | A: every app that received the alarm / B: only apps that took it (+ Insight?) | #414478 "all tes apps that has recieved the staff security"; #414480 Insight can "take" | Architect | medium | 1 |
| D-05 | Does DM90i store GPS positions? | A: forward only, nothing stored / B: store in the alarm log with a defined retention period | #414478 "will recieve GPS updates ... that should be send out" (inferred: storage not stated) | Architect | medium | 1 |
| D-06 | Scope and bounds of the interval SystemParameter | A: one global value, min/max validated (e.g. 0 or ≥ N s) / B: per unit or site | #414477 "the timer interval should be a settings in SystemParameter"; only 0 and 30 s defined | Dev | medium | 0.5 |

## SPIKE
| ID | Question the spike answers | Evidence | Owner | Timebox | Conf. |
|---|---|---|---|---|---|
| S-01 | Can TES App Android send GPS reliably on a 30 s interval while backgrounded, locked or in Doze (foreground service, permissions, battery)? | #414476 "send in the GPS position ... on a time interval" (inferred: Android background limits) | Dev | 1 day | high |
| S-02 | What does embedding Google Maps in the existing staff security view need (SDK, API key, licence cost, no-network behaviour)? | Feature "We should embedded google maps to that view and show the position" | Dev | 1 day | high |
| S-03 | Does Insight have a staff security take/accept flow today, and how are concurrent takes (Insight + app) resolved? | #414480 "It should be possibly to take an Staff security alarm on Insight" | Dev | 0.5 day | medium |

## ASK THE PO
| ID | Question | Evidence | Why it matters | Conf. |
|---|---|---|---|---|
| P-01 | Is iOS in scope, or only Android? | #414476 "TES App Android"; #414481 just "TES App" | Could double the app work | high |
| P-02 | Which story owns the prio 0 alarm-card highlight and the map embedding? | Feature "a color over the whole 'card'"; "embedded google maps"; no story covers either | The visible core of the feature has no story | high |
| P-03 | Are "take", "accept", "acknowledge" and "sign as handled" separate alarm states? | #414479 title "acknowledge" vs body "Sign as handled"; #414480 "Take and accept" | Without this the state machine and the stop signal (D-02) can't be built | high |
| P-04 | What is signing "by a phrase": free text, a fixed phrase, or a code? | #414479 "by Employed ID or just a phrased" | Can't design the validation or the UI | high |
| P-05 | Should the map show a trail of the alarming user's positions, or the positions of all responders? | #414481 "must show all the GPS position" | Decides whether responders must send GPS too | medium |
| P-06 | Is sharing a staff member's live location with every alarm recipient acceptable for privacy (consent, who may see it)? | #414478 "send out to all tes apps" (inferred: personal data) | Could block release, and drives D-04 and D-05 | medium |
| P-07 | Can acceptance criteria and the empty problem statement, value and dependencies be added before estimation? | Feature "🔧 Problem Statement:" empty, "State: Ready"; all stories have no AC or points | The feature can't be estimated or tested as written | high |

## ALREADY ANSWERED (by code)
| ID | Question | Answer | file:line |
|---|---|---|---|
| — | No code available | Step 2 skipped | — |

## Not checked
- TES App Android source (GPS sending, alarm list, existing staff security view): code not available
- DM90i source (login response, SystemParameter, alarm forwarding): code not available
- Insight source (take/accept staff security): code not available
- W9 device integration: code not available
