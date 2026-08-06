## 1. Settle the replacement wording

- [x] 1.1 Draft the single canonical sentence for the report-sink convention, to be reused in meaning across prompts, generator notes, and docs. It must name the sink, state that the confinement is prompt discipline, and attribute the non-enforcement to `bash: allow` rather than to any harness.
- [x] 1.2 Draft the in-message variant for the two non-reporting legs.

## 2. Agent prompts (`analysts/agents/`)

- [x] 2.1 Replace the `## Guardrails` closing sentence in `operational-analyst.md` (line 57) with the canonical wording naming `.acordia/reports/`.
- [x] 2.2 Replace the same in `fusion-analyst.md` (line 50).
- [x] 2.3 Replace the `## Guardrails` closing sentence in `target-network-analyst.md` (line 48) with the in-message variant.
- [x] 2.4 Replace the same in `defender-detection-analyst.md` (line 48).
- [x] 2.5 Reword the `edit` block's inline comment on `operational-analyst.md` (line 7) and `fusion-analyst.md` (line 7) from `write reports here only` to convention-marking wording, preserving the trailing grid-competency annotation.
- [x] 2.6 Diff the four guardrail sections against each other and confirm one shared form, and that no harness is named as the reason.

## 3. Generator (`tools/build-plugins.py`)

- [x] 3.1 Rewrite the path-scoped branch of `write_note` (lines 327–331) to state the sink as a convention no harness enforces, keeping the disclosure that the agent can write anywhere.
- [x] 3.2 Confirm the blanket read-only branch (lines 333–337) is left byte-identical — the spec requires it unchanged.
- [x] 3.3 Rewrite the Claude path-scope comment note (lines 409–411) on the same terms, removing the "Claude Code cannot express a path scope … prompt-level **here**" contrast.
- [x] 3.4 Update the explanatory code comment at lines 392–395, which states the same rationale for the reviewer.
- [x] 3.5 Bump `VERSION` (line 55) `2.1.0` → `2.2.0`. If `harden-plugin-distribution` has already applied and moved it, take the next MINOR above the current value instead.

## 4. Documentation

- [x] 4.1 Collapse `README.md` lines 164–167 so the sink is stated once as a universal convention; keep the omp `xd://` transport-`write` disclosure and the `bash`-is-a-write-channel line, and drop the "opencode confines" contrast.
- [x] 4.2 Rename the "**Scoped-write exception**" label in `CLAUDE.md` line 86 to a report-sink convention and align its body sentence.
- [x] 4.3 Correct `openspec/config.yaml` lines 37–49, whose project context carries the same "enforced to different depths per harness" framing and is injected into every future artifact.
- [x] 4.4 Check `README.md` line 199 ("Verifying an install") still reads correctly — it describes the scoped exception as an expectation to confirm, which remains true.

## 5. Regenerate and verify

- [x] 5.1 Run `tools/build-plugins.py` to regenerate the plugin trees and both marketplace catalogs.
- [x] 5.2 Run `tools/build-plugins.py --check` and confirm it exits clean with no drift.
- [x] 5.3 Read the two generated omp reporting analysts and confirm `metadata.generated.write_access` carries the new wording; read the two generated omp read-only legs and confirm their note is unchanged.
- [x] 5.4 Read the two generated Claude reporting analysts and confirm the path-scope comment carries the new wording, `disallowedTools` still names `Edit`, `NotebookEdit`, `Task`, and `Write` is still absent.
- [x] 5.5 Confirm the version reached all files carrying it, in both catalogs and both plugin manifests per pillar.
- [x] 5.6 Grep the whole repository for the retired phrases — "cannot express a path scope", "opencode confines", "Scoped-write exception", "prompt-level here" — and confirm only intentional occurrences remain.
- [x] 5.7 Confirm no permission map, skill body, command wrapper, or operators-pillar file changed.

## 6. Close out

- [x] 6.1 Run `openspec validate --change reframe-report-sink-convention` and resolve any finding.
- [x] 6.2 Sync the three delta specs into `openspec/specs/` and archive the change.
