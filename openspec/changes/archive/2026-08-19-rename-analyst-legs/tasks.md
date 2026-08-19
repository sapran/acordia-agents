# Tasks

## 1. Rename the files
- [x] 1.1 `git mv` the two agent files to `target-analyst.md` and `overwatch-analyst.md`
- [x] 1.2 `git mv` the two canonical wrapper files to match
- [x] 1.3 Confirm filename stem equals frontmatter `name` for all nine agents

## 2. Rewrite every live reference
- [x] 2.1 Rewrite both identifiers across all 17 live files carrying them
- [x] 2.2 Point the `/target` and `/defender` short aliases at the new agent names
- [x] 2.3 Confirm zero residual live occurrences of either old name
- [x] 2.4 Confirm `openspec/changes/archive/**` is unchanged

## 3. Record provenance
- [x] 3.1 Append the leg-rename note to `docs/roles/operational-analyst.md`, after the grid
- [x] 3.2 Confirm the 39 skill anchors still land on grid rows L67-L108

## 4. Update the specs
- [x] 4.1 Modify the roster requirement to enumerate the new analyst filenames
- [x] 4.2 Add the requirement that a leg agent is named for the question it answers
- [x] 4.3 `openspec validate --all --strict`
