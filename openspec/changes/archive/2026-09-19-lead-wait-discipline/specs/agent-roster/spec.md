## MODIFIED Requirements

### Requirement: Directed credential collection requires orientation first

Before `cyber-analyst` issues a directed credential-sweep brief for an Aleph-backed collection, it SHALL obtain and read a current orientation return covering carried operational knowledge and technical terrain. It SHALL then obtain or derive the mission/value read for the discovered assets, fuse those reads itself, and include the resulting asset-and-credential hypothesis register in the credential brief. Credential extraction SHALL NOT be the first substantive search when this orientation is available and relevant.

Across shipped runtime doctrine the packet SHALL be enumerated once, in `credential-harvest-triage`. The orchestrator prompt SHALL name that skill rather than restate the packet's contents. This spec remains the packet's normative contract.

#### Scenario: Lead dispatches orientation before credential work

- **WHEN** a directed credential sweep is requested against an Aleph-backed collection
- **THEN** `cyber-analyst` dispatches Collection and Terrain orientation work before issuing credential-sweep instructions, and reads their notes before credential prioritisation

#### Scenario: Orientation packet reaches the credential brief

- **WHEN** the lead has read the orientation returns
- **THEN** the credential brief carries scoped collections, corpus state, asset/system classes, non-secret fingerprints, evidence and provenance, observed/inferred status, freshness, confidence, mission relevance, expected credential forms, planned specialist owners, named mission/value gaps, exposure, and omissions

#### Scenario: Runtime doctrine enumerates the packet once

- **WHEN** the orchestrator prompt and `credential-harvest-triage` are read together
- **THEN** the packet is enumerated in the skill, and the orchestrator names the skill rather than restating its contents

#### Scenario: Incomplete orientation blocks prioritisation

- **WHEN** the Aleph orientation return is missing or lacks the fields required for credential scoping
- **THEN** the lead reports the missing fields and requests bounded orientation work rather than presenting generic credential priorities as a completed plan

## ADDED Requirements

### Requirement: The orchestrator works while its legs run and joins before it ends

`cyber-analyst` SHALL treat waiting on a dispatched leg as the residual case rather than its default posture. Before re-entering a wait, its prompt SHALL direct it to perform the analysis available to it without a pending return — verifying returns already in hand, establishing the size and shape of the corpus, naming the gaps its legs are not covering, and revising the operating picture — and SHALL name `maintaining-operating-picture` as the skill that owns that work. Waiting SHALL be what the orchestrator does when no such work remains.

`cyber-analyst` SHALL NOT end a session while a leg it dispatched is still running. Its prompt SHALL direct it either to collect that leg's return, or to cancel the leg explicitly and record in its product what the cancellation gave up. A leg's work ending without either SHALL be treated as a loss rather than a completion.

Every specialist assignment `cyber-analyst` issues SHALL name the agent it is for. The prompt SHALL state this as a positive property of an assignment rather than as a prohibition on omission, because an assignment that names no agent is served by a general-purpose worker without an analyst's doctrine and reports no error.

This requirement governs the interval after dispatch and the boundary at session end. It does not restate `Orchestrator fan-out follows real dependencies`, which governs which questions are dispatched and when.

#### Scenario: Waiting is named as the residual case

- **WHEN** `cyber-analyst`'s prompt is read
- **THEN** it directs the orchestrator to do the analysis available without a pending return before re-entering a wait, and names `maintaining-operating-picture` as the skill owning that work

#### Scenario: A leg still running blocks session end

- **WHEN** the orchestrator is about to end a session and a dispatched leg has not returned
- **THEN** its prompt directs it to collect the return or to cancel the leg explicitly

#### Scenario: A cancelled leg's loss is recorded

- **WHEN** the orchestrator cancels a leg before that leg returns
- **THEN** its prompt directs it to record in its product what the cancellation gave up

#### Scenario: Every assignment names its agent

- **WHEN** the orchestrator issues a specialist assignment
- **THEN** its prompt states that an assignment names the agent it is for, as a property the orchestrator checks before sending rather than as a prohibition on omitting a field

#### Scenario: The doctrine reaches every surface carrying the orchestrator body

- **WHEN** the orchestrator body is read from the agent file or from either lead command wrapper
- **THEN** all three carry this doctrine byte-identically
