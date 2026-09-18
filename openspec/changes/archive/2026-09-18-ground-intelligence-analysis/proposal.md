## Why

The analyst pillar names a shared analytic spine but does not yet distinguish clearly between a target model shared across analysts and operators, an explicit collection gap, a machine-generated hypothesis, and a supported human judgement. The library already contains Heuer, SAT and Lindsay; selected lib.ai passages add Clark's target-centric model and Cvetko and Davydiuk's human-centred CTI framing, which let the distribution state those boundaries without attributing grid-derived techniques to literature.

## What Changes

- Add `Clark` and `Cvetko-Davydiuk` once each to the literature register with their live lib.ai document identifiers.
- Ground the competency-grid prose in a target model shared with collectors and the human operator; make collection gaps explicit; and distinguish automation output from an analyst conclusion.
- Update only the affected analytic-spine skills:
  - `human-automation-teaming` gains the doctrinal human/automation boundary and declares the selected source.
  - `naming-the-gaps` gains target-model and explicit-gap framing, but keeps its collection-tasking procedure anchored only to its grid row.
  - `outcome-judgement` makes access-held-for-later an explicit possible end and declares the existing Lindsay performance/outcome boundary.
- Preserve the rule that Heuer and Pherson/Heuer are method background, not blanket `doctrine_source` labels for grid-derived procedures.
- Update the published specifications, regenerate the tracked ACORDIA map, and make a MINOR version bump in all three required distribution JSON locations.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `doctrinal-provenance`: record the distinction between doctrine sourced from the register and grid-derived analytic technique detail, including the selected target-model and human–automation sources.
- `skill-library`: define the selected analytic-spine boundaries as observable content of the affected skills.
- `competency-map-derivation`: state the shared-spine doctrinal framing that the grid and derived map must carry.

## Impact

- `docs/roles/sources.md`
- `docs/roles/operational-analyst.md`
- `acordia-analysts/skills/{human-automation-teaming,naming-the-gaps,outcome-judgement}/SKILL.md`
- `openspec/specs/{doctrinal-provenance,skill-library,competency-map-derivation}/spec.md` and this change's delta specifications
- `acordia-map.html`
- `acordia-analysts/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, and `.omp-plugin/marketplace.json`
