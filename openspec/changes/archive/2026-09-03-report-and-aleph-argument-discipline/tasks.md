## 1. Literature gate

- [x] 1.1 Search the lib.ai library before authoring any shipping prose: `library_route` with
  `granularity="document"` on "verification of a written intelligence product before it is handed to
  a decision-maker" and on "citation practice and source identifiers in written intelligence
  reporting".
- [x] 1.2 Record the outcome verbatim in `proposal.md` under `## Literature`, including the empty
  finding and what was searched. Confirm nothing returned contradicts the shipped wording.

## 2. `briefing-reporting`

- [x] 2.1 Append a `## Method` bullet requiring a real parser for a second format, naming the inline
  constructs a regex pass drops without erroring, and requiring the parser used to be named.
- [x] 2.2 Append a `## Method` bullet requiring identifiers to be cited in full, separating what is
  displayed from what is recorded.
- [x] 2.3 Append a `## Signals / outputs` bullet requiring a rendered product to be verified twice —
  no surviving source-format tokens, and a resolved sample of its references — and naming a link
  count as proving neither.
- [x] 2.4 Leave frontmatter untouched: no `doctrine_source`, `metadata.acordia` unchanged.

## 3. `aleph-entity-graph`

- [x] 3.1 Insert a `### Constructing the call` subsection after the closing line of `## Tooling —
  state which one you have` and before `## Method`.
- [x] 3.2 State `entity_id` on `get_entity`, `get_entity_text`, `expand_entity`, `entity_tags` and
  `similar_entities`, `profile_id` for a profile, `id` and `entity` as wrong, and the dropped-key
  failure in both of its outcomes.
- [x] 3.3 State that the argument object is serialised in code, naming quoted-phrase escaping as the
  failure and cross-referencing `analytic-tooling-scripting`.
- [x] 3.4 Change nothing else — in particular not the `collection` scope contract in `## Method`,
  which 6.6.0 settled.

## 4. Version and generated artifact

- [x] 4.1 Bump `6.6.0` → `6.7.0` in all three manifests:
  `acordia-analysts/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`,
  `.omp-plugin/marketplace.json`.
- [x] 4.2 Re-derive `acordia-map.html`, which embeds skill bodies as rendered HTML, validating the
  transform by reproducing every unchanged record byte-for-byte before writing, and hand-patch the
  version badge.

## 5. Verify

- [x] 5.1 Confirm every argument name against the pinned server source:
  `git -C ~/git/aleph-mcp show 9bd04af0:src/aleph_mcp/server.py` shows `entity_id` on the five entity
  tools and `profile_id` on `get_profile`.
- [x] 5.2 Reproduce the acceptance baseline the reporting discipline exists to prevent: the shipped
  `report.html` yields tail lengths `{6: 5, 7: 2, 8: 29, 40: 5}`, i.e. 35 of 40 references
  unresolvable. Do not regenerate the artefact.
- [x] 5.3 `~/ai/checks/check-acordia.sh` passes on the worktree.
- [x] 5.4 `openspec validate --all --strict` passes.
- [x] 5.5 Both catalogs byte-identical, all four JSON files parse.
- [x] 5.6 Grid-marks and skill-sets checks report `problems: 0` with `rows checked` equal to the
  grid's row count — confirming, not assuming, that no grid fact moved.
- [x] 5.7 Load the regenerated map cold, assert the landing route paints, sweep every route for
  `Not found`, and assert zero page errors.

## 6. Land

- [x] 6.1 `openspec archive report-and-aleph-argument-discipline --yes`, re-validate.
- [x] 6.2 Review with `reviewer` and `security-reviewer`; fix or dismiss each finding.
- [x] 6.3 Merge to `develop`.
- [x] 6.4 Prove the edits reach the opwe profile, whose skills are symlinks into the main checkout.
- [x] 6.5 Remove the worktree and delete the local and remote branch.
