## MODIFIED Requirements

### Requirement: Dispatch descriptions are the routing signal

Each specialist's `description` SHALL state its domain in one sentence, conveying the same routing signal as its CyberStrike counterpart's description, because `description` is the only routing signal a subagent has. Each agent's `description` SHALL additionally open with the pillar provenance tag `ACORDIA Operations — `, ahead of the domain sentence and without altering it, because these names (`operator`, `web-application`, `mobile-application`, `cloud-security`, `internal-network`) are generic enough to be mistaken for a harness built-in, and a write-capable agent is the one whose origin the user most needs to see.

#### Scenario: Description conveys the domain

- **WHEN** `internal-network` is inspected
- **THEN** its `description` conveys internal-network and Active Directory work — AD attacks, Kerberos, lateral movement

#### Scenario: Description carries the pillar tag

- **WHEN** any agent under `operators/agents/` is inspected
- **THEN** its `description` begins with `ACORDIA Operations — `
- **AND** the domain sentence following the tag is unchanged in meaning

#### Scenario: Provenance is carried by the description, not the name

- **WHEN** the agent files, the primary's `task` whitelist, and the skill slugs are inspected
- **THEN** no agent filename, agent name, or skill slug carries a distribution prefix
