## MODIFIED Requirements

### Requirement: Analyst prompts carry the four cross-cutting sections

Each of the five analyst prompts SHALL carry a credential-harvest section naming
`credential-harvest-triage`, an exhaustive-processing section naming `exhaustive-data-processing`, an
Aleph-corpora section naming `aleph-entity-graph`, and a tool-discipline section stating that native
read/grep/glob are preferred and `bash` is for work no native tool fits. A leg SHALL state that it
cannot fan out and must surface an unfinished remainder to the orchestrator.

The credential-harvest section SHALL, in **all five** prompts including the orchestrator, state that
ownership is classified before any other handling decision and that only target-owned material may be
written down; that a credential-reading command terminates in a file write rather than in standard
output; and that a value is never restated in text the agent authors, including what a leg hands back
to the orchestrator. The orchestrator's section SHALL carry these in the same terms as a leg's rather
than by reference to the legs, because the orchestrator is the agent that fuses the findings and
writes the product.

#### Scenario: Sections present

- **WHEN** any of the five analyst prompts is read
- **THEN** it carries credential-harvest, exhaustive-processing, Aleph-corpora and tool-discipline sections

#### Scenario: Leg surfaces a remainder instead of fanning out

- **WHEN** a slice is larger than a leg can finish
- **THEN** its prompt requires it to report the remainder to the orchestrator

#### Scenario: Every prompt states the credential routing rule

- **WHEN** each of the five prompts' credential-harvest section is read, the orchestrator's included
- **THEN** it requires ownership to be classified first, confines writing to target-owned material,
  requires a credential-reading command to terminate in a file write rather than standard output, and
  forbids restating a value in agent-authored text including a hand-back to the orchestrator

#### Scenario: The orchestrator states the rule rather than delegating it

- **WHEN** `cyber-analyst`'s credential-harvest section is searched for the routing rule
- **THEN** the rule is stated in the section itself and not left to the legs' prompts
