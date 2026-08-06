## 1. The spec

- [x] 1.1 Modify the "Method contract for evidence-reading skills" requirement so the criterion is normative, the enumeration is a record of present membership at twenty-two skills, and a scenario forbids the enumeration from narrowing the criterion.

## 2. The seven skill bodies

- [x] 2.1 `ot-embedded` — inventory step over firmware images, HMI projects, ladder logic, and historian exports; bounded-and-exhaustive reading; citation shape for binary and project artefacts; degradation for each optional tool named.
- [x] 2.2 `overwatch` — inventory step over console exports, alert queues, and ticket dumps; bounded-and-exhaustive reading; a console-appropriate citation shape (query plus timestamp) since there is no file offset; degradation when a console is unreachable.
- [x] 2.3 `effect-on-target-verification` — inventory step over the observables gathered; bounded-and-exhaustive reading; citation shape tying each observable to its source; degradation when a second source is unavailable.
- [x] 2.4 `assessing-take-value` — inventory step over the delivered take; exhaustive coverage before judging completeness, since a truncation verdict from a head read is the exact failure; citation shape; degradation for missing verification tools.
- [x] 2.5 `analytic-tooling-scripting` — inventory step naming the enumeration tool; coverage discipline requiring the script to process 100% of records rather than being written against the first ones; provenance/citation for derived outputs; degradation when a parser cannot handle the format.
- [x] 2.6 `data-integration-tooling` — inventory step over input datasets; coverage and record-count reconciliation across the join; provenance shape carrying each row back to its source artefact; degradation for unavailable inputs.
- [x] 2.7 `change-cycle-forecasting` — inventory step over version and release evidence; bounded-and-exhaustive reading; citation shape for the evidence behind a predicted date; degradation when release data is unavailable.

## 3. Version and regeneration

- [x] 3.1 Bump `VERSION` to `2.4.0` — MINOR, seven skill bodies reach users.
- [x] 3.2 Rebuild both plugin trees.

## 4. Verification

- [x] 4.1 Confirm each of the seven now contains an inventory tool reference, coverage language, a citation shape, and a degradation clause.
- [x] 4.2 Confirm the seventeen spine skills were not modified.
- [x] 4.3 Confirm all 73 skills still parse and the frontmatter gate passes.
- [x] 4.4 Confirm `--check` is clean, including the version gate, and that the build is deterministic.
