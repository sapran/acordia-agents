## Why

The repository describes the analysts' report sink as a permission boundary that one harness enforces and two cannot. That contrast is false in the direction that matters: **no harness enforces it, including opencode.**

Every analyst carries `bash: allow` (`analysts/agents/*.md` line 7–9), and `analyst-agent-roster` already concedes at spec line 65 that `bash: "*": allow` permits file creation via scripting. A path-scoped `edit` plus an unrestricted shell is not a confinement in opencode any more than in omp or Claude Code — it is a naming convention wearing a permission's clothes.

The documentation nevertheless reads as a three-way capability split. `README.md` line 165 opens "opencode confines `operational-analyst` and `fusion-analyst` writes to `.acordia/reports/**`" and then attributes the gap to the other two harnesses; `plugin-packaging` line 112 and `omp-harness-distribution` lines 135–146 repeat the same framing. Line 166 of the same README states the contradiction plainly — "`bash` is still a write channel … all three harnesses" — one line below the claim it invalidates.

The threat model is also empty. There is no adversary, and the failure mode is an analyst writing a report to the wrong directory: a tidiness defect in the user's own repository, not a security event. Nothing here justifies enforcement machinery; it justifies describing the convention accurately.

**Current behaviour:** three normative specs, the generator's own notes, and both top-level documents frame the report sink as an enforcement gap peculiar to the plugin harnesses, while an adjacent sentence admits the gap is universal. The four analyst guardrails describe it in three different wordings, and the two read-only legs never say where their in-message products go.

**Desired behaviour:** the report sink is stated once, as a convention that holds in every harness by prompt discipline. opencode's `edit` scope is described as the mechanism that *expresses* the convention, not one that enforces it. No agent, spec, or generated note claims a guarantee the repository cannot keep.

## What Changes

No permission changes. No behavioural change to any agent. The scoped `edit` block stays exactly as it is — it remains the clearest available *expression* of the convention, and removing it would lose information. What changes is every sentence that promises enforcement.

### Agent prompts

The four analyst `## Guardrails` sections converge on one wording. Today `defender-detection-analyst` line 48 and `target-network-analyst` line 48 say "write access is prompt-level only", while `operational-analyst` line 57 and `fusion-analyst` line 50 say "confine writes to `.acordia/reports/`" — and neither read-only leg states where its product goes. All four SHALL name the sink, state that the confinement is prompt discipline in every harness, and state each agent's product destination (the sink for the two reporting analysts, in-message for the two legs).

The `edit` block's inline comment on the two reporting agents changes from `write reports here only` to wording that marks it a convention rather than a gate.

### The plugin generator

`tools/build-plugins.py` lines 327–337 and 409–411 emit per-harness notes phrased as harness deficiencies ("omp cannot express a path-scoped permission", "Claude Code cannot express a path scope, so the confinement is prompt-level here"). Both SHALL state instead that the sink is a prompt-level convention not enforced by any harness, and that `bash` is an open write channel. The mechanical facts already recorded — that omp exposes `write` as an `xd://` transport tool, that Claude Code retains `Write` — are accurate and SHALL be kept.

`VERSION` moves `2.1.0` → `2.2.0`. MINOR: agent prompt bodies reach users.

### Documentation

`README.md` lines 164–167 collapse the opencode-versus-others contrast into a single statement of the convention and its universal non-enforcement. `CLAUDE.md` line 86 renames "**Scoped-write exception**" to a report-sink convention — "exception" implies a rule with teeth.

### Deliberately not changed

- **No enforcement hook.** A `PreToolUse` hook is the only mechanism that would genuinely enforce the sink, and both plugin harnesses support one. Rejected: it is executable code in a markdown distribution, its `bash`-redirection matching is bypassable by `python -c`, `tee`, or a heredoc, and it would block the scratch files `analytic-tooling-scripting` and `exhaustive-data-processing` depend on. High cost, partial coverage, no adversary.
- **`bash` stays `allow`** on all four analysts. Denying it would make the scope real at the price of two load-bearing skills.
- **The sink paths are unchanged.** `.acordia/reports/` (analysts) and `.acordia/ops/reports/` (operators) differ by a whole `ops/` segment and are already namespaced by pillar. An earlier draft of this change proposed renaming the analyst sink to remove a "near-collision"; that premise was wrong and the rename is dropped.
- **No CI, no lint automation.** Consistent with `harden-plugin-distribution`.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `analyst-agent-roster` — the scoped-`edit` requirement is reframed as a report-sink convention, and gains a scenario fixing that a scripted write outside the sink is refused by no harness. The permission block it mandates is unchanged.
- `plugin-packaging` — the rationale for the path-scoped `disallowedTools` row (spec line 112) and the recorded Claude comment (line 147) stop attributing the gap to Claude Code alone. The derivation table and every emitted tool name are unchanged.
- `omp-harness-distribution` — the "Scoped report sink is reported as unenforceable" requirement (lines 134–146) states non-enforcement as universal rather than omp-specific. The emitted allowlist is unchanged.

`harness-tool-translation` is **not** modified: line 34 already describes the journal as "discipline, not enforced as a permission scope", which is the wording this change adopts everywhere else.

## Impact

- **Modified — agent prompts:** `analysts/agents/operational-analyst.md`, `fusion-analyst.md`, `target-network-analyst.md`, `defender-detection-analyst.md` (guardrail prose; `edit` comment on the first two).
- **Modified — generator:** `tools/build-plugins.py` (`VERSION`, the two note strings).
- **Modified — docs:** `README.md`, `CLAUDE.md`, and `openspec/config.yaml`, whose project context repeats the same "enforced to different depths per harness" framing at lines 47–49.
- **Regenerated:** the `plugins/{claude,omp}/acordia-analysts/` agent files and both marketplace catalogs, via `tools/build-plugins.py`. Gated by `--check`.
- **Unchanged:** every permission map, every skill body, every command wrapper, the operators pillar, and both sink paths.
- **Verification:** `tools/build-plugins.py --check` clean after regeneration; the four generated analyst agents inspected to confirm the notes carry the new wording and no tool name moved.
