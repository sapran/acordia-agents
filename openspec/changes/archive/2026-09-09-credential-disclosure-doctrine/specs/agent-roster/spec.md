## MODIFIED Requirements

### Requirement: Analyst prompts carry the four cross-cutting sections

Each of the five analyst prompts SHALL carry a credential-harvest section naming
`credential-harvest-triage`, an exhaustive-processing section naming `exhaustive-data-processing`, an
Aleph-corpora section naming `aleph-entity-graph`, and a tool-discipline section stating that native
read/grep/glob are preferred and `bash` is for work no native tool fits. A leg SHALL state that it
cannot fan out and must surface an unfinished remainder to the orchestrator.

The credential-harvest section SHALL, in **all five** prompts including the orchestrator, name
`credential-harvest-triage` as the source of the handling rules, state that ownership is settled before
any other handling decision, and express the permission as a **closed grant** — what may be recorded —
rather than as a list of prohibitions, so that an ownership the prompt does not enumerate falls outside
the grant instead of through it.

Each of the **four legs** SHALL additionally state that a credential-reading command terminates in a
file write rather than in standard output; that values, and any command carrying one, are held in a
credential file named in the working notes rather than written inside them; and that a value never
enters what the leg hands back. A leg runs the extractions and writes the notes its caller later reads,
so these are leg-side rules.

The **orchestrator's** section SHALL state that it opens a leg's credential file only as a judgement
needs it rather than as part of the routine read it makes of that leg's notes, and that a product
carrying values is written rather than returned in a reply. It is the agent that correlates across legs
and writes the product, so it SHALL NOT be cut off from the values those two jobs require; the
distinction the prompt draws is between a deliberate read and an automatic one, not between permitted
and forbidden.

#### Scenario: Sections present

- **WHEN** any of the five analyst prompts is read
- **THEN** it carries credential-harvest, exhaustive-processing, Aleph-corpora and tool-discipline sections

#### Scenario: Leg surfaces a remainder instead of fanning out

- **WHEN** a slice is larger than a leg can finish
- **THEN** its prompt requires it to report the remainder to the orchestrator

#### Scenario: Every prompt states the credential routing rule

- **WHEN** each of the five prompts' credential-harvest section is read, the orchestrator's included
- **THEN** it names `credential-harvest-triage` as the source of the handling rules, requires ownership
  to be settled first, and states the permission as a closed grant of what may be recorded rather than
  as a list of prohibitions

#### Scenario: A leg states the extraction and credential-file rules

- **WHEN** each of the four leg prompts' credential-harvest section is read
- **THEN** it requires a credential-reading command to terminate in a file write rather than standard
  output, requires values and any command carrying one to be held in a credential file named in the
  working notes rather than written inside them, and forbids a value entering the hand-back

#### Scenario: A hand-back keeps values out of the notes

- **WHEN** the hand-back contract's written-working clause is read
- **THEN** a credential value, and a command carrying one in its arguments, is excepted from the notes
  file and written to the credential file the notes name

#### Scenario: The orchestrator states the rule rather than delegating it

- **WHEN** `cyber-analyst`'s credential-harvest section is searched for the routing rule
- **THEN** the rule is stated in the section itself and not left to the legs' prompts, and it permits
  the credential file a leg's notes name to be opened as a judgement needs it rather than as part of
  the routine notes read, with a product carrying values written rather than returned

### Requirement: Every prompt states a hand-back contract

Each of the five agent prompts SHALL state how its work returns across a dispatch boundary, in four
parts:

1. **The working is written down.** The full working — evidence with its identifiers, the queries and
   commands run, what was rejected and why, and what was deliberately not done — SHALL be written to
   a notes file in the task's working directory before the agent returns. A credential value, and a
   command carrying one in its arguments, SHALL be excepted from that file and written to the
   credential file beside it, which the notes name; otherwise the hand-back contract would put into
   the notes exactly what the credential rule keeps out of them, and the notes are the file a caller
   reads to fuse.
2. **What returns is bounded and self-describing.** The reply SHALL be a summary carrying the
   judgement, its confidence, the gaps that bound it, and **the name of the notes file** where the
   evidence lives.
3. **The bound is treated as real.** The prompt SHALL state that a read exceeding the bound is cut in
   transit without warning to either side, and that a read which does not fit means the question was
   too large — to be reported as such, naming what was left out, rather than handed back truncated.
4. **The contract holds when nothing supplies its inputs.** Every leg has a command wrapper that
   dispatches it straight from a person, so a leg may run with no orchestrator above it and a brief
   that names neither directory nor bound. Each prompt SHALL therefore address its reply to whoever
   dispatched it rather than to the lead by name; SHALL create a working directory and identify it by
   name when the brief names none; and SHALL keep the summary short, letting the notes carry the
   rest, when no bound is stated.

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

#### Scenario: A leg dispatched directly, with neither input supplied

- **WHEN** a person dispatches a leg through its command wrapper, which passes the brief alone and
  names no directory and no bound
- **THEN** its prompt still requires a notes file — in a directory the leg creates and identifies by
  name — and a short summary pointing at it, rather than a reply addressed to an absent lead
