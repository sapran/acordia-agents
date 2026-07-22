## 1. Extract the pattern library

- [ ] 1.1 Create `analysts/skills/credential-harvest-triage/references/credential-patterns.md` containing five classed sections: API keys (provider prefixes), auth material (Kerberos, JWT, OAuth), password hashes (bcrypt/argon2/NTLM/…), connection strings (DSN shapes), private keys (PEM/OpenSSH/PuTTY markers). Preserve the "verify current format at provider docs" caveat.
- [ ] 1.2 Remove the inline pattern-library block from `analysts/skills/credential-harvest-triage/SKILL.md`. Replace with a one-sentence pointer: "See `references/credential-patterns.md` for provider prefixes, hash formats, connection-string shapes, and private-key markers."
- [ ] 1.3 Verify `install.sh` behaviour: `./install.sh --dry-run` shows the reference file symlinking alongside `SKILL.md` under `~/.config/opencode/skills/credential-harvest-triage/`.

## 2. Retarget the seven credential-adjacent skills

- [ ] 2.1 Update `## Credential extraction` in `analysts/skills/disk-memory-forensics/SKILL.md` to reference `references/credential-patterns.md` under `credential-harvest-triage` instead of the inline block
- [ ] 2.2 Repeat 2.1 for `identity-directory-trust`
- [ ] 2.3 Repeat 2.1 for `log-artefact-interpretation`
- [ ] 2.4 Repeat 2.1 for `cloud-controlplane-analysis`
- [ ] 2.5 Repeat 2.1 for `web-api-authflow-analysis`
- [ ] 2.6 Repeat 2.1 for `os-host-internals`
- [ ] 2.7 Repeat 2.1 for `implant-payload-re`
- [ ] 2.8 Cross-check: no `## Credential extraction` section still references the inline block by content excerpt

## 3. Add the bucket-partition step

- [ ] 3.1 Amend `## Triage procedure` in `analysts/skills/credential-harvest-triage/SKILL.md` to include a bucket-partition step between inventory and per-category scan. Enumerate the five buckets: (A) identity/directory/cloud-controlplane → `target-network-analyst`; (B) host-forensic → whichever leg holds the host under analysis; (C) web/API auth → `target-network-analyst`; (D) log-artefact → `defender-detection-analyst`; (E) implant/payload RE → cross-cutting via `implant-payload-re`, reported to `fusion-analyst`.
- [ ] 3.2 Add a paragraph stating each bucket's slice is dispatched with only that slice, and that fusion re-merges classifications via `multi-source-fusion`.
- [ ] 3.3 Add one sentence to `## Credential harvest` in `analysts/agents/operational-analyst.md` naming the bucket-partition step and the three-leg parallel dispatch.
- [ ] 3.4 Verify permission blocks (`edit`, `bash`, `task`) unchanged in `operational-analyst.md`
- [ ] 3.5 Verify the three-leg `task` whitelist is unchanged
- [ ] 3.6 Verify no leg agent's prompt has been modified

## 4. Validate

- [ ] 4.1 `openspec validate --all --strict` passes
- [ ] 4.2 `test -f analysts/skills/credential-harvest-triage/references/credential-patterns.md`
- [ ] 4.3 `grep -c 'references/credential-patterns.md' analysts/skills/*/SKILL.md` reports at least 8 hits (seven credential-adjacent + the triage skill's pointer)
- [ ] 4.4 `grep -q 'bucket' analysts/skills/credential-harvest-triage/SKILL.md` succeeds and appears in the triage procedure section
- [ ] 4.5 Existing invariants hold: analyst count = 4, leg subagents = 3, skill count = 40, `edit: deny` on all agents
