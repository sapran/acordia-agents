## 1. Extract the pattern library

- [x] 1.1 Create `analysts/skills/credential-harvest-triage/references/credential-patterns.md` containing the classed sections: API keys (provider prefixes), auth material (JWT/OAuth/bearer/basic), password hashes (MD5crypt/bcrypt/SHA-crypt/NTLM/NetNTLMv2), connection strings (DSN shapes), private keys (PEM markers), cloud service accounts, and k8s/secret files. Preserves the "verify current format at provider docs" caveat.
- [x] 1.2 Remove the inline pattern-library block from `analysts/skills/credential-harvest-triage/SKILL.md`. Replaced with a naming pointer paragraph linking `references/credential-patterns.md` and stating it is the single source of truth for detection patterns.
- [x] 1.3 Verify `install.sh` behaviour: `./install.sh --dry-run --pillar analysts` symlinks the whole `credential-harvest-triage` directory to `~/.config/opencode/skills/credential-harvest-triage`, so `references/credential-patterns.md` rides along (both `link` and `copy` modes carry the subdir).

## 2. Retarget the pattern-citing credential-adjacent skills

Only three of the seven credential-adjacent skills cite the pattern library specifically; the other four (`disk-memory-forensics`, `identity-directory-trust`, `cloud-controlplane-analysis`, `os-host-internals`) cite `credential-harvest-triage` for the **classification schema**, which stays in `SKILL.md` — those links remain correct and are intentionally left unchanged (minimal-change).

- [x] 2.1 `log-artefact-interpretation` — retargeted the "pattern-library prefixes" mention to link `../credential-harvest-triage/references/credential-patterns.md`
- [x] 2.2 `web-api-authflow-analysis` — retargeted the "pattern-library prefixes from credential-harvest-triage" link to the reference file
- [x] 2.3 `implant-payload-re` — retargeted the "pattern-library grep from credential-harvest-triage" link to the reference file
- [x] 2.4 Verified the four schema-citing skills (`disk-memory-forensics`, `identity-directory-trust`, `cloud-controlplane-analysis`, `os-host-internals`) correctly still point at `credential-harvest-triage/SKILL.md` for classification/reporting — no retarget needed
- [x] 2.5 Cross-check: no skill body still references the inline block by content excerpt (`grep 'AKIA\[0-9A-Z\]{16}'` returns only the reference file)

## 3. Add the bucket-partition step

- [x] 3.1 Amended `## Triage procedure` in `credential-harvest-triage/SKILL.md` to insert a bucket-partition step (new step 2) between inventory and first-pass scan. Enumerates five buckets: (A) identity/directory/cloud-controlplane → `target-network-analyst`; (B) host-forensic → whichever leg holds the host; (C) web/API auth → `target-network-analyst`; (D) log-artefact → `defender-detection-analyst`; (E) implant/payload RE → cross-cutting via `implant-payload-re`, reported to `fusion-analyst`. Downstream steps renumbered 3–8.
- [x] 3.2 Stated each bucket's slice is dispatched with only that slice; the correlate step (6) now names `fusion-analyst` re-merging classifications via `multi-source-fusion`.
- [x] 3.3 Added a sentence to `## Credential harvest` in `analysts/agents/operational-analyst.md` naming the bucket-partition step and the three-leg parallel dispatch.
- [x] 3.4 Verified permission blocks (`edit`, `bash`, `task`) unchanged in `operational-analyst.md`
- [x] 3.5 Verified the three-leg `task` whitelist unchanged
- [x] 3.6 Verified no leg agent's prompt was modified (only `operational-analyst.md` among agents)

## 4. Validate

- [x] 4.1 `openspec validate --all --strict` passes
- [x] 4.2 `test -f analysts/skills/credential-harvest-triage/references/credential-patterns.md`
- [x] 4.3 `grep -l 'credential-patterns.md' analysts/skills/*/SKILL.md` reports 4 files (the triage skill's own pointer + the three pattern-citing skills) — the accurate count given only three skills cite the library
- [x] 4.4 `grep -q 'Bucket partition' analysts/skills/credential-harvest-triage/SKILL.md` succeeds within the triage procedure section
- [x] 4.5 Existing invariants hold: analyst count = 4, leg subagents = 3, skill count = 40, `edit: deny` on all agents
