# Feature snapshot: 404917 (as of 2026-03-04)

Source: Azure DevOps work item fields at the snapshot date. Comments, history, people and links outside the hierarchy are excluded.

## 404917 [Feature] TES App staff security step 2
State: Ready · Story points: none

**Description:**
💡 General Description/Feature Hypothesis:

Change the flow that TES app has on receiving staff security alarms. The Alarm should be shown as all other alarms in the Alarmlist but it has to be visible that it is staff security alarm, may be a color over the whole "card" or somethings else that draw attention so the staff knows that this i a prio 0 alarm.

when the staff "takes" the alarm we could use the same view that we have today on staff security. We should embedded google maps to that view and show the position in the view

🔧 Problem Statement:

💰 Business Value:

💼 Dependencies:

🔒 Other:

### 414476 [User Story] TES App Android: Send in GPS updates
State: New · Story points: none

**Description:**
If a staff security alarm has been triggered either by W9 or by TES app, then should the App send in the GPS position to the DM90i on a time interval until the alarm has been handled.

the time interval should be send to the App on login

the default value: 30 seconds

if the value is 0 the app should only send in the alarm with position and not send updates

### 414477 [User Story] DM90i: Send the GPS update time interval
State: New · Story points: none

**Description:**
If TES app has staff security activated the DM90i should send how often TES App should send the GPS update to DM90i on the login response.

the timer interval should be a settings in SystemParameter

Default value: 30 seconds

### 414478 [User Story] DM90i: Send GPS updates to TES app
State: New · Story points: none

**Description:**
If one TES app has send in the staff security and have GPS updates activated, The DM90i will recieve GPS updates on certain time intervall that should be send out to all tes apps that has recieved the staff security like follow me

### 414479 [User Story] DM90i: Appfeature for be able to acknowledge staff security alarms
State: Active · Story points: none

**Description:**
2 Appfeatures for staff secuirty

- An appfeature if "Sign as handled" should be showned or not in the App
- An appfeature if the signing should be by Employed ID or just a phrased

### 414480 [User Story] Insight: Take and accept a staff security
State: New · Story points: none

**Description:**
It should be possibly to take an Staff security alarm on Insight

### 414481 [User Story] TES App: Follow me on staff security
State: New · Story points: none

**Description:**
On staff security the TES App that has started the alarm will also send in GPS updates, the DM90i will send the GPS updates to the apps that has got the alarms and must show all the GPS position in the embedded google maps view

