## ADDED Requirements

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
