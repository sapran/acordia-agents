## 1. Settle the replacement reason

- [x] 1.1 Draft the canonical clause, reused in meaning across all four sites: a path-scoped `edit` rule is unenforceable in every harness because `bash: allow` is an open write channel at any path; omp's inability to express a path scope is an additional limitation, not the reason.

## 2. Specs

- [x] 2.1 Replace the second paragraph of the "Operators are write-capable" requirement in `openspec/specs/operator-agent-roster/spec.md` (line 72) with the canonical reason, preserving the requirement's normative force and its closing sentence about naming `.acordia/ops/…` in the prompt body.
- [x] 2.2 Add the "The reason given is universal, not per-harness" scenario to that requirement.
- [x] 2.3 Replace the causal clause in the "The `.acordia/ops/` operation journal" requirement in `openspec/specs/harness-tool-translation/spec.md` (line 34), keeping the sentence's conclusion and the five-row table untouched.
- [x] 2.4 Add the "Non-enforcement is stated as universal" scenario to that requirement.
- [x] 2.5 Confirm both requirements still forbid path-scoped rules at least as strongly as before, and that no scenario was dropped.

## 3. Documentation

- [x] 3.1 Correct `CLAUDE.md` line 103 — replace "a scoped rule would hold in opencode and silently evaporate in omp" with the canonical reason, keeping the bullet's lead ("Write-capable by default — the deliberate opposite of the analyst posture") and the `edit: allow` statement.
- [x] 3.2 Correct `docs/agents-skills-extension-workbook.md` lines 646–648 on the same terms, preserving the surrounding sentences about the shared `.acordia/reports/` convention and `scope_check`'s substitution logic.
- [x] 3.3 Cross-read the corrected `CLAUDE.md` bullet against the analyst-posture bullet at line 86 and confirm the two pillars now give one consistent account of the mechanism.

## 4. Verify

- [x] 4.1 Grep the repository for `enforced in opencode`, `hold in opencode`, `would be enforced`, `silently evaporate`, and `silently absent`, and confirm the only remaining hits are under `openspec/changes/archive/`.
- [x] 4.2 Run `tools/build-plugins.py --check` and confirm it exits clean **without** a rebuild, proving no generated output depended on these files.
- [x] 4.3 Confirm `VERSION` is unchanged and no file under `plugins/`, `.omp-plugin/`, or `.claude-plugin/` is modified.
- [x] 4.4 Confirm no agent prompt, permission map, skill body, or command wrapper changed.
- [x] 4.5 Run `openspec validate correct-operator-path-scope-framing --strict` and resolve any finding.

## 5. Close out

- [x] 5.1 Sync the two delta specs into `openspec/specs/` and archive the change.
