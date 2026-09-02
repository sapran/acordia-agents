## MODIFIED Requirements

### Requirement: `aleph-entity-graph` skill exists

The library SHALL contain a skill `acordia-analysts/skills/aleph-entity-graph/SKILL.md` naming the discipline of working collected material that has already been ingested into an Aleph instance as a FollowTheMoney entity graph, rather than as a pile of documents. It SHALL be a first-class procedural cross-cutting skill, SHALL declare its cross-cutting/procedural nature in its body, and SHALL NOT be added as a row to the competency grid.

The skill body SHALL contain: (a) a **cross-cutting notice** declaring the skill procedural and non-grid and naming the grid rows it composes; (b) a **data-model** section stating that Aleph stores FollowTheMoney entities grouped into collections, that schemata inherit, and that `entity`-typed properties are the graph edges; (c) a **conditional tooling** paragraph naming the MCP server's registered read tools by their bare verbs, stating that a harness may expose them under a mount prefix, and naming the `bash` + HTTP API fallback otherwise; (d) a **scope-first, inventory-first, facet-first method** — name the collection every search is scoped to, enumerate collections and read their statistics, survey a result set with facets at `limit=0` before pulling rows, narrow with `filter:` constraints, pivot on entities and on resolved identities via expand/tags/similar/match/profiles/entitysets/xref, and read document text last and bounded; (e) a **limits** section stating the ceilings and query semantics that change the method; and (f) a **take-assessment** section feeding `assessing-take-value`.

Clause (c) SHALL NOT mandate a prefixed tool-name form. The `aleph-mcp` server registers its tools unprefixed and its own specification explicitly refuses to guarantee any prefix, stating that the mount configuration is where that expectation is satisfied; a prefix a caller observes is composed by the host from the mount name. The tooling paragraph SHALL therefore name the tool verbs, SHALL state that a harness may apply a mount prefix and give the observed form as an example rather than a requirement, and SHALL direct the analyst to match on the verb rather than on a literal prefix.

The tooling paragraph SHALL state what the `bash` + HTTP fallback gives up relative to the tools, because on that path the analyst inherits the obligations the server was discharging: no refusal at the search ceiling, no expansion cap, no stripping of document-sized text properties, no derived `caption`, and no read-only allowlist between the caller and a write endpoint. It SHALL name collection scope among them: the fallback's example URL SHALL carry a `filter:collection_id` constraint, and the paragraph SHALL state that an omitted one searches every collection the key can read with nothing in the response to signal it.

The method's pivot step SHALL name profile-scoped pivots alongside entity-scoped ones, and SHALL name the `profile_id` field carried on search and expansion results as their entry point. It SHALL state the analytic rule that a profile-scoped pivot is preferred over an entity-scoped one where a profile exists, because the entity in hand is one fragment of an actor whose other fragments carry edges invisible from it.

The method's first step SHALL be collection scope, ahead of inventory, because an unscoped Aleph search is answered rather than refused. It SHALL name `collection` as the argument that carries scope and as a required argument on `search_entities` and `match_entity`; SHALL name the forms it accepts — a numeric id, or a `foreign_id` resolved server-side, with a list accepted by the two search tools only; SHALL name the literal `collection="*"` as the only instance-wide scope and the `_note` that annotates a `search_entities` reply at that scope; SHALL state that a blank value is refused rather than read as "no scope"; and SHALL state that `collection_id` inside `filters` is refused rather than honoured. The narrowing step SHALL NOT present collection as one of its filter keys.

The step SHALL state the consequence of omitting scope rather than only the requirement to supply it: a search that names no collection returns another collection's rows, ranked, well-formed and plausible, with no error, no warning and no empty result. It is stated as a consequence because enforcement is not uniform — the tools refuse a missing `collection` and the HTTP fallback does not — and because the one number that would expose a wrong scope is a reported total above 10,000, which this same skill has already taught the analyst to read as a floor rather than a count.

The method SHALL direct the analyst to read the applied scope back from the reply's `searched.collection` field, which reports the resolved numeric ids or `"*"`, rather than assume the scope requested is the scope applied. A required argument establishes that something was passed; it does not establish that a `foreign_id` or a list resolved to the collections intended, and every such resolution produces a successful reply.

The take-assessment section SHALL require a hit's own `collection_id` to be checked against the collection that was scoped to, because that mismatch is the only symptom a wrongly-scoped search produces.

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

#### Scenario: Scope is the method's first decision

- **WHEN** the method's first step is read
- **THEN** it requires `collection` on every search, names the id, `foreign_id` and list forms, names
  `collection="*"` as the only instance-wide scope with its `_note` annotation, and states that
  `collection_id` inside `filters` is refused

#### Scenario: An unscoped search is answered, not refused

- **WHEN** the first step's rationale is read
- **THEN** it states that a search naming no collection returns another collection's rows, ranked and
  plausible, with no error, no warning and no empty result

#### Scenario: The applied scope is read back rather than assumed

- **WHEN** a search reply is handled
- **THEN** the method directs the analyst to read `searched.collection` and confirm the resolved ids
  are the ones asked for

#### Scenario: Narrowing does not carry scope

- **WHEN** the narrowing step is read
- **THEN** collection is named as not among the `filters` keys, and the reader is pointed back at the
  `collection` argument

#### Scenario: The fallback path names its unenforced scope

- **WHEN** the `curl` fallback branch is read
- **THEN** its example URL carries a `filter:collection_id` constraint and the prose states that an
  omitted one searches every readable collection with nothing in the response to signal it

#### Scenario: A hit's collection is checked against the scope

- **WHEN** the take-assessment section is read
- **THEN** it requires verifying a hit's own `collection_id` against the collection that was scoped
  to, and names that mismatch as the failure's only symptom
