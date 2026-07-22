## 1. Author the `exhaustive-data-processing` skill

- [x] 1.1 Create `analysts/skills/exhaustive-data-processing/SKILL.md` with opencode frontmatter (`name: exhaustive-data-processing`, `description` phrased for trigger quality — fires on bulk material such as a dump, archive, log bundle, or dataset a single read cannot fully capture)
- [x] 1.2 Add a `## Cross-cutting notice` declaring the skill procedural and non-grid, inheriting the procedural-skill exception from `analyst-skill-library`, and naming `analytic-tooling-scripting` and the three legs as what it composes
- [x] 1.3 Add a `## The sampling trap` section naming the three failure modes (bounded read window; partial inspection of tool hits; fan-out that only distributes sampling if each leaf reads a head)
- [x] 1.4 Add a `## Method — script-first exhaustion` section: tool pass over 100% of bytes/records (`rg`/`grep`/`awk`/`jq`/parser) → aggregates + located hits; read only located regions into context, never the head; fan-out (orchestrator only) reserved for judgement a script cannot make
- [x] 1.5 Add a `## Coverage ledger` section: declared input scope (denominator), per-step accounting (scanned / parsed / deferred-with-reason), per-leaf coverage receipt `{scope declared, scope covered, method, deferred + why}`, orchestrator reconciliation with rejection of non-reconciling receipts, and a final total-coverage statement or named deferred remainder
- [x] 1.6 Add a `## Fan-out contract` section: only the orchestrator fans out (legs are `task: deny`); disjoint bounded slices; a leg surfaces overflow back rather than sampling
- [x] 1.7 Add `## Guardrails` inheriting passive posture and no-raw-credential-values
- [x] 1.8 Verify frontmatter validates against the opencode contract (`name` matches `^[a-z0-9]+(-[a-z0-9]+)*$`, ≤64 chars, equals folder slug; `description` 1–1024 chars) and carries no `sha256`/`signature` and no CyberStrike-only fields

## 2. Orchestrator prompt forcing-function

- [x] 2.1 In `analysts/agents/operational-analyst.md`, add a `## Exhaustive data processing` H2 stating exhaustion is a precondition (script-first before judgement) and that the orchestrator owns coverage reconciliation — rejects any leg return whose receipt does not reconcile to its dispatched slice, and re-dispatches or sub-partitions
- [x] 2.2 Name `exhaustive-data-processing` in the section
- [x] 2.3 Verify the `edit`, `bash`, and `task` permission blocks and the three-leg whitelist are unchanged

## 3. Leg prompt forcing-functions

- [x] 3.1 Add a `## Exhaustive data processing` H2 to `analysts/agents/target-network-analyst.md`: never sample the slice; script-exhaust it; emit a coverage receipt alongside `## What to return`; surface overflow back (cannot fan out)
- [x] 3.2 Same section in `analysts/agents/defender-detection-analyst.md`
- [x] 3.3 Same section in `analysts/agents/fusion-analyst.md`
- [x] 3.4 Name `exhaustive-data-processing` in each leg's section
- [x] 3.5 Verify each leg's `edit`/`bash`/`task` blocks and `description` frontmatter are unchanged

## 4. Credential-harvest cross-reference

- [x] 4.1 In `analysts/skills/credential-harvest-triage/SKILL.md`, point the first-pass scan and deep-pass at `exhaustive-data-processing`: the pattern scan covers 100% of each bucket's text-decodable bytes, every hit is classified, and each bucket returns a coverage receipt
- [x] 4.2 Verify the edit is additive — classification schema, bucket partition, procedure steps, pattern-library pointer, and guardrails are unchanged

## 5. Harmonise the seven "sample" skills

Reword only the read-discipline bullet, replacing the "sample" read-verb framing with "bounded-context reads driven by an exhaustive tool pass; process every located hit, not just the first". Substance (grep-first, scoped read) is preserved.

- [x] 5.1 `analysts/skills/protocol-routing-architecture/SKILL.md` (also fix "Map layers from that sample" → "from those reads")
- [x] 5.2 `analysts/skills/own-footprint-analysis/SKILL.md`
- [x] 5.3 `analysts/skills/evasion-antianalysis/SKILL.md`
- [x] 5.4 `analysts/skills/pattern-of-life-baselining/SKILL.md`
- [x] 5.5 `analysts/skills/vuln-attacksurface-mapping/SKILL.md`
- [x] 5.6 `analysts/skills/log-artefact-interpretation/SKILL.md` ("Read by bounded sampling" → bounded-context + exhaustive coverage)
- [x] 5.7 `analysts/skills/endpoint-telemetry-edr/SKILL.md` ("sample event archives" → filter-scoped reads over the full channel, every matching event processed)
- [x] 5.8 Confirm no read-verb "sample" remains in any of the fifteen evidence-reading skills' `## Method` sections; confirm the "specimen" / "test fixture" / "provider-sampled logs" uses in `implant-payload-re`, `analytic-tooling-scripting`, `cloud-identity-log-analysis`, `human-automation-teaming` are untouched

## 6. Source-of-truth and posture checks

- [x] 6.1 `git diff docs/roles/operational-analyst.md` shows no change (no grid edit)
- [x] 6.2 `install.sh` and `uninstall.sh` unchanged (skill picked up by the `skills/*` glob)
- [x] 6.3 No agent `edit`/`bash`/`task` permission block changed in this change

## 7. Validate

- [x] 7.1 `openspec validate --all --strict` passes
- [x] 7.2 `test -f analysts/skills/exhaustive-data-processing/SKILL.md`
- [x] 7.3 `grep -q '^description:' analysts/skills/exhaustive-data-processing/SKILL.md` and `grep -q 'procedural' analysts/skills/exhaustive-data-processing/SKILL.md` succeed
- [x] 7.4 `grep -lc 'Exhaustive data processing' analysts/agents/*.md` reports all four agents
- [x] 7.5 `grep -c 'exhaustive-data-processing' analysts/agents/operational-analyst.md analysts/agents/target-network-analyst.md analysts/agents/defender-detection-analyst.md analysts/agents/fusion-analyst.md` reports ≥1 per file
- [~] 7.6 `opencode debug skill exhaustive-data-processing` — deferred: opencode binary is present but the skill is not deployed to `~/.config/opencode/skills/` in this worktree, so `debug skill` cannot resolve it; frontmatter verified structurally via `openspec validate --strict` and the grep checks above instead
- [x] 7.7 Skill count invariant: `ls analysts/skills | wc -l` reports one more than before this change
