# Pre-Flight: 404917 TES App staff security step 2
Prompt version: v0.1 · Code check: done (AlarmServer.Database, AlarmServer.Koala, AlarmServer.Swamp, AlarmServer.Web) · Readiness: 1 (shaped: state is Ready, but no story has AC or estimates, problem/value/dependencies are empty, and the cross-component fan-out decisions are open)

## Top 3 before anything else
1. D-01: Existing position push goes only to the accepter once the alarm is taken. #414478 wants all receivers. Pick one.
2. S-01: Find out how a TES-app staff security alarm is stored today. The existing position path only works for RestLog alarms.
3. P-01: Define "handled". It decides when every app stops sending GPS.

## DECIDE
| ID | Decision needed | Options | Evidence | Owner | Conf. | Min |
|---|---|---|---|---|---|---|
| D-01 | Who receives GPS updates after someone takes the alarm? | A: only the taker (current code) / B: all apps that received it, until handled | PositioningHelper.java:61-73 vs #414478 "send out to all tes apps that has recieved" | Architect | high | 2 |
| D-02 | How does the app send GPS updates in? | A: reuse `PUT /v1/submitalarm/{alarmId}` (needs REST API token) / B: new message in the app XML protocol | AlarmResource.java:310-323, 312; #414476 | Architect | medium | 1.5 |
| D-03 | Can follow-me show several tracks per alarm? | A: add sender id to `AlarmPositionUpdate` + GeoPositionLog / B: show only the originator | AlarmPositionUpdate.kt:6-10; db_setup.sql:3311-3317; #414481 "show all the GPS position" | Architect | high | 1.5 |
| D-04 | Which push channel carries the 30 s updates? | A: keep `UPDATE_ALARM_POSITION` (has visible alert text) / B: silent push or MQTT only | Pusher.java:274, 384-390; PositioningHelper.java:84-87 | Dev | medium | 1 |
| D-05 | Which login path(s) get the interval parameter? | A: both GprsClient and IpClient / B: GprsClient only | GprsClient.java:620-655; IpClient.java:1163-1168 | Dev | medium | 1 |
| D-06 | Does interval 0 replace the existing `SendGeoPosWithStaffSecurity` feature? | A: interval replaces it / B: keep both, define precedence | db_data.sql.template:1140; #414476 "if the value is 0 ..." | Dev | medium | 1 |
| D-07 | Is the interval only sent when `StaffSecurity` is enabled? | A: gate on StaffSecurity AppFeature / B: always send | db_data.sql.template:1113; #414477 "If TES app has staff security activated" | Dev | medium | 0.5 |

## SPIKE
| ID | Question the spike answers | Evidence | Owner | Timebox | Conf. |
|---|---|---|---|---|---|
| S-01 | Is a TES-app staff security alarm a RestLog alarm, so `updateAlarmPosition`'s "ongoing" check works for it? | PositioningHelper.java:116-127; RestAlarmRepository.java:35-36 | Architect | 0.5 d | medium |
| S-02 | For a W9-triggered staff security alarm, which phone sends GPS, and how is it linked to the alarm id? | #414476 "triggered either by W9 or by TES app"; IpacsWlrAlarmHandler.java:125-141 | Dev | 0.5 d | high |
| S-03 | Does accepting in Insight write `AlarmAccepted`, and so redirect position pushes to a user with no app device? | PositioningHelper.java:64-67; #414480 | Architect | 0.5 d | medium |
| S-04 | Can the Android app send GPS every 30 s with the screen locked or the app in background (permissions, battery)? | #414476 "on a time interval until the alarm has been handled" (inferred) | Dev | 1 d | medium |
| S-05 | Will changing `pushAlarmPositionUpdate` break the WLR/ipacs/external API callers? There are no tests for this area. | IpacsWlrAlarmHandler.java:203; WlrHelper.java:23; only 4 tests, all in rest/src/test | Tester | 0.5 d | high |

## ASK THE PO
| ID | Question | Evidence | Why it matters | Conf. |
|---|---|---|---|---|
| P-01 | Does "handled" mean taken, signed as handled, or alarm closed? | #414476 "until the alarm has been handled"; #414479 "Sign as handled" | Sets when all apps stop sending GPS | high |
| P-02 | Is the iOS TES app in scope for v1? | #414476 title "TES App Android"; #414481 no platform | Doubles app work and test matrix | high |
| P-03 | What are the acceptance criteria for each story? | No AC in any story; feature state "Ready" | Testers can't verify anything | high |
| P-04 | Who provides and pays for the Google Maps key? | Feature "We should embedded google maps" | Licence/cost blocker for release | medium |
| P-05 | Is storing staff GPS for up to 3 days acceptable for privacy? | AlarmRepository.java:474-488 | GDPR, staff are tracked | medium |
| P-06 | Does Insight also show the map, or only take and accept? | #414480 "take an Staff security alarm on Insight" | Scope of Insight work | medium |
| P-07 | For phrase signing, what is the phrase and who sets it? | #414479 "or just a phrased" | Needs a field/setting nobody owns | medium |
| P-08 | What visual treatment marks the prio 0 card? | Feature "may be a color over the whole card or somethings else" | UX open; app can't start | medium |

## ALREADY ANSWERED (by code)
| ID | Question | Answer | file:line |
|---|---|---|---|
| A-01 | Are app features already sent to the app at login? | Yes, as a `DisabledFeatures` list. Booleans only, so #414479 needs two new boolean rows. | MessageCommon.java:124-161; db_setup.sql:611-615 |
| A-02 | Do staff security flags already exist? | Yes: `StaffSecurity`, `SendGeoPosWithStaffSecurity`, `ShowW9StaffSecurity` | db_data.sql.template:1113, 1140, 1145 |
| A-03 | Is there a server path to receive and push alarm positions? | Yes: `updateAlarmPosition` → `pushAlarmPositionUpdate` via push + MQTT, logged to GeoPositionLog | PositioningHelper.java:61-91, 112-147 |
| A-04 | How is a new SystemParameter added? | Migration row (Id/Description/Value) + `SystemParameter.Int` enum entry; read at login, so changes apply on next login | db_setup.sql:1820-1825; SystemParameter.java:11-63; GprsClient.java:630-651 |
| A-05 | Do new app features need admin UI work? | No. Rows with `SpecialHandling=0` are listed automatically; only translations needed | SystemParameterAppFeatures.php:70 |

## Not checked
- TES App Android and iOS: code not available
- Insight: code not available
- Google Maps integration: not in repos
- W9 device side: only server-side handling visible
- "DM90i" assumed to be AlarmServer.Swamp + Database + Web (inferred from `se.tunstall.dm80.*` packages)
