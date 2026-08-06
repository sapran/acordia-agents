## Why

The analyst pillar's Aleph capability was reachable only by accident and described inaccurately.

**Unreachable.** `aleph-entity-graph` is non-grid, so it appears in no agent's compiled skill set and no agent prompt names it. Selection therefore depends entirely on opencode's description-match. The two other non-grid procedural skills in this library — `credential-harvest-triage` and `exhaustive-data-processing` — are each *required* to appear as an H2 section in all four analyst prompts, for exactly this reason. Aleph was the outlier.

**Inaccurate.** The skill misdescribes the server it drives:

- It hardcodes `aleph_`-prefixed tool names the server does not register. `aleph-mcp` registers tools unprefixed and its own spec explicitly refuses to guarantee any prefix — the host composes one from the mount name. Worse, this repository's governing requirement *mandates* the prefixed wording, so the skill was correct against its spec and wrong against reality; both had to move together. The skill was also internally inconsistent, using the prefixed form in its tooling paragraph and the bare form in its method.
- It asserts nothing about Aleph's actual query semantics. Entity-search `q` is **not** fuzzy — the fuzzy overlay belongs to collection search — so a misspelt or transliterated name silently fails to match, and an analyst assuming otherwise manufactures false negatives on precisely the name variants that matter. Multi-term `q` also matches on only 66% of its terms, so adding words widens rather than narrows.
- Four of the twelve tools it could call were never named, and its `caption` guidance describes behaviour the server has since superseded by deriving captions itself.
- Its `curl` fallback is presented as an equivalent path. It is not: on that path the analyst inherits every bound the server was enforcing, and the skill never said so.

**Incomplete against the server.** `aleph-mcp` now exposes Aleph's profile subsystem — the investigator's recorded decision that several entities are one actor — plus entityset detail, at seventeen tools rather than twelve. The skill told analysts to make identity resolution explicit while naming only the scored-candidate tools to do it from.

## What Changes

- `analysts/skills/aleph-entity-graph/SKILL.md` — tooling paragraph names the seventeen registered tool verbs and states that the prefix is the harness's, not the server's; the fallback branch states what it costs; the pivot step gains profile-scoped pivots entered through `profile_id`; the narrowing step states that `q` is not fuzzy and matches on 66% of terms; the `caption` limit is split by path; the take-assessment section distinguishes a recorded profile from an unjudged candidate. Prose only — no frontmatter change.
- All four analyst agent prompts gain an `## Aleph corpora` H2 section naming `aleph-entity-graph`, each with its own lens: routing for the orchestrator, cross-collection correlation for fusion, ownership and address structure for target-network, operation-owned exposure for defender-detection. Additive; no existing section rewritten and no permission block touched.
- `VERSION` in `tools/build-plugins.py` bumped `2.0.0` → `2.1.0` (MINOR: user-reaching prose in an agent prompt and a skill body, no roster or distribution-shape change), and the plugin trees regenerated.

Out of scope: the competency grid gains no Aleph row, and `aleph-entity-graph` is added to no agent's grid-derived skill set. Aleph is a tool, not a competency.

## Capabilities

### New Capabilities

None. Both affected capabilities already exist.

### Modified Capabilities

- `analyst-skill-library`: the `aleph-entity-graph` requirement's tooling clause currently mandates naming the `aleph_*` tools — the clause that forces the inaccuracy — and must instead require tool verbs plus a harness-applies-the-prefix statement. New obligations: the fallback's cost, profile-scoped pivots and their `profile_id` entry point, and the true query semantics.
- `analyst-agent-roster`: adds a requirement for an `## Aleph corpora` H2 section in every agent prompt, mirroring the existing credential-harvest and exhaustive-processing section requirements.

## Impact

- `analysts/skills/aleph-entity-graph/SKILL.md` — six prose edits across the tooling, method, limits and take-assessment sections.
- `analysts/agents/operational-analyst.md`, `fusion-analyst.md`, `target-network-analyst.md`, `defender-detection-analyst.md` — one new H2 section each.
- `tools/build-plugins.py` — `VERSION` bump; regenerated output under `plugins/`, `.claude-plugin/`, `.omp-plugin/`.
- `docs/roles/operational-analyst.md` — untouched, deliberately.
- Upstream: the tool names cited here are the surface `aleph-mcp` publishes in its own `extend-profile-tool-surface` change. That server is not vendored here and this repository stays markdown-only; the skill references tool verbs and nothing more.
