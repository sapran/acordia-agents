## Why

The `opwe` profile permits four concurrent task agents, but the shipped `cyber-analyst` credential-sweep flow deliberately dispatches only Collection and Terrain together, then blocks Mission and subsequent work on a fusion barrier. The result is an effective two-leg ceiling imposed by prompt choreography rather than by the harness.

The library supports specialised operating units, lead coordination, and economy of scarce attention, but it does not prescribe a numerical parallel-dispatch breadth. This change therefore treats broader fan-out as an engineering decision: dispatch every independent, bounded read without waiting; retain a barrier only when its input is genuinely required by the next read.

## What Changes

- Update the competency-source prose to distinguish genuine dependency barriers from the former paired orientation sequence.
- Update the `cyber-analyst` prompt so it creates one bounded, disjoint assignment per independent specialist question and dispatches all such assignments together, including multiple instances of the same specialist when a corpus must be partitioned.
- Preserve lead ownership of prioritisation and fusion: a dependent mission valuation or credential brief waits only for the returns it consumes.
- Modify the agent-roster specification to require dependency-driven fan-out and make the prompt contract testable by review.
- Regenerate the two lead wrappers from the canonical orchestrator body and bump the plugin minor version across its three declarations.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `agent-roster`: Define dependency-driven orchestration fan-out and preserve lead fusion responsibility.
- `competency-map-derivation`: Record the revised operating-model prose from which the lead prompt derives.
- `skill-library`: Give parallel instances of one leg a distinct, lead-supplied output-file identity while retaining the single-instance filename fallback.

## Impact

- `docs/roles/operational-analyst.md`
- `acordia-analysts/agents/cyber-analyst.md`
- Lead command wrappers that carry the canonical orchestrator body
- `openspec/specs/agent-roster/spec.md` and `openspec/specs/skill-library/spec.md`, plus their delta specs
- The three plugin version declarations
