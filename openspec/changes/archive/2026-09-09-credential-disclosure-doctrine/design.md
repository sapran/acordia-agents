## Context

See `proposal.md` — Why. Three constraints shape the approach.

**One act feeds three destinations.** A command printing to standard output places its bytes in the
model's context, in the session's displayed output, and in the session transcript on disk, all at
once. Measured rather than assumed: the transcript for one working session of this repository held
84,479 bytes of raw tool output stored verbatim under `toolUseResult`. A command redirecting to a file
places bytes in none of the three. There is no third setting. Any doctrine that tries to permit one of
those destinations while forbidding another is describing a control the harness does not offer.

**The distribution ships no runtime.** `tools/` holds three scripts and all three run at install or
check time; none runs during analysis. A masking helper, a vault binary or a hook would be the first
analysis-time runtime, which is a change to the shape of the distribution and therefore a MAJOR bump
and its own proposal. This change is doctrine only, so every rule it states must be one an analyst can
follow with the tools already in the prompt.

**The grid does not constrain guardrail prose.** Rows in `docs/roles/operational-analyst.md` carry a
skill name, a stable row id and five column marks. No prose. So rewording a guardrail inside a skill
cannot drift from the source of truth, and this change touches no competency.

## Goals / Non-Goals

**Goals:**

- Replace one prohibition over one undifferentiated destination with a routing rule over named
  destinations, so an analyst can follow it by choosing where output goes rather than by suppressing
  content.
- Make ownership the gate, so the case that genuinely needs an absolute prohibition — the operation's
  own material — is stated as a field rather than as an aside in one prompt.
- Close the `cyber-analyst` omission in the same change, since the orchestrator is the agent that
  fuses findings and writes the product.
- Leave the library's analytic capability intact: correlation across sources, which the triage
  procedure's step 6 already requires, stops being a workflow the skill demands and its own guardrail
  denies.

**Non-Goals:**

- Enforcement. No hook, no filter, no helper. Named as out of scope in the proposal and restated in
  the specs as a prohibition on claiming enforcement the distribution does not have.
- A masking or fingerprinting scheme. Considered and dropped — see Decisions.
- A second `.acordia/` sink. Values live in a credential file beside the analyst's notes in the
  working directory the brief already names, not in a new tree under `.acordia/`. Review corrected an
  earlier draft of this design that put values in the working notes themselves: the orchestrator is
  required to read a leg's notes before fusing, so that draft would have pulled every value into its
  context automatically.
- Any change to `docs/roles/operational-analyst.md`, `skill-sets.json`, or the roster.

## Decisions

**Ownership is a required field with four values, failing safe to `operation`.**

Two values would be simpler and wrong. A collected artefact does not sort itself: one memory capture
holds the target's credentials and, if an operator touched the host, the operation's own. An analyst
who must pick between `target` and `operation` with no third option will pick one, and the failure is
silent. `unknown` makes the unresolved case sayable, and routing it as operation-owned puts the
default on the side where the error is cheap: over-protecting a target credential costs a re-run,
under-protecting an operation credential burns infrastructure that is still in use.

`third-party` is the fourth because the two-party model has no place for a partner's token found in
the target's vault, or an employee's personal password from a browser profile. Folding those into
`target` would have the product disclose an individual's personal credential to their employer — a
harm to someone who is not party to the engagement. Splitting corporate from personal within
`third-party` keeps the remediation-relevant case disclosable while holding the personal one to
classification, which is also what `briefing-reporting` already says about personal identifiers.

Alternative considered: leave ownership in prose in the prompts, as `overwatch-analyst` has it today.
Rejected — the whole relaxation is conditioned on it, so a rule stated in one prompt of five and in no
schema field would be the load-bearing element of the design and the least visible thing in it.

**No masking or fingerprint scheme.**

An earlier shape of this change carried a keyed-HMAC handle — `CRED:ntlm:a3f91c2e` — that an analyst
would reason about in place of the value, with resolution at render time. It was dropped when the
operator accepted values reaching context: an analyst permitted to see the value needs no token to
reason about it, and the machinery costs a runtime the distribution does not have.

One finding from that work is worth keeping in the record because it is a defect in the shipped rule
rather than in the discarded design. `credential-harvest-triage` today permits a "hash-of-value if
disambiguation is needed". A bare digest of a weak credential is a lookup, not a mask — for any
password worth stealing, `sha256(value)` *is* the value. The guardrail rewrite removes that permission
rather than restating it, and nothing in this change reintroduces a bare digest.

**The redirect discipline is stated with its reason, not as a style rule.**

"Terminate in a file write" reads as tidiness unless the analyst knows that the alternative writes to
three places simultaneously. Each statement of the rule therefore carries the mechanism, because a
rule whose cost is invisible is a rule that gets skipped the first time a quick `grep` would be
convenient.

**`operational-memory` is not relaxed.**

It is the one skill whose prohibition survives untouched, and the specs state that explicitly rather
than leaving it to inference. The distinction is durability: working notes belong to one engagement
and are the operator's to destroy, while the memory record is read by everyone who comes next. That is
also the distinction that makes the relaxation safe elsewhere — a permission scoped to an engagement's
own notes is not a permission to accumulate credentials across engagements.

**Grounding is cited where doctrine carries the claim, and omitted where technique does.**

`credential-harvest-triage` gains `doctrine_source: [Monte#operational-security,
Heuer#information-quantity]`. Monte, p. 125, defines operational security as minimising exposure of the
operation's existence and marks it defensive in nature though it furthers an offensive mission — which
is why the operation's own material is a different category from the target's rather than a stricter
case of it. Monte, p. 129, states that acquiring awareness is itself less operationally secure, and
Heuer, p. 79, that information beyond what a judgement needs raises confidence without raising
accuracy; together they ground "look deliberately" as a cost/benefit judgement rather than a
squeamishness about seeing secrets.

The redirect discipline itself carries no attribution. No work in the register prescribes where a
shell command sends its output, and a citation there would falsely imply one does.

**The empty result is recorded, not filled.**

The library was searched for what the canon says about disclosing credential material in a finished
product and returned nothing on the point. That goes into `docs/roles/sources.md` under *Gaps —
searched and not found*, so a later reader knows the search happened. The disclosure rule is therefore
this repository's own reasoning from the consumer's need, and is marked as such rather than attributed.

## Risks / Trade-offs

**The rule reads as a permission to collect credentials.** → The relaxation is a permission to
*record* what analysis already surfaced, not to widen collection. The passive posture is untouched:
no validation, no login attempt, no probe. Every statement of the new permission sits in a section
that already forbids active touching, and the specs keep the "passive posture preserved" scenario
unchanged.

**A value read for a judgement is in the transcript whether or not it is restated.** → True and
unavoidable in doctrine. "Look deliberately" bounds how often it happens; it cannot make it zero. The
proposal names the `PreToolUse` / `PostToolUse` hook as the thing that would, and places it outside
this change rather than implying the prose achieves it.

**The credential file becomes a store nobody destroys.** → This is the risk the doctrine creates
rather than inherits: it gathers into one named file what previously sat scattered through notes. The
rule therefore gives the file a place, an end and an owner — beside the notes in the working directory
the brief names, destroyed when the engagement closes, named in the hand-off so whoever inherits it
knows it exists. `operational-memory` stays closed so nothing accumulates across engagements. Beyond
that the lifetime of an operator's own working directory is the operator's to manage; the distribution
states a convention and has never claimed to enforce a path.

**`briefing-reporting` is the largest single reversal and the easiest to half-apply.** → Its citation
paragraph, its verification paragraph and its spec requirement all move together. Applying the
citation change alone would leave a skill that permits a credential in the product and then requires
the analyst to read that product back to verify it, which would place every value it carries into the
transcript. The tasks keep the two in one step for that reason.

**Both lead command wrappers must move with the orchestrator prompt.** → They carry the
`cyber-analyst` body byte-identically, and `tools/check-acordia.sh` verifies that identity, so a missed
wrapper fails the gate rather than shipping. The check is run in the worktree before the PR.
