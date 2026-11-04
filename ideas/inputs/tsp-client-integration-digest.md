# Digest: Feature 431577, TSP Client Integration

Source: ADO IHCP, fetched 4 Nov 2026 via `az boards` (feature, 10 children and parent epic, plus comments on 2 stories). Personal names are omitted.
Repos: `ihcp` (main, about 344 MB, branch `main`), `tes` (about 1 GB, branch `develop`).

## Status
- Feature state **Implementing** (created 17 Sep 2026). Parent epic 434390 "ADDA IL | Funnel" is still just the empty template.
- Children: 7 user stories, all **New** with **no story points**. There are 2 UX stories: "Ny brukare" (Closed) and "Edit client" (Resolved).
- So UX is done but the backend stories haven't started, which makes this a **live case**: refinement and decisions are still ahead.

## What the feature says
- MVP: sync TES **Client** (= "Brukare", "Care recipient", "Service user") to TSP **Service Agreement**, to remove duplicate data entry, with TSP as a backend only.
- Scope: set up integration (433193), fetch organisations from TSP (433194), create (433195), update personal info (433196), add/update alarm code (433225), delete (433197), and relatives/co-residents (434540).
- Out of scope: client creation other than "Skapa ny brukare".
- Key model: TES generates a unique **"TSP Användarkod"** shared by all of a client's service agreements. 1 alarm code = 1 service agreement.
- Dependencies: "**Potential** dependency to TSP and DM90" (undecided).

## Open questions already raised by humans (ground truth for the live test)
- (19 Oct, 433196) What about a Navigil watch with **no service agreement**? Can updates reach TSP then?
- (19 Oct, 433225) How do we add/update alarms in the **new TES web**? Should **all** alarm codes go to TSP? Does deleting an alarm code belong here? TSP **soft-deletes** service agreements but TES has no such concept.
- (2 Nov, 433196) Is "Medicinsk information" sustainable from a **legal, audit and GDPR** point of view? Could we reuse "Viktig information"?

## Gaps visible in the text (facilitator's first read, not yet verified)
- No error handling, retry or offline behaviour when TSP is down. Sync direction and conflicts (edits made directly in TSP?) aren't mentioned.
- Uniqueness of Användarkod: who guarantees it, and is there a race between TES and TSP?
- Migrating existing clients (customers who already use both systems) isn't mentioned.
- Auth/credentials appear only as "endpoint information".
- Organisation sync: a manual and an automatic trigger, but no frequency, and no rule for what happens to clients when an organisation is "flagged".

## Data quality caveat
The Azure CLI output was decoded as cp1252, so Swedish characters show as `�` in story text (for example "Anv�ndarkod"). Fix it before building (set UTF-8 output), or the tool's input will be degraded.
