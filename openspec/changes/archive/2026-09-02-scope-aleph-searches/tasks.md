## 1. Method

- [x] 1.1 Add a new first step to `## Method` in
  `acordia-analysts/skills/aleph-entity-graph/SKILL.md`: `collection` is required on
  `search_entities` and `match_entity`, takes a numeric id, a `foreign_id` or a list of either,
  `collection="*"` is the only instance-wide scope and is annotated in `_note`, `collection_id` does
  not go in `filters`, and `searched.collection` is read back rather than assumed.
- [x] 1.2 State the consequence in the same step: an unscoped search is answered successfully, so a
  query that meant one collection and did not say so returns another collection's rows, ranked and
  plausible, with no error.
- [x] 1.3 Renumber the following six steps 2–7.

## 2. Narrowing and fallback

- [x] 2.1 In the narrowing step, name collection as not among the `filters` keys and point back at
  the `collection` argument.
- [x] 2.2 Add `filter:collection_id` to the `curl` example URL in `## Tooling`, and state that on
  that path an omitted filter searches every readable collection with no `_note`, no `searched` block
  and nothing else to signal it.

## 3. Take assessment

- [x] 3.1 Extend the "Provenance is per collection, not per instance" bullet with the check: verify a
  hit's own `collection_id` against the collection scoped to, because that mismatch is the failure's
  only symptom.

## 4. Version and generated artifact

- [x] 4.1 Bump `6.5.0` → `6.6.0` in all three manifests:
  `acordia-analysts/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`,
  `.omp-plugin/marketplace.json`.
- [x] 4.2 Re-derive `acordia-map.html`, which embeds skill bodies as rendered HTML. Validate the
  transform by reproducing every pre-change record byte-for-byte before writing, and hand-patch the
  version badge.

## 5. Verify

- [x] 5.1 `~/ai/checks/check-acordia.sh` passes on the worktree.
- [x] 5.2 `openspec validate --all --strict` passes.
- [x] 5.3 Confirm frontmatter untouched, so `metadata.acordia` and `skill-sets.json` stay valid and no
  `·`-separated prompt line moves.
- [x] 5.4 Load the regenerated map cold with an empty hash, assert `#main` painted, sweep every route
  for `Not found`, and assert zero page errors.

## 6. Land

- [x] 6.1 `openspec archive scope-aleph-searches --yes`, re-validate.
- [ ] 6.2 Review with `reviewer` and `security-reviewer`; fix or dismiss each finding.
- [ ] 6.3 Merge to `develop`, then fast-forward `main` so installs reach it.
- [ ] 6.4 Remove the worktree and delete the branch.
