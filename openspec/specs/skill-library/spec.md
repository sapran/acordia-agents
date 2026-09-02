# skill-library Specification

## Purpose

Defines the analyst skill library — where a skill lives, the frontmatter contract both
harnesses parse, the description that selects it, its one-to-one derivation from the competency grid,
and the reading and reference-file disciplines its bodies follow.

## Requirements

### Requirement: Skills live in their own pillar under a plain slug

Each skill SHALL live at `acordia-analysts/skills/<slug>/SKILL.md`, one directory per skill. The slug
SHALL be kebab-case matching `^[a-z0-9]+(-[a-z0-9.]*)*$`, SHALL carry no pillar or distribution prefix,
and SHALL equal the frontmatter `name`, because both harnesses default a skill's name to its directory
name. `acordia-analysts/skills/` is the only path root a skill may occupy: no `SKILL.md` SHALL exist
outside it, and no generated or translated copy of a skill SHALL exist in the repository.

How many skills that root holds is stated by *The library is the analyst library, sized by the grid
rather than by this spec*, not here, because the count moves with the grid. The scenario below keeps
its published title, *Library counts are what each pillar ships*, though there is now one pillar:
OpenSpec matches a MODIFIED block's scenarios against the published spec by title, so retitling one
reads as dropping it and fails the archive step. The title is legacy; its body carries the truth.

#### Scenario: Slug, name and directory agree

- **WHEN** any skill directory is inspected
- **THEN** its `SKILL.md` frontmatter `name` equals the directory name and carries no prefix

#### Scenario: One copy per skill

- **WHEN** the repository is enumerated for `SKILL.md` files
- **THEN** every one lives under `acordia-analysts/skills/`, exactly once

#### Scenario: No second library root exists

- **WHEN** the repository is searched for a `skills/` directory outside `acordia-analysts/`
- **THEN** none is found

#### Scenario: Library counts are what each pillar ships

- **WHEN** the library is counted
- **THEN** the analyst pillar is the only pillar, and its total is the grid's arithmetic rather than a figure fixed here or a two-pillar sum

### Requirement: Skill frontmatter contract

Each `SKILL.md` SHALL declare `name` (lowercase-hyphen, 1-64 characters) and `description` (1-200
characters, per *The description is the selection surface*), and MAY declare `metadata`. It SHALL
declare no other key. A `metadata` block SHALL carry the `acordia` key alone: with the ported library
gone, no `metadata.cyberstrike` block remains anywhere in the tree, and one SHALL NOT be reintroduced
except by a change that ports material and needs a provenance record for it.

Every CyberStrike-only field SHALL stay dropped: `category`, `version`, `author`, `tags`, `owasp_id`,
`cis_id`, `cis_benchmark`, `tech_stack`, `cwe_ids`, `chains_with`, `prerequisites`, `severity_boost`.
The prohibition outlives the port that brought these keys in. The contract has room for exactly three
keys and no harness reads any of the twelve, so the list is what distinguishes a field that is merely
unused from one that is excluded: deleting it along with the library that introduced it would leave
nothing standing between a future import and twelve keys nothing consumes.

The signing triple `sha256` / `signature` / `signed_by` SHALL stay dropped. Every body here is
hand-edited and no step recomputes a digest, so a retained hash is stale on its first edit; a stale
digest is worse than none, because any verifier that honours it reads a legitimately edited skill as
tampered and drops it without saying so, while the body sits intact on disk.

No skill SHALL declare a tool list, a permission map, or any harness-restriction field.

#### Scenario: Only contract fields present

- **WHEN** any skill's frontmatter is parsed
- **THEN** its keys are a subset of `name`, `description`, `metadata`

#### Scenario: Field values are within the contract

- **WHEN** any skill's frontmatter is validated
- **THEN** `name` matches the kebab-case pattern and is at most 64 characters, `description` is 1-200 characters, and the body is non-empty

#### Scenario: No signing or restriction fields

- **WHEN** any skill's frontmatter is inspected
- **THEN** it carries no `sha256`, `signature`, `signed_by`, `tools`, or `permission` key

#### Scenario: No provenance block survives the strip

- **WHEN** any skill's `metadata` block is read
- **THEN** it carries `acordia` and no `cyberstrike` key, because the library that recorded upstream attribution is gone

### Requirement: The description is the selection surface

Because both harnesses select a skill by matching its `description`, each `description` SHALL open
with an imperative naming the work only that skill does, and SHALL then give the trigger — the
situation in which that work is wanted. It SHALL be 1–200 characters.

The ceiling is a budget obligation, not a style preference. A host renders the library as a
*catalogue* in the system prompt — one entry per skill, costing `97 + len(name) + len(description) +
len(location)` characters — and that catalogue has a finite budget, 18,000 characters on OpenClaw
2026.7.1. A host that exceeds the budget does not drop the overrunning skill and does not fail: it
drops **every** description in the catalogue and renders names and paths alone. An overlong
description therefore costs every *other* skill its selection surface, which is why the bound is
per-description and hard rather than an aggregate the library could average its way past.

Across the library the mean `description` length SHALL be at most 180 characters, so that the
catalogue for any single analyst's skill set stays under 12,000 characters and leaves a host room for
skills of its own.

A description SHALL NOT open with a selection-boilerplate clause: `Use when`, `Apply when`, `Use to`,
`Use this skill`, and their variants are prohibited openings, because they are common to every skill
and therefore discriminate between none of them. A bare topic label SHALL NOT be used either.

Within a family, no two descriptions SHALL compete: each SHALL name work its siblings do not cover.
Where two are inseparable, the two skills SHALL be merged rather than shipped as competing siblings.

Compression SHALL NOT be achieved by dropping the trigger. Where a description must lose material to
reach the ceiling, what goes is enumeration — worked examples, lists of artefact types, restatements
of the body — and what stays is the pair a selecting model needs: the work only this skill does, and
the situation that calls for it.

#### Scenario: Description states applicability

- **WHEN** any skill's description is read
- **THEN** it states the situation the skill applies to, not merely its topic

#### Scenario: Description discriminates between siblings

- **WHEN** two skills in the same family are compared
- **THEN** each description names work the other does not cover

#### Scenario: Boilerplate openings are absent

- **WHEN** every description under `acordia-analysts/skills/` is read
- **THEN** none begins with `Use when`, `Apply when`, `Use to`, `Use this skill` or an equivalent selection-boilerplate clause

#### Scenario: Every description is within the ceiling

- **WHEN** every `description` under `acordia-analysts/skills/` is measured as characters after YAML folding
- **THEN** none exceeds 200 characters, and the mean across the library is at most 180

#### Scenario: A role-scoped catalogue renders with descriptions

- **WHEN** a host loads the skill set named in any one analyst's prompt and renders its catalogue at `97 + len(name) + len(description) + len(location)` per entry
- **THEN** the total is under 12,000 characters, so the catalogue renders with descriptions intact rather than degrading to the names-and-paths compact format

#### Scenario: The worked collision is separated

- **WHEN** `multi-source-fusion` and `maintaining-operating-picture` descriptions are compared
- **THEN** one names consolidating disconnected strands into one coherent picture and the other names stopping an already-fused picture from rotting — timestamping, decay on perishable facts, re-verification before reliance — rather than a shared "target picture" phrasing

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

### Requirement: Cross-cutting deep skills are ordinary skills

The two cross-cutting deep skills — reverse-engineering (implant/payload behaviour) and
operational-technology/embedded — SHALL be authored as ordinary `SKILL.md` files, not agents. Their
relationship to the legs that draw on them SHALL be stated in prose (skill body / agent prompt), not
via a `chains_with` frontmatter edge. Every skill SHALL be reachable by name from at least one agent
prompt: a skill no prompt names is unreachable in practice, because a prompt's `·`-separated lines are
the only agent-to-skill binding either harness offers.

#### Scenario: RE and OT are plain skills

- **WHEN** the reverse-engineering and operational-technology skills are inspected
- **THEN** each is a `SKILL.md` with contract frontmatter, no `chains_with` field, and neither has its own agent file

#### Scenario: No skill is orphaned

- **WHEN** every analyst skill slug is searched for in the five analyst prompts
- **THEN** each appears on at least one prompt's skill line

### Requirement: Method contract for evidence-reading skills

Skills whose `Objective` involves reading collected material (files, memory dumps, logs, packet captures, configuration archives) SHALL structure their `## Method` section as four ordered elements: (a) an **inventory step** that names the tool used to enumerate the input (e.g. `find`, `glob`, `list`, or a file-typing tool); (b) a **bounded-context, exhaustive-coverage discipline** — reads into the analyst's context stay scoped (offset, line-range, or a targeted tool hit) and never wholesale-load a multi-megabyte artefact into context, **and** the input SHALL be covered in full by a prior tool pass (a script, `grep`/`rg`, or a parser processing 100% of the bytes or records) that drives which scoped regions are read; a finding or conclusion SHALL NOT rest on the opening portion of an artefact while the remainder goes unprocessed, and every located hit SHALL be processed, not only the first; (c) a **citation format** that anchors each observation to `<path>:<offset>` or `<path>@L<line>`; (d) a **degradation policy** stating what the analyst does when each optional external tool named in the body is unavailable.

The criterion above is normative and determines scope on its own. A skill meeting it SHALL carry the four elements whether or not it appears in any enumeration, because a closed list makes coverage depend on whether a name was remembered rather than on what the skill does. The following twenty-one skills currently meet the criterion: `analytic-tooling-scripting`, `assessing-take-value`, `c2-beacon-exfil-analysis`, `change-cycle-forecasting`, `cloud-controlplane-analysis`, `data-integration-tooling`, `disk-memory-forensics`, `endpoint-telemetry-edr`, `evasion-antianalysis`, `identity-directory-trust`, `implant-payload-re`, `log-artefact-interpretation`, `os-host-internals`, `ot-embedded`, `overwatch`, `own-footprint-analysis`, `packet-traffic-analysis`, `pattern-of-life-baselining`, `protocol-routing-architecture`, `vuln-attacksurface-mapping`, `web-api-authflow-analysis`. This enumeration records the present membership and SHALL be extended whenever a skill that reads collected material is added or an existing skill's Method begins to direct such reading; it SHALL NOT be read as narrowing the criterion. Analytic-spine skills (whose input is analyst reasoning, not collected material) SHALL NOT be subject to this requirement.

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

- **WHEN** each of the twenty-one enumerated skills is inspected
- **THEN** its `## Method` carries an inventory step, bounded-and-exhaustive reading language, a citation shape, and a degradation policy for each optional tool it names

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

### Requirement: Procedural skills MAY co-locate reference files

A procedural cross-cutting skill MAY ship supplementary content in a `references/` subdirectory alongside its `SKILL.md`. When it does, the skill body SHALL contain a naming pointer to each reference file, so a session that reads only `SKILL.md` knows the reference exists and what class of content lives there. A harness installs the whole skill directory, so sibling reference files land alongside `SKILL.md` with no packaging step.

Reference files SHALL be markdown. Structured formats (YAML, JSON) SHALL NOT be used unless a consumer exists in the repo — this repo has no code path that loads structured references.

#### Scenario: Reference file colocated with skill

- **WHEN** a procedural skill declares a reference file
- **THEN** the file lives at `acordia-analysts/skills/<slug>/references/<name>.md`

#### Scenario: Skill body names each reference file

- **WHEN** a procedural skill's `SKILL.md` is inspected
- **THEN** for every reference file present, the body contains a naming pointer stating the file's path relative to `SKILL.md` and what class of content it holds

#### Scenario: `credential-harvest-triage` carries `credential-patterns.md`

- **WHEN** `acordia-analysts/skills/credential-harvest-triage/` is inspected
- **THEN** it contains `SKILL.md` and `references/credential-patterns.md`, and `SKILL.md` names the reference file

#### Scenario: Reference file is markdown

- **WHEN** any reference file under a procedural skill is inspected
- **THEN** it is a `.md` file

### Requirement: `credential-harvest-triage` skill exists

The library SHALL contain a skill `acordia-analysts/skills/credential-harvest-triage/SKILL.md` providing (a) a classification schema for credential findings (type, subtype, status, scope, source, reuse potential, priority), (b) a triage procedure that begins with **inventory**, then performs a **bucket partition** step assigning material to a leg-owned bucket, then scans, classifies, correlates, prioritises, and reports, and (c) a **pointer** to a co-located pattern-library reference file for common credential material. It SHALL declare its cross-cutting/procedural nature in its body and SHALL NOT be added as a row to the competency grid.

The **bucket partition** step SHALL enumerate five buckets and their target legs:

- Bucket A — identity / directory / cloud-controlplane material → `terrain-analyst`
- Bucket B — host-forensic material (memory, SAM, DPAPI, keychain, shadow) → whichever leg holds the host under analysis
- Bucket C — web / API auth material → `terrain-analyst`
- Bucket D — log-artefact material → `overwatch-analyst`
- Bucket E — implant / payload RE material → cross-cutting via `implant-payload-re`, reported to `cyber-analyst`, which holds the fused picture itself

Each bucket's slice SHALL be dispatched with only that slice. The procedure SHALL state that per-leg classifications feed back into `multi-source-fusion` for cross-leg correlation.

#### Scenario: Triage skill loads in a harness

- **WHEN** a harness loads the analyst pillar
- **THEN** `credential-harvest-triage` is discovered from `acordia-analysts/skills/` and is invokable

#### Scenario: Body carries schema, procedure, and pattern library

- **WHEN** the triage skill is inspected
- **THEN** it contains a classification schema, a bucket-partition step, a numbered triage procedure downstream of the partition, and a pointer to the pattern library at `references/credential-patterns.md`

#### Scenario: Bucket partition maps to existing legs

- **WHEN** the bucket-partition step is read
- **THEN** every bucket routes to one of `terrain-analyst`, `overwatch-analyst`, `cyber-analyst`, or the cross-cutting `implant-payload-re` skill, and no bucket routes to a leg not on the current whitelist

#### Scenario: No bucket names a retired leg

- **WHEN** the bucket-partition step is searched for `target-analyst` or `fusion-analyst`
- **THEN** neither is found, because neither agent exists

#### Scenario: Not a grid row

- **WHEN** the competency grid in `docs/roles/operational-analyst.md` is inspected
- **THEN** no row corresponds to `credential-harvest-triage`

### Requirement: `analyst-loop` skill exists

The library SHALL contain a skill `acordia-analysts/skills/analyst-loop/SKILL.md` naming the
end-neutral analytic loop — mission-read (through `mission-analyst`), terrain-read (through
`terrain-analyst`), defender-read (through `overwatch-analyst`), take-read (through
`collection-analyst`), judgement (calibrated, via spine skills), next-move — as a first-class
procedural cross-cutting skill.

The loop SHALL carry no delegated fusion step. The fused picture is held by `cyber-analyst` itself, so
the four leg reads converge in the orchestrator's own hands rather than in a leg's, and no step of the
loop SHALL name a leg that fuses on the orchestrator's behalf.

Because the distribution ships no executing agent, the loop's judgement step SHALL rest on evidence
reported by the four legs and by the human operator the product is handed to, and its next-move step
SHALL name a move for that person rather than a dispatch the pillar performs itself.

The skill body SHALL contain: (a) a **cross-cutting notice** declaring the skill procedural and
non-grid; (b) a **loop-shape** section naming the six steps in one sentence each; (c) a
**loop-invariants** section stating end-neutrality (every pass reaches a judgement plus a next move),
gap-naming on every judgement, calibrated confidence on every judgement, and passive posture; (d) a
**where-this-runs** paragraph stating the loop is the orchestrator's workflow, and that a leg session
matching this skill surfaces the need for a full pass back to the orchestrator rather than attempting
the loop itself.

The skill's `description` SHALL be authored for trigger quality — stating WHEN to run the loop, not WHAT it is — so description-match selection fires cleanly on operator sessions asking for a fresh analytic round.

The skill SHALL declare its cross-cutting/procedural nature and SHALL NOT be added as a row to the competency grid. The `## Method` contract for evidence-reading skills (from `analyst-verifiability-anchors`) SHALL NOT apply — this skill reads no files.

#### Scenario: Loop skill loads in a harness

- **WHEN** a harness loads the analyst pillar
- **THEN** `analyst-loop` is discovered from `acordia-analysts/skills/` and is invokable

#### Scenario: Body carries the four required sections

- **WHEN** the loop skill is inspected
- **THEN** it contains a cross-cutting notice, a loop-shape section naming six steps, a loop-invariants section, and a where-this-runs paragraph

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

### Requirement: `exhaustive-data-processing` skill exists

The library SHALL contain a skill `acordia-analysts/skills/exhaustive-data-processing/SKILL.md` naming the discipline that processes bulk collected material in full rather than sampling its opening portion. It SHALL be a first-class procedural cross-cutting skill, and SHALL declare its cross-cutting/procedural nature in its body and SHALL NOT be added as a row to the competency grid.

The skill body SHALL contain: (a) a **cross-cutting notice** declaring the skill procedural and non-grid; (b) a **sampling-trap** section naming why head-and-stop occurs (a bounded read window; partial inspection of tool hits; fan-out that merely distributes sampling if each leaf still reads a head); (c) a **script-first exhaustion** method — run a tool over 100% of the input's bytes or records (`rg`/`grep`/`awk`/`jq`/a parser) to produce aggregates and located hits, read only located regions into context (never the head), and reserve fan-out for judgement a script cannot make; (d) a **coverage-ledger** section requiring a declared input scope (denominator), per-step accounting (scanned / parsed / deferred-with-reason), a per-leaf coverage receipt, and a final statement of total coverage or the named deferred remainder; (e) a **fan-out contract** stating that only the orchestrator fans out (legs are `task: deny`), slices are disjoint and bounded, and a leg whose slice overflows surfaces the remainder back to the orchestrator rather than sampling it.

The skill's `description` SHALL be authored for trigger quality — stating WHEN to apply the discipline (bulk material such as a dump, archive, log bundle, dataset, or any artefact a single read cannot fully capture) — so description-match selection fires on data-analysis sessions.

The `## Method` contract for evidence-reading skills SHALL NOT apply to this skill: it is procedural and defines the strengthened reading discipline rather than being audited against it, the same treatment applied to `analyst-loop`.

#### Scenario: Skill loads in a harness

- **WHEN** a harness loads the analyst pillar
- **THEN** `exhaustive-data-processing` is discovered from `acordia-analysts/skills/` and is invokable

#### Scenario: Body carries the five required sections

- **WHEN** the skill is inspected
- **THEN** it contains a cross-cutting notice, a sampling-trap section, a script-first exhaustion method, a coverage-ledger section, and a fan-out contract

#### Scenario: Trigger-quality description

- **WHEN** a session must analyse a bulk artefact (dump, archive, log bundle, dataset)
- **THEN** the skill's `description` is specific enough for the harness to select it

#### Scenario: Not a grid row

- **WHEN** the competency grid in `docs/roles/operational-analyst.md` is inspected
- **THEN** no row corresponds to `exhaustive-data-processing`

#### Scenario: Coverage ledger requires a reconciled denominator

- **WHEN** the coverage-ledger section is read
- **THEN** it requires a declared input scope, per-step accounting that reconciles to that scope, a per-leaf coverage receipt, and a final total-coverage statement or a named deferred remainder

### Requirement: `aleph-entity-graph` skill exists

The library SHALL contain a skill `acordia-analysts/skills/aleph-entity-graph/SKILL.md` naming the discipline of working collected material that has already been ingested into an Aleph instance as a FollowTheMoney entity graph, rather than as a pile of documents. It SHALL be a first-class procedural cross-cutting skill, SHALL declare its cross-cutting/procedural nature in its body, and SHALL NOT be added as a row to the competency grid.

The skill body SHALL contain: (a) a **cross-cutting notice** declaring the skill procedural and non-grid and naming the grid rows it composes; (b) a **data-model** section stating that Aleph stores FollowTheMoney entities grouped into collections, that schemata inherit, and that `entity`-typed properties are the graph edges; (c) a **conditional tooling** paragraph naming the MCP server's registered read tools by their bare verbs, stating that a harness may expose them under a mount prefix, and naming the `bash` + HTTP API fallback otherwise; (d) a **scope-first, inventory-first, facet-first method** — name the collection every search is scoped to, enumerate collections and read their statistics, survey a result set with facets at `limit=0` before pulling rows, narrow with `filter:` constraints, pivot on entities and on resolved identities via expand/tags/similar/match/profiles/entitysets/xref, and read document text last and bounded; (e) a **limits** section stating the ceilings and query semantics that change the method; and (f) a **take-assessment** section feeding `assessing-take-value`.

Clause (c) SHALL NOT mandate a prefixed tool-name form. The `aleph-mcp` server registers its tools unprefixed and its own specification explicitly refuses to guarantee any prefix, stating that the mount configuration is where that expectation is satisfied; a prefix a caller observes is composed by the host from the mount name. The tooling paragraph SHALL therefore name the tool verbs, SHALL state that a harness may apply a mount prefix and give the observed form as an example rather than a requirement, and SHALL direct the analyst to match on the verb rather than on a literal prefix.

The tooling paragraph SHALL state what the `bash` + HTTP fallback gives up relative to the tools, because on that path the analyst inherits the obligations the server was discharging: no refusal at the search ceiling, no expansion cap, no stripping of document-sized text properties, no derived `caption`, and no read-only allowlist between the caller and a write endpoint. It SHALL name collection scope among them: the fallback's example URL SHALL carry a `filter:collection_id` constraint, and the paragraph SHALL state that an omitted one searches every collection the key can read with nothing in the response to signal it.

The method's pivot step SHALL name profile-scoped pivots alongside entity-scoped ones, and SHALL name the `profile_id` field carried on search and expansion results as their entry point. It SHALL state the analytic rule that a profile-scoped pivot is preferred over an entity-scoped one where a profile exists, because the entity in hand is one fragment of an actor whose other fragments carry edges invisible from it.

The method's first step SHALL be collection scope, ahead of inventory, because an unscoped Aleph search is answered rather than refused. It SHALL name `collection` as the argument that carries scope and as a required argument on `search_entities` and `match_entity`; SHALL name the forms it accepts — a numeric id, or a `foreign_id` resolved server-side, with a list accepted by the two search tools only; SHALL name the literal `collection="*"` as the only instance-wide scope and the `_note` that annotates a `search_entities` reply at that scope; SHALL state that a blank value is refused rather than read as "no scope"; and SHALL state that `collection_id` inside `filters` is refused rather than honoured. The narrowing step SHALL NOT present collection as one of its filter keys.

The step SHALL state the consequence of omitting scope rather than only the requirement to supply it: a search that names no collection returns another collection's rows, ranked, well-formed and plausible, with no error, no warning and no empty result. It is stated as a consequence because enforcement is not uniform — the tools refuse a missing `collection` and the HTTP fallback does not — and because the one number that would expose a wrong scope is a reported total above 10,000, which this same skill has already taught the analyst to read as a floor rather than a count.

The method SHALL direct the analyst to read the applied scope back from the reply's `searched.collection` field, which reports the resolved numeric ids or `"*"`, rather than assume the scope requested is the scope applied. A required argument establishes that something was passed; it does not establish that a `foreign_id` or a list resolved to the collections intended, and every such resolution produces a successful reply.

The take-assessment section SHALL require a hit's own `collection_id` to be checked against the collection that was scoped to, because that mismatch is the only symptom a wrongly-scoped search produces.

The limits section SHALL state all three of the following as method-changing facts, not as trivia:

- Entity search cannot page past `limit + offset = 9999`, so a total above that means the result set is **unenumerated** and must be split by facet or narrowed — deep pagination is not a way to read a collection.
- Graph expansion is capped separately and far lower (200 entities per property by default), so a reported `count` above the cap means that edge was **sampled**, and the analyst SHALL say so.
- The unbounded `_stream` export requires WRITE on the collection, so a read-only analyst key cannot bulk-export; a full local copy is a human-run `aleph-coldbackup` job rather than a session action.

The skill SHALL additionally state Aleph's real entity-search query semantics, because assuming otherwise manufactures false negatives on the name variants that matter: `q` is **not fuzzy** on entity search, so a misspelt or transliterated name will not match and `match_entity` is the tolerant name-lookup path; and a multi-term `q` requires only 66% of its terms, so precision comes from `filter:` constraints rather than from adding words.

Where the skill states a limit that the MCP tools discharge but the fallback does not, it SHALL attribute the limit to the path rather than asserting it unconditionally. `caption` is the case in point: the server derives one from the instance's own per-schema property ordering, so it is populated under the tools and the analyst's own problem under `curl`.

The skill's `description` SHALL be authored for trigger quality — stating WHEN the discipline applies (the take lives in an Aleph instance) — so description-match selection fires, because neither harness binds skills to an agent.

The skill SHALL hold the analyst read-only posture explicitly: it SHALL name search, expansion and bounded text reads as in scope, and SHALL name ingestion, entity writes, tagging, on-demand cross-reference runs and deletion as out of scope and belonging to the operator or the human. It SHALL state that the API key is expected to be READ-scoped and that a 403 naming WRITE or admin rights is the boundary working, not an obstacle to route around.

The `## Method` contract for evidence-reading skills SHALL NOT apply to this skill: it is procedural and defines its own reading discipline, the same treatment applied to `analyst-loop` and `exhaustive-data-processing`.

#### Scenario: Skill loads in a harness

- **WHEN** a harness loads the analyst pillar
- **THEN** `aleph-entity-graph` is discovered from `acordia-analysts/skills/` and is invokable

#### Scenario: Body carries the six required sections

- **WHEN** the skill is inspected
- **THEN** it contains a cross-cutting notice, a FollowTheMoney data-model section, a conditional tooling paragraph, an inventory-first and facet-first method, a limits section, and a take-assessment section

#### Scenario: Trigger-quality description

- **WHEN** a session must analyse take that has been ingested into an Aleph instance
- **THEN** the skill's `description` is specific enough for the harness to select it without a per-agent binding

#### Scenario: Not a grid row

- **WHEN** the competency grid in `docs/roles/operational-analyst.md` is inspected
- **THEN** no row corresponds to `aleph-entity-graph`

#### Scenario: All three ceilings are stated

- **WHEN** the limits section is read
- **THEN** it names the 9999 search window, the separate per-property expansion cap, and the WRITE requirement on `_stream`, and states the analytic consequence of each

#### Scenario: Tool references degrade instead of assuming a harness

- **WHEN** the skill runs in a harness that mounts the MCP tools under a different prefix from the one an example gives, or mounts none at all
- **THEN** the body has already stated that the prefix is the harness's and not the server's, directing the analyst to match on the tool verb, and has named the `bash` + HTTP API fallback for the no-mount case

#### Scenario: Fallback names what it costs

- **WHEN** the tooling paragraph's fallback branch is read
- **THEN** it states that the analyst inherits bounding, text-stripping, caption derivation and the read-only allowlist, so the fallback is a transfer of responsibility rather than an equivalent path

#### Scenario: Resolved identities are reachable from a search hit

- **WHEN** the method's pivot step is read
- **THEN** it names the profile-scoped pivots and the `profile_id` field that reaches them, and states that a profile-scoped pivot is preferred where a profile exists

#### Scenario: Query semantics are stated, not assumed

- **WHEN** the narrowing step or the limits section is read
- **THEN** it states that entity-search `q` is not fuzzy, names `match_entity` as the tolerant name-lookup path, and states that a multi-term `q` matches on 66% of its terms

#### Scenario: A profile is distinguished from a candidate match

- **WHEN** the take-assessment section is read
- **THEN** an unjudged `xref_results` or `similar_entities` match is still routed to `hypothesis-testing`, and a profile is named as a recorded human decision that can itself be wrong and is scoped per collection

#### Scenario: Read-only posture is explicit

- **WHEN** the guardrails section is read
- **THEN** ingestion, entity writes, tagging, cross-reference triggering and deletion are named as out of scope, and the READ-scoped API key is named as the enforcement point

#### Scenario: Scope is the method's first decision

- **WHEN** the method's first step is read
- **THEN** it requires `collection` on every search, names the id, `foreign_id` and list forms, names
  `collection="*"` as the only instance-wide scope with its `_note` annotation, and states that
  `collection_id` inside `filters` is refused

#### Scenario: An unscoped search is answered, not refused

- **WHEN** the first step's rationale is read
- **THEN** it states that a search naming no collection returns another collection's rows, ranked and
  plausible, with no error, no warning and no empty result

#### Scenario: The applied scope is read back rather than assumed

- **WHEN** a search reply is handled
- **THEN** the method directs the analyst to read `searched.collection` and confirm the resolved ids
  are the ones asked for

#### Scenario: Narrowing does not carry scope

- **WHEN** the narrowing step is read
- **THEN** collection is named as not among the `filters` keys, and the reader is pointed back at the
  `collection` argument

#### Scenario: The fallback path names its unenforced scope

- **WHEN** the `curl` fallback branch is read
- **THEN** its example URL carries a `filter:collection_id` constraint and the prose states that an
  omitted one searches every readable collection with nothing in the response to signal it

#### Scenario: A hit's collection is checked against the scope

- **WHEN** the take-assessment section is read
- **THEN** it requires verifying a hit's own `collection_id` against the collection that was scoped
  to, and names that mismatch as the failure's only symptom

### Requirement: Every skill declares its family

Every `SKILL.md` SHALL declare `metadata.acordia.family`, naming exactly one of five families:
`analytic-spine`, `target-modelling`, `defender-reading`, `evidence-forensics`, `take-handling`. The
seven families the ported library used — `web-attack`, `web-methodology`, `host-postexploit`,
`cloud-postexploit`, `directory-attack`, `mobile`, `operations-discipline` — retire with it, and no
skill SHALL declare one. The tag is documentation, not a gate: nothing enforces it and no harness
reads it. It exists so a reader can see which skills compete for selection, and so the description
contract in *The description is the selection surface* has a defined set of siblings to discriminate
against.

The field SHALL sit inside the existing `metadata.acordia` block. `target-modelling` spans both the
Mission and Terrain columns of the grid and SHALL NOT be renamed or split to match them: the value
names a body of subject matter rather than an agent, nothing reads it, and splitting it would edit ten
skill files to no observable effect.

The scenario *Provenance is untouched* keeps its published title although no provenance block remains,
because OpenSpec matches a MODIFIED block's scenarios by title and a retitled one reads as dropped.

#### Scenario: Every skill lands in exactly one family

- **WHEN** every skill's `metadata.acordia.family` value is collected
- **THEN** each skill declares exactly one, every value is one of the five, and every family has at least one member

#### Scenario: A retired family value is absent

- **WHEN** the library's family values are collected
- **THEN** none is `web-attack`, `web-methodology`, `host-postexploit`, `cloud-postexploit`, `directory-attack`, `mobile` or `operations-discipline`

#### Scenario: Provenance is untouched

- **WHEN** a skill's frontmatter is read after the family tag is added
- **THEN** there is no `metadata.cyberstrike` block left to disturb, because the ported library that carried upstream attribution is gone

### Requirement: The library is the analyst library, sized by the grid rather than by this spec

With `acordia-operators/` deleted, the distribution SHALL hold exactly one skill library: every
`SKILL.md` in the repository SHALL live under `acordia-analysts/skills/`. The ported technique library
SHALL be gone from the tree rather than folded into the analyst library — no cloned body, no
`wstg-*` bundle, no `attack-*`, `*-postexploit`, `mobile-*`, `operation-journal` or `bolts` directory
SHALL be carried across.

The library's size SHALL be stated as an arithmetic, never as a fixed total: **one skill per skill row
of the appendix grid in `docs/roles/operational-analyst.md`, plus the named procedural cross-cutting
skills** — `analyst-loop`, `credential-harvest-triage`, `exhaustive-data-processing` and
`aleph-entity-graph`. The row count is fixed by the grid, not by this specification. The grid's own
content edits land in a later phase of this change, so any total written here would be a claim about a
file this delta does not touch: at the time the delta is written the grid carries 38 skill rows and
those four procedural skills exist, so the library holds 42, and that is a reading of the grid rather
than a requirement on it. A later grid edit SHALL change the expected total without changing this
requirement.

No requirement, prompt, catalog entry, manifest or document SHALL assert a two-pillar or combined
skill total, because there is one library. Where a number is needed it SHALL be obtained by counting
`acordia-analysts/skills/*/SKILL.md` at the time of reading.

#### Scenario: One library, one path root

- **WHEN** the repository is enumerated for `SKILL.md` files
- **THEN** every match lives under `acordia-analysts/skills/`, and no `acordia-operators/` path exists

#### Scenario: The total is the grid's arithmetic

- **WHEN** the library is counted against the grid
- **THEN** the file count equals the grid's skill-row count plus the four named procedural skills, and no requirement fixes a different total

#### Scenario: A grid edit moves the count without touching this requirement

- **WHEN** a skill row is added to or removed from the grid
- **THEN** the expected library total changes with it, and this requirement is unchanged, because it fixes the arithmetic and not the number

#### Scenario: No combined total survives

- **WHEN** the live specs and the shipped tree are searched for a combined two-pillar skill total — a single figure claiming to count both libraries, or an "analyst pillar holds N and the operations pillar holds M" phrasing — excluding `openspec/changes/archive/**`, which records what was true when each change shipped
- **THEN** no match remains

#### Scenario: The library stays markdown-only

- **WHEN** every file under `acordia-analysts/skills/` is inspected
- **THEN** each is a `.md` file, and no Python or other executable script has been added

### Requirement: Reporting skills state a rendering and citation discipline

A skill that governs a written product handed to a decision-maker SHALL state the discipline for
rendering that product into a second format and for citing identifiers inside it. `briefing-reporting`
is that skill and SHALL carry all three of the following.

It SHALL require a second format — HTML, PDF, a deck — to be produced with a real parser for that
format, and SHALL name a hand-written line-prefix pass as the thing not to do. It SHALL state the
reason rather than only the rule: inline emphasis, code spans, tables and inline links are what a
regex converter drops, and it drops them without erroring, so the output is well-formed and wrong in
the places nobody inspected. It SHALL require the analyst to probe for an available parser and to say
which one was used, and SHALL NOT name a specific parser, which is a property of the host rather than
of the distribution.

It SHALL require an identifier cited in the product to be carried whole, however long, and SHALL
state that a shortened hash or a truncated id reads as a citation while being unlookupable. It SHALL
separate display from record: the rendering may shorten what is *displayed*, never what is
*recorded*.

It SHALL require a rendered product to be verified twice over — that no source-format tokens survive
in the output, and that a sample of its evidence references has been resolved against the system that
issued them — and SHALL name a link count as detecting neither failure, because a truncated
identifier produces a well-formed link to nothing and a count is satisfied identically by working and
broken references.

#### Scenario: A rendered product is converted with a parser

- **WHEN** the reporting skill's method is read by an analyst who must also produce HTML, PDF or a deck
- **THEN** it requires a real parser for that format, names a hand-written line-prefix or regex pass
  as dropping inline emphasis, code spans, tables and inline links without erroring, and requires the
  parser actually used to be named

#### Scenario: Identifiers are cited in full

- **WHEN** the reporting skill's method is read
- **THEN** it requires the whole identifier to be carried into the product however long it is, states
  that a truncated identifier cannot be looked up, and confines shortening to what is displayed
  rather than what is recorded

#### Scenario: A rendered product's references are resolved, not counted

- **WHEN** the reporting skill's signals and outputs are read
- **THEN** a finished rendered product requires both that no source-format tokens survive and that a
  sample of its references has been resolved against the issuing system, and a link count is named as
  proving neither

### Requirement: Aleph tool calls name the identifier argument and are built in code

`aleph-entity-graph` SHALL state how a call to the Aleph tools is constructed, in a subsection placed
with its tooling paragraph rather than inside its numbered method, because argument construction
applies to every call at every step rather than once per investigation.

It SHALL name `entity_id` as the identifier argument on every tool that takes one — `get_entity`,
`get_entity_text`, `expand_entity`, `entity_tags`, `similar_entities` — SHALL name `profile_id` for a
profile, and SHALL name `id` and `entity` as the wrong keys. It SHALL state that an unrecognised
argument key is dropped rather than refused, and SHALL name both resulting outcomes: a failure naming
a missing `entity_id`, or a call that reaches the server and returns a not-found which reads as a bad
identifier rather than as a bad call. It SHALL state that the second outcome is why the mistake
repeats undetected.

It SHALL require the argument object to be built with a JSON serialiser inside a script rather than
written by hand, SHALL name quoted-phrase escaping as the failure — a `q` joining quoted phrases with
`OR` needs every inner quote escaped, and a hand-written object escapes the first phrase and then
stops — and SHALL cross-reference `analytic-tooling-scripting` as the same path already recommended
for replacing many interactive calls with one loop.

Every argument name stated SHALL be traceable to the `aleph-mcp` server's own tool signatures rather
than to recollection of them.

#### Scenario: The identifier argument is named

- **WHEN** the tooling section of `aleph-entity-graph` is read
- **THEN** `entity_id` is named as the identifier argument on `get_entity`, `get_entity_text`,
  `expand_entity`, `entity_tags` and `similar_entities`, `profile_id` is named for a profile, and
  `id` and `entity` are named as wrong

#### Scenario: An unrecognised argument key is named as silently dropped

- **WHEN** the same section is read
- **THEN** it states that an unrecognised key is dropped rather than refused, and names the
  not-found reply that reads as a bad identifier instead of a bad call as the reason the mistake
  survives repetition

#### Scenario: Query arguments are serialised rather than hand-written

- **WHEN** an analyst must issue a search whose `q` carries more than one quoted phrase
- **THEN** the skill requires the argument object to be serialised in code, names inner-quote
  escaping past the first phrase as the failure, and points at `analytic-tooling-scripting`
