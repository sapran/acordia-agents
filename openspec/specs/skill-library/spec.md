# skill-library Specification

## Purpose
Defines the skill libraries the two pillars ship — where a skill lives, the frontmatter contract both
harnesses parse, the description that selects it, the analyst library's one-to-one derivation from the
competency grid, the operations library's upstream provenance, and the reading and reference-file
disciplines their bodies follow.

## Requirements

### Requirement: Skills live in their own pillar under a plain slug

Each skill SHALL live at `acordia-analysts/skills/<slug>/SKILL.md` or
`acordia-operators/skills/<slug>/SKILL.md`, one directory per skill. The slug SHALL be kebab-case
matching `^[a-z0-9]+(-[a-z0-9.]*)*$`, SHALL carry no pillar or distribution prefix, and SHALL equal
the frontmatter `name`, because both harnesses default a skill's name to its directory name. A skill
SHALL exist in exactly one pillar; no skill directory SHALL be duplicated across the two, and no
generated or translated copy of a skill SHALL exist in the repository.

#### Scenario: Slug, name and directory agree

- **WHEN** any skill directory is inspected
- **THEN** its `SKILL.md` frontmatter `name` equals the directory name and carries no prefix

#### Scenario: One copy per skill

- **WHEN** the repository is enumerated for `SKILL.md` files
- **THEN** every one lives under exactly one of the two pillars' `skills/` directories

#### Scenario: Library counts are what each pillar ships

- **WHEN** the two libraries are counted
- **THEN** the analyst pillar holds 42 skills and the operations pillar holds 39, 81 in total

### Requirement: Skill frontmatter contract

Each `SKILL.md` SHALL declare `name` (lowercase-hyphen, 1-64 characters) and `description` (1-1024
characters), and MAY declare `metadata`. It SHALL declare no other key. Every CyberStrike-only field
SHALL stay dropped: `category`, `version`, `author`, `tags`, `owasp_id`, `cis_id`, `cis_benchmark`,
`tech_stack`, `cwe_ids`, `chains_with`, `prerequisites`, `severity_boost`. The signing triple
`sha256` / `signature` / `signed_by` SHALL stay dropped, because a hash that no longer matches an
edited body is worse than no hash. No skill SHALL declare a tool list, a permission map, or any
harness-restriction field.

#### Scenario: Only contract fields present

- **WHEN** any skill's frontmatter is parsed
- **THEN** its keys are a subset of `name`, `description`, `metadata`

#### Scenario: Field values are within the contract

- **WHEN** any skill's frontmatter is validated
- **THEN** `name` matches the kebab-case pattern and is at most 64 characters, `description` is 1-1024 characters, and the body is non-empty

#### Scenario: No signing or restriction fields

- **WHEN** any skill's frontmatter is inspected
- **THEN** it carries no `sha256`, `signature`, `signed_by`, `tools`, or `permission` key

### Requirement: The description is the selection surface

Because both harnesses select a skill by matching its `description`, each `description` SHALL open
with an imperative naming the work only that skill does, and SHALL then give the trigger — the
situation in which that work is wanted. It SHALL be 1–1024 characters.

A description SHALL NOT open with a selection-boilerplate clause: `Use when`, `Apply when`, `Use to`,
`Use this skill`, and their variants are prohibited openings, because they are common to every skill
and therefore discriminate between none of them. A bare topic label SHALL NOT be used either.

Within a family, no two descriptions SHALL compete: each SHALL name work its siblings do not cover.
Where two are inseparable, the two skills SHALL be merged rather than shipped as competing siblings.

#### Scenario: Description states applicability

- **WHEN** any skill's description is read
- **THEN** it states the situation the skill applies to, not merely its topic

#### Scenario: Description discriminates between siblings

- **WHEN** two skills in the same family are compared
- **THEN** each description names work the other does not cover

#### Scenario: Boilerplate openings are absent

- **WHEN** all 81 descriptions are read
- **THEN** none begins with `Use when`, `Apply when`, `Use to`, `Use this skill` or an equivalent selection-boilerplate clause

#### Scenario: The worked collision is separated

- **WHEN** `macos-postexploit` and `windows-postexploit` descriptions are compared
- **THEN** each names its platform's own mechanisms — TCC and keychain against LSASS and DPAPI — rather than a shared "host post-exploitation" phrasing

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

- **WHEN** every analyst skill slug is searched for in the four analyst prompts
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

- Bucket A — identity / directory / cloud-controlplane material → `target-analyst`
- Bucket B — host-forensic material (memory, SAM, DPAPI, keychain, shadow) → whichever leg holds the host under analysis
- Bucket C — web / API auth material → `target-analyst`
- Bucket D — log-artefact material → `overwatch-analyst`
- Bucket E — implant / payload RE material → cross-cutting via `implant-payload-re`, reported to `fusion-analyst`

Each bucket's slice SHALL be dispatched with only that slice. The procedure SHALL state that per-leg classifications feed back into `multi-source-fusion` for cross-leg correlation.

#### Scenario: Triage skill loads in a harness

- **WHEN** a harness loads the analyst pillar
- **THEN** `credential-harvest-triage` is discovered from `acordia-analysts/skills/` and is invokable

#### Scenario: Body carries schema, procedure, and pattern library

- **WHEN** the triage skill is inspected
- **THEN** it contains a classification schema, a bucket-partition step, a numbered triage procedure downstream of the partition, and a pointer to the pattern library at `references/credential-patterns.md`

#### Scenario: Bucket partition maps to existing legs

- **WHEN** the bucket-partition step is read
- **THEN** every bucket routes to one of `target-analyst`, `overwatch-analyst`, `fusion-analyst`, or the cross-cutting `implant-payload-re` skill, and no bucket routes to a leg not on the current whitelist

#### Scenario: Not a grid row

- **WHEN** the competency grid in `docs/roles/operational-analyst.md` is inspected
- **THEN** no row corresponds to `credential-harvest-triage`

### Requirement: `analyst-loop` skill exists

The library SHALL contain a skill `acordia-analysts/skills/analyst-loop/SKILL.md` naming the end-neutral analytic loop — target-read (through the T&N leg), defender-read (through the Def leg), fusion (through the Fus leg), judgement (calibrated, via spine skills), next-move — as a first-class procedural cross-cutting skill.

The skill body SHALL contain: (a) a **cross-cutting notice** declaring the skill procedural and non-grid; (b) a **loop-shape** section naming the five steps in one sentence each; (c) a **loop-invariants** section stating end-neutrality (every pass reaches a judgement plus a next move), gap-naming on every judgement, calibrated confidence on every judgement, and passive posture; (d) a **where-this-runs** paragraph stating the loop is the orchestrator's workflow, and that a leg session matching this skill surfaces the need for a full pass back to the orchestrator rather than attempting the loop itself.

The skill's `description` SHALL be authored for trigger quality — stating WHEN to run the loop, not WHAT it is — so description-match selection fires cleanly on operator sessions asking for a fresh analytic round.

The skill SHALL declare its cross-cutting/procedural nature and SHALL NOT be added as a row to the competency grid. The `## Method` contract for evidence-reading skills (from `analyst-verifiability-anchors`) SHALL NOT apply — this skill reads no files.

#### Scenario: Loop skill loads in a harness

- **WHEN** a harness loads the analyst pillar
- **THEN** `analyst-loop` is discovered from `acordia-analysts/skills/` and is invokable

#### Scenario: Body carries the four required sections

- **WHEN** the loop skill is inspected
- **THEN** it contains a cross-cutting notice, a loop-shape section naming five steps, a loop-invariants section, and a where-this-runs paragraph

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

- **WHEN** any leg agent (`target-analyst`, `overwatch-analyst`, `fusion-analyst`) is inspected
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

The skill body SHALL contain: (a) a **cross-cutting notice** declaring the skill procedural and non-grid and naming the grid rows it composes; (b) a **data-model** section stating that Aleph stores FollowTheMoney entities grouped into collections, that schemata inherit, and that `entity`-typed properties are the graph edges; (c) a **conditional tooling** paragraph naming the MCP server's registered read tools by their bare verbs, stating that a harness may expose them under a mount prefix, and naming the `bash` + HTTP API fallback otherwise; (d) an **inventory-first, facet-first method** — enumerate collections and read their statistics, survey a result set with facets at `limit=0` before pulling rows, narrow with `filter:` constraints, pivot on entities and on resolved identities via expand/tags/similar/match/profiles/entitysets/xref, and read document text last and bounded; (e) a **limits** section stating the ceilings and query semantics that change the method; and (f) a **take-assessment** section feeding `assessing-take-value`.

Clause (c) SHALL NOT mandate a prefixed tool-name form. The `aleph-mcp` server registers its tools unprefixed and its own specification explicitly refuses to guarantee any prefix, stating that the mount configuration is where that expectation is satisfied; a prefix a caller observes is composed by the host from the mount name. The tooling paragraph SHALL therefore name the tool verbs, SHALL state that a harness may apply a mount prefix and give the observed form as an example rather than a requirement, and SHALL direct the analyst to match on the verb rather than on a literal prefix.

The tooling paragraph SHALL state what the `bash` + HTTP fallback gives up relative to the tools, because on that path the analyst inherits the obligations the server was discharging: no refusal at the search ceiling, no expansion cap, no stripping of document-sized text properties, no derived `caption`, and no read-only allowlist between the caller and a write endpoint.

The method's pivot step SHALL name profile-scoped pivots alongside entity-scoped ones, and SHALL name the `profile_id` field carried on search and expansion results as their entry point. It SHALL state the analytic rule that a profile-scoped pivot is preferred over an entity-scoped one where a profile exists, because the entity in hand is one fragment of an actor whose other fragments carry edges invisible from it.

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

### Requirement: Thirty operations skills cloned from CyberStrike

`acordia-operators/skills/` SHALL contain the thirty skill directories cloned from CyberStrike, each
holding a `SKILL.md`:

- **26 standalone technique skills** cloned from `.cyberstrike/skill/<name>/SKILL.md`: `ad-security`,
  `attack-cache-poison`, `attack-cors`, `attack-graphql`, `attack-host-header`,
  `attack-idor-automation`, `attack-jwt`, `attack-open-redirect`, `attack-prototype-pollution`,
  `attack-race-condition`, `attack-rate-limit-bypass`, `attack-request-smuggling`, `attack-ssrf`,
  `attack-ssti`, `attack-subdomain-takeover`, `attack-websocket`, `attack-xxe`, `aws-postexploit`,
  `azure-postexploit`, `cicd-attacks`, `ebpf-attacks`, `k8s-postexploit`, `kerberos-attacks`,
  `macos-postexploit`, `recon-methodology`, `windows-postexploit`.
- **4 OWASP WSTG bundle skills** cloned from
  `.cyberstrike/skill/WEB/OWASP_WSTG_4.2/<name>/SKILL.md`: `wstg-recon-config`, `wstg-auth-session`,
  `wstg-injection`, `wstg-logic-client-api`.

`bun-file-io`, the twenty-seventh standalone CyberStrike skill, SHALL NOT be cloned: it documents Bun
file APIs for CyberStrike's own development and carries no security capability.

The library MAY additionally contain skills **authored in this repository** rather than cloned. Such a
skill SHALL NOT carry `metadata.cyberstrike`, because that block is upstream attribution and claiming
it for local text would corrupt the port record. Seven exist as of 3.1.0: `operation-journal`,
`gcp-postexploit`, and the five `mobile-*` skills. `docs/roles/operator.md` SHALL record them as
authored here, so the provenance record stays a complete account of what the pillar contains.

#### Scenario: Library membership is exact

- **WHEN** `acordia-operators/skills/` is listed
- **THEN** the thirty cloned directories are present, each containing a `SKILL.md`, alongside the skills authored here

#### Scenario: Development skill excluded

- **WHEN** the library is inspected for `bun-file-io`
- **THEN** it is absent

#### Scenario: Authored skills are not dressed as ported

- **WHEN** a skill authored in this repository is inspected
- **THEN** it carries no `metadata.cyberstrike`, and `docs/roles/operator.md` lists it as authored here

### Requirement: Provenance recorded in metadata

Each cloned skill SHALL record its origin under `metadata.cyberstrike` as the repository-relative source path it was cloned from, so a diff against upstream is mechanical.

#### Scenario: Source path recorded

- **WHEN** any operations skill's `metadata.cyberstrike` block is read
- **THEN** it names the `.cyberstrike/skill/...` path the body was cloned from

### Requirement: Bodies carry no tool the harness lacks

A cloned skill body SHALL name no CyberStrike platform tool. Every `attack_script <name>` invocation SHALL be replaced by a standard tool invocation or an explicit inline command carrying the same testing intent, and no body SHALL reference `add_intel`, `report_vulnerability`, `update_vrt_check`, `methodology_status`, `scope_check`, `ensure_tools`, `hackbrowser`, or the `skill` CLI.

The eleven skills that invoke `attack_script` upstream — `attack-jwt`, `attack-idor-automation`, `attack-race-condition`, `attack-subdomain-takeover`, `attack-ssti`, `attack-rate-limit-bypass`, `attack-xxe`, `attack-graphql`, `attack-ssrf`, `attack-open-redirect`, `attack-cors` — SHALL retain the same testing intent, expressed as a standard tool invocation or an explicit inline command.

#### Scenario: No platform tool named

- **WHEN** the thirty skill bodies are searched for CyberStrike platform tool names
- **THEN** none is found

#### Scenario: Replaced invocation keeps the intent

- **WHEN** a former `attack_script` step is compared to its replacement
- **THEN** the replacement performs the same test using a standard tool or an explicit command, rather than dropping the step

#### Scenario: Attack scripts are not vendored

- **WHEN** the repository is inspected after the change
- **THEN** no Python or other executable attack script has been added — the repository remains markdown-only

### Requirement: Bodies otherwise preserve upstream methodology

Apart from the frontmatter reduction and the tool substitutions, a cloned body SHALL preserve its upstream payloads, commands, tables, and phase structure. Cloning SHALL NOT be an occasion to rewrite technique content, because the upstream body is the reviewed artifact.

#### Scenario: Technique content unchanged

- **WHEN** a cloned body is diffed against its CyberStrike source
- **THEN** the differences are confined to frontmatter reduction, tool substitutions, and the section removals required by them

### Requirement: Corpus skills are not published

The generated compliance and technique corpora under `.cyberstrike/skill/` — CIS benchmarks (5,000 skills), NIST control families (1,606), MITRE ATT&CK enterprise, mobile, and ICS (898 combined), and the 121 individual WSTG leaf skills — SHALL NOT be cloned into this pillar. Both harnesses list every discovered skill's name and description in the system prompt, so publishing them would add roughly 190,000 tokens to every session.

#### Scenario: Corpus absent from the library

- **WHEN** `acordia-operators/skills/` is listed
- **THEN** no `cis-*`, NIST-control, or MITRE-technique skill directory is present, and the only `wstg-*` entries are the four bundles

#### Scenario: Exclusion is recorded

- **WHEN** `docs/roles/operator.md` is read
- **THEN** it records the corpora that were not published and the prompt-cost reason

### Requirement: A technique has exactly one owning skill

Every technique the operations pillar ships SHALL have exactly one owning skill. Two skills SHALL NOT
carry the same technique, and a prompt SHALL NOT carry a technique a skill owns. Where a technique
plausibly belongs to two skills, the owner SHALL be stated in both bodies as an explicit boundary
sentence rather than left to the reader.

#### Scenario: No technique has two owners

- **WHEN** a command or payload appears in one operations skill
- **THEN** it does not appear in another, unless one of the two names the other as the owner

#### Scenario: Boundary is written down

- **WHEN** two skills border on the same ground
- **THEN** each body states which of them owns what

### Requirement: `operation-journal` skill exists

`acordia-operators/skills/operation-journal/SKILL.md` SHALL carry the `.acordia/ops/` contract that
the five operations prompts previously restated: the file layout (`scope.md`, `intel.md`, `coverage.md`,
`findings/<slug>.md`, `reports/<name>.md`), the severity scale
(`critical`/`high`/`medium`/`low`/`informational`), the confidence scale
(`confirmed`/`high`/`medium`/`low`), the logging discipline (log intel on discovery rather than in a
batch; read `coverage.md` before claiming a category complete; read `scope.md` before touching a new
target), the evidence-quality rule (the request sent, a concrete response summary, and the reasoning
that proves or disproves the finding), the finding-file shape, and the chaining rule that a chain's
severity is the chain's own, not the maximum of its parts.

#### Scenario: Skill carries the whole contract

- **WHEN** `operation-journal` is read
- **THEN** it states the five file paths, both scales, the logging discipline, the evidence-quality rule, the finding-file shape and the chaining rule

#### Scenario: Prompts stop restating it

- **WHEN** the five operations prompts are searched for the severity or confidence scale
- **THEN** only domain-specific additions remain, and the scales themselves appear once, in the skill

### Requirement: `gcp-postexploit` skill exists

`acordia-operators/skills/gcp-postexploit/SKILL.md` SHALL cover Google Cloud post-exploitation on the
pattern the pillar already uses for `aws-`, `azure-` and `k8s-postexploit`: enumeration of the
identity and project surface, privilege-escalation paths, data and secret access, persistence, and
the logging surface the actions touch. It exists because `cloud-security` claims GCP in its
description and carries GCP technique text; a claim with no skill behind it is the defect this closes.

#### Scenario: GCP claim has a skill behind it

- **WHEN** `cloud-security`'s description and technique lines name GCP
- **THEN** `gcp-postexploit` resolves in the same pillar and carries the GCP technique detail

#### Scenario: Shape matches its siblings

- **WHEN** `gcp-postexploit` is compared with `azure-postexploit`
- **THEN** it follows the same section order and depth

### Requirement: Five mobile skills exist

The operations library SHALL contain `mobile-data-storage`, `mobile-crypto-keys`,
`mobile-platform-ipc`, `mobile-resilience-bypass` and `mobile-instrumentation`, carrying the technique
detail previously held in `mobile-application`'s `## Key techniques by area`. Each SHALL state what it
owns and SHALL NOT compete with its siblings on description. Network, authentication and
business-logic testing for mobile targets SHALL be pointed at the skills that already own them
(`attack-jwt`, `attack-idor-automation`, the `wstg-*` bundles) rather than duplicated.

#### Scenario: Five directories present

- **WHEN** `acordia-operators/skills/` is listed
- **THEN** the five `mobile-*` skills are present, each with a `SKILL.md`

#### Scenario: The admission is gone

- **WHEN** `mobile-application`'s prompt is searched for a claim that the pillar ships no mobile skill library
- **THEN** none is found, and the five slugs appear on its skill lines

#### Scenario: Siblings do not compete

- **WHEN** the five descriptions are compared pairwise
- **THEN** each names work the other four do not cover

### Requirement: `attack-sqli` skill exists

`acordia-operators/skills/attack-sqli/SKILL.md` SHALL carry SQL injection as a first-class skill,
holding the detection payloads, database fingerprinting, union-based extraction, blind-SQLi and
`sqlmap` reference content that `wstg-injection` carried at lines 12–104. It SHALL follow the shape of
`attack-ssrf` and `attack-xxe`, and SHALL carry the `metadata.cyberstrike` `source` and `commit` of the
bundle the text came from, because the text is moved rather than authored.

#### Scenario: SQLi has its own skill

- **WHEN** the `attack-*` family is enumerated
- **THEN** `attack-sqli` is present alongside the other seventeen

#### Scenario: Provenance follows the text

- **WHEN** `attack-sqli`'s frontmatter is read
- **THEN** its `metadata.cyberstrike` names the same `source` path and `commit` as `wstg-injection`

#### Scenario: The bundle no longer carries the method

- **WHEN** `wstg-injection` is read
- **THEN** its SQL-injection entry is a one-line pointer to `attack-sqli`, carrying no payload table

### Requirement: `linux-postexploit` skill exists

`acordia-operators/skills/linux-postexploit/SKILL.md` SHALL cover Linux post-exploitation reachable
with ordinary userland access: SUID/SGID and capability abuse, sudo-rule abuse, cron and
systemd-timer persistence, SSH key and agent-socket theft, shadow handling, container-escape checks
from the host, and kernel-exploit triage. It SHALL follow the shape of `windows-postexploit`.

The boundary with `ebpf-attacks` SHALL be stated in both bodies: `ebpf-attacks` owns anything needing
`CAP_BPF`/`CAP_SYS_ADMIN` and a loaded BPF program; `linux-postexploit` owns what ordinary userland
access reaches.

#### Scenario: Linux userland has a home

- **WHEN** an operator holds a shell on a Linux host without loading a BPF program
- **THEN** `linux-postexploit` resolves and carries the escalation and persistence paths

#### Scenario: Boundary is written in both bodies

- **WHEN** `linux-postexploit` and `ebpf-attacks` are read
- **THEN** each states which of the two owns kernel-instrumentation work and which owns ordinary userland work

### Requirement: Every skill declares its family

Every `SKILL.md` in both pillars SHALL declare `metadata.acordia.family`, naming exactly one of twelve
families: `analytic-spine`, `target-modelling`, `defender-reading`, `evidence-forensics`,
`take-handling`, `web-attack`, `web-methodology`, `host-postexploit`, `cloud-postexploit`,
`directory-attack`, `mobile`, `operations-discipline`. The tag is documentation, not a gate: nothing
enforces it and no harness reads it. It exists so a reader can see which skills compete for selection,
and so the description contract below has a defined set of siblings to discriminate against.

The field SHALL sit inside the existing `metadata.acordia` block on an analyst skill, and SHALL be
added as an `acordia` key beside the untouched `metadata.cyberstrike` block on a ported operations skill.

#### Scenario: Every skill lands in exactly one family

- **WHEN** all 81 skills' `metadata.acordia.family` values are collected
- **THEN** each skill declares exactly one, every value is one of the twelve, and every family has at least one member

#### Scenario: Provenance is untouched

- **WHEN** a ported operations skill's frontmatter is read after the family tag is added
- **THEN** its `metadata.cyberstrike` block is unchanged

### Requirement: A bundle points at a dedicated skill rather than restating it

Where a WSTG bundle covers ground a dedicated skill owns, the bundle SHALL carry a one-line pointer to
that skill instead of the Method. Before a section becomes a pointer, the destination skill SHALL be
confirmed to carry the Method, and any payload, flag or table row the bundle holds and the skill lacks
SHALL be appended to the skill first.

A bundle SHALL keep its WSTG identity, its provenance block, its routing, and every section for which
no dedicated skill exists.

#### Scenario: Duplicated section becomes a pointer

- **WHEN** a bundle section's Method is carried by a dedicated skill
- **THEN** the bundle holds a pointer line naming that skill, and no payload table for it

#### Scenario: Unowned section stays whole

- **WHEN** a bundle section has no dedicated skill — XSS, command injection, LFI/path traversal, HTTP parameter pollution, mass assignment, privilege-escalation patterns
- **THEN** it stays in the bundle in full

#### Scenario: Nothing is lost to a pointer

- **WHEN** a section is reduced to a pointer
- **THEN** every payload and flag it held is present in the destination skill
