## Context

The guard has been inert since it was written. `docs/implementation-notes.md` recorded the measurement
on 2026-09-02 and named the candidate fix — "a positive check the agent must perform and report" — and
parked it because it is an agent-prompt change carrying its own proof obligation. This change discharges
that obligation.

## The defect is a phrasing class, not a wording problem

A conditional on an absence has no trigger. "If you cannot dispatch, stop" asks the model to notice
something that is not there, and nothing in its input draws attention to the gap: the tool list simply
contains fewer entries than it would otherwise. Every other rule in the prompt is triggered by something
present — a brief, a leg's return, a corpus, a decision point — so this one rule was the only one with no
occasion to fire, which is why it never did.

Making the check positive gives it an occasion: the session's start. The model is asked to look, and to
emit a token either way. This is why the verdict is required on *both* branches rather than only on
failure — a rule that produces output only in the rare case is a rule the model can satisfy by doing
nothing, and it is unfalsifiable from the transcript. Requiring `dispatch: available` on the common path
is what makes its absence visible.

## Why the wording refuses the expected answer

`— from what you hold, not what you expect` is load-bearing. The orchestrator's own prompt tells it that
it directs four legs, so the role implies the capability, and a model asked "can you dispatch?" will
answer from the role unless told not to. The 2026-09-02 run is the evidence: the agent *did* enumerate
its tools and *did* see the absence, and still did not act on it. Looking was never the failure;
connecting the observation to the rule was.

## Alternatives considered

**Raise `task.maxRecursionDepth` in the profile.** Fixes the instance, not the class. It also widens leg
capability past the design — the leg prompts state that a leg cannot fan out — and leaves every other
profile exposed.

**Detect after the fact, by requiring the product to name each leg's notes file.** Worth doing, and the
pasted sweep briefs now do it, but it catches a run that has already been wasted. It is a complement to
this change, not a substitute.

**Remove the orchestrator's own analysis tools so it must delegate.** Rejected on repository doctrine:
capability is granted by omission and a capability problem is never fixed by adding a denylist.

## Ceiling

The prompt sat at 10,479 of 10,500 characters, so the change had to pay for itself twice — once for the
check, and again for the fix to the first review's finding that the loop doctrine had been scoped into
the failure branch. The ceiling requirement prescribes the method — move technique detail to the skill
that owns it, never delete routing or guardrails — so two moves were made:

- the instrument-choice detail to `gain-loss-calculus`, which already compares a move against the null
  option and now compares it against a non-cyber instrument, carrying the substitute / complement /
  support definitions with it rather than only the names;
- the working-directory convention (dated slug, `README.md` holding the request verbatim) to
  `briefing-reporting`, which owns the shape of a product and its record.

The orchestrator keeps the routing in both cases, and keeps the claim that is its own: that Analysis is
a core activity and starving it produces capability without effectiveness. Result: 10,453 of 10,500.

## Risks

The check costs a line of output at the top of every lead session, on a prompt with 47 characters of
headroom. If a later change needs that space, the honest move is another move-to-skill, not deleting the
verdict — a silent guard is what this change exists to end.
