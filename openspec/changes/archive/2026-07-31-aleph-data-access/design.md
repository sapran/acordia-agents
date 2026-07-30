# Design — Aleph data access for the analyst pillar

## The three options considered

| Option | Verdict |
| --- | --- |
| A new analyst agent (a fifth leg) that owns Aleph | **Rejected.** The roster is derived: `docs/roles/operational-analyst.md` grid → `analyst-agent-roster` → `analysts/agents/*.md`. A fifth leg means editing the ACORDIA competency grid, i.e. changing the role framework to accommodate one vendor's product. Aleph is a tool, not a competency. |
| A skill only, driving the HTTP API through `bash` | **Viable, and the fallback path this change ships.** Costs nothing and works today, because analysts already carry `bash: allow`. Weak on bounding: `curl` output goes straight into context, and `alephclient`'s CLI verbs are write-oriented (`crawldir`, `delete`, `flush`, `write-entities`), so the destructive commands sit one token away from the read ones. |
| A skill plus a read-only MCP server | **Chosen.** The MCP layer enforces the bounding — hard-failing deep pagination, capping expansion, stripping document text from search hits — which is precisely what a prompt cannot enforce. The skill carries the competence: what to query, in what order, and how much to believe the answer. |

The two halves solve different problems. An MCP server without the skill produces an agent that issues one broad `search_entities` and stops. A skill without the server still works, which is why the body is written conditionally rather than assuming the tools exist.

## Why the server is not in this repository

`CLAUDE.md`: *"Markdown-only distribution … No application code, no build, no runtime, no tests."* `analyst-skill-library` further restricts co-located reference files to markdown. So the server lives in its own repository (`aleph-mcp`), exactly as `datashare-mcp` does for the ICIJ Datashare equivalent. This is a constraint, not a preference.

## Why the boundary is the API key, not a permission rule

The ideal would be to grant the Aleph MCP to the analyst legs with the mutating tools denied per agent. That works in one harness and not in the other:

- **opencode:** MCP tools are named `sanitize(serverName) + "_" + sanitize(toolName)` and are gated twice against that literal key — `Permission.disabled()` filters the tool list sent to the model, and the MCP wrapper calls `ctx.ask({ permission: key })` before invoking. A per-agent `permission` deny is real.
- **omp:** `docs/agents-skills-extension-workbook.md` §7.3 records, verified on omp 17.1.8, that the `xd://` transport tools `read` and `write` are present whenever `tools.xdev` is on — the default — *regardless of the agent's `tools:` allowlist*. Every mounted MCP device is invoked through them. There is no per-agent MCP scoping.

A repo-side permission rule would therefore hold in opencode and silently evaporate in omp. That is the same failure mode `harness-tool-translation` already documents for path-scoped `edit`, and the same reason `.acordia/ops/` is described as discipline rather than enforced as a scope.

So the boundary moves upstream, out of the harness entirely: **mint an Aleph role whose collection ACL is `read=true, write=false`.** Destructive endpoints (`DELETE /api/2/collections/<id>`, `DELETE /api/2/entities/<id>`, `POST .../mappings/<id>/flush`, `_bulk` with `mutable=true`) are then refused server-side no matter which harness, agent or tool issues the call. Defence in depth remains available — the `aleph-mcp` server exposes no write tool at all — but correctness does not depend on it.

**Accepted cost.** `GET /api/2/collections/<id>/_stream` requires WRITE on the collection and the global stream requires admin. A read-only key therefore cannot bulk-export, and is capped at the 9999-result search window. This is why `aleph-coldbackup` needs a write-scoped key and is named in the skill as a human-run job rather than a session action, and why the method is facet-first: the analyst must narrow a result set rather than try to enumerate it.

## Why the skill does not expose raw Elasticsearch DSL

The sibling `datashare-mcp` deliberately exposes raw ES DSL plus a mapping resource, because Datashare's search *is* Elasticsearch. Aleph's is not: `q` becomes a lenient `query_string` **plus** a fuzzy `multi_match` boost Aleph adds over its text fields, and structured constraints arrive as repeated `filter:<field>` arguments handled by Aleph's own `SearchQueryParser`. Handing the model raw DSL would bypass that layer and produce queries that behave differently from everything documented about Aleph. The skill teaches Aleph's grammar instead.

## Why no agent prompt is touched

opencode has no per-agent `skills:` field; composition is by prompt reference plus description match. The prompts' skill lists are compiled from the grid columns, so inserting a non-grid slug into one would break the bijection that `competency-map-derivation` and `analyst-agent-roster` enforce. A triggering-quality `description` is the whole mechanism, and it is the thing the added requirement audits.

`fusion-analyst` is nonetheless the natural consumer — its deep set already holds `multi-source-fusion`, `data-integration-tooling` and `assessing-take-value`, and an Aleph collection is mixed-source take needing exactly those. That relationship is stated in prose in the skill body, not wired as a binding.

## Open question deferred

Whether a future change should add a *second*, write-capable Aleph capability for the operators pillar (ingesting collected material into a case file). It would need its own server, its own write-scoped key, and its own risk argument, and it does not belong in the read-only Analysis pillar.
