## ADDED Requirements

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

## MODIFIED Requirements

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

Each `SKILL.md` SHALL declare `name` (lowercase-hyphen, 1-64 characters) and `description` (1-1024
characters), and MAY declare `metadata`. It SHALL declare no other key. A `metadata` block SHALL carry
the `acordia` key alone: with the ported library gone, no `metadata.cyberstrike` block remains anywhere
in the tree, and one SHALL NOT be reintroduced except by a change that ports material and needs a
provenance record for it.

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
- **THEN** `name` matches the kebab-case pattern and is at most 64 characters, `description` is 1-1024 characters, and the body is non-empty

#### Scenario: No signing or restriction fields

- **WHEN** any skill's frontmatter is inspected
- **THEN** it carries no `sha256`, `signature`, `signed_by`, `tools`, or `permission` key

#### Scenario: No provenance block survives the strip

- **WHEN** any skill's `metadata` block is read
- **THEN** it carries `acordia` and no `cyberstrike` key, because the library that recorded upstream attribution is gone

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

- **WHEN** every description under `acordia-analysts/skills/` is read
- **THEN** none begins with `Use when`, `Apply when`, `Use to`, `Use this skill` or an equivalent selection-boilerplate clause

#### Scenario: The worked collision is separated

- **WHEN** `multi-source-fusion` and `maintaining-operating-picture` descriptions are compared
- **THEN** one names consolidating disconnected strands into one coherent picture and the other names stopping an already-fused picture from rotting — timestamping, decay on perishable facts, re-verification before reliance — rather than a shared "target picture" phrasing

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

## REMOVED Requirements

### Requirement: Thirty operations skills cloned from CyberStrike

**Reason**: `acordia-operators/` is deleted, so neither the thirty cloned directories nor the skills authored beside them have a pillar to live in or a library to bound.

**Migration**: Nothing is carried into `acordia-analysts/`. `docs/roles/operator.md` is archived rather than deleted, so the port record — what came from commit `359655518`, what was excluded, and what was authored here — stays readable; an installation that already holds `acordia-operators` keeps its copy, frozen at 4.2.0, until it is uninstalled by hand.

### Requirement: Provenance recorded in metadata

**Reason**: No skill is cloned any more, so there is no `metadata.cyberstrike` block left to carry a source path and no upstream diff to keep mechanical.

**Migration**: The prohibition on reintroducing the block is stated in `Skill frontmatter contract`; the upstream paths themselves remain in the archived `docs/roles/operator.md`.

### Requirement: Bodies carry no tool the harness lacks

**Reason**: The requirement bounded cloned bodies to tools the two harnesses actually have, and there are no cloned bodies left to bound.

**Migration**: The invariant its last scenario carried — the repository stays markdown-only, no executable script is vendored — is kept, as a scenario of `The library is the analyst library, sized by the grid rather than by this spec`.

### Requirement: Bodies otherwise preserve upstream methodology

**Reason**: It governed the diff between a cloned body and its CyberStrike source; with no cloned bodies, there is nothing to diff.

**Migration**: None. The upstream repository remains the source for anyone who wants that technique text.

### Requirement: Corpus skills are not published

**Reason**: The corpora were excluded from the operations pillar, which no longer exists, and no analyst skill derives from `.cyberstrike/skill/`.

**Migration**: The exclusion and its prompt-cost reason stay recorded in the archived `docs/roles/operator.md`, so the ~190,000-token argument survives the pillar it was made about.

### Requirement: A technique has exactly one owning skill

**Reason**: Its subject is the technique content the operations pillar shipped — payloads and commands with a single owning skill. The analyst library ships no technique content, so the requirement has no artifact to govern.

**Migration**: Overlap between analyst skills is governed by `The description is the selection surface`: within a family no two descriptions compete, and an inseparable pair is merged rather than bounded by an ownership sentence.

### Requirement: `operation-journal` skill exists

**Reason**: The skill and the five operations prompts that deferred to it are deleted, so `.acordia/ops/` has no writer and the severity, confidence and journal contracts have no reader.

**Migration**: An analyst product is written under the analyst prompts' own `.acordia/reports/` convention; the journal contract stays readable in the repository's history at 4.2.0.

### Requirement: `gcp-postexploit` skill exists

**Reason**: It existed so `cloud-security`'s GCP claim had a skill behind it, and both that agent and this skill are deleted with the pillar.

**Migration**: None. No analyst skill claims GCP post-exploitation; `cloud-controlplane-analysis` reads a control plane's collected evidence and makes no target contact.

### Requirement: Five mobile skills exist

**Reason**: The five `mobile-*` skills and the `mobile-application` prompt whose technique text they held are deleted with the pillar.

**Migration**: None. Mobile technique content is not carried into the analyst library.

### Requirement: `attack-sqli` skill exists

**Reason**: SQL injection payloads and `sqlmap` reference content are technique material of the deleted pillar, and the `wstg-injection` bundle it was split out of is deleted with it.

**Migration**: None. The analyst library reads already-collected material and ships no attack payloads.

### Requirement: `linux-postexploit` skill exists

**Reason**: Post-exploitation on a held shell is target contact, which no agent in the distribution performs after this change; its boundary partner `ebpf-attacks` is deleted too.

**Migration**: None. Host evidence already collected is read by `os-host-internals` and `disk-memory-forensics`, which escalate nothing.

### Requirement: A bundle points at a dedicated skill rather than restating it

**Reason**: The four WSTG bundles it governed and the dedicated skills they pointed at are all deleted, so there is no bundle to reduce and no destination to check first.

**Migration**: None.

### Requirement: `bolts` skill exists

**Reason**: A bolt is a remote position holding offensive tooling aimed at an engagement target; with no agent making target contact, the posture has nothing left to separate from local work.

**Migration**: None. Analyst work reads collected material from wherever the session runs, and no analyst skill dials a target.
