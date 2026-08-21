## ADDED Requirements

### Requirement: A row id is minted once, recorded in the grid, and never reused

Every skill row of the grid in `docs/roles/operational-analyst.md` SHALL carry its own stable row id,
recorded in the grid row itself, so that the grid — not a line number and not a skill directory — is
where a row's identity lives. The id SHALL be kebab-case, SHALL be minted once when the row is
created, and SHALL NOT change when the row is reworded, re-marked, moved to another section, or
renamed. Where a row is deleted its id SHALL be retired: it SHALL NOT be reused for a different
competency, because a reused id silently re-points every artifact that cited the old one at a
competency nobody meant.

Nothing in this distribution resolves a row id at install or dispatch time, so an unresolved id can
never fail at runtime — it can only be caught before the change lands. A skill whose `row` matches no
grid row, a grid row carrying no id, and two rows carrying the same id SHALL each be treated as a
defect that blocks the change. Two things catch it: the external drift script
`~/ai/checks/check-acordia.sh`, which this change extends to enumerate the grid's ids and match them
against the skills, and a reviewer reading the grid and the skill frontmatter as a pair. Neither is a
build step, because this repository ships none.

#### Scenario: Every row carries exactly one id

- **WHEN** the grid's skill rows are enumerated
- **THEN** each carries exactly one kebab-case row id, and no two rows carry the same one

#### Scenario: Rewording or moving a row keeps its id

- **WHEN** a row's competency wording changes, its marks change, or it moves to another grid section
- **THEN** its row id is unchanged, and no skill frontmatter is edited on account of the move

#### Scenario: A deleted row's id is retired

- **WHEN** a row is removed from the grid
- **THEN** its id is recorded as retired and is never assigned to a later row

#### Scenario: An unresolvable row id blocks the change

- **WHEN** a skill declares a `row` that matches no grid row
- **THEN** the drift script and the reviewer report it and the change does not land, because no harness would ever report it

## MODIFIED Requirements

### Requirement: Column-to-agent mapping (prompt skill set)

Each of the five grid columns (Core, Mission, Terrain, Def, Coll) SHALL define one agent's skill set:
Core → `cyber-analyst`, Mission → `mission-analyst`, Terrain → `terrain-analyst`, Def →
`overwatch-analyst`, Coll → `collection-analyst`. A cell mark places its row's skill into that agent's
**prompt skill set**, named on the agent's `·`-separated skill lines, because neither target harness
binds skills to an agent through frontmatter.

The column set SHALL be closed: the labels a skill's `grid_deep_in` and `grid_working_in` lists may
carry are exactly those five column headers and no others, so that renaming a column is a single
grid-plus-frontmatter edit rather than a search for whatever spellings accumulated.

#### Scenario: Column defines the agent's set

- **WHEN** the Terrain column is read top to bottom
- **THEN** every marked row's skill is named in `terrain-analyst`'s prompt, and unmarked rows are not

#### Scenario: Five columns, five agents, no orphan

- **WHEN** the grid's column headers are compared against the agents in `acordia-analysts/agents/`
- **THEN** each of the five columns maps to exactly one agent and each agent is named by exactly one column

#### Scenario: Mark lists carry only column labels

- **WHEN** a skill's `grid_deep_in` and `grid_working_in` values are read
- **THEN** every entry is one of Core, Mission, Terrain, Def, Coll

### Requirement: Skill frontmatter carries the grid anchor

Every **skill** in `acordia-analysts/skills/` SHALL carry a `metadata.acordia` frontmatter block
anchoring it to its origin. A grid-row skill SHALL carry `grid_row` — the anchored row — together
with `grid_deep_in`, `grid_working_in`, `row` and `source`. A procedural cross-cutting skill that
corresponds to no row SHALL carry `grid_row: null`, `procedural: true` and `source` naming the
openspec change that introduced it, and MAY additionally carry `cross_cutting: true` and a
`composes` list of the grid-row slugs it draws together. `source` SHALL resolve to a path that
exists in the repository.

**The anchor SHALL NOT carry a line number.** A grid-row skill's `row` SHALL name the grid row's
stable id and its `source` SHALL be exactly `docs/roles/operational-analyst.md`, with no `#L`
fragment. The retired form `source: docs/roles/operational-analyst.md#L<n>` SHALL NOT appear: a line
anchor is invalidated by any edit that shifts a line, and it fails silently, because the anchor still
resolves — to the wrong row. Nothing reads these anchors at install or dispatch time, so a wrong line
number produces no error anywhere; it simply misinforms the next reader. Identity therefore lives in
the row, which moves with its content, rather than in a coordinate that describes where the row
happened to sit.

`grid_row` and `row` are not the same key twice. `grid_row` is the row's current slug and SHALL equal
the skill's frontmatter `name`; `row` is the identity minted once for that row and SHALL survive a
rewording or a rename that changes the slug. Where a row has never been renamed the two strings
coincide, and that coincidence SHALL NOT be relied on.

Every such block also carries the `family` key required by `skill-library`, which sits in the same
`metadata.acordia` block alongside the anchor. A skill whose body rests on a specific work MAY also
carry the optional `doctrine_source` attribution defined by `doctrinal-provenance`, which sits in the
same block and SHALL NOT displace the grid anchor: a grid-row skill keeps `row` and `source` whether
or not it also cites the literature.

**Agents SHALL carry no anchor.** An agent file's frontmatter is exactly `name`, `description` and
`color`, so the role, column and source paragraph that the anchor used to carry are recorded in
`docs/roles/operational-analyst.md` and in the agent's own prompt body instead. The anchor existed to
let a generator read an artifact's provenance without knowing its pillar; with the generator gone, and
with one pillar left, the reader is a person, and a fourth and fifth frontmatter key on an agent buys
nothing.

#### Scenario: Grid-row skill carries the four keys

- **WHEN** any `acordia-analysts/skills/<row-slug>/SKILL.md` derived from a grid row is inspected
- **THEN** its frontmatter contains `metadata.acordia` with `grid_row`, `grid_deep_in`, `grid_working_in` and `source`

#### Scenario: The row id is required alongside the four

- **WHEN** the same block is inspected for the anchor introduced by this change
- **THEN** it also contains `row`, so a grid-row skill carries five keys in total and none of the original four is dropped

#### Scenario: The anchor names a row, not a line

- **WHEN** a grid-row skill's `source` and `row` are read
- **THEN** `source` is exactly `docs/roles/operational-analyst.md` with no `#L` fragment, and `row` matches the id on exactly one grid row

#### Scenario: Inserting a row above the grid invalidates nothing

- **WHEN** a row is inserted near the top of the grid, shifting the line number of every row below it
- **THEN** no skill's `row` or `source` needs editing, and no anchor is left pointing at the wrong competency
- **AND** under the retired `#L<n>` form every shifted row's anchor would have become silently wrong, which is why the form was replaced

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

- **WHEN** any agent file in `acordia-analysts/agents/` is inspected
- **THEN** its frontmatter is exactly `name`, `description` and `color`, with no `metadata` key

#### Scenario: Every analyst skill is anchored and its source resolves

- **WHEN** every `metadata.acordia` block in `acordia-analysts/skills/` is enumerated
- **THEN** each declares `grid_row` (a row slug or `null`) and a `source` whose path exists in the repository
- **AND** no `source` anywhere in the library carries a `#L` fragment

#### Scenario: Skill anchor schema is exhaustive

- **WHEN** a skill's `metadata.acordia` is inspected
- **THEN** it contains only the keys declared for its class — `family` plus `grid_row`/`grid_deep_in`/`grid_working_in`/`row`/`source` for a grid-row skill, and `family` plus `grid_row`/`procedural`/`source` with the optional `cross_cutting`/`composes` for a procedural one, either class optionally carrying `doctrine_source` — and no others

### Requirement: Merging two rows moves the grid first and preserves both marks

Where two grid rows describe one judgement, they MAY be merged into one row, and the merge SHALL be
performed in the grid before any skill directory or prompt line is touched. The surviving row's marks
SHALL be the union of the two rows' marks, taking the stronger mark per column, because a column that
held `●` on either row still owns the merged competency deeply. The surviving row SHALL keep its own
row id, and the absorbed row's id SHALL be retired.

The merge SHALL be a fold, not a deletion: every distinct element of the absorbed skill's Method SHALL
be present in the surviving skill's body afterwards. `Outcome judgement` absorbing
`Effect-on-target verification` is the worked case — the observable-channel inventory, the first-party
versus independent-confirmation split, the `<log>:<offset>` citation form and the honeypot tells all
survive in `outcome-judgement`.

#### Scenario: Grid changes before the artifacts

- **WHEN** two rows are merged
- **THEN** the grid edit and the artifact edits land in the same change, with the grid stated as the reason for the artifact change

#### Scenario: Stronger mark wins per column

- **WHEN** one row absorbs another and a column held `●` on the absorbed row and `○` on the survivor
- **THEN** that column reads `●` on the merged row, for every one of the five columns alike

#### Scenario: The survivor keeps its id and the absorbed id is retired

- **WHEN** two rows are merged
- **THEN** the surviving row's id is unchanged, every skill citing it needs no edit, and the absorbed row's id is never reassigned

#### Scenario: Nothing is dropped in the fold

- **WHEN** the surviving skill is compared against the absorbed skill's Method
- **THEN** every distinct element of the absorbed Method appears in the survivor, and the absorbed directory no longer exists

#### Scenario: No dangling reference remains

- **WHEN** the repository is searched for the absorbed skill's slug
- **THEN** no prompt, skill body, spec, document or command wrapper names it
