## Context

The pillar dispatches four legs from one lead and fuses their reads centrally. That structure is
correct and is not in question here — the deployment that raised the defect confirmed the running
shape matches what `cyber-analyst` describes. What is missing is the contract on the return path.

A delegated agent's return value is bounded in every harness the pillar targets, and the bound is
enforced by truncation rather than by refusal. Nothing raises an error, nothing warns the child that
its text was cut, and nothing tells the parent it received a fragment. Both harnesses also promote
text only: files the child wrote are not carried back, but they are still there to be read.

That last fact is what makes the fix possible. The channel is narrow; the shared filesystem is not.
So the design is to stop using the narrow channel for the thing that does not fit.

## Goals / Non-Goals

**Goals**

- Every analyst writes its full working somewhere durable before it returns.
- What returns is small, self-describing, and points at the working.
- The bound is known to the analyst *before* it writes, not discovered after it is cut.
- The prose survives being installed on any harness, including harnesses that do not exist yet.

**Non-Goals**

- Naming a character count, a harness, a tool, a path, a model or a context window. Each of these
  was correct for exactly one deployment and wrong everywhere else, and a wrong number in a shipped
  prompt is worse than no number, because it reads as authoritative.
- Changing the delegation architecture, the roster, the skill sets or the competency grid's rows.
- Enforcing anything. There is no runtime here; the prompt is the only mechanism.

## Decisions

**The bound is supplied, never fixed.** The prompt says the dispatching brief states the bound and
that the analyst treats it as real. A deployment sets it from its own truncation limit. This is
Lindsay p. 178's prowords — a script agreed in advance by the planners, not improvised at the moment
of transmission — and it is the only phrasing that stays true when the limit differs per harness.

**The lead supplies it, so an unstated bound is the lead's defect.** Assigning the duty matters more
than stating it exists. The lead already dispatches with objective, logic, stage, tempo and risk
tolerance; the directory and the bound join that list. A leg that is told nothing cannot be blamed
for a read that did not fit.

**A read that does not fit is a finding, not a formatting problem.** The instruction is to say the
question was too large and name what was left out. This preserves the lead's ability to
re-partition, which is the same move the prompts already require when a data slice is too large to
process exhaustively. Silent truncation destroys that ability, because the lead never learns the
partition was wrong.

**The task directory is stated by the brief, not constructed.** In the reporting deployment the lead
and the legs reach one directory under two different names, because the legs are sandboxed. Any
absolute path written into a prompt is therefore wrong on one side of that boundary. The lead passes
on what its own brief gave it.

**The `README.md` holds the request verbatim.** A paraphrase of the request is already an analytic
judgement, and it is the judgement most likely to be wrong at the start of a task, when least is
known. Keeping the original text costs nothing and is what makes the directory readable months later
or after the lead's own context has been compacted.

**The contract goes in prose sections, not frontmatter.** Frontmatter is exactly three keys and no
harness reads a fourth. Placement is beside each prompt's existing *What to return* section, because
that is where an analyst is already being told what its output is, and a contract stated far from it
would be read as a separate topic.

## Risks / Trade-offs

- **The prompts grow.** Every prompt is a per-dispatch cost. Mitigated by writing the contract once
  per prompt, in one short section, and by leaving the existing *What to return* section to say what
  the content is — the new section says only where it goes and how much of it travels.
- **An operator whose deployment supplies no bound gets a contract with a hole in it.** Accepted: the
  prompt still requires the notes file and still requires the summary to name it, which is most of
  the benefit. The alternative — a default number — is exactly the harness-specific figure this
  change refuses to ship.
- **The convention is unenforceable.** True of every posture in this distribution, including the
  read-only-inputs rule. Prompt contracts are what the pillar has.

## Migration

None. Nothing consumes these sections programmatically, no skill line moves, and the declaration in
`skill-sets.json` is unaffected. An installed 6.3.0 keeps working; a user picks this up by upgrading.
