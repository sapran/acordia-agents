## Context

Both defects come from the same run and share a shape: the analyst did the analytic work well, then
lost part of it in the mechanics of handing it over or of addressing a tool. Neither skill was
disobeyed. `briefing-reporting` was followed to the letter — the product led with its judgement,
marked confidence, named gaps and landed in the right place — and the skill simply had nothing to say
about what happens when that product is also rendered into HTML. `aleph-entity-graph` was likewise
followed: scope, facet, narrow, pivot, read late. It has nothing to say about how the call itself is
assembled.

That is why neither fix is a correction. Both are additions at the point where the skill currently
goes quiet.

## Why the reporting rule is about verification, not about HTML

The obvious framing is "use a markdown library". It is too narrow: the same failure recurs with PDF,
with a deck, with anything where the source format is not the delivered format, and a rule naming one
converter would not transfer.

The transferable part is that **a regex converter fails silently**. It handles what it models and
passes the rest through as literal text, so it never errors, and the product it emits is
well-formed — just wrong in the places nobody looked. The rule therefore names the failure mode
(inline emphasis, code spans, tables, inline links) rather than a tool, requires a real parser for
the target format, and requires the analyst to say which one they used. Naming the parser is what
makes the choice reviewable.

The citation rule is the same argument at identifier level. A truncated hash is not a degraded
citation; it is a citation that has stopped being one, while continuing to look like one. Shortening
for display is legitimate and common, so the rule separates the two: carry the identifier whole into
what is *recorded*, and let the rendering shorten what is *shown*.

## Why the verification bullet is separate from both

Because the verification is what actually failed. Both generation passes in the run were checked, and
both checks were link counts. A count is satisfied identically by 40 resolvable references and by 5,
so the check could not distinguish the defect from success — and it was run twice, which is why the
product read as verified.

The bullet therefore states two distinct checks and rejects the substitute explicitly: no
source-format tokens survive in the output, *and* a sample of the references is resolved against the
issuing system. It names counting as detecting neither failure, because a bullet that merely said
"verify the output" would have been satisfied by exactly what was already done.

It sits in `## Signals / outputs` rather than `## Method` deliberately. The other bullets there
describe what a finished product looks like; a rendered product that has not been resolution-checked
is not finished, which is the claim being made.

## Why the Aleph subsection sits with tooling, not in the method

`## Method` is a numbered sequence performed once per investigation: scope, inventory, facet, narrow,
pivot, read, script. Argument construction is not a step in that sequence — it applies to every call
at every step, including the ones the analyst reaches after abandoning the sequence.

`## Tooling — state which one you have` is where the analyst establishes which surface they are
addressing and what it does and does not enforce for them. That is the same decision. The subsection
extends it: having established that the tools are mounted, this is how a call to them is built. It
also inherits the section's closing instruction to say which path you are on, so the argument rules
land against a named surface rather than in the abstract.

## Stating the identifier argument without restating the schema

The server's schema already requires `entity_id`, so a skill that only listed parameter names would
be redundant with the tool description the analyst can already see.

What the schema cannot carry is the **shape of the failure**. An unrecognised key is dropped rather
than refused, which splits the outcome in two: sometimes the call fails naming a missing `entity_id`,
which is diagnostic; and sometimes it reaches the server carrying no identifier and returns a
not-found, which reads as a bad *identifier* rather than a bad *call*. The second outcome is why the
mistake survived five occurrences across two runs — the analyst concluded the entity did not exist
and moved on.

Naming both outcomes is the part that is not redundant. The count is included because it is the
evidence that the failure is silent enough to repeat.

## Why serialisation, and why it points at an existing skill

The six malformed searches were not carelessness in the ordinary sense — each one escaped its first
quoted phrase correctly and then stopped. That is a hand-construction failure with a characteristic
signature, and it lands on the second phrase, which in this corpus was the non-English one, which is
exactly the phrase the search needed.

A rule saying "escape carefully" would restate the thing that already failed. The rule instead moves
the escaping out of the analyst's hands: build the object with a serialiser inside a script. That is
the same path `analytic-tooling-scripting` already recommends for the repetitive case, so the
subsection points at it rather than duplicating its argument — and the cross-reference makes the
throughput benefit visible at the moment the analyst is deciding how to make one call, not just
twenty.

## Why ADDED and not MODIFIED

The two new requirements are added, not folded into the existing requirement
`aleph-entity-graph skill exists`. That requirement runs to roughly 129 lines and carries 17
scenarios, and a `## MODIFIED Requirements` block replaces the whole requirement — every scenario
must be re-carried verbatim. Re-stating 17 scenarios to add two sentences is how a scenario gets
silently dropped, and `--strict` names the omission only if the omission is total.

`briefing-reporting` is `family: analytic-spine` and is exempted from the `Method contract for
evidence-reading skills` requirement, so nothing existing governs its body either. Two new
requirements, one per skill, leave every existing scenario untouched.

## Literature

Searched and recorded in `proposal.md`: two `library_route` queries, 20 documents returned, all at
floor relevance and all on other questions. **The canon holds nothing on rendering a product into a
second format or on the completeness of a source identifier.**

That is the expected result rather than a surprising one. Both edits are tool- and format-mechanics —
technique detail, in `CLAUDE.md`'s terms — and the register exists for doctrinal claims about how the
work is divided, what an operation is for, and how a judgement is framed. Neither skill gains a
`doctrine_source`: attaching one would assert that a registered work prescribes a markdown parser or
a JSON serialiser, which none does.

## What is deliberately not attempted

The skills do not name a specific parser, a specific serialiser or a specific link-checking
procedure. Which parser exists is a property of the host, and a distribution that hard-coded one
would ship a dependency it cannot guarantee. The requirement is that a real parser is used and named,
and that references are resolved rather than counted — both checkable in the product without the
skill prescribing a tool.

The existing `report.html` is left exactly as it is. It is the measurement that justifies the change,
and 35-of-40 is only evidence for as long as the artefact still says so.
