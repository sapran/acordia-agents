## MODIFIED Requirements

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

### Requirement: Column-to-agent mapping (prompt skill set)

Each of the four grid columns (Core, T&N, Def, Fus) SHALL define one agent's skill set: Core →
`operational-analyst`, T&N → `target-network-analyst`, Def → `defender-detection-analyst`, Fus →
`fusion-analyst`. A cell mark places its row's skill into that agent's **prompt skill set**, named on
the agent's `·`-separated skill lines, because neither target harness binds skills to an agent through
frontmatter.

#### Scenario: Column defines the agent's set
- **WHEN** the T&N column is read top to bottom
- **THEN** every marked row's skill is named in `target-network-analyst`'s prompt, and unmarked rows are not

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

## REMOVED Requirements

### Requirement: Frontmatter carries grid anchor

**Reason**: The requirement bound the anchor to *every* derived artifact, agents included, and specified the agent-side keys (`pillar`, `role`, `column`, `source_paragraph`) plus a schema-exhaustiveness rule covering them. Agent frontmatter is now exactly `name`, `description`, `color`, so the agent half of the requirement has no artifact left to describe.

**Migration**: The skill half is restated below as `Skill frontmatter carries the grid anchor`, unchanged in substance. Agent provenance is read from `docs/roles/operational-analyst.md` and `docs/roles/operator.md` instead of from frontmatter.

## ADDED Requirements

### Requirement: Skill frontmatter carries the grid anchor

Every **skill** in `acordia-analysts/skills/` SHALL carry a `metadata.acordia` frontmatter block
anchoring it to its origin. A grid-row skill SHALL carry `grid_row` — the anchored row — together
with `grid_deep_in`, `grid_working_in` and `source`. A procedural cross-cutting skill that
corresponds to no row SHALL carry `grid_row: null`, `procedural: true` and `source` naming the
openspec change that introduced it, and MAY additionally carry `cross_cutting: true` and a
`composes` list of the grid-row slugs it draws together. `source` SHALL resolve to a path that
exists in the repository.

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

- **WHEN** all 43 analyst skills' `metadata.acordia` blocks are enumerated
- **THEN** each declares `grid_row` (a row slug or `null`) and a `source` whose path exists in the repository

#### Scenario: Skill anchor schema is exhaustive

- **WHEN** a skill's `metadata.acordia` is inspected
- **THEN** it contains only the keys declared for its class — `grid_row`/`grid_deep_in`/`grid_working_in`/`source` for a grid-row skill, `grid_row`/`procedural`/`source` plus the optional `cross_cutting`/`composes` for a procedural one — and no others
