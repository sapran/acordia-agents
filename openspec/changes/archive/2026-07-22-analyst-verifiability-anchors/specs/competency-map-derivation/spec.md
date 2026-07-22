## ADDED Requirements

### Requirement: Frontmatter carries grid anchor

Every artifact derived from `docs/roles/operational-analyst.md` SHALL carry a `metadata.acordia` frontmatter block anchoring it to its origin in the grid. opencode's frontmatter contract (workbook §6) admits arbitrary `metadata.*` fields and silently ignores unknown keys, so this addition is spec-driven, not runtime-required.

**For grid-row skills** — `metadata.acordia` SHALL declare four keys: `grid_row` (the row slug, matching the skill's `name`); `grid_deep_in` (list of column names in which the skill is marked `●`); `grid_working_in` (list of column names in which the skill is marked `○`); `source` (a citation of the form `docs/roles/operational-analyst.md#L<line>` pointing to the row's line in the grid).

**For procedural cross-cutting skills** (e.g. `credential-harvest-triage`) — `metadata.acordia` SHALL declare `grid_row: null`, `procedural: true`, and `source` pointing at the openspec change that authorised the skill.

**For agents** — `metadata.acordia` SHALL declare three keys: `leg` (the agent's short name — one of `orchestrator`, `target-network`, `defender-detection`, `fusion`); `column` (the grid column the agent maps to — one of `Core`, `T&N`, `Def`, `Fus`); `source_paragraph` (a citation of the form `docs/roles/operational-analyst.md#L<start>-<end>` pointing at the paragraph the prompt body was derived from).

The schema is exhaustive. New keys under `metadata.acordia` SHALL require a further openspec change amending this requirement.

#### Scenario: Grid-row skill carries the four keys

- **WHEN** any `analysts/skills/<row-slug>/SKILL.md` derived from a grid row is inspected
- **THEN** its frontmatter contains `metadata.acordia` with `grid_row`, `grid_deep_in`, `grid_working_in`, and `source`

#### Scenario: Procedural skill declares its non-grid status

- **WHEN** `analysts/skills/credential-harvest-triage/SKILL.md` is inspected
- **THEN** its `metadata.acordia` contains `grid_row: null`, `procedural: true`, and `source` pointing at an openspec change

#### Scenario: Agent carries leg, column, and paragraph anchor

- **WHEN** any `analysts/agents/*.md` file is inspected
- **THEN** its frontmatter contains `metadata.acordia` with `leg`, `column`, and `source_paragraph`

#### Scenario: Column-mark set matches marks in the grid

- **WHEN** a skill's `grid_deep_in` ∪ `grid_working_in` is compared against the columns marked on its row in `docs/roles/operational-analyst.md`
- **THEN** the two sets are equal and disjoint (`grid_deep_in` covers `●`, `grid_working_in` covers `○`)

#### Scenario: Row slug matches skill name

- **WHEN** a grid-row skill's `metadata.acordia.grid_row` is compared against its frontmatter `name`
- **THEN** they are identical

#### Scenario: Schema is exhaustive

- **WHEN** an artifact's `metadata.acordia` is inspected
- **THEN** it contains only the keys declared for its class (grid-row skill / procedural skill / agent), and no others
