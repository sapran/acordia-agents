## ADDED Requirements

### Requirement: `exhaustive-data-processing` skill exists

The library SHALL contain a skill `analysts/skills/exhaustive-data-processing/SKILL.md` naming the discipline that processes bulk collected material in full rather than sampling its opening portion. It SHALL be a first-class procedural cross-cutting skill, and SHALL declare its cross-cutting/procedural nature in its body and SHALL NOT be added as a row to the competency grid.

The skill body SHALL contain: (a) a **cross-cutting notice** declaring the skill procedural and non-grid; (b) a **sampling-trap** section naming why head-and-stop occurs (a bounded read window; partial inspection of tool hits; fan-out that merely distributes sampling if each leaf still reads a head); (c) a **script-first exhaustion** method — run a tool over 100% of the input's bytes or records (`rg`/`grep`/`awk`/`jq`/a parser) to produce aggregates and located hits, read only located regions into context (never the head), and reserve fan-out for judgement a script cannot make; (d) a **coverage-ledger** section requiring a declared input scope (denominator), per-step accounting (scanned / parsed / deferred-with-reason), a per-leaf coverage receipt, and a final statement of total coverage or the named deferred remainder; (e) a **fan-out contract** stating that only the orchestrator fans out (legs are `task: deny`), slices are disjoint and bounded, and a leg whose slice overflows surfaces the remainder back to the orchestrator rather than sampling it.

The skill's `description` SHALL be authored for trigger quality — stating WHEN to apply the discipline (bulk material such as a dump, archive, log bundle, dataset, or any artefact a single read cannot fully capture) — so opencode's description-match selection fires on data-analysis sessions.

The `## Method` contract for evidence-reading skills SHALL NOT apply to this skill: it is procedural and defines the strengthened reading discipline rather than being audited against it, the same treatment applied to `analyst-loop`.

#### Scenario: Skill loads from opencode

- **WHEN** opencode starts
- **THEN** `exhaustive-data-processing` is discovered from `~/.config/opencode/skills/` and is invokable

#### Scenario: Body carries the five required sections

- **WHEN** the skill is inspected
- **THEN** it contains a cross-cutting notice, a sampling-trap section, a script-first exhaustion method, a coverage-ledger section, and a fan-out contract

#### Scenario: Trigger-quality description

- **WHEN** a session must analyse a bulk artefact (dump, archive, log bundle, dataset)
- **THEN** the skill's `description` is specific enough for opencode to select it

#### Scenario: Not a grid row

- **WHEN** the competency grid in `docs/roles/operational-analyst.md` is inspected
- **THEN** no row corresponds to `exhaustive-data-processing`

#### Scenario: Coverage ledger requires a reconciled denominator

- **WHEN** the coverage-ledger section is read
- **THEN** it requires a declared input scope, per-step accounting that reconciles to that scope, a per-leaf coverage receipt, and a final total-coverage statement or a named deferred remainder

## MODIFIED Requirements

### Requirement: Method contract for evidence-reading skills

Skills whose `Objective` involves reading collected material (files, memory dumps, logs, packet captures, configuration archives) SHALL structure their `## Method` section as four ordered elements: (a) an **inventory step** that names the tool used to enumerate the input (e.g. `find`, `glob`, `list`, or a file-typing tool); (b) a **bounded-context, exhaustive-coverage discipline** — reads into the analyst's context stay scoped (offset, line-range, or a targeted tool hit) and never wholesale-load a multi-megabyte artefact into context, **and** the input SHALL be covered in full by a prior tool pass (a script, `grep`/`rg`, or a parser processing 100% of the bytes or records) that drives which scoped regions are read; a finding or conclusion SHALL NOT rest on the opening portion of an artefact while the remainder goes unprocessed, and every located hit SHALL be processed, not only the first; (c) a **citation format** that anchors each observation to `<path>:<offset>` or `<path>@L<line>`; (d) a **degradation policy** stating what the analyst does when each optional external tool named in the body is unavailable.

The requirement applies to the following fifteen skills only: `disk-memory-forensics`, `log-artefact-interpretation`, `cloud-controlplane-analysis`, `web-api-authflow-analysis`, `os-host-internals`, `implant-payload-re`, `identity-directory-trust`, `packet-traffic-analysis`, `endpoint-telemetry-edr`, `c2-beacon-exfil-analysis`, `protocol-routing-architecture`, `own-footprint-analysis`, `evasion-antianalysis`, `pattern-of-life-baselining`, `vuln-attacksurface-mapping`. Analytic-spine skills (whose input is analyst reasoning, not collected material) SHALL NOT be subject to this requirement.

#### Scenario: Method starts with an inventory step

- **WHEN** an evidence-reading skill's `## Method` section is read
- **THEN** its first ordered element names the tool used to enumerate the input before any read happens

#### Scenario: Reads into context are bounded, never wholesale

- **WHEN** an evidence-reading skill's `## Method` describes reading the input into context
- **THEN** the read is scoped (offset, line-range, or targeted tool hit), and no step instructs a wholesale load of a multi-megabyte artefact into context

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
