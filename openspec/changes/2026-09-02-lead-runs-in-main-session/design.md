## Context

The pillar ships five prompts. Four are legs and are delivered by dispatch, which is the mechanism
that loads an agent prompt. The fifth is an orchestrator, and dispatch is precisely the mechanism that
disables it: a spawned agent cannot spawn. So the one prompt that must reach a dispatching session is
the one prompt the distribution has no way to deliver.

## Delivery mechanisms considered

A distributable plugin can put text into a session that can still dispatch by exactly one route in the
harnesses this pillar targets.

**Command wrapper — chosen.** A file-based slash command expands its markdown body into prompt text
delivered to the current session. The session keeps its own tool set, so it can dispatch. This is the
only mechanism the plugin can ship that reaches a dispatching session.

**A cwd context file.** Re-read at session open. Rejected: a plugin cannot place a file in a user's
working directory, and the file would have to be authored per operation by someone. It is also not
sticky — context files are session-opening instructions, not re-attached each turn — so it buys less
persistence than it appears to.

**A skill the main agent reads.** Rejected on measured evidence: the run that motivated this change
made zero skill reads across 92 tool calls, and skill uptake across the wider corpus is roughly a
third of sessions. A delivery path that depends on the model electing to read something is not a
delivery path for the prompt that governs the whole operation.

**A pointer to the agent file inside the wrapper.** Would keep one source of truth. Rejected: command
expansion supports only `args`, `ARGUMENTS` and `arguments`, with no plugin-root path substitution, so
the wrapper cannot name the file's location portably; and it would reintroduce the dependency on the
model choosing to perform a read.

## The duplication, and why it is acceptable

Inlining puts the orchestrator's body in three files. This repository deleted its generator in 3.0.0
and has no build step, so nothing regenerates them and drift is a real risk — a wrapper silently a
version behind the agent is exactly the class of defect this change exists to remove.

The repository already has a precedent for hand-maintained byte-identical files: the two marketplace
catalogs, checked by the drift gate. The same treatment applies here. The gate is the reason the
duplication is safe, so the invariant ships with the change rather than after it, and is negative-
tested — induced drift must be shown to fail the gate before the change is called done.

Three copies is the cost of a harness that offers one delivery path. The alternative is a lead that
loads correctly and cannot lead, which is worse because it does not announce itself.

## Keeping the agent file

`cyber-analyst.md` stays in `agents/`. Removing it would change the roster and force a MAJOR bump, and
it remains legitimately useful when someone wants the orchestrator's judgement over material already
gathered, with no legs to dispatch.

But it must not be silently usable as a lead. The refusal instruction is the guard: an orchestrator
that cannot dispatch says so and names the wrapper, converting a silent degradation into a loud one.
This mirrors the existing leg requirement that a specialist which cannot fan out surfaces the
remainder rather than absorbing it.

## What is deliberately not attempted

Prose invocation — "use cyber-analyst" typed as a sentence — cannot be intercepted by anything the
distribution ships. The change makes the correct route work and makes the incorrect route loud; it
cannot make an unrouted sentence work. That residue is recorded rather than papered over.
