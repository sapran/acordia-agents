## MODIFIED Requirements

### Requirement: `credential-harvest-triage` skill exists

The library SHALL contain a skill `acordia-analysts/skills/credential-harvest-triage/SKILL.md` providing (a) a classification schema for credential findings (ownership, type, subtype, status, scope, source, reuse potential, priority, asset, asset-class, mission-relevance, and credential-hypothesis), (b) an Aleph triage procedure that first validates a lead-supplied orientation packet, then inventories the selected material, reconciles it to the packet's asset classes, performs a bucket partition assigning material to a leg-owned bucket, scans, classifies, correlates, performs a residual sweep, prioritises and reports, (c) a raw-archive branch that begins with the existing artefact inventory and uses an orientation packet when supplied, (d) a pointer to a co-located pattern-library reference file for common credential material, and (e) a pointer to a co-located report-layout reference file fixing the shape of the HTML sweep product. The skill SHALL stop Aleph credential prioritisation and return an orientation gap when the packet is missing or incomplete.

The bucket partition step SHALL enumerate five buckets and their target legs:

- Bucket A — identity / directory / cloud-controlplane material → `terrain-analyst`
- Bucket B — host-forensic material (memory, SAM, DPAPI, keychain, shadow) → whichever leg holds the host under analysis
- Bucket C — web / API auth material → `terrain-analyst`
- Bucket D — log-artefact material → `overwatch-analyst`
- Bucket E — implant / payload RE material → cross-cutting via `implant-payload-re`, reported to `cyber-analyst`, which holds the fused picture itself

Each bucket's slice SHALL be dispatched with only that slice. The procedure SHALL state that per-leg classifications feed back into `multi-source-fusion` for cross-leg correlation. Targeted findings SHALL be associated with the asset register and mission threads. A residual sweep SHALL cover unexplained endpoints, unknown system classes, and credential forms absent from the orientation packet, and shall report whether a second targeted pass is required. P0–P3 priority SHALL account for scope, reuse potential, freshness, confidence, asset criticality and mission relevance, with ease of use as the tie-breaker.

#### Scenario: Triage skill loads in a harness

- **WHEN** a harness loads the analyst pillar
- **THEN** `credential-harvest-triage` is discovered from `acordia-analysts/skills/` and is invokable

#### Scenario: Body carries schema, procedure, and pattern library

- **WHEN** the triage skill is inspected
- **THEN** it contains an orientation-packet input contract, a classification schema, a bucket-partition step, a numbered targeted-and-residual triage procedure downstream of packet validation, a pointer to the pattern library at `references/credential-patterns.md`, and a pointer to the report layout at `references/report-layout.md`

#### Scenario: Bucket partition maps to existing legs

- **WHEN** the bucket-partition step is read
- **THEN** every bucket routes to one of `terrain-analyst`, `overwatch-analyst`, `cyber-analyst`, or the cross-cutting `implant-payload-re` skill, and no bucket routes to a leg not on the current whitelist

#### Scenario: No bucket names a retired leg

- **WHEN** the bucket-partition step is searched for `target-analyst` or `fusion-analyst`
- **THEN** neither is found, because neither agent exists

#### Scenario: Not a grid row

- **WHEN** the competency grid in `docs/roles/operational-analyst.md` is inspected
- **THEN** no row corresponds to `credential-harvest-triage`

#### Scenario: Schema carries ownership

- **WHEN** the triage skill's classification schema is inspected
- **THEN** `ownership` is one of its fields

#### Scenario: Schema carries asset context

- **WHEN** the triage skill's classification schema is inspected
- **THEN** `asset`, `asset-class`, `mission-relevance`, and `credential-hypothesis` are fields, and ownership is settled before the other handling decisions

#### Scenario: Missing Aleph orientation stops prioritisation

- **WHEN** an Aleph-backed triage run has no complete orientation packet
- **THEN** it reports the missing packet fields and coverage impact and does not launch generic credential prioritisation

#### Scenario: Targeted work precedes residual work

- **WHEN** an orientation packet is complete
- **THEN** triage scans the selected asset-specific slices before running the residual sweep, associates residual discoveries with orientation gaps, and reports whether another targeted pass is required

#### Scenario: The report layout fixes presentation without widening disclosure

- **WHEN** `references/report-layout.md` is read
- **THEN** it organises the product by the system each credential opens, requires every credential value to sit inside a collapsed disclosure element rather than in a heading, dateline, banner, field cell, tag or summary, requires that disclosure element to be written only where ownership permits the value into the product so that an ownership-refused finding is a credential block with no disclosure element at all, requires every credential block to carry an `Ownership` row, requires an evidence link to carry the whole identifier with only the displayed text shortened, and states that it decides presentation only while `SKILL.md`'s guardrails decide what may be disclosed

### Requirement: `analyst-loop` skill exists

The library SHALL contain a skill `acordia-analysts/skills/analyst-loop/SKILL.md` naming the end-neutral analytic loop — mission-read (through `mission-analyst`), terrain-read (through `terrain-analyst`), defender-read (through `overwatch-analyst`), take-read (through `collection-analyst`), judgement (calibrated, via spine skills), next-move — as a first-class procedural cross-cutting skill.

For directed credential collection, the loop SHALL additionally require a collection-planning preflight before credential scoping: refresh carried operational memory, obtain technical terrain orientation for the scoped Aleph collection, obtain mission/value assessment for discovered assets, build an asset-and-credential hypothesis register, and only then enter credential triage and targeted extraction. A residual sweep SHALL follow targeted extraction and feed unexplained systems back into the asset register. This preflight SHALL gate credential planning without becoming a seventh universal leg read or replacing the six-step end-neutral loop.

The loop SHALL carry no delegated fusion step. The fused picture is held by `cyber-analyst` itself, so the four leg reads converge in the orchestrator's own hands rather than in a leg's, and no step of the loop SHALL name a leg that fuses on the orchestrator's behalf.

Because the distribution ships no executing agent, the loop's judgement step SHALL rest on evidence reported by the four legs and by the human operator the product is handed to, and its next-move step SHALL name a move for that person rather than a dispatch the pillar performs itself.

The skill body SHALL contain: (a) a cross-cutting notice declaring the skill procedural and non-grid; (b) a loop-shape section naming the six steps and the collection-planning preflight; (c) a loop-invariants section stating end-neutrality (every pass reaches a judgement plus a next move), gap-naming on every judgement, calibrated confidence on every judgement, passive posture, and the orientation gate for directed credential collection; (d) a where-this-runs paragraph stating the loop is the orchestrator's workflow, and that a leg session matching this skill surfaces the need for a full pass back to the orchestrator rather than attempting the loop itself.

The skill's `description` SHALL be authored for trigger quality — stating WHEN to run the loop, not WHAT it is — so description-match selection fires cleanly on operator sessions asking for a fresh analytic round.

The skill SHALL declare its cross-cutting/procedural nature and SHALL NOT be added as a row to the competency grid. The `## Method` contract for evidence-reading skills (from `analyst-verifiability-anchors`) SHALL NOT apply — this skill reads no files.

#### Scenario: Loop skill loads in a harness

- **WHEN** a harness loads the analyst pillar
- **THEN** `analyst-loop` is discovered from `acordia-analysts/skills/` and is invokable

#### Scenario: Body carries the four required sections

- **WHEN** the loop skill is inspected
- **THEN** it contains a cross-cutting notice, a loop-shape section naming six steps and the collection-planning preflight, a loop-invariants section, and a where-this-runs paragraph

#### Scenario: The loop routes through the four legs and fuses nowhere

- **WHEN** the loop-shape section is read
- **THEN** it names mission-read, terrain-read, defender-read, take-read, judgement and next-move, routes the first four through `mission-analyst`, `terrain-analyst`, `overwatch-analyst` and `collection-analyst`, and names no leg holding the fused picture

#### Scenario: Judgement rests on reported evidence

- **WHEN** the judgement and next-move steps are read
- **THEN** the judgement is drawn from evidence the legs and the human operator report, and the next move is one that operator makes, because no agent in the distribution acts on a target

#### Scenario: Trigger-quality description

- **WHEN** an operator session asks for a fresh end-neutral analytic pass
- **THEN** `analyst-loop`'s `description` is specific enough for the harness to select it

#### Scenario: Not a grid row

- **WHEN** the competency grid in `docs/roles/operational-analyst.md` is inspected
- **THEN** no row corresponds to `analyst-loop`

#### Scenario: Orchestrator references the skill; legs do not

- **WHEN** `acordia-analysts/agents/cyber-analyst.md` is inspected
- **THEN** it names `analyst-loop` in one sentence within its existing loop-describing paragraph

#### Scenario: Legs do not reference the loop skill

- **WHEN** any leg agent (`mission-analyst`, `terrain-analyst`, `overwatch-analyst`, `collection-analyst`) is inspected
- **THEN** it does not name `analyst-loop`

## ADDED Requirements
### Requirement: Credential pattern reference carries asset fingerprints

The credential pattern reference at `acordia-analysts/skills/credential-harvest-triage/references/credential-patterns.md` SHALL retain its existing credential-value pattern sections and add a separate non-secret `## Asset fingerprints used to steer searches` section. The section SHALL cover MinIO/S3-compatible storage, databases, SMB/NFS, Kubernetes/container systems, CI/CD, VPN/remote access, identity systems and SSH. Asset fingerprints SHALL steer selection of targeted searches only; they SHALL NOT be treated as credential values or as permission to validate access.

#### Scenario: Asset fingerprints are present without replacing credential patterns

- **WHEN** the pattern reference is inspected
- **THEN** the existing API-key, auth-material, hash, connection-string, private-key, cloud-service-account and Kubernetes/secret-file sections remain present and the asset-fingerprint section is also present

#### Scenario: Fingerprints are non-secret selectors

- **WHEN** an asset fingerprint is used in triage
- **THEN** it identifies a system class or search context and does not trigger credential validation or live provider contact
