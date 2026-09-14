## 1. Foundation

- [x] 1.1 Add the proposal, design and `skill-library` delta spec for `search-artefacts-not-mentions`, with every quoted figure obtained from a read-only faceted query against the live instance rather than restated from the originating note.
- [x] 1.2 Record the literature search in `docs/roles/sources.md` under `## Gaps — searched and not found`: `Heuer` p. 81 and `Monte` pp. 26–27 ground volume-is-not-quality and directed targeting, neither grounds query construction, so the addition carries no `doctrine_source`.

## 2. Aleph method

- [x] 2.1 Add a `### Searching for artefacts rather than mentions` subsection to `acordia-analysts/skills/aleph-entity-graph/SKILL.md` stating: schema is the file-class discriminator and its facet carries true counts; empty `mime_type`/`extension` facets are an instance indexing property and not evidence; a format word or extension in `q` measures mentions, with the measured figures; `file_name` is a filter value rather than a wildcard-searchable field.
- [x] 2.2 In the same subsection, state the structural-marker route for a format no facet can isolate, the rule that a marker discriminates by its rarest token because the index discards punctuation, the instruction to price a candidate marker at `limit=0` and read its `schema` facet before building on it, and the link from the existing 66% rule to why added vocabulary widens in any language.
- [x] 2.3 Require the coverage statement to separate classes enumerated by schema from formats reached only by marker, and to name any marker that hit the cap as sampled.

## 3. Patterns and triage

- [x] 3.1 Add a non-secret `## Config-file structural markers` section to `acordia-analysts/skills/credential-harvest-triage/references/credential-patterns.md` covering WireGuard/AmneziaWG, OpenVPN, PuTTY, IPsec/IKE and Windows RDP, each string established from upstream format documentation or the live corpus.
- [x] 3.2 State in that section that the same pattern behaves differently over raw bytes than as an Aleph `q` term, name the subset whose tokens survive, and add the carrier-pivot rule for a passphrase that lives in a different document from the config, including the measured over-match of the obvious password-vocabulary forms.
- [x] 3.3 Extend step 3 of `acordia-analysts/skills/credential-harvest-triage/SKILL.md` so an Aleph slice establishes file class by schema before scanning and treats the extension form as a cross-check, pointing at `aleph-entity-graph` for the measured detail.

## 4. Release surfaces

- [x] 4.1 Bump all three analyst version literals from `6.12.0` to `6.13.0` and keep both marketplace catalogs byte-identical.

## 5. Verification and delivery

- [x] 5.1 Run `~/ai/checks/check-acordia.sh` against the worktree, the four CLAUDE.md invariant scripts by hand, the catalog diff, the four-file JSON parse check, and `openspec validate --all --strict`.
- [x] 5.2 Re-run the shipped marker set against the live instance and confirm each string is established by corpus hit or upstream documentation, with no credential value read, printed or recorded.
- [x] 5.3 Confirm the competency grid is unchanged and both edited skills remain `procedural` with `grid_row: null`, so the bijection and every column's mark set are untouched.
- [x] 5.4 Review the complete diff with a correctness reviewer and a security reviewer, fix or explicitly dismiss findings, archive the OpenSpec change, re-run strict validation and the drift gate, and commit on `feat/search-artefacts-not-mentions`.
