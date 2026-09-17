## ADDED Requirements

### Requirement: Selected doctrine register identifiers resolve

Each `doctrine_source` reference carried by `target-sustainment-analysis` SHALL resolve through `docs/roles/sources.md` to a live lib.ai document record. The register SHALL preserve the repository's paired Orye–Maennel pagination convention: offprint p. 5 corresponds to *Silent Battle* proceedings p. 117.

#### Scenario: Selected doctrine can be re-read from the register
- **WHEN** `target-sustainment-analysis` cites selected doctrine through `doctrine_source`
- **THEN** every cited register entry resolves to a live library record

#### Scenario: Orye–Maennel pagination remains intelligible
- **WHEN** an Orye–Maennel citation is read from the register
- **THEN** its context distinguishes offprint p. 5 from proceedings p. 117
