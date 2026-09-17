## ADDED Requirements

### Requirement: Mission Analyst owns target sustainment analysis

`mission-analyst` SHALL own the organisational sustainment read: whether the target can continue its mission through suppliers and contractors, stock and spares, transport and distribution, maintenance and repair, trained personnel, and external services. The prompt SHALL name `target-sustainment-analysis` as deep skill and state that it hands back an evidenced sustainment judgement, not a recommended action.

The read SHALL remain bounded by the Mission Analyst’s organisational remit. It SHALL not claim Terrain’s technical dependency analysis, create a sixth analyst, or encompass digital supply-chain analysis.

#### Scenario: The Mission prompt names the sustainment competency
- **WHEN** the Mission Analyst deep-skill line and `skill-sets.json` declaration are compared
- **THEN** each contains `target-sustainment-analysis`, and no other analyst’s deep or working declaration gains it

#### Scenario: The hand-back remains analytical
- **WHEN** the Mission Analyst returns a sustainment read
- **THEN** it states the sustainment judgement, confidence, evidence gaps, and notes location without ranking interventions or directing action
