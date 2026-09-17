## ADDED Requirements

### Requirement: `target-sustainment-analysis` composes one Mission sustainment judgement

The library SHALL contain `acordia-analysts/skills/target-sustainment-analysis/SKILL.md`, a normal grid-row skill in the `target-modelling` family. It SHALL model whether a target organisation can continue its mission through suppliers and contractors, inventory and spares, transport and distribution, maintenance and repair, trained personnel, and external services.

Its method SHALL produce a sustainment model, critical-dependency register, resilience assessment, and effect-assessment plan. It SHALL compose rather than duplicate `target-mission-analysis`, `nontechnical-context-integration`, `change-cycle-forecasting`, `target-friction-susceptibility`, and `outcome-judgement`; it SHALL not rank intervention points or recommend action. It SHALL distinguish observed relationships from inferred ones and name material gaps.

#### Scenario: The sustainment skill has a distinct selection surface
- **WHEN** `target-sustainment-analysis` is compared with other `target-modelling` skills
- **THEN** its description discriminates organisational sustainment and continuity analysis from mission-thread mapping and friction susceptibility

#### Scenario: The skill produces an assessed sustainment model
- **WHEN** the skill is applied to a target mission
- **THEN** its working identifies dependencies, alternatives, recovery constraints, confidence, and an evidence plan for mission-level effects rather than an asset list or an action recommendation

#### Scenario: Digital supply-chain analysis remains out of scope
- **WHEN** the skill is read for supported dependency types
- **THEN** it excludes software components, CI/CD, package registries, cloud-service dependency graphs, and equivalent digital supply-chain analysis
