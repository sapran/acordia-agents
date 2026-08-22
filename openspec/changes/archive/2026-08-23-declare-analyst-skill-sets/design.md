## Context

The mapping this change makes machine-readable was never missing — it was unparseable. Each prompt
already carries it in two forms, and reading both is what corrects the record:

| binding | where | carries |
|---|---|---|
| `·`-separated line under a skill heading | 5 prompts | 19–30 slugs each |
| slug in backticks in a procedural section | 5 prompts | the same 3 procedural skills, in every prompt |

`6.1.0` read only the first and drew two wrong conclusions from it: that three skills were named in
no prompt, and that `overwatch-analyst`'s catalogue cost 11,114. Reading both gives true set sizes of
22, 25, 29, 31 and 33, and a true worst-case cost of 12,211 — over the 12,000 target `6.1.0` reported
as met. Those corrected sizes also match the handoff's own indicative scan (22, 25, 28, 31, 32) far
more closely than `6.1.0`'s did, which is the signal that the handoff's regex had caught both
bindings and `6.1.0`'s had not.

## Goals / Non-Goals

**Goals:**

- One file a host can read to load a single analyst's skills.
- A check that proves the file matches the prompts, in both directions, and can be shown to fail.
- The largest analyst genuinely under 12,000, measured on its true set.

**Non-Goals:**

- Resolving the grid/prompt disagreement about the analytic spine. Deferred, with reasons, in the
  proposal.
- Deciding what the procedural skills *should* belong to. The declaration records that all five
  prompts name them; it makes no claim that this is the right division.
- A frontmatter field on the agent. Rejected below.

## Decisions

**A separate JSON file, not a frontmatter key.**

The handoff asks for "a machine-readable field", which reads most naturally as agent frontmatter.
Rejected, for two reasons that compound. Agent frontmatter is contractually exactly `name`,
`description`, `color`, and `agent-roster` states that anything else "either restricts a capability
the agent is meant to have or is silently ignored". A key literally named `skills` is the plausible
name for an allowlist, and this pillar's entire posture is capability-by-omission — the failure would
be a silently narrowed agent, which is the worst class of defect here because nothing reports it.
Changing that contract to admit one inert key would spend the contract's whole value.

The file also has to reach the consumer. The consumer is the host that renders the catalogue, so the
declaration ships inside `acordia-analysts/` rather than in `docs/`, where an installed plugin could
not see it.

**The prompts stay authoritative; the file is a transcription.**

Two copies of one fact is how this repository already acquired the grid/prompt drift, so adding a
third copy without a check would be repeating the known failure. The mitigation is that the
declaration is explicitly *not* a second source of truth: the requirement names the prompt as
authority, and the check is bidirectional, so a divergence is a defect in the file rather than an
open question about which is right.

*Alternative considered — make the `·` lines contractual and skip the file.* The lines are already
parseable; a ten-line regex reads all five prompts. But `agent-roster` explicitly forbids stating
their adjacency as a contract, and more practically, no host will implement a bespoke parser for
`·`-separated slugs under enumerated heading texts to decide which skills to load. A JSON file is
read in one line by anything. The check is what buys back the safety that a single source would have
given for free.

**A hard per-description ceiling was the right instrument, and this proves it.**

`6.1.0` chose a hard 200-character ceiling over the handoff's mean-based target, on the argument that
a mean bounds the library without bounding any role. That argument is what limited this correction to
a 268-character trim: the undercount added three skills to every role, and because no single
description could exceed 200, the damage was bounded and local. Had the library been sitting at a
mean with a long tail, the same undercount could have put a role arbitrarily far over.

## Risks / Trade-offs

- **`overwatch-analyst` clears 12,000 by 57 characters.** That is thin, and one skill added to its
  set would break it. The number to keep in view is the real one: against the 18,000-character host
  budget it leaves 6,057 for the host's own skills, which is ample. 12,000 is the handoff's headroom
  target, not the budget, and a future roster change should re-measure rather than assume.
- **Nothing in the repository runs the check.** There is no build and no test suite, so the
  declaration joins the invariants that depend on `~/ai/checks/check-acordia.sh` and on a reviewer.
  The check is documented in `CLAUDE.md` in runnable form; folding it into the external gate is a
  separate edit to a file outside this project and was not made here.
- **The declaration can rot silently between checks.** A prompt edited without the file will pass
  every harness, load correctly, and ship a wrong declaration — the file is inert to both harnesses.
  This is the same exposure as the two marketplace catalogs, and is why the check is bidirectional
  rather than one-way.
- **The corrected figures supersede published ones.** `6.1.0`'s release notes and PR carry 11,114 and
  the three-orphan claim. Both are wrong; the records in the tree are corrected here, but anything
  already read elsewhere is not.
