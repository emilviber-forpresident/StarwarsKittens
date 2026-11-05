# Pre-Flight: 431577 TSP Client Integration
Prompt v0.2 · Code check: done (repos/ihcp, repos/tes) · Readiness: 1 (shaped: all child stories are `New` with no estimates, #434540 has no AC, and the stories contradict the sync design already decided in `ihcp/features/tsp-data-integration`)

## Top 3 before anything else
1. S-01: TES→ArcGateway sync **cannot authenticate today** (Keycloak `ihcp_arg` scope descoped). Nothing in this feature can be demoed end to end until someone owns that.
2. D-05: the new IHCP.Tes has **no** create/update/delete client or alarm commands, and TES Web has no client pages. The sync design also assumes TSP tenants stop using legacy writers. All of this is in this feature's scope and is not in any story.
3. D-02: how the "TSP Användarkod" is generated and kept unique. The DB column is nullable and not unique, and uniqueness "in TSP" can only be checked asynchronously through ArcGateway.

## Agenda (15 min)
Time budget: DECIDE 10 min · SPIKE 2 min (confirm owner + timebox only) · ASK THE PO 3 min (PO collects answers async where possible).

### DECIDE
| ID | Decision needed | Options | Evidence | Owner | Conf. | Min |
|---|---|---|---|---|---|---|
| D-05 | Which write path do TSP-enabled tenants use for clients, and what happens to legacy writers? | A: build new IHCP.Tes commands + TES Web pages, and block or hide legacy person/alarm editing for TSP tenants / B: also hook the legacy WebForms `person.aspx` save | Feature "Skapa ny brukare"; #432680/#434072 new UI; `ihcp/features/tsp-data-integration/SPEC.md:6` "legacy TES writers… are not detected"; only `RequestCareRecipientReconcileCommand` exists (`IHCP.Tes.Application/MasterDataSync/Commands/RequestCareRecipientReconcileCommand.cs:9`) | Architect | high | 2 |
| D-02 | Who generates the TSP Användarkod, in what format, and how is "not already in TSP" enforced? | A: TES generates from a tenant sequence, a filtered unique index in DB, ArcGateway rejects on TSP collision / B: ArcGateway allocates and reserves the code, TES stores the result | #433195 "Number needs to be unique and not already exist in TSP"; `tes/.../Tables/tes_Person.sql:29,62` `VARCHAR(30) NULL`, non-unique index; DTO allows 64 (`IHCP.Api.Dto/ArcGateway/CareRecipientState.cs:14`); TSP has no tenant model (`S8-DISCUSSION.md:330`) | Architect | high | 2 |
| D-01 | What makes a client "synced": an explicit "Sync to TSP" choice, or derived eligibility? | A: explicit per-client flag (new column) / B: derived: TSP-org department + TSP code + ≥1 active alarm (current code) | Feature "select 'Sync to TSP' and then… a TSP organization"; #433195 Gherkin "When an Alarm Code is added… created in TSP"; `IHCP.Tes.Application/MasterDataSync/DesiredState.cs:75-88`; D9 "Preliminary… confirm with product" (`S8-DISCUSSION.md:28`) | Architect | high | 1 |
| D-03 | Where TSP organisations live in TES | A: separate read-only tree/table (#433194 wording) / B: TES departments with TSP scope id in `MappingKey` (decided D6/D12), plus guards | #433194 "Store in a New Organizational Tree, with read only"; `S8-DISCUSSION.md:25,30,409-412`; `MappingKeyUpdateEventHandler.cs:67` `Guid.Parse` on any `MappingKey` breaks on non-GUID scope ids | Architect | high | 1 |
| D-04 | What "delete client" means in TES and TSP | A: terminate (`TerminationDate`) → person `DELETE` → ARC `Avveckla` + stock deallocation / B: new soft-delete flag on the client | #433197 "Soft Delete… trigger a Soft Delete in TSP"; `SPEC.md:60-65`; legacy delete is hard (`tes/.../Api/Services/PersonService.cs:107`), and `DeleteTerminatedPersonsJob` culls terminated persons (`S8-DISCUSSION.md:271`); removal semantics belong to this feature (D29, `S8-DISCUSSION.md:47`) | Architect | high | 1 |
| D-06 | Which feature extends the desired-state contract with personal info, address, medical info and contacts? Where is the schema change made? | A: this feature extends `CareRecipientState` + ArcGateway mapping / B: tsp-data-integration Phase 4 does it, this feature only adds TES fields | #433196 "add 'Medicinsk Information'… free text"; DTO carries only `TspCode`, `PerformerScopeId` (`CareRecipientState.cs:15,22`); gap list `S8-DISCUSSION.md:370-375`; TES schema owner is TES_DbUp (D5/D25, `S8-DISCUSSION.md:24,43`); no medical field in IHCP.Tes (inferred: no `Medic*` hits outside audit entities) | Architect | high | 1 |
| D-07 | What does "set up integration / endpoint information" in Control Panel actually configure? | A: TES admin only toggles the per-tenant switch; TSP endpoint/credentials/root scope are set up by ops in ArcGateway / B: build a tenant onboarding API in ArcGateway that the TES admin UI writes to (secret handling needed) | #433193 "In Control Panel/settings… Endpoint information"; switch `TspMasterDataSyncEnabled` (`IHCP.Tes.Infrastructure/MasterDataSync/MasterDataSyncRepository.cs:10`, D23); ArcGateway `Tenants` has no root scope/credential, and there is no onboarding API (`_bmad-output/implementation-artifacts/deferred-work.md:105-110`) | Architect | high | 1 |
| D-08 | How the admin sees sync result and errors after save (pending/error/registered) | A: TES Web pulls `sync-status` on demand (D27) / B: push (MQTT/SSE/SignalR, deferred to this feature) | No story covers sync status UI; `S8-DISCUSSION.md:45` (D27); `deferred-work.md:172`; `SPEC.md:13` "User sees pending/error/registered state" | Dev | medium | 1 |

### SPIKE
| ID | Question the spike answers | Evidence | Owner | Timebox | Conf. |
|---|---|---|---|---|---|
| S-01 | Who provisions the Keycloak `ihcp_arg` scope in target environments, and when? Until then TES tokens get `invalid_scope` and sync cannot run | D26 "TES-to-ArcGateway sync therefore cannot authenticate" (`S8-DISCUSSION.md:44`); `deferred-work.md:275` | Architect | 0.5 day | high |
| S-02 | Can TSP notify scope create/update/delete, or must ArcGateway poll `GET /public/api/scopes`? Are scope ids stable, and how is the tenant root scope found? | #433194 "trigged automatically"; `SPEC.md:169`; root scope must start with `TES` (`S8-DISCUSSION.md:453-455`); no scope code in `IHCP.ArcGateway/src` (search returned nothing) | Dev | 2 days | medium |
| S-03 | Referral/assessment needs a referrer (TES staff name, phone, email, DOB) and `AssessedById` from a TSP user's email. What does TES send for these? | `S8-DISCUSSION.md:336,348` (enabler scripts) | Dev | 1 day | medium |
| S-04 | Where do the contact and cohabitant sync rules (#434540) come from? They exist in neither legacy code nor the enabler scripts | #434540 (no AC); Q6/D28 provisional (`S8-DISCUSSION.md:46,357-363`); legacy terminate hard-deletes cohabitant links (`S8-DISCUSSION.md:268`) | Dev | 1 day | medium |

### ASK THE PO
| ID | Question | Evidence | Why it matters | Conf. |
|---|---|---|---|---|
| P-01 | For TSP-enabled tenants, are integration-fed persons (e.g. Treserva) and legacy edits allowed? If yes, should they sync? | Out of scope "Any client creation except 'Skapa ny brukare'"; `SavePersonCommand` overwrites/clears TSPCode (`S8-DISCUSSION.md:273`); `SPEC.md:6` | Undetected writes leave TSP silently out of date, and a nulled TSP code breaks the link | high |
| P-02 | A TSP org with clients is removed and "flagged": does sync for its clients stop, continue, or need a move? Is an empty removed org deleted? | #433194 "flag the Organization… And not remove it" | Updates go to a scope that no longer exists; the user sees errors with no remedy | high |
| P-03 | What happens in TSP when a client stops being eligible (moved to a non-TSP org, sync unticked, last alarm code removed)? | Removal semantics owned here (D29, `S8-DISCUSSION.md:47`); no story covers it | Without an answer: orphaned active agreements in TSP, or accidental terminations | high |
| P-04 | #433225 has no criteria for changing or removing an alarm code, and its Gherkin is a copy of #433195's. Removed alarm code = terminate that agreement? | #433225 Gherkin identical to #433195; `SPEC.md:116` alarm `DELETE` terminates | It can't be tested, and stock deallocation is irreversible in TSP | high |
| P-05 | "Audit logs for add/update/delete client": in TES (which log), in ArcGateway operations, or both? Who reads them, and for how long? | #433197 "We need audit logs…"; `sys_ObjectLog` is incomplete (`S8-DISCUSSION.md:298`); ArcGateway already audits operations (`SPEC.md:211`) | Otherwise the work is unsized and duplicated, and medical/PII retention is unclear | medium |
| P-06 | "Medicinsk information": which TSP field does it map to, who may see it, and can it go in logs? | #433196; SPEC redacts medical notes (`SPEC.md:160,207`) | Privacy classification and the TSP mapping block D-06 | medium |
| P-07 | "TES always overwrites TSP": are ARC operators' edits on agreements expected to be lost? Are pre-existing TSP agreements adopted? | #433196/#433225 "should always overwrite"; adoption `SPEC.md:49` | Operators lose data without warning; duplicate agreements | medium |
| P-08 | Which TES role may enable the integration and sync clients? What is the "potential dependency to TSP and DM90"? | #433193 "adequate permissions"; feature Dependencies "Potential dependency to TSP and DM90" | Without these the negative Gherkin can't be tested, and the dependency can't be planned | medium |

## Already answered by the code
| ID | Question | Answer | file:line |
|---|---|---|---|
| A-01 | Does a client update hit one or all service agreements? | All active agreements of the care recipient under the tenant scope (D15). This matches #433196 | `ihcp/features/tsp-data-integration/SPEC.md:50`; `S8-DISCUSSION.md:33` |
| A-02 | Does a save wait for TSP? | No. A domain event writes to the transactional outbox and a worker submits later, so the save never depends on ArcGateway | `SPEC.md:14,231`; `IHCP.Tes.Infrastructure/MasterDataSync/MasterDataSyncOutboxWorker.cs` |
| A-03 | Is there a per-tenant on/off switch? | Yes: global flag `TspMasterDataSync` plus `sys_Parameter` `TspMasterDataSyncEnabled` (default off) | `IHCP.Tes.Application/FeatureFlags.cs:11`; `MasterDataSyncRepository.cs:10` |
| A-04 | Which TSP org does a client belong to? | Its one active department; the scope comes from that department's `MappingKey`. The alarm's department does not override it (D8) | `DesiredState.cs:29`; `S8-DISCUSSION.md:27` |
| A-05 | Alarm code ↔ service agreement, and existing agreements in TSP? | One active alarm = one agreement. An existing `Tspcode + AlarmCode` agreement is adopted, not duplicated | `SPEC.md:49,92` (FR-4) |
| A-06 | Bursts of edits and concurrent admins? | `sourceVersion` ordering, supersede of pending work, one operation in flight per care recipient | `SPEC.md:34-36,103` (FR-16) |
| A-07 | Can an alarm code move between clients? | No. A move = end the old alarm and create a new one (D24). New alarm commands must not change `PersonGuid` | `S8-DISCUSSION.md:42` |

## Code map (only if the code check was done)
| Component / file | What changes or why it matters | Agenda IDs |
|---|---|---|
| `ihcp/IHCP/IHCP.Tes/src/IHCP.Tes.Application` (new client/alarm commands + domain events → outbox) | Nothing exists yet; these must raise the reconcile events | D-05, D-04, A-07 |
| `IHCP.Tes.Application/MasterDataSync/DesiredState.cs`, `CareRecipientReconciler.cs` | Eligibility rule and what is sent | D-01, P-03 |
| `ihcp/IHCP/IHCP.Api/.../IHCP.Api.Dto/ArcGateway/CareRecipientState.cs` (generated; change source contract) | Holds only TSP code + scope; personal/medical fields missing | D-06, P-06 |
| `ihcp/IHCP/IHCP.ArcGateway/src` | Scope import, tenant root scope/credentials, TSP code collision check, terminate workflow | S-02, D-07, D-02, D-04 |
| `IHCP.Tes.Application/Departments/DomainEvents/MappingKeyUpdateEventHandler.cs:67` | `Guid.Parse` on `MappingKey` breaks with TSP scope ids | D-03 |
| `tes/Server/Database/TESDatabaseProject` (`tes_Person.sql`, `TES_DbUp`) | TSPCode width/uniqueness, medical info column, any sync flag / org flag columns | D-02, D-06, D-01 |
| `ihcp/IHCP/IHCP.TesWeb/apps/web` | No client pages yet; new Ny brukare/edit pages, org picker, sync status | D-05, D-08 |
| `tes/Client/TES_Web/TESWeb/person.aspx`, `person.SaveClickFunctionality.cs:279-281` | Legacy manual TSP code entry + only uniqueness check; still a write path | D-05, D-02 |
| `tes/Client/TES_Web/TESWeb/Api/Services/PersonService.cs:107,261` + `DeleteTerminatedPersonsJob` | Hard delete / culling bypasses sync | D-04 |
| `IHCP.Tes.Infrastructure/MasterDataSync/MasterDataSyncRepository.cs:10` | Per-tenant enable switch the Control Panel would set | D-07, A-03 |
| Keycloak Configurator / realm `ihcp_arg` scope | Blocks all TES→ArcGateway calls | S-01 |
| `tes/Common/TES2DataObjects/TESIntegration/Commands/Persons/SavePersonCommand.cs` | Integrations overwrite/clear TSPCode | P-01 |

## Parked
- Tester: #433225 and #433195 share the same Gherkin; rewrite once P-04 is answered (#433225 Gherkin)
- Architect: ArcGateway lease expiry can let an older write land after a newer one (`deferred-work.md:231`)
- Architect: children already applied in TSP are not removed by a person `DELETE` until MS7/MS8 (`deferred-work.md:294`)
- Dev: legacy `p_PersonTerminate` leaves alarm codes open, so "active alarm" after termination depends on `TerminationDate` (`S8-DISCUSSION.md:270,315`)
- Architect: `MappingKey` is also used by legacy personnel-role import; a Swedish tenant using it conflicts with TSP scope ids (`S8-DISCUSSION.md:406`)
- Dev: legacy TSP client secret in plain text in the enabler scripts; consider rotation (`S8-DISCUSSION.md:365`)
- Dev: Aspire acceptance DB has no outbox table (built from EF, not DbUp); needed once acceptance tests cover client stories (`S8-DISCUSSION.md:43`)
- Architect: ArcGateway must protect TSP from load on initial bulk sync when a tenant is enabled (`SPEC.md:102,209`, inferred bulk case)
- UX: #432680 is Closed and #434072 Resolved, but neither mentions TSP org picker or "Sync to TSP" (#432680, #434072)
- PO: Feature success criteria mention "Fetch Organizations" but no story owns the TES admin UI for listing/triggering org sync (#433194, inferred)

## Not checked
- TSP/ARC API itself (scope change notification, code collision search, field for medical info): not in `repos/`.
- DM90: not in `repos/`; dependency unclear.
- Keycloak realm/Configurator provisioning for `ihcp_arg`: only referenced in docs, not verified in code.
- `IHCP.TesWeb` was searched by keyword only; no full route review.
- Many answers come from design docs in `ihcp/features/tsp-data-integration` (sibling feature, decisions dated 2026-10-29 to 2026-11-02), not from running code. Confirm they still hold.
- Name mapping assumed: "Client/Brukare" = `TesPerson`/`tes_Person`; "ARC/TSP Organization" = TSP scope = `TesDepartment.MappingKey`; "Control Panel" = Kontrollpanelen (legacy or new TES Web, unclear); "TSP Användarkod" = `tes_Person.TSPCode` (inferred).
