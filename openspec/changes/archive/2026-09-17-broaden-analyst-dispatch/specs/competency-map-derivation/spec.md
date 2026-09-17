## MODIFIED Requirements

### Requirement: Structural mappings from grid to artifact

The derivation SHALL bind the grid's structure to artifacts as follows: the leg's italic operating
question → subagent `description`; the leg's prose paragraph → agent prompt body; the operating-model
prose under `## How the pieces fit` → the orchestrator's routing and fusion instructions; the grid's
section header → a documentation grouping of the skills, carried as the skill's `metadata.acordia`
family tag rather than as a harness field, because neither harness has a skill `category`.

The operating-model prose SHALL distinguish a real information dependency from a roster-based pairing:
it directs the orchestrator to fan out independent bounded specialist questions, including disjoint
slices owned by one leg, while keeping lead fusion and every dependency-driven join barrier.

#### Scenario: Italic question becomes the dispatch signal

- **WHEN** a leg's italic operating question is read
- **THEN** it is used (in meaning) as that subagent's `description`

#### Scenario: Operating model directs lead routing

- **WHEN** the `## How the pieces fit` prose is read
- **THEN** the orchestrator prompt derives its fan-out, dependency-barrier and lead-fusion instructions from it

#### Scenario: Section header becomes a documented grouping

- **WHEN** a grid section header is read
- **THEN** the skills beneath it are grouped under one family in documentation and in skill metadata, not under a harness-level category
