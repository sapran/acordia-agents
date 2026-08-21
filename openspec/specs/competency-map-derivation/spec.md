# competency-map-derivation Specification

## Purpose

Establishes the competency grid in `docs/roles/operational-analyst.md` as the single source of truth for the analyst agents and skills, and fixes the derivation rules: row-to-skill bijection, column-to-agent prompt skill sets, deep-versus-working mark semantics, stable row identity, and the structural mappings from grid to artifact.

## Requirements

### Requirement: The competency grid is the single source of truth

The appendix grid in `docs/roles/operational-analyst.md` SHALL be the authoritative source for the
analyst agents and skills. Agents and skills SHALL be derived from it, and SHALL NOT be hand-maintained
in parallel with it. No tool compiles the grid forward: the derivation is performed by whoever edits
the grid, in the same change, which is why the grid edit SHALL come first and the artifacts SHALL
follow it rather than the reverse.

#### Scenario: Grid edit drives regeneration

- **WHEN** a cell or row in the grid changes
- **THEN** the affected skills and agent prompt skill sets are updated from the grid in the same change, not edited independently

#### Scenario: The grid moves first

- **WHEN** a skill is added, merged or removed
- **THEN** the grid row is edited before the skill directory and the prompt lines are touched

### Requirement: Row-to-skill mapping is one-to-one

Each skill row of the grid SHALL compile to exactly one library skill, and each library skill SHALL trace back to exactly one grid row. There SHALL be no skill without a row and no row without a skill.

#### Scenario: Bijection holds

- **WHEN** the grid rows and the library skills are enumerated
- **THEN** they form a one-to-one correspondence

### Requirement: Column-to-agent mapping (prompt skill set)

Each of the four grid columns (Core, T&N, Def, Fus) SHALL define one agent's skill set: Core →
`cyber-analyst`, T&N → `target-analyst`, Def → `overwatch-analyst`, Fus →
`fusion-analyst`. A cell mark places its row's skill into that agent's **prompt skill set**, named on
the agent's `·`-separated skill lines, because neither target harness binds skills to an agent through
frontmatter.

#### Scenario: Column defines the agent's set

- **WHEN** the T&N column is read top to bottom
- **THEN** every marked row's skill is named in `target-analyst`'s prompt, and unmarked rows are not

### Requirement: Mark semantics — deep versus working

A `●` mark SHALL denote a deep/defining skill for that agent and a `○` mark SHALL denote a working/baseline skill; both place the skill in the agent's prompt skill set, but the distinction SHALL be preserved for prompt emphasis and documentation.

#### Scenario: Deep and working both included, distinctly

- **WHEN** a row has `●` in one column and `○` in another
- **THEN** the skill is named in both agents' prompts, marked deep for the first and working for the second

### Requirement: Structural mappings from grid to artifact

The derivation SHALL bind the grid's structure to artifacts as follows: the leg's italic operating
question → subagent `description`; the leg's prose paragraph → agent prompt body; the grid's section
header → a documentation grouping of the skills, carried as the skill's `metadata.acordia` family tag
rather than as a harness field, because neither harness has a skill `category`.

#### Scenario: Italic question becomes the dispatch signal

- **WHEN** a leg's italic operating question is read
- **THEN** it is used (in meaning) as that subagent's `description`

#### Scenario: Section header becomes a documented grouping

- **WHEN** a grid section header is read
- **THEN** the skills beneath it are grouped under one family in documentation and in skill metadata, not under a harness-level category

### Requirement: Skill frontmatter carries the grid anchor

Every **skill** in `acordia-analysts/skills/` SHALL carry a `metadata.acordia` frontmatter block
anchoring it to its origin. A grid-row skill SHALL carry `grid_row` — the anchored row — together
with `grid_deep_in`, `grid_working_in` and `source`. A procedural cross-cutting skill that
corresponds to no row SHALL carry `grid_row: null`, `procedural: true` and `source` naming the
openspec change that introduced it, and MAY additionally carry `cross_cutting: true` and a
`composes` list of the grid-row slugs it draws together. `source` SHALL resolve to a path that
exists in the repository.

Every such block also carries the `family` key required by `skill-library`, which sits in the same
`metadata.acordia` block alongside the anchor.

**Agents SHALL carry no anchor.** An agent file's frontmatter is exactly `name`, `description` and
`color`, so the pillar, role, column and source paragraph that the anchor used to carry are recorded
in `docs/roles/operational-analyst.md` and in the agent's own prompt body instead. The anchor existed
to let a generator read an artifact's provenance without knowing its pillar; with the generator gone,
the reader is a person, and a fifth and sixth frontmatter key on an agent buys nothing.

#### Scenario: Grid-row skill carries the four keys

- **WHEN** any `acordia-analysts/skills/<row-slug>/SKILL.md` derived from a grid row is inspected
- **THEN** its frontmatter contains `metadata.acordia` with `grid_row`, `grid_deep_in`, `grid_working_in` and `source`

#### Scenario: Procedural skill declares its non-grid status

- **WHEN** `acordia-analysts/skills/credential-harvest-triage/SKILL.md` is inspected
- **THEN** its `metadata.acordia` contains `grid_row: null`, `procedural: true`, and `source` pointing at an openspec change

#### Scenario: Column-mark set matches marks in the grid

- **WHEN** a skill's `grid_deep_in` ∪ `grid_working_in` is compared against the columns marked on its row in `docs/roles/operational-analyst.md`
- **THEN** the two sets are equal and disjoint (`grid_deep_in` covers `●`, `grid_working_in` covers `○`)

#### Scenario: Row slug matches skill name

- **WHEN** a grid-row skill's `metadata.acordia.grid_row` is compared against its frontmatter `name`
- **THEN** they are identical

#### Scenario: Agent carries no metadata block

- **WHEN** any agent file in either pillar is inspected
- **THEN** its frontmatter is exactly `name`, `description` and `color`, with no `metadata` key

#### Scenario: Every analyst skill is anchored and its source resolves

- **WHEN** all 42 analyst skills' `metadata.acordia` blocks are enumerated
- **THEN** each declares `grid_row` (a row slug or `null`) and a `source` whose path exists in the repository

#### Scenario: Skill anchor schema is exhaustive

- **WHEN** a skill's `metadata.acordia` is inspected
- **THEN** it contains only the keys declared for its class — `family` plus `grid_row`/`grid_deep_in`/`grid_working_in`/`source` for a grid-row skill, and `family` plus `grid_row`/`procedural`/`source` with the optional `cross_cutting`/`composes` for a procedural one — and no others

### Requirement: Merging two rows moves the grid first and preserves both marks

Where two grid rows describe one judgement, they MAY be merged into one row, and the merge SHALL be
performed in the grid before any skill directory or prompt line is touched. The surviving row's marks
SHALL be the union of the two rows' marks, taking the stronger mark per column, because a column that
held `●` on either row still owns the merged competency deeply.

The merge SHALL be a fold, not a deletion: every distinct element of the absorbed skill's Method SHALL
be present in the surviving skill's body afterwards. `Outcome judgement` absorbing
`Effect-on-target verification` is the worked case — the observable-channel inventory, the first-party
versus independent-confirmation split, the `<log>:<offset>` citation form and the honeypot tells all
survive in `outcome-judgement`.

#### Scenario: Grid changes before the artifacts

- **WHEN** two rows are merged
- **THEN** the grid edit and the artifact edits land in the same change, with the grid stated as the reason for the artifact change

#### Scenario: Stronger mark wins per column

- **WHEN** the `Outcome judgement` row absorbs the `Effect-on-target verification` row
- **THEN** the T&N column reads `●` rather than `○`, because that column held the deep mark on the absorbed row

#### Scenario: Nothing is dropped in the fold

- **WHEN** the surviving skill is compared against the absorbed skill's Method
- **THEN** every distinct element of the absorbed Method appears in the survivor, and the absorbed directory no longer exists

#### Scenario: No dangling reference remains

- **WHEN** the repository is searched for the absorbed skill's slug
- **THEN** no prompt, skill body, spec, document or command wrapper names it
