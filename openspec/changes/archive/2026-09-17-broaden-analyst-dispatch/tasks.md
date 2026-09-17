## 1. Source and prompt

- [x] 1.1 Update `docs/roles/operational-analyst.md` so the operating model directs dependency-driven fan-out and same-leg disjoint slices; verify the lead prompt derives the same rule.
- [x] 1.2 Update `acordia-analysts/agents/cyber-analyst.md` to dispatch independent specialist assignments together and retain only real dependency barriers; verify its prompt text has no fixed two-leg sequence.
- [x] 1.3 Regenerate the canonical lead body in both lead command wrappers; verify each wrapper body is byte-identical to `cyber-analyst.md`.

## 2. Distribution and verification

- [x] 2.1 Bump the three synchronized plugin version declarations to `6.18.0`, the next available minor version; verify the catalogs remain byte-identical and all three values agree.
- [x] 2.2 Run `~/ai/checks/check-acordia.sh` against the worktree; verify its version, catalog, prompt, provenance, and ceiling checks pass.
- [x] 2.3 Run `openspec validate --all --strict`; verify the new delta specs validate.
- [x] 2.4 Review the complete worktree diff against the proposal and resolve any in-scope correctness issue before archive.
