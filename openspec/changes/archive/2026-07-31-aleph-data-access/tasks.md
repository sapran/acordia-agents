## 1. Author the `aleph-entity-graph` skill

- [x] 1.1 Create `analysts/skills/aleph-entity-graph/SKILL.md` with opencode frontmatter (`name: aleph-entity-graph` equal to the folder slug, `description` phrased for trigger quality — fires when the take lives in an Aleph instance)
- [x] 1.2 Add a `## Cross-cutting notice` declaring the skill procedural and non-grid and naming the grid rows it composes
- [x] 1.3 Add a data-model section covering collections, FtM schema inheritance, and `entity`-typed properties as the graph edges
- [x] 1.4 Add a conditional `## Tooling` paragraph — `aleph_*` MCP tools where mounted, `bash` + HTTP API with `jq` projection otherwise, and say which path is in use
- [x] 1.5 Add an inventory-first, facet-first `## Method`
- [x] 1.6 Add a `## Limits that change the method` section covering the 9999 search window, the 200-per-property expansion cap, the WRITE requirement on `_stream`, and the rate limit
- [x] 1.7 Add an `## Assessing the take` section feeding `assessing-take-value`
- [x] 1.8 Add `## Signals / outputs` and `## Guardrails`, the latter naming every mutation path as out of scope and the READ-scoped key as the enforcement point
- [x] 1.9 Verify the frontmatter against the opencode contract (`name` matches `^[a-z0-9]+(-[a-z0-9]+)*$`, ≤64 chars, equals the folder slug; `description` 1–1024 chars) and carries no `sha256`/`signature` and no CyberStrike-only fields

## 2. Source-of-truth and posture checks

- [x] 2.1 `git diff docs/roles/operational-analyst.md` shows no change (no grid edit)
- [x] 2.2 `git diff analysts/agents/` shows no change (no prompt or permission edit)
- [x] 2.3 `install.sh` and `uninstall.sh` unchanged (the skill is picked up by the `skills/*` glob)

## 3. Validate

- [x] 3.1 `openspec validate --all --strict` passes
- [x] 3.2 `test -f analysts/skills/aleph-entity-graph/SKILL.md`
- [x] 3.3 The body contains all six required sections
- [x] 3.4 The body contains no reference to a tool the harness may not provide without stating the condition and the fallback
- [x] 3.5 Skill count invariant: `ls analysts/skills | wc -l` reports one more than before this change
