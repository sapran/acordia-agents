## Context

Eight pointers, five bodies, one reference directory. The question is what address a pointer gives a
session that has just read a `SKILL.md` and now wants the file beside it.

Measured on the operator's `mini` host, 2026-09-14: `skill://credential-harvest-triage/references/report-layout.md`
resolves. A print-mode session in the `opwe` profile returned 325 lines from
`~/.omp/profiles/opwe/plugins/cache/plugins/acordia___acordia-analysts___6.13.0/skills/credential-harvest-triage/references/report-layout.md`.
That path is from the session's own tool record, not the model's reply — the model's prose quoted a
native path that does not exist on that host, which is itself a reminder that a model's summary is
not evidence of what a tool did.

**Goals:**

- Every pointer carries an address that opens without reconstruction.
- One construct, no added sentence per pointer.
- Nothing asserted about a harness that has not been measured.

**Non-Goals:**

- Enforcing any of it. There is no build step and no code path that reads a skill body; this is prose
  an analyst follows.
- Moving, renaming or editing either reference file.
- A repository-wide convention for `skill://` beyond reference pointers. Agent prompts name skills by
  bare slug because that is the binding both harnesses match on, and that stays.

## Decisions

**The link text keeps the relative filename; the link target carries the URI.**
`[`references/report-layout.md`](skill://credential-harvest-triage/references/report-layout.md)`
states both addresses in one construct and adds no prose. The alternative — replace the relative path
with the URI outright — was rejected on a harness-scope argument: `skill://` is an omp internal URI,
verified working there and **not** verified in Claude Code, which also installs this plugin. Dropping
the relative form would trade a measured failure in omp for an unmeasured one in the other harness.
Keeping both means the worst case is the address a harness already had.

**The `../<slug>/references/…` form is removed rather than kept alongside.** It is not a second
useful address. It presumes both a sibling layout on disk and a resolver that reads relative to a
skill body, and no harness offers the second — so it is a third thing for a session to try and fail.
The owning slug is in the URI, which is the information `../` was carrying.

**One preventive sentence, in the owning skill only.** The observed failure was not a missing
address; it was an invented one. An address alone does not refuse
`~/.omp/agent/skills/<slug>/references/…`, so the notice names that move and forbids it. It goes in
`## Cross-cutting notice` — skill-wide, so it covers both files once instead of being repeated in the
two section paragraphs. The four consuming skills get no such sentence: they point at a file they do
not own, and the rule belongs with the owner.

**The requirement is MODIFIED, not ADDED.** No published scenario becomes false — the dual form still
states the relative path the existing scenario asks for. What is wrong with the published requirement
is weaker and more durable: it is satisfiable by a pointer that gives the relative path alone, which
is the defect. A requirement that permits the bug is a requirement that reopens it, one edit later.

## Risks / Trade-offs

**`skill://` is unverified in Claude Code.** → The relative filename stays in the link text, so a
Claude Code session is no worse off than before this change; and the plugin's own directory is where
that harness already resolves sibling files from. Recorded here rather than asserted in the spec: no
spec text credits either harness with resolving the URI.

**Eight link targets edited by substitution could silently miss one.** → Each substitution asserted
its exact expected occurrence count before applying, and a closing scan over all 45 skills confirmed
zero remaining link targets containing `references/` that do not begin `skill://`.

**A ninth pointer will be added by someone who has not read this.** → That is what the MODIFIED
requirement is for, and it is the only mechanism available: the repository ships no build step, so the
obligation is checkable by reading and by nothing else.
