---
name: aleph-entity-graph
description: Use when the take lives in an Aleph instance — search, pivot and expand the FollowTheMoney entity graph across collections instead of reading documents one by one.
metadata:
  acordia:
    cross_cutting: true
    procedural: true
    composes: [multi-source-fusion, data-integration-tooling, exhaustive-data-processing, assessing-take-value, analytic-tooling-scripting]
---

# Aleph Entity Graph

## Cross-cutting notice
This skill is **procedural and non-grid**. It corresponds to no row of the competency grid in `docs/roles/operational-analyst.md`; it composes existing rows — `multi-source-fusion`, `data-integration-tooling`, `exhaustive-data-processing`, `assessing-take-value` and `analytic-tooling-scripting` — into the specific discipline of working a corpus that has already been ingested into Aleph. Do not add it to the grid.

## Objective
Turn an Aleph instance from a document pile into a queryable entity graph: find the entities that matter, establish who and what they connect to, judge how good the underlying material is, and read only the text you actually need.

## When to use
- The collected material has been ingested into an Aleph instance (OCCRP investigative platform) rather than handed over as loose files.
- You need to relate people, companies, addresses, phones, emails, payments and documents to each other, not just search text.
- You must cross-check a name from elsewhere in the operation against an already-indexed corpus.

Use `exhaustive-data-processing` instead when the material is a raw dump on disk. Use this skill once it is *in* Aleph — Aleph has already done the extraction and entity resolution, and re-grinding the files by hand discards that work.

## The data model in one paragraph
Aleph stores **FollowTheMoney (FtM) entities**, grouped into **collections** (one investigation or one dataset). Every entity has a `schema` (`Person`, `Company`, `Address`, `Email`, `Document`, `Pages`…), a `caption`, and typed `properties`. Schemata inherit: `Person` and `Company` are both `LegalEntity`, which is a `Thing`. Properties whose type is `entity` are **the graph edges** — `Ownership.owner` points at a `LegalEntity`, and Aleph auto-generates the reverse edge, so a company can be walked back to its owners. Some schemata (`Ownership`, `Directorship`, `Payment`, `UnknownLink`) exist purely to *be* a relationship between two entities. Read `aleph://schema/<Name>` before writing a filter against a schema you have not used.

## Tooling — state which one you have
- **If `aleph_*` tools are mounted** (the `aleph-mcp` server, tool names `aleph_search_entities`, `aleph_expand_entity`, `aleph_get_entity_text`, …), use them. They enforce Aleph's real limits and strip document text out of search hits so it does not silently consume your context.
- **Otherwise fall back to `bash`** with the HTTP API directly:
  `curl -s -H "Authorization: ApiKey $ALEPHCLIENT_API_KEY" "$ALEPHCLIENT_HOST/api/2/entities?q=…&filter:schema=Person&limit=20" | jq …`
  Under this fallback you own the bounding: pipe through `jq` to project only the fields you need, and never cat a whole response into context.

Do not assume either path exists — check, say which you are on, and name the constraint if neither is available.

## Method
1. **Inventory before querying.** `list_collections` (or `GET /api/2/collections`) to see what this key can read, then `get_collection` for each candidate. Its `statistics` block breaks the collection down by schema, country and language — that is your denominator and it costs one call.
2. **Facet before pulling rows.** Run the search you intend with `limit=0` and `facets=["schema","collection_id","countries","languages"]`. You learn the shape of the result set for almost no context, and you find out immediately whether the query is too broad.
3. **Narrow with filters, not with paging.** `filters` are exact matches — different keys are ANDed, values inside one list are ORed. `q` is an Elasticsearch query_string: quote phrases, use `AND`/`OR`/`NOT` and wildcards. Add `highlight` when you need to see *why* something matched without reading the document.
   **Every search is scoped to a schema branch, always.** Aleph selects its search index from the schema filter and rejects a query that carries none. The general scope is `Thing` — people, companies, addresses, documents, emails. Relationships are *not* under `Thing`: `Ownership`, `Directorship`, `Payment` and `UnknownLink` descend from `Interval` and must be asked for by name. If you search for "ownership" as text and find nothing, this is usually why.
4. **Pivot on entities, not on text.** Once you have an entity id:
   - `expand_entity` — its graph neighbours, grouped by property. This is how ownership, directorship, membership, family and email correspondence are walked. Each group reports a `count`, so a truncated group still tells you the true degree.
   - `entity_tags` — how many other entities share this one's phone, email, address or name. The cheapest pivot in Aleph, and often the one that finds the connection.
   - `similar_entities` / `match_entity` — identity resolution. `match_entity` takes an FtM fragment you supply, so it is the way to check a name obtained elsewhere in the operation against the whole index.
   - `list_entitysets` / `entityset_items` — lists, network diagrams and timelines curated by human investigators. Read them before re-deriving the same structure yourself.
   - `xref_results` — matches already computed between this collection and other datasets (sanctions lists, registries). Empty means no cross-reference has been run, not that there are no matches.
5. **Read text last, and bounded.** `get_entity_text` with `offset`/`limit`; check `total_chars` and `truncated` before asking for more. A search with `highlight` usually settles whether a term occurs; only read the body when you need the surrounding argument.
6. **Script the repetitive part.** Per `analytic-tooling-scripting`: when the same pivot must run over dozens of entities, write the loop and aggregate the results, rather than issuing dozens of interactive calls and reading each one.

## Limits that change the method
These are Aleph's, not the tool's, and no amount of paging works around them:

- **`limit + offset` may never exceed 9999** on entity search — Elasticsearch's result window. Deep pagination is therefore *not* a way to read a whole collection. If a result set is larger, it must be split by facet (per schema, per collection, per country, per date range) or narrowed. A tool that clamps this silently would let you believe you reached the end; treat any total above 9999 as "unenumerated".
- **Graph expansion has a separate, much lower ceiling** — 200 entities per property by default. A `count` above that means you saw a sample of that edge, and you must say so.
- **A reported total is a floor, not a count.** Aleph caps the number it reports at 10,000. `total: 10000` means "at least 10,000", so never quote it as a population figure — facet instead, because facet buckets carry true counts.
- **`caption` may be absent.** Some instances return no caption at all; the identifying value then sits in `properties.name`, `properties.fileName` or `properties.title`. Do not conclude an entity is unnamed because the caption is empty.
- **Bulk export needs a write-scoped key.** `GET /api/2/collections/<id>/_stream` requires WRITE on the collection; the global stream requires admin. An analyst holding a read-only key cannot stream a collection out, by design. If a full local copy is genuinely required, that is a human-run `aleph-coldbackup` job, not something to attempt from the session.
- **Rate limiting** is around 30 requests/minute for unprivileged callers. Prefer one faceted query over twenty narrow ones.

## Assessing the take
Feed what you find into `assessing-take-value` rather than treating an Aleph hit as fact:
- **Provenance is per collection, not per instance.** A `Person` from a leaked archive and a `Person` from a sanctions list carry entirely different weight. Always carry `collection_id` with a claim.
- **Entities are derived, not observed.** Most were generated by extraction or by a mapping over a source table. An `Ownership` edge is only as good as the registry row behind it.
- **Cross-reference matches are candidates.** `xref_results` and `similar_entities` return scores; a match without a human `judgement` is a hypothesis, and belongs in `hypothesis-testing`, not in the picture.
- **Currency matters.** Registry-derived collections go stale; check the collection's `updated_at` before asserting a present-tense relationship.
- **Absence proves little.** Not finding a name may mean the corpus never covered that jurisdiction. Say which collections you actually searched, and name the gap through `naming-the-gaps`.

## Signals / outputs
- A named set of entities with ids and collection provenance, not a list of documents.
- The relationship paths that were actually walked, with the property names traversed and any edge whose `count` exceeded the expansion cap flagged as partial.
- Identity-resolution decisions made explicit: which entities you treated as the same actor, and on what evidence.
- A coverage statement: which collections were searched, which queries were run, and which result sets exceeded the 9999 ceiling and were therefore only sampled.

## Guardrails
- **Read only.** This skill searches, expands and reads. It never ingests, writes, tags, cross-references on demand, or deletes — those change another team's investigation. If a write is genuinely needed, hand it to the operator or the human, do not attempt it.
- The API key is expected to be READ-scoped; if a call fails with 403 mentioning WRITE or admin, that is the boundary working, not an obstacle to route around.
- Never place raw credential values, personal identifiers beyond what the judgement requires, or bulk document text into a report. Report classifications, entity ids and provenance.
