## Why

`aleph-entity-graph` tells an analyst how to facet, how to pivot, what `q` will and will not match,
and which three ceilings change the method. It never tells them to say which collection they are
searching. Step 1 is "Inventory before querying", step 2 facets on `collection_id`, step 3 says
"narrow with filters" — and nowhere does the body state that a search which names no collection is
answered anyway, from every collection the key can read.

**Aleph does not refuse an unscoped search.** It returns rows: ranked, well-formed, plausible, and
from a corpus nobody chose. There is no error, no warning and no empty result set, so the failure has
no symptom other than a `collection_id` on the hits that the analyst never looks at.

It has already shipped a wrong answer. On a live analysis run (2026-09-02) the analyst spent three
turns working out how to scope a search to one collection, and its second attempt silently answered
from a different one: `total: 10000` with `collection_id: 833` on the rows, where the correctly
scoped query on collection `874` returned `total: 5695`. The 10,000 figure is Aleph's reported cap —
the limits section of this very skill already says a reported total is a floor, not a count — so the
one number that could have exposed the wrong scope was the number the skill had already taught the
analyst to distrust. Nothing else in the reply differed.

Two causes, and the server's half is already fixed. `aleph-mcp` had no `collection` parameter on
`search_entities`: scope lived inside a free-form `filters` dict as `filters={"collection_id":
"874"}`, while the neighbouring `get_collection` took `collection`. The analyst generalised the
neighbour's word, the harness bridge dropped the argument it did not recognise, and the search ran
unscoped. The server now requires `collection` on `search_entities` and `match_entity` and refuses
`collection_id` inside `filters`, so that exact mistake now fails loudly rather than silently.

The skill's half is not fixed. A required argument the body never mentions is a required argument the
analyst discovers by trial, which is what cost three turns; and the `curl` fallback the skill also
offers enforces nothing at all, so on that path the silent failure survives the server fix intact.

## What Changes

- **Collection scope becomes the method's first step**, ahead of inventory. It states the argument
  (`collection`), the forms it accepts (numeric id, `foreign_id`, or a list of either, resolved
  server-side), the one literal that searches everything (`"*"`, annotated in the reply's `_note`),
  where scope does **not** go (`collection_id` inside `filters`, now refused), and the field that
  reports the scope actually applied (`searched.collection`, read rather than assumed).
- **The step states why it is required rather than only that it is.** An unscoped search succeeds,
  so the consequence of omitting scope is a plausible answer from the wrong dataset — not an error
  the analyst will be shown.
- **The narrowing step stops implying scope is a filter.** `filters` remains exact-match AND/OR
  narrowing; collection is named as not among its keys and pointed back at the argument.
- **The `curl` fallback carries the constraint in its example URL** and states that on that path an
  omitted `filter:collection_id` searches every readable collection with nothing in the response to
  signal it — no `_note`, no `searched` block.
- **Take assessment gains the check that catches the failure.** The provenance bullet already says to
  carry `collection_id` with a claim; it now also says to verify a hit's own `collection_id` against
  the collection that was scoped to, because that mismatch is the only symptom the failure has.
- **No new capability is claimed.** Every statement about the server traces to the `aleph-mcp`
  contract; nothing about scope is asserted for the fallback path, where nothing enforces it.

## Capabilities

### Modified Capabilities

- `skill-library`: `aleph-entity-graph` SHALL make collection scope the first decision of its method,
  SHALL state that an unscoped search is answered rather than refused, and SHALL require the applied
  scope to be read back from the reply rather than assumed.

## Impact

- **1 skill body** — `acordia-analysts/skills/aleph-entity-graph/SKILL.md`. Frontmatter untouched, so
  `metadata.acordia` stays valid and `skill-sets.json` needs no edit.
- **0 agent prompts** — no `·`-separated skill line changes; the skill is already carried where it
  belongs.
- **0 source-document changes** — `aleph-entity-graph` is procedural with `grid_row: null`, so no grid
  row, column or mark moves and both grid transcriptions stay valid.
- **1 generated artifact** — `acordia-map.html` embeds skill bodies as rendered HTML, so it is
  re-derived and ships in the same commit.
- **Specs**: `skill-library`.
- **Version**: MINOR, `6.5.0` → `6.6.0`. A skill body reaches every user, so it must bump; the roster
  and the distribution shape are unchanged, so it is not MAJOR.

## Out of scope, recorded not fixed

- **The `curl` path cannot be made safe from here.** The skill can tell an analyst to add
  `filter:collection_id`; nothing on that path refuses an omission. The change states the exposure
  instead of pretending to close it.
- **Faceting on `collection_id`** stays in the facet step. It is degenerate under a single-collection
  scope and still correct under a list or `"*"`, so it is left alone rather than rewritten.
- **The harness bridge that dropped the argument** is an omp defect already filed by the
  `2026-09-02-lead-runs-in-main-session` change. A required parameter now makes it fail closed, which
  is the most a distribution can do about it.
