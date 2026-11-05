# Feature snapshot: 431577 (as of 2026-10-18)

Source: Azure DevOps work item fields at the snapshot date. Comments, history, people and links outside the hierarchy are excluded.

## 431577 [Feature] TSP Client Integration
State: Implementing · Story points: none

**Description:**
💡 General Description/Feature Hypothesis:

For ADDA IL we need to establish a integration to TSP.

** Please note that in this feature we will refer to "Client". Client is the same thing as "Brukare", "Care Recipient", "Service user" in TES. Or "Service Agreement" in TSP **

This feature covers the Client synchronization part and should be considered a MVP solution, any scope beyond the MVP scope will be covered in a separate feature.
🔍In Scope

- Set up integration
- #433193
- Fetch Organization from TSP and present it in TES.
- #433194
- Create a new client and enable it to be syncronized into TS
- #433195
- Update the client and it should be syncronized to TSP
- #433196
- #433225
- Remove the client and it should be syncronized to TSP
- #433197

❌ Out of Scope

- Any client creation except for "Skapa ny brukare"

🔧 Problem Statement:

- Remove duplicate data entry across TES and TSP.
- Strive towards giving customers one user interface and one operational workflow in TES.
- Reduce the risk of inconsistent or incorrectly entered data across
systems.
- Reduce customer complexity by keeping TSP as a backend service rather
than a customer-facing application.
- Create the integration foundation required to manage the complete alarm
service chain in TES.

💼 Dependencies:
Potential dependency to TSP and DM90

🔒 Other:
User stories to cover the flow for this feature:
As an authorized administrator, I want to enable the integration between TES and TSP, so that the organization can start using the alarm receiving center flows in TES.
As an authorized administrator, I want to retrieve the ARC organization from the TES organization’s view, so that the organization does not have to maintain the same structure in both systems.
As an authorized administrator, I want to create a client in TES so that i can have it syncronized to TSP
As an authorized administrator, I want to update a client in TES so that the changes can be updated in TSP automatically
As an authorized administrator, I want to delete a client in TES so that the changes can be updated in TSP automatically

Important technical information:

- Basic principles in the Client Syncronization is as follows:
- In TES there will be one Client.
- If the client is syncronized to ARC, TES will generate a unique number - called a TSP Användarkod
- The "Användarkod" will be the unique identifier between TES and ARC
- In ARC a client is called "Service Agreement" and one client can have several "Service Agremeents"
- A alarm code in TES equals one Service agreement in ARC. Meaning that multiple alarm codes = multiple service ageements
- Eventhough a Client has multiple Service Agreements, they will all share the TSP Användarkod Example

- When a Client is created the client needs to be assigned a "TSP Användarkod" that needs to be matched the Service Agreement in TSP.
- When a Client is updated, all service agreements associated with the “TSP User Code” must be reviewed and the relevant changes applied. These may include a new alarm code, updated medical information, changes to next-of-kin details, and care recipient linking.

**Success criteria:**
- You should be able to set up a integration towards TSP through TES
- The integration should fetch Organizations from TSP
- When and if the TSP integration is activated;
- Once you create a New Client in TES you should be able to select "Sync to TSP" and then being able to select a TSP organization
- Once you update a user that is located in a TSP Organization and/or is syncronized to TSP, the updates should be reflected in TSP.

### 432680 [UX Story] Old > New TES web | Ny brukare
State: Closed · Story points: none

**Description:**
Update the current 'Ny brukare', don't be locked to previous design. Also think of the other menu choices and how they can work together. There also will be no sidebar. Needs to be closer related aesthetically to the reassurance dashboard.

### 433193 [User Story] Set up integration
State: New · Story points: none

**Description:**
As a TES Admin
I need to set up a integration to ARC/TSP
So that i can syncronize data between the systems

**Acceptance criteria:**
- Placeholder
- In setttings you should be able to set up:
- Endpoint information

### 433194 [User Story] Get Organization from ARC
State: New · Story points: none

**Description:**
As a TES Admin
I want to get all organizations from ARC
So that i can add users to the recently fetched organizations and syncronize to TSP

**Acceptance criteria:**
- Fetch Organization
- Store in a New Organizational Tree (With read only?)

### 433195 [User Story] Add Client
State: New · Story points: none

**Description:**
As a TES Admin
I want that the client i created in TES should be syncronized to ARC as a Service agreement
So that i can have a one to one relation between the system

**Acceptance criteria:**
- Client should be syncronized if a ARC Organization is choosen when creating the client
- When the client is created, TES needs to generate a unique number to write in TSP
- Number needs to be unique and not already exist in TSP
- This unique number will then be "TSP Användarkod"

### 433196 [User Story] Update Client personal information
State: New · Story points: none

**Description:**
As a TES Admin
I need my clients personal information to be updated in ARC if updated in TES (and is actively syncronized to TSP)
So that i can ensure that my clients information is updated in both platforms

**Acceptance criteria:**
- Basic principles in the Client Syncronization is as follows:
- In TES there will be one Client.
- If the client is syncronized to ARC, TES will generate a unique number - called a TSP Användarkod
- The "Användarkod" will be the unique identifier between TES and ARC
- In ARC a client is called "Service Agreement" and one client can have several "Service Agremeents"
- A alarm code in TES equals one Service agreement in ARC. Meaning that multiple alarm codes = multiple service ageements
- Eventhough a Client has multiple Service Agreements, they will all share the TSP Användarkod
- When we update personal information in TES, the changes should be reflected to all service agreements
- No matter what changes we do, the common denominator is "TSP Användarkod"
- TES data syncronized to TSP, should always overwrite what is in TSP

### 433197 [User Story] Delete Client
State: New · Story points: none

**Description:**
As a TES Admin,
I need to be able to delete a client in TES and the changes should be reflected to ARC
So that i have the same information in both systems

**Acceptance criteria:**
- Basic principles in the Client Syncronization is as follows:
- In TES there will be one Client.
- If the client is syncronized to ARC, TES will generate a unique number - called a TSP Användarkod
- The "Användarkod" will be the unique identifier between TES and ARC
- In ARC a client is called "Service Agreement" and one client can have several "Service Agremeents"
- A alarm code in TES equals one Service agreement in ARC. Meaning that multiple alarm codes = multiple service ageements
- Eventhough a Client has multiple Service Agreements, they will all share the TSP Användarkod
- When we delete a client in TES, all service agreements sharing the TSP Användarkod should be removed
- The delete should be a "Soft Delete" in TES, and it should trigger a "Soft Delete" in TSP.

### 433225 [User Story] Update/Add Alarm Code on Client
State: New · Story points: none

**Description:**
As a TES Admin
I need to be able to add Alarm Codes to my client in TES and it should be syncronized to a current or new service agreement in TSP (and is actively syncronized to TSP)
So that i can ensure that my clients alarm codes is updated in both systems.

**Acceptance criteria:**
- Basic principles in the Client Syncronization is as follows:
- In TES there will be one Client.
- If the client is syncronized to ARC, TES will generate a unique number - called a TSP Användarkod
- The "Användarkod" will be the unique identifier between TES and ARC
- In ARC a client is called "Service Agreement" and one client can have several "Service Agremeents"
- A alarm code in TES equals one Service agreement in ARC. Meaning that multiple alarm codes = multiple service ageements
- Eventhough a Client has multiple Service Agreements, they will all share the TSP Användarkod
- When we add a new alarm code to a client in TES, we need to create a new Service Agreement in TSP
- No matter what changes we do, the common denominator is "TSP Användarkod"
- TES data syncronized to TSP, should always overwrite what is in TSP

### 434072 [UX Story] New TES web | Edit Client personal information
State: Active · Story points: none

**Description:**
We need a new edit page when editing a Clients personal information.

To reach the Edit Clients personal information go to TES:

- Click on "Kontrollpanelen"
- Click on "Sök Brukare"
- Search for a random Brukare
- Click on "Redigera"

Direct link to a brukare:
https://dmzfinal.tdsmachines.com/person.aspx?personid=a62e45b4-488c-4c22-8ac7-aec300c0851c

### 434540 [User Story] Update Närstående/Sammanboende
State: New · Story points: none

**Description:**
AS a TES Admin,
I need to make sure that Updates to "Närstående" and "Sammanboende" is syncronized to ARC.
So that TSP is up to date with this information

