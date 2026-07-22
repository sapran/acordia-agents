## 1. Source of truth — spec

- [x] 1.1 Apply the delta to `openspec/specs/analyst-agent-roster/spec.md` via `openspec archive` (main-spec sync applies the MODIFIED requirement: default-deny; path-scoped `edit` for the two reporting agents; blanket `edit: deny` for the two legs).
- [x] 1.2 `openspec validate --all --strict` passes.

## 2. Contract docs

- [x] 2.1 `docs/agents-skills-extension-workbook.md` §6: document that opencode's `edit` permission accepts path-scoped globs (last-match-wins, like `bash`), and the reporting-write convention `{ "*": deny, ".acordia/reports/**": allow }` for agents holding the "Briefing & written reporting" grid competency.
- [x] 2.2 `CLAUDE.md`: update the "Read-only posture is mandatory. Every analyst carries `edit: deny`" guidance to state the two-agent scoped exception (`operational-analyst`, `fusion-analyst` → scoped `.acordia/reports/**`; the two legs stay blanket `edit: deny`).

## 3. Agent frontmatter

- [x] 3.1 `analysts/agents/operational-analyst.md`: change `edit: deny` to the path-scoped block; do not touch the `bash` or `task` blocks.
- [x] 3.2 `analysts/agents/fusion-analyst.md`: change `edit: deny` to the path-scoped block; do not touch the `bash` block.
- [x] 3.3 Confirm `analysts/agents/target-network-analyst.md` and `analysts/agents/defender-detection-analyst.md` remain blanket `edit: deny` (no change).

## 4. Report destination reference

- [x] 4.1 In the `briefing-reporting` skill (named by both reporting agents), name `.acordia/reports/` as the report landing zone so the sanctioned path is discoverable at run time. Additive — existing sections and permission blocks untouched.

## 5. Verify

- [x] 5.1 Frontmatter of both reporting agents parses; resolved `edit` = `{ "*": deny, ".acordia/reports/**": allow }` (opencode `debug agent` reads installed config, not the worktree, so parse is the local gate).
- [x] 5.2 `target-network-analyst` and `defender-detection-analyst` frontmatter still resolves `edit: deny`.
- [x] 5.3 Re-run `openspec validate --all --strict`.
