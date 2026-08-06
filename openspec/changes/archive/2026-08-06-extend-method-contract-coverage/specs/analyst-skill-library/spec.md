## MODIFIED Requirements

### Requirement: Method contract for evidence-reading skills

Skills whose `Objective` involves reading collected material (files, memory dumps, logs, packet captures, configuration archives) SHALL structure their `## Method` section as four ordered elements: (a) an **inventory step** that names the tool used to enumerate the input (e.g. `find`, `glob`, `list`, or a file-typing tool); (b) a **bounded-context, exhaustive-coverage discipline** — reads into the analyst's context stay scoped (offset, line-range, or a targeted tool hit) and never wholesale-load a multi-megabyte artefact into context, **and** the input SHALL be covered in full by a prior tool pass (a script, `grep`/`rg`, or a parser processing 100% of the bytes or records) that drives which scoped regions are read; a finding or conclusion SHALL NOT rest on the opening portion of an artefact while the remainder goes unprocessed, and every located hit SHALL be processed, not only the first; (c) a **citation format** that anchors each observation to `<path>:<offset>` or `<path>@L<line>`; (d) a **degradation policy** stating what the analyst does when each optional external tool named in the body is unavailable.

The criterion above is normative and determines scope on its own. A skill meeting it SHALL carry the four elements whether or not it appears in any enumeration, because a closed list makes coverage depend on whether a name was remembered rather than on what the skill does. The following twenty-two skills currently meet the criterion: `analytic-tooling-scripting`, `assessing-take-value`, `c2-beacon-exfil-analysis`, `change-cycle-forecasting`, `cloud-controlplane-analysis`, `data-integration-tooling`, `disk-memory-forensics`, `effect-on-target-verification`, `endpoint-telemetry-edr`, `evasion-antianalysis`, `identity-directory-trust`, `implant-payload-re`, `log-artefact-interpretation`, `os-host-internals`, `ot-embedded`, `overwatch`, `own-footprint-analysis`, `packet-traffic-analysis`, `pattern-of-life-baselining`, `protocol-routing-architecture`, `vuln-attacksurface-mapping`, `web-api-authflow-analysis`. This enumeration records the present membership and SHALL be extended whenever a skill that reads collected material is added or an existing skill's Method begins to direct such reading; it SHALL NOT be read as narrowing the criterion. Analytic-spine skills (whose input is analyst reasoning, not collected material) SHALL NOT be subject to this requirement.

#### Scenario: Method starts with an inventory step

- **WHEN** an evidence-reading skill's `## Method` section is read
- **THEN** its first ordered element names the tool used to enumerate the input before any read happens

#### Scenario: Sampling is bounded, never wholesale

- **WHEN** an evidence-reading skill's `## Method` describes reading the input
- **THEN** the reading is scoped (offset, line-range, or targeted grep hit), and no step instructs a wholesale load of a multi-megabyte artefact

#### Scenario: Coverage is exhaustive, never a head sample

- **WHEN** an evidence-reading skill's `## Method` describes deriving a finding or conclusion from an artefact
- **THEN** the artefact is covered in full by a tool pass over 100% of its bytes or records, every located hit is processed, and no step derives a conclusion from the opening portion while the remainder is left unprocessed

#### Scenario: Findings cite a byte or line anchor

- **WHEN** an evidence-reading skill's `## Method` describes recording a finding
- **THEN** it specifies the citation shape as `<path>:<offset>` or `<path>@L<line>`

#### Scenario: Degradation policy per optional tool

- **WHEN** an evidence-reading skill names an optional external tool (e.g. `pypykatz`, `secretsdump.py`, `tshark`)
- **THEN** its `## Method` states what to do when that tool is unavailable — either a fallback path or an explicit "flag the gap and stop"

#### Scenario: Analytic-spine skills exempted

- **WHEN** an analytic-spine skill's `## Method` is inspected
- **THEN** it is not required to follow the four-element contract, because the skill has no file inventory step and no optional tools to degrade

#### Scenario: The criterion governs, not the enumeration

- **WHEN** a skill's `Objective` involves reading collected material but its name is absent from the enumeration
- **THEN** the requirement still binds it, and the omission is a defect in the enumeration rather than an exemption for the skill

#### Scenario: Every enumerated skill carries the elements

- **WHEN** each of the twenty-two enumerated skills is inspected
- **THEN** its `## Method` carries an inventory step, bounded-and-exhaustive reading language, a citation shape, and a degradation policy for each optional tool it names
