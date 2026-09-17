## ADDED Requirements

### Requirement: Mission sustainment analysis derives from one Mission grid row

The competency grid SHALL carry one `target-sustainment-analysis` row under *The target as an organisation*, with one stable row id and a `●` mark in Mission only. That row SHALL derive exactly one grid-row skill and place its slug on `mission-analyst`'s deep skill line; it SHALL place the slug in no other analyst prompt unless a future grid mark changes.

The competency models target-side organisational sustainment: suppliers and contractors, inventory and spares, transport and distribution, maintenance and repair, trained personnel, and external services needed to continue a mission. Digital supply-chain analysis — software components, CI/CD, package registries, cloud-service dependency graphs, and equivalent ecosystem dependencies — SHALL NOT be represented by this row.

#### Scenario: The Mission row derives the complete binding
- **WHEN** the `target-sustainment-analysis` row is traced from the grid
- **THEN** exactly one matching skill carries its stable row id and Mission deep mark, and `mission-analyst` alone names it on a deep skill line

#### Scenario: Target sustainment stays distinct from digital supply chains
- **WHEN** the row and its derived skill are read
- **THEN** they cover organisational sustainment dependencies and explicitly exclude digital supply-chain analysis
