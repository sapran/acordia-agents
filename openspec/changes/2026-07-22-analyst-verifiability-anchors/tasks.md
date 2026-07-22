## 1. Method contract for evidence-reading skills

- [ ] 1.1 Restructure `## Method` in `analysts/skills/disk-memory-forensics/SKILL.md` to declare, in order: (a) inventory step naming tool, (b) bounded sampling discipline, (c) citation format `<path>:<offset>` or `<path>@L<line>`, (d) degradation policy per optional external tool
- [ ] 1.2 Repeat 1.1 for `log-artefact-interpretation`
- [ ] 1.3 Repeat 1.1 for `cloud-controlplane-analysis`
- [ ] 1.4 Repeat 1.1 for `web-api-authflow-analysis`
- [ ] 1.5 Repeat 1.1 for `os-host-internals`
- [ ] 1.6 Repeat 1.1 for `implant-payload-re`
- [ ] 1.7 Repeat 1.1 for `identity-directory-trust`
- [ ] 1.8 Repeat 1.1 for `packet-traffic-analysis`
- [ ] 1.9 Repeat 1.1 for `endpoint-telemetry-edr`
- [ ] 1.10 Repeat 1.1 for `c2-beacon-exfil-analysis`
- [ ] 1.11 Repeat 1.1 for `protocol-routing-architecture`
- [ ] 1.12 Repeat 1.1 for `own-footprint-analysis`
- [ ] 1.13 Repeat 1.1 for `evasion-antianalysis`
- [ ] 1.14 Repeat 1.1 for `pattern-of-life-baselining`
- [ ] 1.15 Repeat 1.1 for `vuln-attacksurface-mapping`
- [ ] 1.16 Cross-check: no analytic-spine skill has been touched (`reasoning-under-uncertainty`, `key-assumptions-check`, `calibrated-confidence`, `hypothesis-testing`, `assessing-take-value`, `outcome-judgement`, `gain-loss-calculus`, `naming-the-gaps`, `deception-detection`, `change-cycle-forecasting`, `maintaining-operating-picture`, `human-automation-teaming`, `nontechnical-context-integration`, `method-timing-risk-decision`, `overwatch`, `target-mission-analysis`, `briefing-reporting`, `analytic-tooling-scripting`, `data-integration-tooling`, `effect-on-target-verification`, `detection-capability-analysis`, `multi-source-fusion`)

## 2. Leg return contract

- [ ] 2.1 Add `## What to return` H2 to `analysts/agents/target-network-analyst.md` — hypothesis + calibrated confidence + named gaps + recommended next collection/method + credential findings routed to `credential-harvest-triage` bins (P0–P3) with source paths. Advisory tone, not schema.
- [ ] 2.2 Repeat 2.1 for `analysts/agents/defender-detection-analyst.md`
- [ ] 2.3 Repeat 2.1 for `analysts/agents/fusion-analyst.md`
- [ ] 2.4 Add `## Output discipline` H2 to `analysts/agents/operational-analyst.md` — how the primary aggregates the three legs' returns (attribution of hypothesis to leg, gaps unioned, next-collection prioritised across legs, credential findings de-duplicated across legs)
- [ ] 2.5 Verify no agent's `description` frontmatter has changed (must remain the italic operating question)
- [ ] 2.6 Verify no permission block (`edit`, `bash`, `task`) has changed

## 3. Frontmatter anchor

- [ ] 3.1 Add `metadata.acordia` block to every `analysts/skills/*/SKILL.md` — for grid-row skills: `{ grid_row, grid_deep_in, grid_working_in, source: "docs/roles/operational-analyst.md#L<n>" }`; for `credential-harvest-triage`: `{ grid_row: null, procedural: true, source: "openspec/changes/archive/2026-07-22-credential-harvest-capability/proposal.md" }`
- [ ] 3.2 Add `metadata.acordia` block to every `analysts/agents/*.md` — `{ leg, column, source_paragraph: "docs/roles/operational-analyst.md#L<start>-<end>" }`
- [ ] 3.3 Cross-check: every skill's `grid_row` matches a row in `docs/roles/operational-analyst.md` (except procedural skills)
- [ ] 3.4 Cross-check: every skill's `grid_deep_in` and `grid_working_in` unions cover the columns the skill is marked in on the grid, and no others
- [ ] 3.5 Cross-check: every agent's `column` corresponds to its grid column (Core / T&N / Def / Fus)

## 4. Validate

- [ ] 4.1 `openspec validate --all --strict` passes
- [ ] 4.2 `grep -l "## What to return" analysts/agents/{target-network,defender-detection,fusion}-analyst.md` returns 3 matches
- [ ] 4.3 `grep -l "## Output discipline" analysts/agents/operational-analyst.md` returns 1 match
- [ ] 4.4 `grep -c "metadata:" analysts/skills/*/SKILL.md analysts/agents/*.md` reports one hit per file (0 unchanged files)
- [ ] 4.5 Each of the 15 evidence-reading skills' `## Method` begins with an inventory step (spot-check three chosen at random)
