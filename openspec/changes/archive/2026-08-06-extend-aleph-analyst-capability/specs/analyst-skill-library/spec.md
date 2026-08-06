# analyst-skill-library Specification

## MODIFIED Requirements

### Requirement: `aleph-entity-graph` skill exists

The library SHALL contain a skill `analysts/skills/aleph-entity-graph/SKILL.md` naming the discipline of working collected material that has already been ingested into an Aleph instance as a FollowTheMoney entity graph, rather than as a pile of documents. It SHALL be a first-class procedural cross-cutting skill, SHALL declare its cross-cutting/procedural nature in its body, and SHALL NOT be added as a row to the competency grid.

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

- **WHEN** the skill runs in a harness that mounts the MCP tools under a different prefix from the one an example gives, or mounts none at all
- **THEN** the body has already stated that the prefix is the harness's and not the server's, directing the analyst to match on the tool verb, and has named the `bash` + HTTP API fallback for the no-mount case, satisfying `harness-tool-translation`

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
