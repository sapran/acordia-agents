## 1. Pillar scaffold and provenance

- [ ] 1.1 Create `operators/agents/` and `operators/skills/` directories
- [ ] 1.2 Write `docs/roles/operator.md`: source-of-truth map (each ported agent → CyberStrike prompt path; each ported skill → `.cyberstrike/skill/` path; the CyberStrike commit the port was taken from), plus the recorded non-ports (proxy pipeline, harness-internal agents, `bun-file-io`, the four corpora) with reasons
- [ ] 1.3 Add the CyberStrike-to-portable substitution table and the `.acordia/ops/` journal layout to `docs/agents-skills-extension-workbook.md`

## 2. Agent prompts

- [ ] 2.1 Write `operators/agents/operator.md` — `mode: primary`, `task` whitelist of the four specialists, `edit: allow`, `bash: allow` + destructive denies; body ported from `prompt/cyberstrike.txt` + `prompt/methodology/common-methodology.txt` with ReAct discipline, delegation quality rules, long-running-task strategy, journal section, authorization/scope gate, deep-skill line
- [ ] 2.2 Write `operators/agents/web-application.md` from `prompt/web-application.txt` (+ methodology common and forced-continuation), naming the WSTG bundles and web attack skills
- [ ] 2.3 Write `operators/agents/mobile-application.md` from `prompt/mobile-application.txt`
- [ ] 2.4 Write `operators/agents/cloud-security.md` from `prompt/cloud-security.txt`, naming the cloud/k8s post-exploitation skills
- [ ] 2.5 Write `operators/agents/internal-network.md` from `prompt/internal-network.txt`, naming the AD/Kerberos/host post-exploitation skills
- [ ] 2.6 Verify no agent prompt names a CyberStrike platform tool, a `list` tool, or a skill absent from `operators/skills/`

## 3. Skill library

- [ ] 3.1 Clone the 16 web/application attack skills (`attack-*`) with reduced frontmatter, provenance metadata, when-clause descriptions, and `attack_script` substitutions
- [ ] 3.2 Clone the 10 infrastructure skills (`ad-security`, `kerberos-attacks`, `ebpf-attacks`, `cicd-attacks`, `recon-methodology`, `aws-postexploit`, `azure-postexploit`, `k8s-postexploit`, `windows-postexploit`, `macos-postexploit`) under the same rules
- [ ] 3.3 Clone the 4 WSTG bundle skills (`wstg-recon-config`, `wstg-auth-session`, `wstg-injection`, `wstg-logic-client-api`)
- [ ] 3.4 Verify every skill: slug equals `name`, frontmatter keys ⊆ {`name`, `description`, `metadata`}, no signing fields, no platform-tool reference, body diff against source confined to frontmatter and substitutions

## 4. Translator

- [ ] 4.1 Derive the omp `tools` allowlist from the source `permission` map (`edit`+`write` when edit is not denied, `browser` when allowed, `task`+`spawns` when the task map names agents)
- [ ] 4.2 Make the Tool-discipline paragraph rewrite conditional on the paragraph being present; keep the surviving-`list` assertion unconditional
- [ ] 4.3 Make the write-access metadata note three-way (denied / path-scoped / allowed)
- [ ] 4.4 Record in generated metadata that per-command bash denies have no omp equivalent when the source carries them
- [ ] 4.5 Prove analyst output is unchanged: translate `analysts/agents/*.md` before and after, diff the generated files

## 5. Documentation

- [ ] 5.1 Update `README.md`: pillar list, operators' write-capable posture, install examples with `--pillar operators`
- [ ] 5.2 Update `CLAUDE.md`: pillar scope, the operator format contract, the journal convention, source-of-truth chain for this pillar

## 6. Verification

- [ ] 6.1 `openspec validate --all --strict`
- [ ] 6.2 `./install.sh --pillar operators --harness both --dry-run` exits zero and lists 35 artifacts
- [ ] 6.3 Install to a temp target for each harness and confirm the translated agents carry the expected `tools`, `spawns`, and metadata
- [ ] 6.4 `opencode debug agent operator` and one specialist resolve with the expected mode and permissions; `opencode debug skill` resolves one cloned skill
- [ ] 6.5 Confirm the analyst pillar still installs and resolves unchanged
