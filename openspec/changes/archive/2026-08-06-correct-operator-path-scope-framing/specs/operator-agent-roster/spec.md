## MODIFIED Requirements

### Requirement: Operators are write-capable

Operators execute; they write scripts, evidence, journal entries, and reports. Every operator agent SHALL set `edit: allow`, making this the first write-capable pillar in the repository and the deliberate opposite of the analyst posture (`edit: deny`).

The pillar SHALL NOT rely on path-scoped writes, because **a path-scoped `edit` rule is unenforceable in every harness**. Every operator agent carries `bash: allow`, an open write channel at any path, so a scoped rule would be defeated by a shell redirection in opencode exactly as in omp and Claude Code (see `analyst-agent-roster`, where the analyst pillar's report sink is fixed as a convention on the same grounds). omp additionally cannot express a path scope at all, but that is a secondary limitation, not the reason.

The reason SHALL NOT be stated as a harness asymmetry — "enforced in opencode and silently absent in omp" — because no harness enforces such a rule, and that phrasing has propagated into documentation and into later changes reasoning by analogy. Where an operator is expected to write, the prompt body SHALL name the destination (`.acordia/ops/…`) as discipline rather than as a permission.

An unscoped `edit: allow` is therefore the honest posture rather than a concession: it claims exactly the capability the agent has.

#### Scenario: File modification allowed

- **WHEN** an operator agent writes or edits a file
- **THEN** the resolved `edit` permission is `allow` and the write proceeds

#### Scenario: No path-scoped write rules

- **WHEN** any operator agent's `edit` block is inspected
- **THEN** it is the scalar `allow`, with no path-keyed sub-rules

#### Scenario: The reason given is universal, not per-harness

- **WHEN** the justification for the unscoped `edit: allow` is read in any live spec or document
- **THEN** it attributes the unenforceability of a path scope to `bash: allow` in every harness
- **AND** it does not claim that such a rule would be enforced in opencode
