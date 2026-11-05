# Pre-Flight working notes: 404917 TES App staff security step 2

Prompt version: v0.1 · Snapshot: 2026-03-04 · Repos: AlarmServer.Database, AlarmServer.Koala, AlarmServer.Swamp, AlarmServer.Web

---

## Step 1: Ask

Format: **[Lens] Question**. Evidence. *Why it matters.* (confidence)

### Developer
1. **[Dev] What exactly ends the GPS update loop: alarm taken/accepted, "Sign as handled", or alarm done/closed?** #414476 "until the alarm has been handled". *App keeps tracking staff forever or stops too early.* (high)
2. **[Dev] Which device sends GPS when the staff security alarm is triggered by a W9 and not by the app?** #414476 "triggered either by W9 or by TES app, then should the App send in the GPS position". *No defined link between the W9 alarm and the phone that should report position.* (high)
3. **[Dev] When interval is 0, does the app still send a single position with the alarm?** #414476 "if the value is 0 the app should only send in the alarm with position". Clear for TES-triggered, unclear for W9-triggered. (medium)
4. **[Dev] What happens to updates when GPS fix is lost, the app goes to background, or the phone is offline? Queue, drop, or send last known?** inferred from #414476. *Battery/permission behaviour on Android decides if follow-me works at all with screen locked.* (medium)
5. **[Dev] When several apps receive the alarm and one takes it, do the others keep receiving GPS updates?** #414478 "send out to all tes apps that has recieved the staff security" vs feature "when the staff 'takes' the alarm". (high)
6. **[Dev] What happens to the interval if it is changed in SystemParameter while apps are logged in?** #414476 "the time interval should be send to the App on login". Only applied at next login. (medium)
7. **[Dev] What does the receiving app show before any GPS position has arrived?** inferred from #414481 "must show all the GPS position". (low)

### Architect
8. **[Arch] Which component is "DM90i" in the repos, and which module owns the login response, the position intake and the push?** #414477, #414478. *Ownership of changes.* (high)
9. **[Arch] Which transport does the app use to send GPS updates: existing REST position update, or a new message in the app's XML protocol?** #414476. (high)
10. **[Arch] Which transport fans out updates to apps (push, MQTT, polling), and is a visible notification acceptable every 30 s?** #414478 "like follow me". (medium)
11. **[Arch] "Show all the GPS position" – positions of whom? Only the originator, or also every app that has the alarm (responders)?** #414481 "the TES App that has started the alarm will also send in GPS updates ... show all the GPS position". *Payload needs sender identity if more than one track.* (high)
12. **[Arch] Where is the new interval parameter gated: on the existing StaffSecurity app feature, or always sent?** #414477 "If TES app has staff security activated". (medium)
13. **[Arch] How does Insight take/accept a staff security alarm, and what does that do to the position fan-out?** #414480. Insight not in repos. (medium)
14. **[Arch] Google Maps: API key ownership, licence cost, and whether the key ships in the app or is configured per customer.** Feature "We should embedded google maps". (medium)
15. **[Arch] Privacy: staff position is personal data. How long are positions stored and who can see them?** inferred. (medium)
16. **[Arch] Load: N apps × one update every 30 s, each fanned out to M apps. Is the server path sized for that?** inferred from #414476/#414478. (low)

### Tester
17. **[Test] There are no acceptance criteria in any story. What are the pass conditions per story?** All stories: no AC field. (high)
18. **[Test] Cross-component end-to-end test needed: App (Android) → DM90i → other apps (+ Insight). Who owns it, and on which environment?** #414476, #414478, #414480, #414481. (medium)
19. **[Test] Boundary values for interval: 0, negative, non-numeric, very small (1 s).** #414477 "settings in SystemParameter". (medium)
20. **[Test] Two simultaneous staff security alarms from different staff: each map must show only its own alarm's positions.** inferred. (medium)

### PO / UX
21. **[PO] Is iOS in scope?** #414476 titled "TES App Android"; #414481 has no platform. (high)
22. **[UX] What is the visual treatment of the prio 0 card?** Feature "may be a color over the whole card or somethings else". Open. (medium)
23. **[PO] Does Insight also show the map / follow-me, or only take and accept?** #414480 only "take an Staff security alarm". (medium)
24. **[PO] What is the "phrase" in "signing ... just a phrased", and who configures it?** #414479. (medium)
25. **[PO] Problem statement, business value and dependencies are empty.** Feature fields. (high)

### Cross-cutting
- **Assumption:** apps receiving the alarm can be identified on the server (needed for "all tes apps that has recieved"). See step 2: yes, via RestAlarmIdPushedToGprsClientIds.
- **Gap between stories:** nobody owns "stop sending" on the server side (#414478 has no end condition); nobody owns how Insight acceptance affects follow-me.
- **Contradiction (soft):** #414478 "all tes apps that has recieved" vs the "take" flow in the feature, see Q5.
- **Readiness:** feature in state Ready, but no story points, no AC, empty problem/value/dependencies; 414479 is Active while siblings are New.

---

## Step 2: Code check

### 2.1 Located files (most likely to change)
| # | File | Why |
|---|---|---|
| 1 | AlarmServer.Swamp/general-server/.../GprsClient.java:620-670 | Builds TES-app login response with SystemParameter elements + features |
| 2 | AlarmServer.Swamp/general-server/.../IpClient.java:1163-1168 | Second login path (`MELoginResponse` passthrough), only features injected |
| 3 | AlarmServer.Swamp/general-server/.../MessageCommon.java:124-161 | Sends AppFeatures to app as `DisabledFeatures` list |
| 4 | AlarmServer.Swamp/stt-common/.../systemparameter/SystemParameter.java:11-63 | Typed SystemParameter ids/defaults (new interval param goes here) |
| 5 | AlarmServer.Swamp/stt-common/.../positioning/PositioningHelper.java:42-147, 216-254 | Existing alarm position update + push to apps + GeoPositionLog |
| 6 | AlarmServer.Swamp/stt-common/.../positioning/AlarmPositionUpdate.kt:6-10 | Position push payload |
| 7 | AlarmServer.Swamp/stt-common/.../push/Pusher.java:274, 384-390 | Push payload for `UPDATE_ALARM_POSITION` |
| 8 | AlarmServer.Swamp/rest/.../resources/AlarmResource.java:310-323, 403-406 | REST position update + getGeoPositions |
| 9 | AlarmServer.Database/db_scripts/db_data.sql.template:1102-1150 | AppFeatures seed (StaffSecurity etc.) |
| 10 | AlarmServer.Database/db_scripts/db_setup.sql:611-615, 1820-1825, 3311-3317 | AppFeatures, SystemParameter, GeoPositionLog schema |
| 11 | AlarmServer.Database/db_scripts/migrate/ (latest db_migrate_1.0.264.sql) | New migration for parameter + app features |
| 12 | AlarmServer.Web/www/SystemParameterAppFeatures.php:34, 70 | Admin UI for app features |

Inferred: "DM90i" = AlarmServer.Swamp (+ Database/Web). Packages are `se.tunstall.dm80.*`; no file names DM90i. Confidence medium.

### 2.2 Step 1 questions answered or sharpened
- **Q8 (ownership): Sharpened.** Login response = general-server (GprsClient/IpClient). Position intake/push = stt-common PositioningHelper, called from rest AlarmResource, ipacs, wlr. Schema = AlarmServer.Database. Admin = AlarmServer.Web.
- **Q9 (transport in): Sharpened.** An existing path is `PUT /v1/submitalarm/{alarmId}` → `PositioningHelper.updateAlarmPosition` (AlarmResource.java:310-323). It checks `restApiTokenExists` (AlarmResource.java:312), i.e. an external API token, not TES app user auth. It only updates if the alarm is ongoing in RestLog (PositioningHelper.java:116-127). Unknown whether TES-app staff security alarms live in RestLog.
- **Q5 (who gets updates): Answered, and conflicts with story.** `pushAlarmPositionUpdate` sends only to the accepting user's device once `AlarmAccepted` has a row; before that to all devices in `RestAlarmIdPushedToGprsClientIds` (PositioningHelper.java:43, 61-73, 95). #414478 asks for "all tes apps that has recieved".
- **Q10 (transport out): Sharpened.** Each update is sent by push (`Pusher.pushToDevice`) AND MQTT (PositioningHelper.java:84-87). `UPDATE_ALARM_POSITION` has a localized alert key `Alarm_Position_Update` (Pusher.java:274) and the APNs payload sets a localized alert message (Pusher.java:384-390). Risk: a visible notification every 30 s per alarm (iOS path at least). Android path at Pusher.java:452 not read.
- **Q11 (sender identity): Sharpened.** `AlarmPositionUpdate(alarmId, isIndoor, alarmPosition, geoAccuracy)` has no sender/user field (AlarmPositionUpdate.kt:6-10). `GeoPositionLog` has only AlarmId, GeoCoordinates, Timestamp (db_setup.sql:3311-3317). Multiple tracks per alarm cannot be told apart today.
- **Q12 (gating): Sharpened.** Existing AppFeatures: `StaffSecurity` (db_data.sql.template:1113), `SendGeoPosWithStaffSecurity` (:1140), `ShowW9StaffSecurity` (:1145). AppFeatures are booleans only (`Enabled tinyint(1)`, db_setup.sql:611-615) and are sent as a `DisabledFeatures` list (MessageCommon.java:124-161). The numeric interval cannot be an AppFeature; it must be a SystemParameter in the login response, as #414477 says. Overlap: `SendGeoPosWithStaffSecurity` vs "interval 0 = only send alarm with position".
- **Q6 (runtime change): Answered (partially).** Login response reads SystemParameter at login time (GprsClient.java:630-651 pattern); a change applies at next login only.
- **Q2 (W9): Sharpened.** W9 alarms come in via ipacs/WLR with indoor (zone) position (IpacsWlrAlarmHandler.java:125-141, 203; WlrHelper.java:23). Nothing in code links a W9 alarm to a TES app's GPS.
- **Q15 (retention): Answered.** GeoPositionLog is deleted with RestLog, between 1 day and 3 days depending on the cleanup interval (AlarmRepository.java:474-488; SystemParameter `CleanupRestLogInterval(130, 72)`, SystemParameter.java:57).
- **Q16 (load): Sharpened.** Each logGeoPosition opens a new DbApi (PositioningHelper.java:216-218); each push creates a new 2-thread pool (PositioningHelper.java:76). GeoPositionLog has no index on AlarmId (db_setup.sql:3311-3317). Low/medium risk at 30 s intervals.
- **Q13 (Insight): Sharpened.** If an Insight user accepting writes `AlarmAccepted`, `getGprsClientIdByUserName` is used for that user (PositioningHelper.java:64-67). An Insight operator likely has no GPRS client, so updates could go nowhere. Insight code not available. (medium, inferred)
- **Not visible in code:** Q1, Q3, Q4, Q7, Q14, Q17-Q25.

### 2.3 Code-only findings
- **C1. Two login paths.** GprsClient builds the login response DOM with SystemParameter elements and features (GprsClient.java:620-655). IpClient passes `MELoginResponse` through and only injects DisabledFeatures, inserted before `<AccessRights>` (IpClient.java:1163-1168; MessageCommon.java:138-141). If `<AccessRights>` is missing, features are dropped silently. The new interval must be added in both, or one path is chosen. (medium)
- **C2. Admin UI for app features is generic.** New rows with `SpecialHandling=0` appear automatically (SystemParameterAppFeatures.php:70). No UI work for #414479 beyond translations (Web/www/languages/*.php). (high)
- **C3. SystemParameter pattern.** Table `Id, Description, Value` (db_setup.sql:1820-1825); typed enum `SystemParameter.Int.<Name>(id, default)` (SystemParameter.java:11-63, highest id seen 150). New parameter needs migration + enum entry. AppFeature `Feature varchar(30)` limits feature name length (db_setup.sql:612). (high)
- **C4. Emergency priority forcing exists only for code 98765 / type 20 "Assault"** (RestAlarmRepository.java:35-36, 150-155; Utils.java:15-18). Unknown whether the TES-app staff security alarm uses this type, i.e. whether "prio 0" is guaranteed server-side. (medium)
- **C5. Test coverage thin.** Only 4 test files in Swamp, all in rest (AlarmResourceTest, AlarmServiceTest, Authentication*). No tests for PositioningHelper, MessageCommon, GprsClient/IpClient login. (high)
- **C6. Other callers of the position path.** `updateAlarmPosition` is also used by ipacs (IpacsWlrAlarmHandler.java:203) and wlr (WlrHelper.java:23). Changing fan-out rules in `pushAlarmPositionUpdate` affects W9/WLR and external API alarms too. (high)
- **C7. Endpoint exists to read the position history:** `GET getGeoPositions/{alarmId}` (AlarmResource.java:403-406). Could give a late-joining app the track so far. (medium)

### Not checked
- TES App Android (and iOS): code not available.
- Insight: code not available.
- Google Maps integration / licensing: not in repos.
- W9 device firmware/protocol beyond the server side.
- AlarmServer.Koala: searched, no staff security, AppFeatures or SystemParameter hits; not relevant as far as visible.
