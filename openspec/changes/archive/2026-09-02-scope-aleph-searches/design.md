## Context

The skill already teaches an analyst to be careful about the things Aleph makes visible: the 9999
paging window, the 200-per-property expansion cap, the 10,000 total that is a floor rather than a
count, the 66% term match that widens a query instead of narrowing it. Every one of those is a fact
the analyst can see going wrong.

Collection scope is not like that. An unscoped search returns a full, ranked, correctly-shaped result
set. Nothing in the reply says "this came from somewhere else". So the failure mode is not that the
analyst gets a worse answer — it is that they get an answer to a question they did not ask, with the
same confidence as a correct one.

That is why the fix is a method step rather than a limits bullet. The limits section describes what
Aleph will not do for you. This belongs where a decision is made.

## Why first, and not appended to inventory

Inventory (`list_collections`, then `get_collection` for candidates) is how the analyst learns which
collections exist and how big each one is. It is the natural place to put "and then pick one" — and
it is the wrong place, for two reasons.

**Inventory is skippable and scope is not.** An analyst handed a collection id in the brief has no
reason to enumerate anything, and will start at the first step that looks like their situation. If
scope lives inside inventory, skipping inventory skips scope.

**Ordering is the argument.** Making scope step 1 says the decision is upstream of every query, not a
parameter of one. The subsequent steps then read as operations *within* a scope: facet within it,
narrow within it, pivot within it, read text within it. That is the discipline the change is trying
to install, and step order is the cheapest way to state it.

## Stating the required argument without restating the server

The tools' own schemas already reject a missing `collection`, so the skill does not need to teach the
mechanics. What the skill has to carry is what a schema cannot: the *forms* that save a call (a
`foreign_id` resolves server-side, so no id lookup comes first), the one literal that means
everything (`"*"`, which a schema cannot mark as dangerous), and the field to read back
(`searched.collection`).

The read-back is the part that is not redundant with the server. A required parameter guarantees the
caller passed *something*; it does not guarantee the resolved scope is what the caller meant. A
`foreign_id` that resolves to an unexpected id, or a list where one element resolves and another does
not, both produce a successful reply. `searched.collection` is the only place the applied scope is
stated, so the method reads it rather than inferring it from the request.

## The fallback is stated, not fixed

`curl` against `/api/2/entities` enforces nothing: no required scope, no `_note`, no `searched`
block. The honest options were to drop the fallback, to add an unenforceable instruction, or to name
the exposure.

Naming it is chosen, consistent with how the paragraph already treats the other five bounds the
fallback gives up. The example URL carries `filter:collection_id` so the correct shape is in front of
the analyst, and the prose says plainly that an omission is unsignalled. A fallback that silently
searches everything is a fallback the analyst should be able to price.

## Literature

None, and none applicable. The change asserts nothing doctrinal — no claim about how analytic work is
divided, what an operation is for, or how a judgement should be framed. Its content is a tool-contract
fact traceable to the `aleph-mcp` specification and a measured run, which `CLAUDE.md` classifies as
technique detail carrying no literature attribution. No `doctrine_source` is added: the skill is
procedural with `grid_row: null`, and its `source` continues to name the change that authorised it
rather than this one, which modifies a body rather than creating a skill.

## What is deliberately not attempted

The skill does not tell the analyst which collection to choose. That is the brief's job, or the
inventory step's, and a skill that guessed would be inventing scope rather than requiring it.
