## ADDED Requirements

### Requirement: Selected intelligence-analysis doctrine is bounded by claim type

The source register SHALL include `Clark` for Robert M. Clark's *Intelligence Analysis: A Target-Centric Approach* (`508633d1`) and `Cvetko-Davydiuk` for Martin Cvetko and Andrii Davydiuk's *Human-Centric Approaches in Cyber Threat Intelligence: Integrating Analytical Insight with Automation* (`8e547dcd`).

`Clark` MAY ground claims that an analyst maintains a target model, makes knowledge gaps explicit, and hands an intelligible model to collectors and the human operator. `Cvetko-Davydiuk` MAY ground claims that an automated output is a hypothesis rather than a confirmed conclusion, and that confidence and provenance bound the distinction. `Lindsay#intelligence-performance` MAY ground the distinction between operational intelligence performance and strategic outcome.

`Heuer` and `SAT` remain analytic-method background. Their methods SHALL NOT be added as blanket `doctrine_source` attribution to grid-derived procedures merely because they inspired the procedure.

#### Scenario: Claim-specific provenance is inspectable
- **WHEN** the selected analytic-spine skills and their grid prose are inspected
- **THEN** each doctrinal claim is attributable to the register key that supports its framing, while the procedure remains anchored to its grid row

#### Scenario: Method inspiration does not masquerade as doctrine
- **WHEN** a grid-derived method such as competing-hypothesis testing or gap tasking is inspected
- **THEN** it retains its `row` and `source` anchor without a blanket `Heuer` or `SAT` attribution
