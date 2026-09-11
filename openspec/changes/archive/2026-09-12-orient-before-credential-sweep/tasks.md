## 1. Foundation

- [x] 1.1 Add the proposal, design, and two capability delta specs for `orient-before-credential-sweep`, grounded in the selected library passages and the current role model.
- [x] 1.2 Update `docs/roles/operational-analyst.md` so the source-of-truth role model states that carried-memory refresh and technical terrain orientation precede directed credential collection, with mission value shaping the resulting priority plan.

## 2. Lead and orientation workflow

- [x] 2.1 Update `acordia-analysts/skills/analyst-loop/SKILL.md` with the collection-planning preflight while preserving the six-step end-neutral loop, passive posture, gap naming, confidence and human next-move rules.
- [x] 2.2 Update `acordia-analysts/agents/cyber-analyst.md` so Collection and Terrain orientation precede credential scoping, the lead reads and fuses their notes, and the credential brief carries the orientation packet fields.
- [x] 2.3 Update `acordia-analysts/agents/collection-analyst.md` and `acordia-analysts/skills/operational-memory/SKILL.md` with the prior-run and Aleph-corpus orientation preflight, including stale/conflicting/no-memory states.
- [x] 2.4 Update `acordia-analysts/agents/terrain-analyst.md` with passive technical asset discovery and the non-secret asset-register return contract before extraction.
- [x] 2.5 Update `acordia-analysts/agents/mission-analyst.md` with asset-to-mission/crown-jewel valuation before credential priorities are fixed.

## 3. Credential triage

- [x] 3.1 Update `acordia-analysts/skills/credential-harvest-triage/SKILL.md` with the Aleph orientation-packet precondition, raw-archive compatibility branch, incomplete-packet stop path, asset associations, asset-aware priority guidance, and targeted-then-residual procedure.
- [x] 3.2 Add the non-secret asset fingerprint section to `acordia-analysts/skills/credential-harvest-triage/references/credential-patterns.md` for MinIO/S3, databases, file shares, Kubernetes/container systems, CI/CD, VPN/remote access, identity systems and SSH.

## 4. Specification and release surfaces

- [x] 4.1 Add agent-roster delta requirements and scenarios for the lead gate and Collection/Terrain/Mission orientation returns.
- [x] 4.2 Modify the published `credential-harvest-triage` and `analyst-loop` requirements in the skill-library delta, reproducing every surviving published scenario by title and adding the new orientation scenarios.
- [x] 4.3 Bump all three analyst plugin version literals from `6.9.0` to `6.10.0` and keep both marketplace catalogs byte-identical.

## 5. Verification and delivery

- [x] 5.1 Run the focused structural ordering check, JSON parse check, catalog diff, `openspec validate --all --strict`, and `~/ai/checks/check-acordia.sh` against the worktree.
- [x] 5.2 Run the available top-level omp smoke check with synthetic non-secret MinIO and VPN/SSH observations; verify orientation precedes credential planning and no live validation occurs.
- [x] 5.3 Review the complete diff with a correctness reviewer and a security reviewer, fix or explicitly dismiss findings, archive the OpenSpec change, rerun strict validation and the drift gate, and commit the logical change on `feat/orient-before-credential-sweep`.
