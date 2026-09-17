## 1. Source of truth and doctrine

- [x] 1.1 Add the Mission-only `target-sustainment-analysis` row and bounded sustainment doctrine to `docs/roles/operational-analyst.md`; verify its stable id is unique and the grid lists 42 rows.
- [x] 1.2 Repair the live document identifiers for `ACORDIA` and `Orye-Maennel` in `docs/roles/sources.md`; verify both ids resolve through lib.ai and preserve Orye offprint p. 5 / proceedings p. 117 citation context.
- [x] 1.3 Update `openspec/config.yaml` and live repository prose that state the skill count from 45 to 46; verify archived OpenSpec records are untouched.

## 2. Skill and Mission binding

- [x] 2.1 Create `acordia-analysts/skills/target-sustainment-analysis/SKILL.md` with a distinct selection description, grid anchor, selected doctrine keys, method, boundary, and outputs; verify its frontmatter and slug satisfy the skill contract.
- [x] 2.2 Bind the new skill to the Mission Analyst deep line and `skill-sets.json`; verify the prompt and declaration match and no other analyst gains the skill.
- [x] 2.3 Update the Mission Analyst prompt only where needed to state the sustainment read and its analytical hand-back; verify it neither recommends action nor claims digital-supply-chain scope.

## 3. Distribution and map

- [x] 3.1 Bump the three version literals from 6.16.0 to 6.17.0 and update live 45-skill descriptions to 46; verify both marketplace catalogs are byte-identical and all three versions agree.
- [x] 3.2 Rebuild `acordia-map.html` from the completed tree, including the new skill record, Mission relationship, 46-skill totals, and version badge; verify the prior-tree model reproduces before replacement.
- [x] 3.3 Cold-load the regenerated map and sweep routes; verify the landing page renders, every route resolves, no page errors occur, and no stale count/version remains.

## 4. Specification and release checks

- [x] 4.1 Re-run `openspec validate --all --strict`; verify every active and published spec validates after the final artifacts are present.
- [x] 4.2 Run `~/ai/checks/check-acordia.sh` against the worktree and the grid/prompt/declaration checks from `CLAUDE.md`; verify version lockstep, catalog identity, provenance, grid derivation, and declared skill-set checks pass.
- [x] 4.3 Review the final diff for scope compliance and map/source-register correctness; verify only the approved Mission sustainment capability landed and digital supply-chain analysis remains absent.
