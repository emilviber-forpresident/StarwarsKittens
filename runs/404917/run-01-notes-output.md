# Pre-Flight working notes: 404917 TES App staff security step 2
Prompt version: v0.1 · Source: `input/feature.md` (snapshot 2026-03-04)

## Step 1: Ask

### Developer lens
| # | Question | Evidence | Why it matters | Conf. |
|---|---|---|---|---|
| Q1 | What event stops the app sending GPS updates: "Sign as handled" in the app, the alarm closed in DM90i, or a stop message from DM90i? | #414476 "on a time interval until the alarm has been handled" | Without a defined stop signal the app may keep tracking forever, or stop too early | high |
| Q2 | When a W9 triggers the alarm, which app sends GPS: an app paired with the W9, or none? | #414476 "triggered either by W9 or by TES app"; #414481 "the TES App that has started the alarm will also send in GPS updates" | The two stories disagree on who the sender is for W9 alarms | high |
| Q3 | How does the app keep sending GPS on interval while backgrounded, screen locked, or under Android Doze? | #414476 "send in the GPS position ... on a time interval" (inferred: Android background limits) | Staff in danger will not have the app in the foreground; updates may silently stop | high |
| Q4 | What does the app send when there is no GPS fix (indoors) or the fix is stale? | #414476 (no mention of accuracy or missing fix), inferred | Map may show a wrong or old position as current | medium |
| Q5 | If the interval changes in SystemParameter during a session, does the app pick it up only at next login? | #414476 "the time interval should be send to the App on login" | Running alarms may use an outdated interval; testers need to know the expected behaviour | medium |
| Q6 | With value 0, "only send in the alarm with position": does today's alarm message already carry a position? | #414476 "if the value is 0 the app should only send in the alarm with position" | If not, the alarm message itself must change too (hidden work) | medium |
| Q7 | What happens to forwarded GPS updates on apps that log in, reconnect, or take the alarm after it started? | #414478 "send out to all tes apps that has recieved the staff security" | Late joiners may see no position until the next update or never | medium |
| Q8 | How are out-of-order or delayed updates handled (timestamp on each update)? | #414478 (no payload defined), inferred | Map could jump back to an old position | medium |
| Q9 | What happens if two responders take the same alarm, or Insight and an app take it at the same time? | #414480 "take an Staff security alarm on Insight"; feature "when the staff 'takes' the alarm" | Concurrency of take/accept across clients is undefined | medium |

### Architect lens
| # | Question | Evidence | Why it matters | Conf. |
|---|---|---|---|---|
| Q10 | What is the message contract for GPS updates app→DM90i and DM90i→apps (new message type or extension of the existing alarm message; fields: lat, lon, accuracy, timestamp, alarm id)? | #414476, #414478 (no payload described) | Three components (Android app, DM90i, possibly Insight) must agree; biggest cross-team risk | high |
| Q11 | What does "TES app has staff security activated" mean technically: an appfeature, a licence, a SystemParameter? | #414477 "If TES app has staff security activated" | Decides when the interval is included in the login response | high |
| Q12 | Is the interval SystemParameter global, or per unit/site/app group? What are the min/max bounds? | #414477 "the timer interval should be a settings in SystemParameter" | Very low values hurt battery and server load; scope affects the data model | medium |
| Q13 | Does DM90i store the GPS positions (alarm log or history) or only forward them? What is the retention? | #414478 "will recieve GPS updates ... that should be send out" | Staff location is personal data (privacy/GDPR); storage means a schema change | medium |
| Q14 | Is Insight a recipient of forwarded GPS updates and does it show a map? | #414478 only names "tes apps"; #414480 only "take and accept" | Insight may need the same contract and a map view, which no story owns | medium |
| Q15 | Embedding Google Maps: SDK, API key, licence cost, behaviour without network? | Feature "We should embedded google maps to that view" | Licence and key management are outside the team's control; cost is unknown | high |
| Q16 | Backward compatibility: how do old TES app versions handle the new login-response field and forwarded GPS messages? | #414477 "on the login response" (inferred) | Mixed app versions in the field could break login or ignore alarms | medium |
| Q17 | Who is authorised to receive another staff member's live position? | #414478 "send out to all tes apps that has recieved the staff security" | Location sharing to every recipient may need a privacy or consent decision | medium |

### Tester lens
| # | Question | Evidence | Why it matters | Conf. |
|---|---|---|---|---|
| Q18 | No story has acceptance criteria. What is "done" for each? | All stories: no AC; "Story points: none" | Nothing can be tested or estimated | high |
| Q19 | How will GPS movement be simulated end to end (Android → DM90i → several apps)? Is a W9 device available for testing? | #414476 "triggered either by W9 or by TES app" | Cross-component test needs a rig; W9 path may be untestable | medium |
| Q20 | Boundary cases for the interval: 0, negative, missing parameter, very large values | #414476 "if the value is 0"; #414477 "Default value: 30 seconds" | Only 0 and default are defined | medium |
| Q21 | Several staff security alarms active at the same time: one map per alarm, or all on one map? | #414481 "must show all the GPS position in the embedded google maps view" (inferred) | Map behaviour with concurrent alarms is undefined | low |

### PO / UX lens
| # | Question | Evidence | Why it matters | Conf. |
|---|---|---|---|---|
| Q22 | Is iOS in scope? Only #414476 says "Android" | #414476 "TES App Android"; #414481 "TES App" | Scope may double for the app work | high |
| Q23 | No story owns the alarm list highlight ("color over the whole card ... prio 0") or the Google Maps embedding | Feature description; no matching story | Core visible part of the feature is unplanned | high |
| Q24 | Define the lifecycle: take / accept / acknowledge / sign as handled. Are these the same or different states? | #414479 title "acknowledge" vs body "Sign as handled"; #414480 "Take and accept" | Different words across stories; state machine unclear | high |
| Q25 | What is "a phrased" signing: free text, a fixed phrase, a password? | #414479 "signing should be by Employed ID or just a phrased" | Can't build validation or UI | high |
| Q26 | "all the GPS position": a trail of the alarming user's positions, or the positions of all responders? | #414481 "must show all the GPS position" | Changes what responders must send as well | medium |
| Q27 | Problem statement, business value and dependencies are empty, yet the feature is "Ready" | Feature: "🔧 Problem Statement:" (empty), "State: Ready" | Readiness state doesn't match content | high |
| Q28 | What is "the same view that we have today on staff security" (step 1)? Is that view in this scope, or reused as-is? | Feature "we could use the same view that we have today" | Hidden dependency on earlier work | medium |

### Cross-feature checks
- **Assumptions:** an existing staff security view exists (feature); alarms have a "prio 0" concept (feature); the alarm message may carry a position (#414476).
- **Open decisions:** stop condition (Q1), W9 sender (Q2), message contract (Q10), storage (Q13), map content (Q26).
- **Gaps between stories:** alarm list highlight and map embedding (Q23); Insight receiving GPS (Q14); stop signal between #414479 and #414476 (Q1).
- **Contradictions:** #414476 vs #414481 on who sends GPS (Q2); "acknowledge" vs "sign as handled" (Q24).
- **Readiness:** feature "Ready" but all stories New/Active with no points and no AC (Q18, Q27).

## Step 2: Code check
Step 2 skipped: no code access (`repos/` not present in the run workspace).
