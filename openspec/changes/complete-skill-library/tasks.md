## 1. Grid first

- [ ] 1.1 In `docs/roles/operational-analyst.md`, rewrite L74 to `| Outcome judgement — end achieved (effect or intel), did the system actually change, & what now | ● | ● | | ○ |` and delete L82 (`Effect-on-target verification`)

## 2. New skills

- [ ] 2.1 Create `acordia-operators/skills/attack-sqli/SKILL.md` from `wstg-injection` lines 12–104, on the `attack-ssrf`/`attack-xxe` pattern, copying `wstg-injection`'s `metadata.cyberstrike` `source` and `commit` exactly
- [ ] 2.2 Create `acordia-operators/skills/linux-postexploit/SKILL.md` on the `windows-postexploit` pattern: SUID/SGID and capabilities, sudo rules, cron and systemd-timer persistence, SSH key and agent-socket theft, shadow handling, host-side container-escape checks, kernel-exploit triage
- [ ] 2.3 State the `ebpf-attacks` ↔ `linux-postexploit` boundary in both bodies
- [ ] 2.4 Move `internal-network.md`'s `**Linux privilege escalation:**` block into `linux-postexploit`, then reduce it in the prompt to one routing line

## 3. Merge effect-on-target-verification into outcome-judgement

- [ ] 3.1 Fold the unique Method of `effect-on-target-verification` into `outcome-judgement`'s effect branch: observable-channel inventory, first-party vs independent confirmation, `<log>:<offset>` citation form, honeypot tells
- [ ] 3.2 Set `outcome-judgement` anchor to `grid_deep_in: [Core, 'T&N']`, `grid_working_in: [Fus]`, `source: docs/roles/operational-analyst.md#L74`
- [ ] 3.3 `git rm -r acordia-analysts/skills/effect-on-target-verification`
- [ ] 3.4 Remove the slug from every line naming it: `operational-analyst` spine 13 → 12, `target-network-analyst` deep 12 → 11, and any skill body, spec, README, CLAUDE.md or command wrapper
- [ ] 3.5 Confirm `grep -rn 'effect-on-target-verification' acordia-* docs openspec/specs README.md CLAUDE.md` returns nothing, while `human-automation-teaming` still resolves

## 4. Shrink the four WSTG bundles to pointers

- [ ] 4.1 `wstg-injection` → ≈ 3,600: SQLi → `attack-sqli`, SSTI → `attack-ssti`, SSRF → `attack-ssrf`, XXE → `attack-xxe`, Host Header → `attack-host-header`; keep XSS, Command Injection, LFI/Path Traversal, HTTP Parameter Pollution, Mass Assignment
- [ ] 4.2 `wstg-auth-session` → ≈ 6,000: JWT → `attack-jwt`, IDOR → `attack-idor-automation`; keep Privilege Escalation Patterns
- [ ] 4.3 `wstg-logic-client-api` → ≈ 5,900: CORS → `attack-cors`, GraphQL → `attack-graphql`, WebSocket → `attack-websocket`, Rate Limiting & Function Abuse → `attack-rate-limit-bypass` + `attack-race-condition`; keep Mass Assignment in APIs
- [ ] 4.4 `wstg-recon-config` → ≈ 5,300: takeover portion of `## Subdomain & Cloud Storage` → `attack-subdomain-takeover`
- [ ] 4.5 Before each pointer, confirm the destination carries the Method; append any payload or flag the bundle holds and the skill lacks
- [ ] 4.6 Removed total ≈ 8,078 chars / 270 lines — a larger cut means content is being deleted, not de-duplicated

## 5. Family taxonomy

- [ ] 5.1 Add `metadata.acordia.family` to every skill: analyst skills inside the existing `metadata.acordia` block, operator skills as an `acordia` key beside the untouched `metadata.cyberstrike`
- [ ] 5.2 Confirm every skill lands in exactly one of the twelve families and every family has ≥1 member; counts sum to 81

## 6. Descriptions

- [ ] 6.1 Rewrite all 81 descriptions discriminator-first: open with an imperative naming the distinct job, then the trigger, 1–1024 chars, no `Use when`/`Apply when`/`Use to` opening
- [ ] 6.2 Separate `macos-postexploit` and `windows-postexploit` on their platform mechanisms (TCC/keychain vs LSASS/DPAPI)
- [ ] 6.3 Within each family, confirm no two descriptions compete

## 7. Orphans and version

- [ ] 7.1 Add `aleph-entity-graph`, `credential-harvest-triage`, `exhaustive-data-processing` to `fusion-analyst.md`'s working-knowledge line
- [ ] 7.2 Bump both `plugin.json` files and both catalogs to 3.2.0; set analyst 42 / operator 39 in both descriptions
- [ ] 7.3 Update `openspec/config.yaml` context counts (43 → 42 analyst)

## 8. Verification

- [ ] 8.1 Counts: 42 analyst skills, 39 operator skills, 81 total
- [ ] 8.2 Every skill declares one of the twelve families; every family non-empty
- [ ] 8.3 No description opens with a boilerplate clause
- [ ] 8.4 No dangling `effect-on-target-verification` anywhere; `human-automation-teaming` intact
- [ ] 8.5 Every skill slug is named on at least one prompt line; every named slug resolves
- [ ] 8.6 Every payload removed from a bundle is present in the destination skill
- [ ] 8.7 Prompt-size ceiling still holds (no body over 10,000 chars)
- [ ] 8.8 Live dispatch reads `attack-sqli` and `linux-postexploit` out of the tree
- [ ] 8.9 `openspec validate --all --strict` passes
