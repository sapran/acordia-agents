## ADDED Requirements

### Requirement: Method contract for evidence-reading skills

Skills whose `Objective` involves reading collected material (files, memory dumps, logs, packet captures, configuration archives) SHALL structure their `## Method` section as four ordered elements: (a) an **inventory step** that names the tool used to enumerate the input (e.g. `find`, `glob`, `list`, or a file-typing tool); (b) a **bounded sampling discipline** that prohibits wholesale reads of large inputs; (c) a **citation format** that anchors each observation to `<path>:<offset>` or `<path>@L<line>`; (d) a **degradation policy** stating what the analyst does when each optional external tool named in the body is unavailable.

The requirement applies to the following fifteen skills only: `disk-memory-forensics`, `log-artefact-interpretation`, `cloud-controlplane-analysis`, `web-api-authflow-analysis`, `os-host-internals`, `implant-payload-re`, `identity-directory-trust`, `packet-traffic-analysis`, `endpoint-telemetry-edr`, `c2-beacon-exfil-analysis`, `protocol-routing-architecture`, `own-footprint-analysis`, `evasion-antianalysis`, `pattern-of-life-baselining`, `vuln-attacksurface-mapping`. Analytic-spine skills (whose input is analyst reasoning, not collected material) SHALL NOT be subject to this requirement.

#### Scenario: Method starts with an inventory step

- **WHEN** an evidence-reading skill's `## Method` section is read
- **THEN** its first ordered element names the tool used to enumerate the input before any sampling happens

#### Scenario: Sampling is bounded, never wholesale

- **WHEN** an evidence-reading skill's `## Method` describes reading the input
- **THEN** the reading is scoped (offset, line-range, or targeted grep hit), and no step instructs a wholesale load of a multi-megabyte artefact

#### Scenario: Findings cite a byte or line anchor

- **WHEN** an evidence-reading skill's `## Method` describes recording a finding
- **THEN** it specifies the citation shape as `<path>:<offset>` or `<path>@L<line>`

#### Scenario: Degradation policy per optional tool

- **WHEN** an evidence-reading skill names an optional external tool (e.g. `pypykatz`, `secretsdump.py`, `tshark`)
- **THEN** its `## Method` states what to do when that tool is unavailable — either a fallback path or an explicit "flag the gap and stop"

#### Scenario: Analytic-spine skills exempted

- **WHEN** an analytic-spine skill's `## Method` is inspected
- **THEN** it is not required to follow the four-element contract, because the skill has no file inventory step and no optional tools to degrade
