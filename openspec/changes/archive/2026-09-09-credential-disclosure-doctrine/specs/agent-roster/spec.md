## MODIFIED Requirements

### Requirement: Analyst prompts carry the four cross-cutting sections

Each of the five analyst prompts SHALL carry a credential-harvest section naming
`credential-harvest-triage`, an exhaustive-processing section naming `exhaustive-data-processing`, an
Aleph-corpora section naming `aleph-entity-graph`, and a tool-discipline section stating that native
read/grep/glob are preferred and `bash` is for work no native tool fits. A leg SHALL state that it
cannot fan out and must surface an unfinished remainder to the orchestrator.

The credential-harvest section SHALL, in **all five** prompts including the orchestrator, state that
ownership is classified before any other handling decision, that material whose ownership is unsettled
is handled as the operation's own, and that a value crosses only as a file its reader opens rather than
in a dispatch, a reply or a hand-back. Each of the **four legs** SHALL additionally state that a
credential-reading command terminates in a file write rather than in standard output and that values
are held in a credential file named in the working notes rather than written inside them, because a leg
runs the extractions and writes the notes the orchestrator later reads. The **orchestrator's** section
SHALL state that it fuses from a leg's notes rather than from the credential file those notes name, and
that a product carrying values is written rather than returned in a reply — it is the agent that fuses
the findings and writes the product, so it is where both of those decisions are taken.

#### Scenario: Sections present

- **WHEN** any of the five analyst prompts is read
- **THEN** it carries credential-harvest, exhaustive-processing, Aleph-corpora and tool-discipline sections

#### Scenario: Leg surfaces a remainder instead of fanning out

- **WHEN** a slice is larger than a leg can finish
- **THEN** its prompt requires it to report the remainder to the orchestrator

#### Scenario: Every prompt states the credential routing rule

- **WHEN** each of the five prompts' credential-harvest section is read, the orchestrator's included
- **THEN** it requires ownership to be classified first, treats unsettled material as the operation's
  own, and permits a value to cross only as a file its reader opens rather than in a dispatch, a reply
  or a hand-back

#### Scenario: A leg states the extraction and credential-file rules

- **WHEN** each of the four leg prompts' credential-harvest section is read
- **THEN** it requires a credential-reading command to terminate in a file write rather than standard
  output, and requires values to be held in a credential file named in the working notes rather than
  written inside them

#### Scenario: The orchestrator states the rule rather than delegating it

- **WHEN** `cyber-analyst`'s credential-harvest section is searched for the routing rule
- **THEN** the rule is stated in the section itself and not left to the legs' prompts, and it requires
  fusing from a leg's notes rather than from the credential file those notes name, with a product
  carrying values written rather than returned
