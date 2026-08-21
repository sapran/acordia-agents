## Context

Two questions drove this change: what should the distribution *be*, and what makes something a
separate agent. The first is answered by the framework, the second by the grid's own stated criterion
plus a constraint from Monte that a subagent harness makes sharper than it is for a human team.

The research record is `docs/methodology-alignment-proposal.md` in the main checkout — a source
register with library document ids, thirty-four numbered passages, and the gap analysis this change
implements. It stays there rather than moving into the change, because it outlives the change: it is
the first artifact `doctrinal-provenance` formalises.

## What makes something a separate agent

The grid already states the rule and then breaks it. It says a specialist is made "not by reasoning
differently — the spine is shared — but by the technical substrate they command deeply enough to take
apart from the inside", and then describes the Fusion analyst as "shallow-but-wide". Three criteria,
made explicit here because the next roster question will need them:

1. **Deep substrate.** A distinct body of technical knowledge the agent takes apart from the inside.
2. **A different question.** Not a different method applied to the same question.
3. **Context isolation that pays.** Dispatching must save the lead more context than the round-trip
   costs.

Fusion fails all three. Its substrate is defined by breadth, its question — "what does all of it
together mean" — is the lead's own job by the lead's own description, and fusing requires ingesting
everything and handing back a summary, which is a *lossy round-trip of exactly the material the lead
most needs unmediated*. Monte names inter-unit communication as the one weak point in the attacker
model — "the different tempos, risk tolerances, tools, expertise, and leadership of the units will
inevitably lead to miscommunication and potential mistakes" — and the fused picture is the single
worst place to put that boundary.

This also fixes the number of legs. Each leg is one of Monte's communication weak points, so the
roster should be the minimum that buys real context isolation, not the maximum the grid can justify.

## Why five and not three

Three — lead, terrain, defender — was the conservative option and remains coherent. Five wins on two
specific grounds.

**Target splits because its halves are different substrates.** The grid already says so: "Two halves.
The business/mission half comes first… The technical half is the terrain itself." Crown-jewels and
mission-thread analysis is organisational work; routing, identity trust and cloud control planes are
not. The organisational half also grows under this change, because Rovner's target-bureaucracy and
target-culture conditionals make the target's procedures, redundancy and reporting norms *modelled
properties* — which is what turns sabotage from a technical effect into an analytic judgement.

**Collection is a real function that was hiding inside Fusion.** Strip the lead's work and the mission
work out of Fusion's five unique skills and what remains is take quality and data-integration tooling
— working the material, not fusing it. That function is independently grounded: Monte puts linguists,
subject-matter experts and domain knowledge under targeting capabilities and notes that strategic
collection "requires substantial analytic capabilities… an enormous amount of information to sort
through, and the exact nature of what is useful may be unknown"; Lindsay has analysts interpreting
collected data and building corporate memory. Named honestly it is collection, not fusion.

## Why the roster does not mirror ACORDIA's three Analysis functions

The framework names target understanding, pattern recognition and operational planning. Mirroring
those 1:1 into agents was considered and rejected, because it reproduces the Fusion defect twice:
*pattern recognition is a method, not a substrate*, and *operational planning is the lead*. Only
target understanding is a substrate, and it is the one that splits. A framework-faithful roster is not
a framework-shaped roster.

## Overwatch and the pillar boundary

`overwatch-analyst` has the deepest substrate in the grid and is not in question, but with only
Analysis shipping it is the leg that reaches into another pillar: ACORDIA puts "overwatch of target
environments" under **Control**, not Analysis. The boundary that keeps it honest is that this agent
performs the *analysis of* detection — how the defence detects in principle, what our own emissions
say, when the defender is likely to be onto us — and does not perform the Control action that follows.
The prompt must state that boundary, or the pillar leaks.

## The consumer

With no operations pillar, an analyst product is handed to a human operator who then acts. This is a
real change to the lead, not a note: `cyber-analyst` currently describes itself as directing
specialists through an operation, and its end-neutral loop asks whether *we* achieved the effect. It
becomes a product for a person, and the loop judges from reported evidence.

The honest cost is that the distribution can no longer be validated end to end inside itself. That is
accepted. The alternative — keeping a pentest pillar so the analysis has something to talk to — is
paying for validation with the coherence of the whole thing.

## Stable row ids

Thirty-eight skills anchor into the grid by line number, spanning L67–L108, and the grid document
states in as many words that nothing may be inserted above it. The scheme has been working only
because nobody has edited the grid's head. This change edits the grid, so the anchors break anyway;
re-anchoring now costs one pass and removes a permanent trap.

Row ids are kebab-case, minted once, carried in the grid row itself, never reused after retirement,
and never renumbered when rows move. The skill carries `row: <id>` and a `source:` without a line
number. Alternatives rejected: content hashes (change when prose is edited, which is the common case),
row numbers (renumber on insert, same defect as lines), and skill slugs as ids (couples the id to a
name that may be renamed for dispatch reasons).

## Deferred deliberately

The **operating-logic axis** — espionage / subversion / sabotage, and the objective taxonomy that sits
beside it — is specified by `doctrinal-provenance` and the grid delta but its *prose* is not authored
in this change. It rests on passages that have not yet been selected, and authoring doctrine before
that selection is precisely the failure the literature-first rule exists to prevent. It lands in the
implementation phase, after selection.

A future **Research** pillar is the ACORDIA-honest expansion if one pillar proves thin. It composes
with Analysis and makes no target contact, so it does not reintroduce the category error this change
removes. Out of scope here.
