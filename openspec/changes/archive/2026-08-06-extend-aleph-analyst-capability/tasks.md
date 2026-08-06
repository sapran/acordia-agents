## 1. Skill accuracy

- [x] 1.1 Replace the hardcoded `aleph_*` prefix in the tooling paragraph with the seventeen registered tool verbs, plus a statement that the harness composes any prefix and the analyst should match on the verb
- [x] 1.2 State what the `bash` + HTTP fallback costs: no search-ceiling refusal, no expansion cap, no text-blob stripping, no derived caption, no read-only allowlist
- [x] 1.3 Add profile-scoped pivots to the method's pivot step, entered through the `profile_id` field, with the rule that a profile-scoped pivot beats an entity-scoped one where a profile exists
- [x] 1.4 Correct the narrowing step: `q` is not fuzzy on entity search, `match_entity` is the tolerant name path, multi-term `q` matches on 66% of terms
- [x] 1.5 Split the `caption` limit by path — derived under the tools, the analyst's problem under `curl`
- [x] 1.6 Update the take-assessment section so a profile reads as a recorded human decision, while an unjudged match still routes to `hypothesis-testing`

## 2. Agent prompts

- [x] 2.1 Add `## Aleph corpora` to `operational-analyst.md` after `## Credential harvest`, routing corpus work to `fusion-analyst` and requiring a coverage claim to name its collections
- [x] 2.2 Add `## Aleph corpora` to `fusion-analyst.md` after `## Exhaustive data processing`, with the cross-collection provenance lens
- [x] 2.3 Add `## Aleph corpora` to `target-network-analyst.md` after `## Exhaustive data processing`, with the ownership/address structure lens
- [x] 2.4 Add `## Aleph corpora` to `defender-detection-analyst.md` after `## Exhaustive data processing`, with the operation-owned exposure lens
- [x] 2.5 Confirm every section is additive: no existing section rewritten, no frontmatter or permission block touched

## 3. Specs

- [x] 3.1 `analyst-skill-library` delta: rewrite clause (c) off the mandated `aleph_*` wording onto tool verbs plus harness-prefix statement
- [x] 3.2 `analyst-skill-library` delta: require the fallback's cost, the profile pivots and `profile_id`, and the true query semantics; amend the harness-degradation scenario to cover a different prefix, not only no mount
- [x] 3.3 `analyst-agent-roster` delta: add the `## Aleph corpora` section requirement, mirroring the credential-harvest requirement's shape and scenario set
- [x] 3.4 `design.md` records why an H2 section does not break the grid bijection, and why reconcile was rejected

## 4. Distribution

- [x] 4.1 Bump `VERSION` in `tools/build-plugins.py` `2.0.0` → `2.1.0` (MINOR: user-reaching prose, no roster change)
- [x] 4.2 Run `tools/build-plugins.py` to regenerate `plugins/`, `.claude-plugin/`, `.omp-plugin/`

## 5. Verification

- [x] 5.1 `openspec validate --all --strict` passes
- [x] 5.2 `tools/build-plugins.py --check` exits 0
- [x] 5.3 `## Aleph corpora` present exactly once in each of the four agent prompts, and `aleph-entity-graph` named in all four
- [x] 5.4 No `edit`/`bash`/`task` permission line changed in any agent diff
- [x] 5.5 No hardcoded prefixed tool name survives in the skill; profile pivots and the not-fuzzy correction are present
- [x] 5.6 `docs/roles/operational-analyst.md` diff is empty
