## 1. Literature gate

- [x] 1.1 Search the lib.ai library before authoring any shipping prose: `library_route` with
  `granularity="document"` on "verification of a written intelligence product before it is handed to
  a decision-maker" and on "citation practice and source identifiers in written intelligence
  reporting".
- [x] 1.2 Record the outcome verbatim in `proposal.md` under `## Literature`, including the empty
  finding and what was searched. Confirm nothing returned contradicts the shipped wording.

## 2. `briefing-reporting`

- [x] 2.1 Append a `## Method` bullet requiring a real parser for a second format, naming the inline
  constructs a regex pass drops without erroring, requiring the parser used to be named, and
  requiring raw-HTML passthrough off with markup inside quoted evidence escaped.
- [x] 2.2 Append a `## Method` bullet requiring identifiers to be cited in full, separating what is
  displayed from what is recorded, and bounding it by class — a credential, token or key is never
  cited, a personal identifier only as far as the judgement requires.
- [x] 2.3 Append a `## Signals / outputs` bullet requiring a rendered product to be verified twice —
  no surviving source-format tokens, and a resolved sample of its references against the system
  already read from, by the same read call — naming a link count as proving neither, and forbidding
  resolution of a reference originating inside the cited material or addressing a target-owned or
  third-party system.
- [x] 2.4 Leave frontmatter untouched: no `doctrine_source`, `metadata.acordia` unchanged.

## 3. `aleph-entity-graph`

- [x] 3.1 Insert a `### Constructing the call` subsection after the closing line of `## Tooling —
  state which one you have` and before `## Method`.
- [x] 3.2 State `entity_id` on `get_entity`, `get_entity_text`, `expand_entity`, `entity_tags` and
  `similar_entities`, `profile_id` for a profile, `id` and `entity` as wrong, and the wrong-key
  behaviour as measured: a closed input schema refuses the call before it reaches Aleph with two
  named validation errors, the whole error text must be read, and a genuine 404 means a wrong
  identifier instead.
- [x] 3.3 State that the argument object is serialised in code, naming quoted-phrase escaping as the
  failure, cross-referencing `analytic-tooling-scripting`, and stating that the `curl` path meets the
  rule by the client's parameter encoding rather than by shell interpolation of corpus-derived values.
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
- [x] 5.8 Reproduce the wrong-key behaviour rather than asserting it: against the pinned `aleph-mcp`
  virtualenv, `get_cached_typeadapter(f).validate_python({"id": "x"})` yields `additionalProperties:
  false` in the schema and two errors — `entity_id: Missing required argument` and `id: Unexpected
  keyword argument`. Confirm in the measured run that the eight refusals over four entities name the
  key, that the loop's `Expecting value: line 1 column 1` hid it, and that the run's `not found
  (404)` replies came from calls carrying a truncated `entity_id` instead.
- [x] 5.9 Prove the ADDED approach dropped nothing: the first 625 lines of
  `openspec/specs/skill-library/spec.md` are byte-identical to `develop`, scenarios go 77 → 83 and
  requirements 14 → 16.

## 6. Land

- [x] 6.1 `openspec archive report-and-aleph-argument-discipline --yes`, re-validate.
- [x] 6.2 Review with `reviewer` and `security-reviewer`; fix or dismiss each finding.
- [x] 6.2a Correct the review findings in the same PR: the invented "dropped rather than refused"
  mechanism (skill body, both spec copies, proposal, design, tasks), the unbounded
  "identifiers in full" rule, the unconstrained reference resolution, the parser's raw-HTML
  passthrough, and the `curl` path's shell interpolation.
- [x] 6.3 Merge to `develop`.
- [x] 6.4 Prove the edits reach the opwe profile, whose skills are symlinks into the main checkout.
- [x] 6.5 Remove the worktree and delete the local and remote branch.
