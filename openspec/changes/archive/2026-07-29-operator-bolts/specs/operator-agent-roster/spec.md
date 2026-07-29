## ADDED Requirements

### Requirement: Every operator prompt names the remote-execution posture

Each operator agent prompt — `operator`, `web-application`, `mobile-application`, `cloud-security`, `internal-network` — SHALL name `bolts` in its `## Working knowledge (draw on as needed)` line. This ensures the remote-execution discipline reaches all five agents rather than sitting in a skill library nobody references.

`bolts` SHALL NOT appear on any agent's `## Your specialist depth (deep)` line, because it is a cross-cutting execution posture rather than a domain depth, and placing it in `deep` would add it to `autoloadSkills` and pay the full-body prompt cost in sessions with no remote host.

#### Scenario: All five agents reference bolts in working knowledge

- **WHEN** any operator agent's `## Working knowledge (draw on as needed)` line is read
- **THEN** `bolts` appears in the `·`-separated list

#### Scenario: No agent references bolts in deep knowledge

- **WHEN** any operator agent's `## Your specialist depth (deep)` line is read
- **THEN** `bolts` does NOT appear in the `·`-separated list
