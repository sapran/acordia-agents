## ADDED Requirements

### Requirement: Directed credential collection requires orientation first

Before `cyber-analyst` issues a directed credential-sweep brief for an Aleph-backed collection, it SHALL obtain and read a current orientation return covering carried operational knowledge and technical terrain. It SHALL then obtain or derive the mission/value read for the discovered assets, fuse those reads itself, and include the resulting asset-and-credential hypothesis register in the credential brief. Credential extraction SHALL NOT be the first substantive search when this orientation is available and relevant.

#### Scenario: Lead dispatches orientation before credential work

- **WHEN** a directed credential sweep is requested against an Aleph-backed collection
- **THEN** `cyber-analyst` dispatches Collection and Terrain orientation work before issuing credential-sweep instructions, and reads their notes before credential prioritisation

#### Scenario: Orientation packet reaches the credential brief

- **WHEN** the lead has read the orientation returns
- **THEN** the credential brief carries scoped collections, asset/system classes, evidence and provenance, freshness, confidence, mission relevance, expected credential forms, planned specialist owners, and named gaps

#### Scenario: Incomplete orientation blocks prioritisation

- **WHEN** the Aleph orientation return is missing or lacks the fields required for credential scoping
- **THEN** the lead reports the missing fields and requests bounded orientation work rather than presenting generic credential priorities as a completed plan

### Requirement: Orientation returns are role-specific

For an orientation-first credential sweep, `collection-analyst` SHALL return carried-memory and Aleph-corpus state; `terrain-analyst` SHALL return a non-secret technical asset register; and `mission-analyst` SHALL return asset-to-mission and crown-jewel valuation. The orchestrator SHALL fuse these returns; no leg SHALL claim the fused operating picture.

#### Scenario: Collection returns prior knowledge and corpus shape

- **WHEN** Collection performs the pre-credential orientation
- **THEN** its notes identify prior assets, aliases, searches, rejected hypotheses, stale or contradictory facts, collection provenance, freshness, coverage limits, and the explicit no-memory state when no prior notes exist

#### Scenario: Terrain returns asset hypotheses before extraction

- **WHEN** Terrain performs the pre-credential orientation
- **THEN** its notes identify observed or inferred system classes and non-secret fingerprints, attach Aleph provenance and entity ids, state freshness and confidence, list likely credential forms, and distinguish asset clues from credential findings

#### Scenario: Mission returns value before ranking

- **WHEN** Mission receives the technical asset register
- **THEN** its return maps assets to mission threads, organisational processes or crown jewels and states the value, uncertainty and information that would change the ranking
