## ADDED Requirements

### Requirement: Every prompt states a hand-back contract

Each of the five agent prompts SHALL state how its work returns across a dispatch boundary, in three
parts:

1. **The working is written down.** The full working — evidence with its identifiers, the queries and
   commands run, what was rejected and why, and what was deliberately not done — SHALL be written to
   a notes file in the task's working directory before the agent returns.
2. **What returns is bounded and self-describing.** The reply SHALL be a summary carrying the
   judgement, its confidence, the gaps that bound it, and **the name of the notes file** where the
   evidence lives.
3. **The bound is treated as real.** The prompt SHALL state that a read exceeding the bound is cut in
   transit without warning to either side, and that a read which does not fit means the question was
   too large — to be reported as such, naming what was left out, rather than handed back truncated.

The reason is that a delegated agent's reply is bounded in every harness this pillar targets, and the
bound is enforced by silent truncation: no error is raised, the child is not told its text was cut,
and the parent cannot see that it received a fragment. Files the child wrote are not carried back but
remain readable, so the durable half of the work SHALL travel by the filesystem and only the
judgement by the reply.

The bound SHALL be stated by the dispatching brief and SHALL NOT be written into any prompt as a
number. A count correct for one harness is wrong on every other, and a wrong number in a shipped
prompt is worse than none because it reads as authoritative.

#### Scenario: Contract present in every prompt

- **WHEN** each of the five agent prompts is read
- **THEN** each states that the full working goes to a notes file, that the reply is a bounded
  summary naming that file, and that the bound is treated as real

#### Scenario: No prompt hard-codes a limit

- **WHEN** the five prompts are searched for a character count, a token count or any other numeric
  reply limit
- **THEN** none is found, and each prompt attributes the bound to the dispatching brief

#### Scenario: A read that does not fit is reported, not truncated

- **WHEN** an analyst's read exceeds the bound its brief stated
- **THEN** its prompt requires it to say the question was too large and name what was left out,
  rather than return a summary that stops mid-sentence

#### Scenario: The summary can be followed to the evidence

- **WHEN** a lead receives a leg's reply
- **THEN** the reply names the notes file, and the lead can read the full working from it without
  re-dispatching

### Requirement: The orchestrator supplies the task directory and the bound

`cyber-analyst` SHALL state the task-directory convention: each task gets its own directory, named
with a short dated slug, holding a `README.md` that carries the originating request **verbatim**, the
date, and one line on what is being settled. The analysts' notes files belong in that same directory,
and the orchestrator SHALL read them before it fuses.

The directory SHALL be stated by the dispatching brief and SHALL NOT be written into any prompt as a
path. A lead and a sandboxed leg can reach one directory under two different names, so any absolute
path in a prompt is wrong on one side of that boundary.

`cyber-analyst` SHALL supply **both** the directory and the reply bound in every dispatch, alongside
the objective, operating logic, stage, tempo and risk tolerance it already carries. An unstated bound
is the orchestrator's defect and not the leg's, because a leg told nothing cannot size a reply it was
never given the size of.

The convention exists so an operation is navigable afterwards — by the human operator the pillar
hands its product to, or by the orchestrator itself once its own context has been compacted. The
request is kept verbatim because a paraphrase is already an analytic judgement, made at the moment
least is known.

#### Scenario: Convention stated in the lead prompt

- **WHEN** `cyber-analyst`'s prompt is read
- **THEN** it states the per-task directory, the dated slug, the `README.md` holding the request
  verbatim with its date and what is being settled, and that the legs' notes go in the same directory

#### Scenario: Both are supplied on dispatch

- **WHEN** `cyber-analyst` dispatches any leg
- **THEN** its prompt requires the brief to state the working directory and the bound on the reply

#### Scenario: No path is baked into a prompt

- **WHEN** the five prompts are searched for an absolute task-directory path
- **THEN** none is found, and the directory is attributed to the dispatching brief

#### Scenario: The lead reads the notes before fusing

- **WHEN** the legs have returned and the orchestrator fuses their reads
- **THEN** its prompt requires it to read the notes files in the task directory, not to fuse from the
  bounded summaries alone
