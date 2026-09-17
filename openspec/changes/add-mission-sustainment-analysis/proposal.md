## Why

The Mission Analyst can already model mission threads, context, change cycles, friction, and outcomes, but has no explicit method for assessing whether a target can sustain its mission through suppliers, stock and spares, transport, maintenance, trained people, contractors, and external services. This leaves a load-bearing organisational dependency read implicit and difficult to dispatch, review, or retain.

## What Changes

- Add `target-sustainment-analysis`, a Mission-owned skill that maps and assesses a target organisation’s sustainment system for military and civilian missions.
- Add its competency-grid row and bind it to the Mission Analyst’s deep-skill set and declared skill set.
- Define the skill’s bounded products: sustainment model, critical-dependency register, resilience assessment, and effect-assessment plan. It composes existing Mission skills; it neither ranks intervention points nor advises action.
- Ground the capability in the selected ACORDIA, MTA, Sand, Rovner, CCH2, and Orye–Maennel doctrine; repair the Orye–Maennel library id in the source register and retain the repository’s established offprint/proceedings pagination convention.
- Explicitly exclude digital supply-chain analysis, including software components, CI/CD, package registries, and cloud-service dependency graphs, for a separate future capability.
- Update the tracked map and every live skill-count and version surface for the new 46-skill library and required MINOR release.

## Capabilities

### New Capabilities

None.

### Modified Capabilities
- `agent-roster`: The Mission Analyst owns and names the new deep capability while retaining the five-agent roster and existing hand-off boundary.
- `skill-library`: The library gains one normal grid-row skill in the existing `target-modelling` family.
- `competency-map-derivation`: The grid gains one stable Mission-only row that derives the skill and its prompt/declaration bindings.
- `doctrinal-provenance`: The new skill uses registered doctrine keys, and the Orye–Maennel library id is corrected to the live record.
- `plugin-distribution`: The user-visible prompt and skill change requires a MINOR version bump across the three lockstep JSON literals.

## Impact

- Authored artifacts: `docs/roles/operational-analyst.md`, `docs/roles/sources.md`, one new skill directory, `acordia-analysts/agents/mission-analyst.md`, and `acordia-analysts/skill-sets.json`.
- Derived presentation: `acordia-map.html`, regenerated from the completed integrated tree and its static count/version surfaces updated.
- Planning/specification: OpenSpec deltas for the listed capabilities and an in-place `openspec/config.yaml` count correction if it states the former library count.
- Distribution: `acordia-analysts/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, and `.omp-plugin/marketplace.json`; the two catalogs remain byte-identical.
- No new agent, command wrapper, skill family, permission surface, or digital-supply-chain capability.