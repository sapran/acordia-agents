## Why

Operational take increasingly arrives already ingested into an **Aleph** instance (the OCCRP investigative data platform) rather than as loose files on disk. Aleph has already done the extraction, entity resolution and cross-referencing; the analyst who treats it as a document pile and greps it by hand throws that work away and re-derives a worse version of it.

No artefact in this repo names Aleph, the FollowTheMoney entity model, or the query discipline that fits Aleph's real constraints. `exhaustive-data-processing` covers raw bulk material on disk and is the right skill for a dump; it is the wrong skill for a corpus that is already an entity graph behind a paginated API with hard ceilings.

Those ceilings are the substantive reason a skill is needed rather than "just use the API": Aleph's `SearchQueryParser` **silently clamps** `limit + offset` past `MAX_PAGE = 9999`, so an analyst paging a large result set is told nothing and concludes it reached the end. Graph expansion has an entirely separate and much lower cap (`ALEPH_MAX_EXPAND_ENTITIES`, default 200). And `_stream`, the only unbounded export, requires **WRITE** on the collection, so a read-only analyst key cannot use it at all. Each of these produces a confidently wrong picture if it is not known in advance.

## What Changes

### New skill: `aleph-entity-graph`

Add `analysts/skills/aleph-entity-graph/SKILL.md` — a procedural cross-cutting skill (same class as `analyst-loop`, `credential-harvest-triage` and `exhaustive-data-processing`) that fires when the take lives in an Aleph instance. It carries:

- **A cross-cutting notice** declaring the skill procedural and non-grid, and naming the grid rows it composes (`multi-source-fusion`, `data-integration-tooling`, `exhaustive-data-processing`, `assessing-take-value`, `analytic-tooling-scripting`).
- **A FollowTheMoney primer** — collections, schemata and their inheritance, and the fact that `entity`-typed properties *are* the graph edges (so `Ownership`/`Directorship`/`Payment` are relationships, not records), with a pointer to reading `aleph://schema/<Name>` before filtering on an unfamiliar schema.
- **A conditional tooling paragraph** — use the `aleph_*` MCP tools where the harness mounts them, otherwise fall back to `bash` + the HTTP API with `jq` projection, and say which path is in use. This satisfies `harness-tool-translation`'s rule that a body names only tools the harness provides, or states the condition and names the fallback.
- **A method** that is inventory-first and facet-first: enumerate collections and read their `statistics` as a denominator; run the intended search at `limit=0` with facets before pulling rows; narrow with `filter:` rather than by paging; then pivot on entities (`expand`, `tags`, `similar`/`match`, entitysets, xref) rather than on text; read document text last and bounded.
- **A limits section** stating the three ceilings as method-changing facts: the 9999 search window (a total above it means "unenumerated", not "read"), the 200-per-property expansion cap (a `count` above it means the edge was sampled), and `_stream` requiring WRITE (so bulk export is a human-run `aleph-coldbackup` job, not a session action).
- **A take-assessment section** feeding `assessing-take-value`: provenance is per collection not per instance; entities are derived rather than observed; xref and similarity results are scored candidates, not findings; registry-derived collections go stale; and absence of a hit proves nothing about coverage.
- **Guardrails** holding the analyst's read-only posture: search, expand and read only — never ingest, write, tag, trigger a cross-reference run, or delete, because those mutate another team's investigation.

### No agent-prompt change

Deliberately none. opencode selects skills by `description` match and has no per-agent `skills:` field, so a triggering-quality description is what makes the skill reachable. The four analyst prompts' skill lists are derived from the competency-grid columns; naming a non-grid skill in them would be exactly the source-of-truth drift the derivation chain exists to prevent.

### No permission change

Also deliberately none, and this is the load-bearing decision. Tool-level permission cannot be the safety boundary for an Aleph integration across both harnesses:

- **opencode can** deny an MCP tool per agent — MCP tools are named `sanitize(server)_sanitize(tool)` and are checked against that literal key by `Permission.disabled()` and by the runtime `ctx.ask()` in the MCP wrapper.
- **omp cannot** — `docs/agents-skills-extension-workbook.md` §7.3 records, verified on omp 17.1.8, that the `xd://` transport tools `read` and `write` are present whenever `tools.xdev` is on regardless of an agent's `tools:` allowlist, and every mounted MCP tool is invoked through them.

A repo-side `permission` rule would therefore hold in opencode and silently evaporate in omp — the same trap already documented for path-scoped `edit` in `harness-tool-translation`. The boundary is placed upstream instead: the skill states that the API key is expected to be READ-scoped, so Aleph refuses destructive calls server-side on either harness.

## Capabilities

### New Capabilities

None. The skill lands inside `analyst-skill-library` as a cross-cutting procedural addition, mirroring `analyst-loop`, `credential-harvest-triage` and `exhaustive-data-processing`.

### Modified Capabilities

- `analyst-skill-library` — one **ADDED** requirement (`aleph-entity-graph` skill exists).

## Impact

- **New files:** `analysts/skills/aleph-entity-graph/SKILL.md`.
- **Modified agent files:** none. No `edit`, `bash` or `task` permission block is touched; the three-leg `task` whitelist is intact.
- **Modified skill files:** none. The addition is purely additive.
- **Source of truth:** the new requirement in `analyst-skill-library` is the normative anchor, exercising the existing "procedural cross-cutting skills" exception in the "One skill per competency-grid row" requirement. `docs/roles/operational-analyst.md` is read for anchor, not modified — **no grid change, no drift.** `competency-map-derivation` and `analyst-agent-roster` are untouched.
- **No install script change.** `install.sh` globs `skills/*` and picks the new skill up automatically.
- **Analyst posture preserved.** The skill authorises no new action: it reads, models and judges. Every mutation path in Aleph is named as out of bounds and left to the operator or the human.
- **External dependency, out of repo:** the `aleph_*` tools referenced conditionally are provided by a separate `aleph-mcp` server, which — per this repository's markdown-only contract — is not and must not be vendored here. The skill is written to work without it.
