# agent-roster

## ADDED Requirements

### Requirement: Every operations prompt names the remote-execution posture

Each of the five operations prompts SHALL name `bolts` in its working-knowledge line, so the discipline
that decides where traffic originates reaches every agent rather than sitting in a library none of them
references.

`bolts` SHALL NOT enter any agent's specialist-depth line. It is a cross-cutting execution posture, not
a domain depth, and the depth lines drive omp's `autoloadSkills`.

#### Scenario: The posture reaches all five prompts
- **WHEN** the working-knowledge line of each operations prompt is read
- **THEN** every one names `bolts`

#### Scenario: The posture is not a specialist depth
- **WHEN** the specialist-depth lines of the operations prompts are read
- **THEN** none names `bolts`
