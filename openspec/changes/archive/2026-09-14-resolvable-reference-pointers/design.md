## Context

Fifteen pointers, eleven bodies, one reference directory. The question is what address a pointer
gives a session that has just read a `SKILL.md` and now wants a file it names.

Measured on the operator's workstation, 2026-09-14:
`skill://credential-harvest-triage/references/report-layout.md` resolves. A print-mode session
returned 325 lines from the profile's plugin cache at 6.13.0. That path is from the session's own tool
record, not the model's reply — the model's prose quoted a native path that does not exist on that
host, which is itself a reminder that a model's summary is not evidence of what a tool did.
`skill://credential-harvest-triage` is proven the same way: the failing sweep opened it correctly two
minutes before it failed on the references.

**Goals:**

- Every pointer carries an address that opens without reconstruction.
- One construct, no added sentence per pointer.
- Nothing asserted about a harness that has not been measured.

**Non-Goals:**

- Enforcing any of it. There is no build step and no code path that reads a skill body; this is prose
  an analyst follows.
- Moving, renaming or editing either reference file.
- A repository-wide convention for `skill://` beyond pointers to a file or a skill. Agent prompts name
  skills by bare slug on their `·`-separated lines because that is the binding both harnesses match
  on, and that stays exactly as it is.

## Decisions

**The link text names the file; the link target carries the URI.**
`[`references/report-layout.md`](skill://credential-harvest-triage/references/report-layout.md)`
states both in one construct and adds no prose. The alternative — replace the filename with the URI
outright — was rejected on a harness-scope argument: `skill://` is an omp internal URI, verified
working there and **not** verified in Claude Code, which also installs this plugin. Dropping the
filename would trade a measured failure in omp for an unmeasured one elsewhere. The two parts are
therefore specified as doing different jobs — the URI is the address, the filename is identification
that also opens the file in a harness resolving siblings — rather than as two addresses both claimed
openable, which is what the first draft of the requirement said and what a reviewer correctly called a
self-contradiction.

**The `../<slug>/…` form is removed rather than kept alongside.** It is not a second useful address.
It presumes both a sibling layout on disk and a resolver that reads relative to a skill body, and no
harness offers the second — so it is a third thing for a session to try and fail. The owning slug is
in the URI, which is the information `../` was carrying.

**The seven skill-to-skill pointers are in scope.** They were not in the first pass, because the
closing scan was written around link targets containing `references/` and could not see them. They are
the same defect in the same class, in the same section of the same bodies, and six of the seven point
at the disclosure doctrine — leaving them would have shipped a half-fix whose remaining half is the
more consequential one. The scope rule that parks unrelated findings does not apply: this is the
change's own subject, found by its own reviewer.

**One preventive paragraph, in the owning skill only.** The observed failure was not a missing
address; it was an invented one, followed by a filesystem-wide search. An address alone refuses
neither, so the notice names both moves and states the terminal behaviour instead: say so, and ask the
operator. The four consuming skills get no such paragraph — they point at a file they do not own, and
the rule belongs with the owner.

**The requirement is MODIFIED, not ADDED.** No published scenario became false — the pointers still
name the file. What was wrong with the published requirement is weaker and more durable: it was
satisfiable by a relative path alone, which is the defect. A requirement that permits the bug is a
requirement that reopens it, one edit later.

## Risks / Trade-offs

**`skill://` is unverified in Claude Code.** → The filename stays in the link text, so a Claude Code
session is no worse off than before this change, and the plugin's own directory is where that harness
already resolves sibling files from. Recorded here rather than asserted in the spec: no spec text
credits either harness with resolving the URI.

**The URI resolves by skill name across every skill root, so it does not close the wrong-copy
failure.** A native install of the same slug shadows the plugin first-wins and silently — that is
exactly what happened on 2026-09-12, with the correct URI resolving into a stale symlink farm. This
change cannot fix that from inside a skill body, and the notice deliberately does not ask an analyst
to audit which copy opened: that is install hygiene, it is documented where the install is managed,
and a prose instruction would give false assurance. The bound worth stating is that anyone able to
plant a skill under the user's native root already owns the session.

**Fifteen link targets edited by substitution could silently miss one.** → Each substitution asserted
its exact expected occurrence count before applying, and the closing scan was widened after the first
pass to every markdown link target under `acordia-analysts/skills/` that begins with neither
`skill://` nor `http` — it now reports zero.

**A sixteenth pointer will be added by someone who has not read this.** → That is what the MODIFIED
requirement is for, and it is the only mechanism available: the repository ships no build step, so the
obligation is checkable by reading and by nothing else.
