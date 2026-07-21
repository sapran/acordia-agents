## ADDED Requirements

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
