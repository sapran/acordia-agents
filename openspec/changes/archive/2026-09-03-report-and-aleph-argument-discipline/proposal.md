## Why

Two defects from one live analysis run (`--profile opwe`, `~/ai/tasks/tele2-siem`, 2026-09-02). Both
were produced by an analyst following the skills as written, so both are gaps in the skills rather
than lapses by the analyst.

**The rendered product was converted with a hand-written regex, and its citations were truncated.**
`briefing-reporting` tells an analyst what a product must contain — bottom line, confidence, gaps, a
dated ask — and says where it lands on disk. It says nothing about producing a second format, so the
analyst wrote a line-prefix markdown converter: markdown tokens survived into `report.html`, because
a regex pass handles block prefixes and silently drops the inline constructs it does not model. And
of the 40 distinct entity links in that artefact, **35 cannot be resolved**: the source cited
truncated hashes and the linkify pattern accepted a 6-character tail. Measured on the shipped
artefact, by tail length: `{6: 5, 7: 2, 8: 29, 40: 5}`.

Both passes were "verified" — by counting the links produced. Neither pass resolved one. A link count
is satisfied identically by 40 working references and by 5, which is why the defect shipped looking
checked.

**Ten of 147 Aleph calls in the same run failed on argument construction, not on analysis.** Three
passed `id` or `entity` where every id-taking tool requires `entity_id`. Six were malformed JSON,
each in the same shape: a hand-written `q` joining quoted phrases with `OR`, with the first phrase's
inner quotes escaped and the rest not — the failure landed on the second, non-English phrase every
time. `aleph-entity-graph` names the tools, the ceilings, the query semantics and the scope argument;
it never names the identifier argument, and it recommends scripting only as a bulk-throughput measure
in its last step, never as the way an argument object is built.

## What Changes

- **`briefing-reporting` gains a rendering discipline.** A second format is produced with a real
  parser for that format, never a hand-written line-prefix pass, and the analyst says which parser
  was used. The reason is stated: inline emphasis, code spans, tables and inline links are precisely
  what a regex converter drops, and it drops them without erroring.
- **`briefing-reporting` gains a citation-completeness rule.** An identifier is carried into the
  product whole, however long; shortening belongs to what is *displayed*, not to what is recorded. A
  truncated id reads as a citation and cannot be looked up.
- **`briefing-reporting` gains the verification that would have caught both.** A rendered product is
  checked twice: no source-format tokens survive, and a sample of its evidence references is
  *resolved* against the system that issued them. Counting links is named as detecting neither
  failure.
- **`aleph-entity-graph` gains a `### Constructing the call` subsection**, placed with the tooling
  paragraph — where the analyst decides which path they are on — rather than inside the method, where
  it would read as a step to perform once.
- **It names the identifier argument**: `entity_id` on `get_entity`, `get_entity_text`,
  `expand_entity`, `entity_tags` and `similar_entities`; `profile_id` for a profile. Not `id`, not
  `entity`. It states why the mistake is expensive: an unrecognised key is dropped rather than
  refused, so the call either fails naming a missing `entity_id` or reaches the server and returns a
  not-found that reads like a bad identifier instead of a bad call.
- **It requires the argument object to be built in code.** A `q` with quoted phrases joined by `OR`
  needs every inner quote escaped; a hand-written object escapes the first and stops. Serialising the
  object inside a script removes the escaping from the analyst's hands, and is the same path
  `analytic-tooling-scripting` already recommends for throughput.
- **No new capability is claimed.** Every argument name traces to the pinned `aleph-mcp` server
  source; every failure count traces to the measured run.

## Capabilities

### Modified Capabilities

- `skill-library`: a reporting skill SHALL state a rendering and citation discipline for a product
  rendered into a second format, and SHALL require its references to be resolved rather than counted;
  `aleph-entity-graph` SHALL name the identifier argument for every tool that takes one and SHALL
  require the argument object to be serialised in code rather than hand-written.

## Literature

Searched before any prose was authored, per `CLAUDE.md` ("Literature first"), via `library_route`
with `granularity="document"`:

- `"verification of a written intelligence product before it is handed to a decision-maker"` — 10
  documents returned, relevance 0.028–0.033. Top hits: Heuer, *Psychology of Intelligence Analysis*
  (`5d880095`, 17 matched passages); Pherson & Heuer, *Structured Analytic Techniques for
  Intelligence Analysis* (`7bc0dcc4`, 17 passages); Kornmaier & Jaouën, *Beyond technical data*
  (`95b1cde6`).
- `"citation practice and source identifiers in written intelligence reporting"` — 10 documents
  returned, relevance 0.029–0.033. Top hits: CyCon X proceedings (`2da0c589`, 1 passage); Meier et
  al., *FeedRank* (`eea13fb8`); Lindsay, *Information Technology and Military Power* (`c31cadf6`, 9
  passages).

**Finding: the canon holds nothing on either point.** Every hit is at floor relevance and every one
is about a different question — cognitive bias and premature closure in analysis, situational-awareness
tooling, the tamper-resistance of threat-intelligence feeds. Nothing addresses rendering a product
into a second format, and nothing addresses the completeness of a source identifier in a written
product. This is recorded as a finding, not filled in from memory.

Consistent with that, both edits are **technique detail** rather than doctrinal claims, so per
`CLAUDE.md` they trace to their grid row and carry **no** `doctrine_source`: a citation there would
falsely imply a registered work prescribes the procedure. Nothing returned contradicts the wording
shipped.

## Impact

- **2 skill bodies** — `acordia-analysts/skills/briefing-reporting/SKILL.md` (two `## Method`
  bullets, one `## Signals / outputs` bullet) and
  `acordia-analysts/skills/aleph-entity-graph/SKILL.md` (one new subsection). Frontmatter untouched
  in both, so `metadata.acordia` stays valid and `skill-sets.json` needs no edit.
- **0 agent prompts** — no `·`-separated skill line changes; both skills are already carried where
  they belong.
- **0 source-document changes** — `briefing-reporting` is an existing grid row (`Core` deep,
  `Mission`/`Terrain`/`Def`/`Coll` working) whose marks and slug are unchanged, and
  `aleph-entity-graph` is procedural with `grid_row: null`. Adding method prose inside an existing
  skill alters no grid fact, and no grid edit is permitted in this change.
- **1 generated artifact** — `acordia-map.html` embeds skill bodies as rendered HTML, so it is
  re-derived and ships in the same commit.
- **Specs**: `skill-library`.
- **Version**: MINOR, `6.6.0` → `6.7.0`. Two skill bodies reach every marketplace consumer, so it
  must bump; the roster and the distribution shape are unchanged, so it is not MAJOR.

## Out of scope, recorded not fixed

- **The existing `report.html` is not regenerated.** Its `{6: 5, 7: 2, 8: 29, 40: 5}` tail
  distribution is the acceptance baseline this discipline exists to prevent, and rewriting the
  artefact would destroy the measurement without changing the skill that produced it.
- **`briefing-reporting` names no specific parser.** The available parser depends on the host, so the
  skill requires probing for one and naming it rather than hard-coding a dependency a distribution
  cannot guarantee.
- **The inert `## If you cannot dispatch` guard** in `acordia-analysts/agents/cyber-analyst.md` is a
  separate defect from the same run, recorded in `docs/implementation-notes.md` and deliberately not
  fixed here.
