# competency-map-derivation Specification

## Purpose
Establishes the competency grid in `docs/roles/operational-analyst.md` as the single source of truth for the analyst agents and skills, and fixes the derivation rules: row-to-skill bijection, column-to-agent prompt skill sets, deep-versus-working mark semantics, and the structural mappings from grid to artifact.

## Requirements

### Requirement: The competency grid is the single source of truth

The appendix grid in `docs/roles/operational-analyst.md` SHALL be the authoritative source for the analyst agents and skills. Agents and skills SHALL be derived from it, and SHALL NOT be hand-maintained in parallel with it.

#### Scenario: Grid edit drives regeneration
- **WHEN** a cell or row in the grid changes
- **THEN** the affected skills and/or agent prompt skill sets are regenerated from the grid, not edited independently

### Requirement: Row-to-skill mapping is one-to-one

Each skill row of the grid SHALL compile to exactly one library skill, and each library skill SHALL trace back to exactly one grid row. There SHALL be no skill without a row and no row without a skill.

#### Scenario: Bijection holds
- **WHEN** the grid rows and the library skills are enumerated
- **THEN** they form a one-to-one correspondence

### Requirement: Column-to-agent mapping (prompt skill set)

Each of the four grid columns (Core, T&N, Def, Fus) SHALL define one agent's skill set: Core → `operational-analyst`, T&N → `target-network-analyst`, Def → `defender-detection-analyst`, Fus → `fusion-analyst`. A cell mark places its row's skill into that agent's **prompt skill set** (opencode has no `skills:` frontmatter field).

#### Scenario: Column defines the agent's set
- **WHEN** the T&N column is read top to bottom
- **THEN** every marked row's skill is named in `target-network-analyst`'s prompt, and unmarked rows are not

### Requirement: Mark semantics — deep versus working

A `●` mark SHALL denote a deep/defining skill for that agent and a `○` mark SHALL denote a working/baseline skill; both place the skill in the agent's prompt skill set, but the distinction SHALL be preserved for prompt emphasis and documentation.

#### Scenario: Deep and working both included, distinctly
- **WHEN** a row has `●` in one column and `○` in another
- **THEN** the skill is named in both agents' prompts, marked deep for the first and working for the second

### Requirement: Structural mappings from grid to artifact

The derivation SHALL bind the grid's structure to artifacts as follows: the leg's italic operating question → subagent `description`; the leg's prose paragraph → agent prompt body; the grid's section header → a documentation grouping of the skills (opencode has no `category` field).

#### Scenario: Italic question becomes the dispatch signal
- **WHEN** a leg's italic operating question is read
- **THEN** it is used (in meaning) as that subagent's `description`

### Requirement: Frontmatter carries grid anchor

Every artifact derived from `docs/roles/operational-analyst.md` SHALL carry a `metadata.acordia` frontmatter block anchoring it to its origin in the grid. opencode's frontmatter contract (workbook §6) admits arbitrary `metadata.*` fields and silently ignores unknown keys, so this addition is spec-driven, not runtime-required.

For an agent the block SHALL carry `pillar` (the source pillar directory), `role` (`orchestrator` or `specialist`), `column` (the grid column the agent compiles from), and `source_paragraph` (the anchored prose). The `leg` key SHALL NOT be used: it duplicated an identity the filename already carries, and it forked the anchor schema against the operators pillar, which had reached the same distinction under the name `role`. One key name for one meaning is what lets the generator read the anchor without knowing which pillar it came from.

For a skill the block SHALL carry `grid_row` — the anchored row, or `null` together with `procedural: true` for a cross-cutting skill that corresponds to no row.

#### Scenario: An agent anchor is readable without pillar-specific handling

- **WHEN** any agent file in either pillar is read
- **THEN** its `metadata.acordia` declares `pillar` and `role`, so a reader needs no pillar-aware branch to learn which agent is the orchestrator

#### Scenario: Grid provenance survives the unification

- **WHEN** an analyst agent's anchor is read
- **THEN** it still declares `column` and `source_paragraph`, the two anchors that are genuinely specific to a grid-derived artifact

#### Scenario: Grid-row skill carries the four keys

- **WHEN** any `analysts/skills/<row-slug>/SKILL.md` derived from a grid row is inspected
- **THEN** its frontmatter contains `metadata.acordia` with `grid_row`, `grid_deep_in`, `grid_working_in`, and `source`

#### Scenario: Procedural skill declares its non-grid status

- **WHEN** `analysts/skills/credential-harvest-triage/SKILL.md` is inspected
- **THEN** its `metadata.acordia` contains `grid_row: null`, `procedural: true`, and `source` pointing at an openspec change

#### Scenario: Agent carries pillar, role, column, and paragraph anchor

- **WHEN** any `analysts/agents/*.md` file is inspected
- **THEN** its frontmatter contains `metadata.acordia` with `pillar`, `role`, `column`, and `source_paragraph`, and carries no `leg` key

#### Scenario: Column-mark set matches marks in the grid

- **WHEN** a skill's `grid_deep_in` ∪ `grid_working_in` is compared against the columns marked on its row in `docs/roles/operational-analyst.md`
- **THEN** the two sets are equal and disjoint (`grid_deep_in` covers `●`, `grid_working_in` covers `○`)

#### Scenario: Row slug matches skill name

- **WHEN** a grid-row skill's `metadata.acordia.grid_row` is compared against its frontmatter `name`
- **THEN** they are identical

#### Scenario: Schema is exhaustive

- **WHEN** an artifact's `metadata.acordia` is inspected
- **THEN** it contains only the keys declared for its class (grid-row skill / procedural skill / agent), and no others
