## Context

See `proposal.md` for motivation. The Mission Analyst already owns the target as an organisation, mission threads, non-technical context, change cycles, friction susceptibility, and organisational outcome judgement. The grid has no explicit competency that joins those inputs into a sustained-mission model.

## Goals / Non-Goals

**Goals:**

- Make target-side organisational sustainment a discoverable Mission Analyst deep competency.
- Produce one coherent judgment across dependency mapping, continuity/recovery assessment, and evidence planning for higher-order mission effects.
- Reuse the existing five Mission skills as distinct inputs rather than duplicating their methods.
- Support military and civilian organisations with mission-neutral language and observed-versus-inferred evidence handling.

**Non-Goals:**

- No new analyst, command wrapper, skill family, permission surface, or action-selection method.
- No ranking of intervention points or recommendation to act.
- No digital supply-chain analysis: software components, CI/CD, package registries, cloud-service dependency graphs, and equivalent ecosystem analysis remain a future capability.

## Decisions

### One grid-row skill composes the supporting skills

Add `target-sustainment-analysis` under the grid’s target-organisation section with a Mission-only deep mark. It is one competency because its products are one continuous Mission judgment: a dependency map has no practical value without continuity/recovery assessment, and neither proves mission consequence without an effect-assessment plan.

The skill calls on existing skills without restating their methods:

- `target-mission-analysis` for the mission process and crown jewels;
- `nontechnical-context-integration` for suppliers, contractors, finance, and procurement context;
- `change-cycle-forecasting` for replenishment, maintenance, replacement, and timing;
- `target-friction-susceptibility` for redundancy, trained alternatives, process rigidity, and absorption;
- `outcome-judgement` for independent evidence of mission consequence.

Adding separate rows for each would create competing, overlapping methods and would obscure the existing skills’ ownership.

### The analysis object is target sustainment

The skill models target-side suppliers and contractors, inventory and spares, transport and distribution, maintenance and repair, trained personnel, and external services. Each dependency is recorded with its mission role, evidence, uncertainty, alternatives, cadence or capacity constraint, and recovery implication.

The method starts from a Mission Process Thread, then maps technical and non-technical supports. It never treats a system asset list as a sustainment model.

### The output is an assessed model, not targeting advice

The full working produces: a sustainment model; a critical-dependency register; a resilience assessment; and an effect-assessment plan naming first-, second-, and third-order observables. The bounded hand-back gives the judgement, confidence, gaps, and notes-file location. It does not identify or rank candidate actions.

### Doctrine is registered by key, with source repairs

The skill’s `doctrine_source` records `ACORDIA`, `MTA`, `Sand`, `Rovner`, `CCH2`, and `Orye-Maennel` with the selected sections. `docs/roles/sources.md` corrects the ACORDIA live document id from the unresolved `17fec536` to `1152d85c`, the paper under the registered CyCon proceedings record `649a6776`, and corrects Orye–Maennel to live id `f28986d1`. Orye–Maennel prose follows the existing citation convention: offprint p. 5 / proceedings p. 117.

### The logistics role is a recorded repository synthesis

The library search covered ACORDIA, Monte, MTA, Sand, Rovner, CCH2, Orye–Maennel, and direct logistics and sustainment queries. It found no work that establishes a logistics or sustainment analyst as a distinct ACORDIA role, nor a ready-made logistics-analysis method. The new grid row is therefore the repository’s bounded synthesis of selected dependency, resilience, and effect-assessment doctrine; it is not attributed to a pre-existing specialist seat.

### Grid-derived artifacts move together

The grid row is the source of truth. Its Mission `●` mark derives the new skill’s anchors, the Mission prompt deep-skill line, and `skill-sets.json` deep declaration. The map is regenerated only after these authored artifacts are complete.

## Risks / Trade-offs

- A broad sustainment model can become an unbounded inventory. The method therefore begins with a named mission process and reports evidence gaps rather than inventing links.
- Military doctrine can overfit civilian targets. The method uses mission, service continuity, and organisational function; military terms remain examples, not defaults.
- The Orye register mismatch must be repaired in the same change. Without it, a `doctrine_source` reference would claim a record the library cannot resolve.
- The additional skill changes the library count to 46. Every live count and version surface, including the map and OpenSpec project context, moves together.