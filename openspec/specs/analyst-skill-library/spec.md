# analyst-skill-library Specification

## Purpose
Defines the opencode-native skill library derived one-to-one from the competency-grid rows in `docs/roles/operational-analyst.md` — file location, slug and frontmatter contract, triggering-quality descriptions, and the treatment of the cross-cutting deep skills as ordinary skills rather than agents.
## Requirements
### Requirement: One skill per competency-grid row

The library SHALL contain exactly one `SKILL.md` file for each skill row of the appendix grid in `docs/roles/operational-analyst.md`, and SHALL NOT merge, split, or omit rows. Section-header rows (the italic group labels) are not skills and SHALL NOT produce files. The library MAY additionally contain **procedural cross-cutting skills** that reuse multiple grid rows and would violate the one-competency-per-row invariant if added as rows themselves; each such skill SHALL declare its cross-cutting nature explicitly in its own body and SHALL NOT appear in the grid.

#### Scenario: Row count matches file count for competency skills
- **WHEN** the grid lists N skill rows (excluding italic section headers)
- **THEN** the library contains at least N `SKILL.md` files, one traceable to each row

#### Scenario: Header rows produce no skill
- **WHEN** a grid line is an italic section label (e.g. *Analytic spine*)
- **THEN** no `SKILL.md` is created for it

#### Scenario: Procedural skill declares its non-grid status
- **WHEN** a procedural cross-cutting skill is inspected
- **THEN** its body states it is procedural/cross-cutting and does not correspond to a grid row

### Requirement: opencode-native location, plain slugs

Each skill SHALL live at `~/.config/opencode/skills/<slug>/SKILL.md`. The slug SHALL be kebab-case with **no prefix** and SHALL equal the frontmatter `name`.

#### Scenario: Loaded by opencode
- **WHEN** opencode starts
- **THEN** the skill is discovered from `~/.config/opencode/skills/` and is invokable

#### Scenario: Slug and name agree, no prefix
- **WHEN** a skill folder is named `<slug>`
- **THEN** its `SKILL.md` frontmatter `name` equals `<slug>` and neither carries an `oa-` or other prefix

### Requirement: opencode frontmatter contract

Each `SKILL.md` SHALL declare the opencode-required fields `name` (lowercase-hyphen, 1–64 chars) and `description` (1–1024 chars). It MAY declare opencode's optional `metadata`. It SHALL NOT rely on CyberStrike-only fields (`category`, `cwe_ids`, `chains_with`, `severity_boost`) for behaviour, and SHALL NOT include `sha256`/`signature`.

#### Scenario: Required fields present and valid
- **WHEN** any library `SKILL.md` is inspected
- **THEN** `name` matches `^[a-z0-9]+(-[a-z0-9]+)*$` and is ≤64 chars, `description` is 1–1024 chars, and the body is non-empty

### Requirement: Triggering-quality descriptions

Because opencode attaches skills by description (there is no per-agent binding), each `description` SHALL state WHEN the skill applies in one sharp sentence, sufficient to trigger the skill for the right task.

#### Scenario: Description drives selection
- **WHEN** opencode evaluates the skill against a matching analytic task
- **THEN** the `description` alone is specific enough to select it

### Requirement: Cross-cutting deep skills are ordinary skills

The two cross-cutting deep skills — reverse-engineering (implant/payload behaviour) and operational-technology/embedded — SHALL be authored as ordinary `SKILL.md` files, not agents. Their relationship to the legs that draw on them SHALL be stated in prose (skill body / agent prompt), not via a `chains_with` frontmatter edge.

#### Scenario: RE and OT are plain skills
- **WHEN** the reverse-engineering and operational-technology skills are inspected
- **THEN** each is a `SKILL.md` with opencode frontmatter, no `chains_with` field, and neither has its own agent file

### Requirement: Credential-extraction sections in credential-adjacent skills

Seven skills SHALL each carry a named `## Credential extraction` section covering, for that skill's domain: artefact locations, canonical extraction tools, and portable extraction patterns. The seven are `disk-memory-forensics`, `identity-directory-trust`, `log-artefact-interpretation`, `cloud-controlplane-analysis`, `web-api-authflow-analysis`, `os-host-internals`, and `implant-payload-re`. The section SHALL be additive — it does not replace the existing `Objective`, `When to use`, `Method`, or `Signals / outputs` sections.

#### Scenario: Section present in each credential-adjacent skill
- **WHEN** any of the seven skills' `SKILL.md` is inspected
- **THEN** it contains a `## Credential extraction` H2 section with domain-specific artefact locations, tools, and patterns

#### Scenario: Enrichment is additive, not a rewrite
- **WHEN** an enriched skill is compared against its pre-enrichment content
- **THEN** the existing sections are unchanged and only the new `## Credential extraction` section is added

#### Scenario: Passive posture preserved
- **WHEN** a credential-extraction section is read
- **THEN** it describes analysis of already-collected material only, references no active credential validation, and stores no raw credential values in its examples

### Requirement: `credential-harvest-triage` skill exists

The library SHALL contain a skill `analysts/skills/credential-harvest-triage/SKILL.md` providing (a) a classification schema for credential findings (type, subtype, status, scope, source, reuse potential, priority), (b) a triage procedure that begins with **inventory**, then performs a **bucket partition** step assigning material to a leg-owned bucket, then scans, classifies, correlates, prioritises, and reports, and (c) a **pointer** to a co-located pattern-library reference file for common credential material. It SHALL declare its cross-cutting/procedural nature in its body and SHALL NOT be added as a row to the competency grid.

The **bucket partition** step SHALL enumerate five buckets and their target legs:

- Bucket A — identity / directory / cloud-controlplane material → `target-network-analyst`
- Bucket B — host-forensic material (memory, SAM, DPAPI, keychain, shadow) → whichever leg holds the host under analysis
- Bucket C — web / API auth material → `target-network-analyst`
- Bucket D — log-artefact material → `defender-detection-analyst`
- Bucket E — implant / payload RE material → cross-cutting via `implant-payload-re`, reported to `fusion-analyst`

Each bucket's slice SHALL be dispatched with only that slice. The procedure SHALL state that per-leg classifications feed back into `multi-source-fusion` for cross-leg correlation.

#### Scenario: Triage skill loads from opencode

- **WHEN** opencode starts
- **THEN** `credential-harvest-triage` is discovered from `~/.config/opencode/skills/` and is invokable

#### Scenario: Body carries schema, procedure, and pattern library

- **WHEN** the triage skill is inspected
- **THEN** it contains a classification schema, a bucket-partition step, a numbered triage procedure downstream of the partition, and a pointer to the pattern library at `references/credential-patterns.md`

#### Scenario: Bucket partition maps to existing legs

- **WHEN** the bucket-partition step is read
- **THEN** every bucket routes to one of `target-network-analyst`, `defender-detection-analyst`, `fusion-analyst`, or the cross-cutting `implant-payload-re` skill, and no bucket routes to a leg not on the current whitelist

#### Scenario: Not a grid row

- **WHEN** the competency grid in `docs/roles/operational-analyst.md` is inspected
- **THEN** no row corresponds to `credential-harvest-triage`

### Requirement: `analyst-loop` skill exists

The library SHALL contain a skill `analysts/skills/analyst-loop/SKILL.md` naming the end-neutral analytic loop — target-read (through the T&N leg), defender-read (through the Def leg), fusion (through the Fus leg), judgement (calibrated, via spine skills), next-move — as a first-class procedural cross-cutting skill.

The skill body SHALL contain: (a) a **cross-cutting notice** declaring the skill procedural and non-grid; (b) a **loop-shape** section naming the five steps in one sentence each; (c) a **loop-invariants** section stating end-neutrality (every pass reaches a judgement plus a next move), gap-naming on every judgement, calibrated confidence on every judgement, and passive posture; (d) a **where-this-runs** paragraph stating the loop is the orchestrator's workflow, and that a leg session matching this skill surfaces the need for a full pass back to the orchestrator rather than attempting the loop itself.

The skill's `description` SHALL be authored for trigger quality — stating WHEN to run the loop, not WHAT it is — so opencode's description-match selection fires cleanly on operator sessions asking for a fresh analytic round.

The skill SHALL declare its cross-cutting/procedural nature and SHALL NOT be added as a row to the competency grid. The `## Method` contract for evidence-reading skills (from `analyst-verifiability-anchors`) SHALL NOT apply — this skill reads no files.

#### Scenario: Loop skill loads from opencode

- **WHEN** opencode starts
- **THEN** `analyst-loop` is discovered from `~/.config/opencode/skills/` and is invokable

#### Scenario: Body carries the four required sections

- **WHEN** the loop skill is inspected
- **THEN** it contains a cross-cutting notice, a loop-shape section naming five steps, a loop-invariants section, and a where-this-runs paragraph

#### Scenario: Trigger-quality description

- **WHEN** an operator session asks for a fresh end-neutral analytic pass
- **THEN** `analyst-loop`'s `description` is specific enough for opencode to select it

#### Scenario: Not a grid row

- **WHEN** the competency grid in `docs/roles/operational-analyst.md` is inspected
- **THEN** no row corresponds to `analyst-loop`

#### Scenario: Orchestrator references the skill; legs do not

- **WHEN** `analysts/agents/operational-analyst.md` is inspected
- **THEN** it names `analyst-loop` in one sentence within its existing loop-describing paragraph

- **WHEN** any leg agent (`target-network-analyst`, `defender-detection-analyst`, `fusion-analyst`) is inspected
- **THEN** it does not name `analyst-loop`

### Requirement: Method contract for evidence-reading skills

Skills whose `Objective` involves reading collected material (files, memory dumps, logs, packet captures, configuration archives) SHALL structure their `## Method` section as four ordered elements: (a) an **inventory step** that names the tool used to enumerate the input (e.g. `find`, `glob`, `list`, or a file-typing tool); (b) a **bounded-context, exhaustive-coverage discipline** — reads into the analyst's context stay scoped (offset, line-range, or a targeted tool hit) and never wholesale-load a multi-megabyte artefact into context, **and** the input SHALL be covered in full by a prior tool pass (a script, `grep`/`rg`, or a parser processing 100% of the bytes or records) that drives which scoped regions are read; a finding or conclusion SHALL NOT rest on the opening portion of an artefact while the remainder goes unprocessed, and every located hit SHALL be processed, not only the first; (c) a **citation format** that anchors each observation to `<path>:<offset>` or `<path>@L<line>`; (d) a **degradation policy** stating what the analyst does when each optional external tool named in the body is unavailable.

The requirement applies to the following fifteen skills only: `disk-memory-forensics`, `log-artefact-interpretation`, `cloud-controlplane-analysis`, `web-api-authflow-analysis`, `os-host-internals`, `implant-payload-re`, `identity-directory-trust`, `packet-traffic-analysis`, `endpoint-telemetry-edr`, `c2-beacon-exfil-analysis`, `protocol-routing-architecture`, `own-footprint-analysis`, `evasion-antianalysis`, `pattern-of-life-baselining`, `vuln-attacksurface-mapping`. Analytic-spine skills (whose input is analyst reasoning, not collected material) SHALL NOT be subject to this requirement.

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

### Requirement: Procedural skills MAY co-locate reference files

A procedural cross-cutting skill MAY ship supplementary content in a `references/` subdirectory alongside its `SKILL.md`. When it does, the skill body SHALL contain a naming pointer to each reference file, so a session that reads only `SKILL.md` knows the reference exists and what class of content lives there. `install.sh` symlinks the whole skill directory; sibling reference files SHALL therefore land alongside `SKILL.md` at deploy time without an install-script change.

Reference files SHALL be markdown. Structured formats (YAML, JSON) SHALL NOT be used unless a consumer exists in the repo — this repo has no code path that loads structured references.

#### Scenario: Reference file colocated with skill

- **WHEN** a procedural skill declares a reference file
- **THEN** the file lives at `analysts/skills/<slug>/references/<name>.md`

#### Scenario: Skill body names each reference file

- **WHEN** a procedural skill's `SKILL.md` is inspected
- **THEN** for every reference file present, the body contains a naming pointer stating the file's path relative to `SKILL.md` and what class of content it holds

#### Scenario: `credential-harvest-triage` carries `credential-patterns.md`

- **WHEN** `analysts/skills/credential-harvest-triage/` is inspected
- **THEN** it contains `SKILL.md` and `references/credential-patterns.md`, and `SKILL.md` names the reference file

#### Scenario: Reference file is markdown

- **WHEN** any reference file under a procedural skill is inspected
- **THEN** it is a `.md` file

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

### Requirement: `aleph-entity-graph` skill exists

The library SHALL contain a skill `analysts/skills/aleph-entity-graph/SKILL.md` naming the discipline of working collected material that has already been ingested into an Aleph instance as a FollowTheMoney entity graph, rather than as a pile of documents. It SHALL be a first-class procedural cross-cutting skill, SHALL declare its cross-cutting/procedural nature in its body, and SHALL NOT be added as a row to the competency grid.

The skill body SHALL contain: (a) a **cross-cutting notice** declaring the skill procedural and non-grid and naming the grid rows it composes; (b) a **data-model** section stating that Aleph stores FollowTheMoney entities grouped into collections, that schemata inherit, and that `entity`-typed properties are the graph edges; (c) a **conditional tooling** paragraph naming the `aleph_*` MCP tools as available only where the harness mounts them and naming the `bash` + HTTP API fallback otherwise; (d) an **inventory-first, facet-first method** — enumerate collections and read their statistics, survey a result set with facets at `limit=0` before pulling rows, narrow with `filter:` constraints, pivot on entities via expand/tags/similar/match/entitysets/xref, and read document text last and bounded; (e) a **limits** section stating the three ceilings that change the method; and (f) a **take-assessment** section feeding `assessing-take-value`.

The limits section SHALL state all three of the following as method-changing facts, not as trivia:

- Entity search cannot page past `limit + offset = 9999`, so a total above that means the result set is **unenumerated** and must be split by facet or narrowed — deep pagination is not a way to read a collection.
- Graph expansion is capped separately and far lower (200 entities per property by default), so a reported `count` above the cap means that edge was **sampled**, and the analyst SHALL say so.
- The unbounded `_stream` export requires WRITE on the collection, so a read-only analyst key cannot bulk-export; a full local copy is a human-run `aleph-coldbackup` job rather than a session action.

The skill's `description` SHALL be authored for trigger quality — stating WHEN the discipline applies (the take lives in an Aleph instance) — so opencode's description-match selection fires, because opencode provides no per-agent skill binding.

The skill SHALL hold the analyst read-only posture explicitly: it SHALL name search, expansion and bounded text reads as in scope, and SHALL name ingestion, entity writes, tagging, on-demand cross-reference runs and deletion as out of scope and belonging to the operator or the human. It SHALL state that the API key is expected to be READ-scoped and that a 403 naming WRITE or admin rights is the boundary working, not an obstacle to route around.

The `## Method` contract for evidence-reading skills SHALL NOT apply to this skill: it is procedural and defines its own reading discipline, the same treatment applied to `analyst-loop` and `exhaustive-data-processing`.

#### Scenario: Skill loads from opencode

- **WHEN** opencode starts
- **THEN** `aleph-entity-graph` is discovered from `~/.config/opencode/skills/` and is invokable

#### Scenario: Body carries the six required sections

- **WHEN** the skill is inspected
- **THEN** it contains a cross-cutting notice, a FollowTheMoney data-model section, a conditional tooling paragraph, an inventory-first and facet-first method, a limits section, and a take-assessment section

#### Scenario: Trigger-quality description

- **WHEN** a session must analyse take that has been ingested into an Aleph instance
- **THEN** the skill's `description` is specific enough for opencode to select it without a per-agent binding

#### Scenario: Not a grid row

- **WHEN** the competency grid in `docs/roles/operational-analyst.md` is inspected
- **THEN** no row corresponds to `aleph-entity-graph`

#### Scenario: All three ceilings are stated

- **WHEN** the limits section is read
- **THEN** it names the 9999 search window, the separate per-property expansion cap, and the WRITE requirement on `_stream`, and states the analytic consequence of each

#### Scenario: Tool references degrade instead of assuming a harness

- **WHEN** the skill runs in a harness where no `aleph_*` MCP tool is mounted
- **THEN** the body has already stated that condition and named the `bash` + HTTP API fallback, satisfying `harness-tool-translation`

#### Scenario: Read-only posture is explicit

- **WHEN** the guardrails section is read
- **THEN** ingestion, entity writes, tagging, cross-reference triggering and deletion are named as out of scope, and the READ-scoped API key is named as the enforcement point

