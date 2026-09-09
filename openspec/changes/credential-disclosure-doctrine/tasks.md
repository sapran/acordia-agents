## 1. The authority skill

- [ ] 1.1 Add `ownership` to the classification schema table in
  `acordia-analysts/skills/credential-harvest-triage/SKILL.md`, with the four values and the fail-safe
  note, and change the table's lead-in so it no longer says analysts record the classification "never
  the raw value"; verify by reading the table back and confirming `ownership` is the first row and the
  lead-in states the ownership gate
- [ ] 1.2 Rewrite the `## Guardrails` section of the same file as the four routing rules plus the
  ownership gate, keeping the passive-only bullet and the escalation bullet, and dropping the
  "hash-of-value if disambiguation is needed" permission; verify no bullet claims the distribution
  enforces, blocks or prevents anything, and that `grep -c 'hash-of-value'` returns 0
- [ ] 1.3 Update triage step 5 to classify ownership before the rest of the schema and step 8 to state
  what the report may carry per ownership; verify both steps name `ownership` and step 8 no longer says
  "Do not include raw credential values"
- [ ] 1.4 Add `doctrine_source: [Monte#operational-security, Heuer#information-quantity]` to the
  skill's `metadata.acordia` block; verify both keys resolve in `docs/roles/sources.md`
- [ ] 1.5 Update the "record the pattern matched and the source location — never the raw value" line in
  `references/credential-patterns.md` to the redirect discipline; verify the file still parses as
  markdown and the pattern blocks are untouched

## 2. The seven credential-extraction sections

- [ ] 2.1 Rewrite the closing cross-cutting line of `## Credential extraction` in
  `disk-memory-forensics`, `identity-directory-trust`, `log-artefact-interpretation`,
  `cloud-controlplane-analysis`, `web-api-authflow-analysis` and `implant-payload-re` so each defers
  classification to `credential-harvest-triage` and requires extraction to terminate in a file write
  rather than standard output, keeping the domain identifier each already names; verify all six close
  with the redirect discipline and none still asserts a value may never be recorded
- [ ] 2.2 Give `os-host-internals` the same closing discipline, which today defers to the triage skill
  without stating the rule at all; verify its cross-cutting line now states where extraction output
  goes
- [ ] 2.3 Reconcile `web-api-authflow-analysis`'s "do not archive contents that are themselves
  PII/credentials" with the new permission; verify the line distinguishes a target-owned credential
  from personal claim data rather than forbidding both

## 3. The reporting skill

- [ ] 3.1 Invert the credential carve-out in `briefing-reporting`'s "Cite identifiers in full" bullet
  so a target-owned credential is carried whole per the ownership gate, an operation-owned or
  unadjudicated one never is, and a personal identifier is carried only as far as the judgement
  requires; verify the bullet no longer says a credential "is not cited at all"
- [ ] 3.2 In the same edit, add the verification carve-out to the rendered-product bullet: verify
  against the draft or by a check reporting a verdict, and never read a rendered product carrying
  credential values back into the session; verify both halves are present, because applying 3.1 alone
  ships a skill that permits a credential in the product and then requires reading it back

## 4. The three remaining skills

- [ ] 4.1 Update `exhaustive-data-processing`'s "No raw credential values in output" guardrail to the
  routing rule; verify it names working notes and the product as the destinations and keeps its
  passive-posture bullet
- [ ] 4.2 Update `packet-traffic-analysis`'s "Never quote raw credential values — cite location only"
  to the routing rule; verify the line still requires a location citation
- [ ] 4.3 Update `aleph-entity-graph`'s report bullet so a target-owned credential may be reported
  while bulk document text and excess personal identifiers stay excluded; verify the three clauses are
  still distinguishable
- [ ] 4.4 Confirm `operational-memory` is unchanged and still forbids a secret unconditionally; verify
  by diffing the file against `origin/develop` and seeing no change

## 5. The five prompts and two wrappers

- [ ] 5.1 Rewrite the `## Credential harvest` section in all five agent prompts to state
  ownership-first classification, the redirect discipline, and the never-restate rule including
  hand-backs, keeping each leg's existing domain sentence; verify all five sections carry the three
  rules and that `cyber-analyst` states them in its own words rather than by reference
- [ ] 5.2 Propagate the `cyber-analyst` body byte-identically into `commands/analyst.md` and
  `commands/cyber-analyst.md`; verify with `tools/check-acordia.sh`, whose orchestrator byte-identity
  check fails if either wrapper drifts

## 6. Docs, version, and gates

- [ ] 6.1 Add the empty-literature gap to `docs/roles/sources.md` under *Gaps — searched and not
  found*, naming what was searched; verify it follows the two existing entries' shape
- [ ] 6.2 Bump 6.7.0 → 6.8.0 in all three occurrences; verify with the version-lockstep check in
  `tools/check-acordia.sh`
- [ ] 6.3 Run `tools/check-acordia.sh` in the worktree and the four by-hand invariant checks from
  `CLAUDE.md` — slug resolution, grid-mark transcription, catalog byte-identity plus JSON parse, and
  skill-set declaration; verify every one reports zero problems and that the grid check's row count
  equals the grid's own
- [ ] 6.4 Run `openspec validate --all --strict`; verify it passes
