## 1. Baseline

- [x] 1.1 Record the starting measurement so the change can be shown to have moved it: 45 skills,
      16,061 description characters, mean 357, max 438, min 298.
- [x] 1.2 Confirm no description is already compliant, so the rewrite covers all 45 and no file is
      skipped as "already short enough".

## 2. Rewrite the descriptions, family by family

Rewrite within a family in one pass, so siblings are compared against each other while they are
being written rather than afterwards. Each rewrite keeps the opening imperative naming the work only
that skill does, keeps the trigger, drops the enumeration, and lands at or under 200 characters.

- [x] 2.1 `analytic-spine` (13) — `analyst-loop`, `analytic-tooling-scripting`, `briefing-reporting`,
      `calibrated-confidence`, `deception-detection`, `gain-loss-calculus`,
      `human-automation-teaming`, `hypothesis-testing`, `key-assumptions-check`,
      `method-timing-risk-decision`, `naming-the-gaps`, `outcome-judgement`,
      `reasoning-under-uncertainty`. This family is carried by every analyst, so its descriptions are
      in every catalogue and its compression buys the most.
- [x] 2.2 `target-modelling` (11) — `change-cycle-forecasting`, `cloud-controlplane-analysis`,
      `identity-directory-trust`, `os-host-internals`, `ot-embedded`, `pattern-of-life-baselining`,
      `protocol-routing-architecture`, `target-friction-susceptibility`, `target-mission-analysis`,
      `vuln-attacksurface-mapping`, `web-api-authflow-analysis`.
- [x] 2.3 `take-handling` (10) — `aleph-entity-graph`, `assessing-take-value`,
      `credential-harvest-triage`, `data-integration-tooling`, `exhaustive-data-processing`,
      `maintaining-operating-picture`, `multi-source-fusion`, `nontechnical-context-integration`,
      `operational-memory`, `take-domain-interpretation`. Contains the collision the spec names by
      hand: `multi-source-fusion` versus `maintaining-operating-picture`.
- [x] 2.4 `defender-reading` (7) — `c2-beacon-exfil-analysis`, `cloud-identity-log-analysis`,
      `detection-capability-analysis`, `endpoint-telemetry-edr`, `evasion-antianalysis`, `overwatch`,
      `own-footprint-analysis`. Holds the current maximum, `cloud-identity-log-analysis` at 438.
- [x] 2.5 `evidence-forensics` (4) — `disk-memory-forensics`, `implant-payload-re`,
      `log-artefact-interpretation`, `packet-traffic-analysis`.

## 3. Verify the ceiling

- [x] 3.1 Measure every description after YAML folding; assert none exceeds 200 and the mean is at
      most 180.
- [x] 3.2 Assert none opens with `Use when`, `Apply when`, `Use to`, `Use this skill` or a variant —
      the pre-existing prohibition, re-checked because every description was rewritten.
- [x] 3.3 Recompute the per-analyst catalogue cost from the union of each prompt's `·`-separated
      lines, at `97 + len(name) + len(description) + len(location)` with the verified 40-character
      host prefix; assert every analyst is under 12,000.
- [x] 3.4 Read the `multi-source-fusion` and `maintaining-operating-picture` pair by hand and confirm
      the rewrite did not collapse them back into a shared "target picture" phrasing.
- [x] 3.5 Confirm no `SKILL.md` changed outside its `description` field — the diff touches one line
      region per file and no body, no `metadata.acordia`, no `name`.

## 4. Release mechanics

- [x] 4.1 Bump the version MINOR in lockstep across all three occurrences:
      `acordia-analysts/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`,
      `.omp-plugin/marketplace.json`.
- [x] 4.2 `diff .claude-plugin/marketplace.json .omp-plugin/marketplace.json` — silence, the two
      catalogs stay byte-identical.
- [x] 4.3 Confirm all three JSON files parse.
- [x] 4.4 Run the prompt-slug resolution one-liner from `CLAUDE.md` — unchanged by this work, but it
      is the check that catches a slug that resolves to nothing and the rewrite touched every skill.
- [x] 4.5 `openspec validate --all --strict`.
- [x] 4.6 Run the external gate `~/ai/checks/check-acordia.sh` on the worktree before opening the PR.

## 5. Record what was not fixed

- [x] 5.1 Park both deferred findings in `docs/implementation-notes.md`: the grid/prompt drift on the
      12-skill shared spine, and the three skills named in no agent prompt
      (`aleph-entity-graph`, `credential-harvest-triage`, `exhaustive-data-processing`). One line
      each — what, where, why parked.
- [x] 5.2 Keep `docs/handoff-skill-catalogue-prompt-budget.md` in the tree as the record this change
      answers, and note in it which of its four acceptance criteria this change meets (2 and 3) and
      which remain open (1 and 4).
