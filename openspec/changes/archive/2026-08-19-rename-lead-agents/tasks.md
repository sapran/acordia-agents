## 1. Rename the two lead agents

- [x] 1.1 `git mv acordia-analysts/agents/operational-analyst.md acordia-analysts/agents/cyber-analyst.md`
- [x] 1.2 `git mv acordia-operators/agents/operator.md acordia-operators/agents/cyber-operator.md`
- [x] 1.3 Set frontmatter `name` to match each new stem; keep frontmatter to exactly `name`, `description`, `color`
- [x] 1.4 Update the prose title in each prompt body and description (`the senior cyber analyst`, `**cyber-operator**`)
- [x] 1.5 Confirm both prompt bodies stay under the 10,000-character ceiling

## 2. Rename the wrappers and keep the old handles

- [x] 2.1 `git mv` both canonical wrappers to `cyber-analyst.md` / `cyber-operator.md`
- [x] 2.2 Add `acordia-operators/commands/operator.md` as the short alias for `/cyber-operator`
- [x] 2.3 Repoint `acordia-analysts/commands/analyst.md` at `cyber-analyst`
- [x] 2.4 Update asserted counts: 18 wrappers, nine aliases, ten operations wrappers

## 3. Disambiguate the pillar sense

- [x] 3.1 Normalise `operator <pillar|library|skill|prompt|agent|wrapper|artifact|file|specialist>` to `operations …` across the live tree, including the line-wrapped case
- [x] 3.2 Leave the human/session sense untouched: the `operators you advise` guardrail, operator journal, operator session, operator-deployed, and the `wstg-auth-session` default-credential row
- [x] 3.3 Fix `agent-to-operator-agent` → `agent-to-operations-agent` in CLAUDE.md
- [x] 3.4 Repair the stale `operators/` directory reference in the workbook (renamed in 3.0.0)

## 4. Preserve provenance and history

- [x] 4.1 Leave `openspec/changes/archive/**` untouched
- [x] 4.2 Keep both `docs/roles/` filenames; retitle the provenance table column to `ACORDIA agent`
- [x] 4.3 Record the upstream-name → agent-name mapping in each `docs/roles/` document
- [x] 4.4 Append the analyst note at end of file so the L67–L108 grid anchors do not shift; re-verify all 39 resolve to a grid row

## 5. Version and verify

- [x] 5.1 Bump 3.2.0 → 4.0.0 in all four version files (two catalogs, two manifests) and confirm they agree
- [x] 5.2 Confirm the two catalogs stay byte-identical
- [x] 5.3 Re-verify the roster: nine agents, three-key frontmatter, stem equals `name`
- [x] 5.4 Re-verify orchestration: `cyber-analyst` names its three legs, `cyber-operator` its four specialists, `mobile-application` → `web-application` hand-off intact
- [x] 5.5 Confirm zero dangling references to the old agent or wrapper paths
- [x] 5.6 Regenerate the browsable HTML map from the renamed tree
- [x] 5.7 `openspec validate --all --strict`
