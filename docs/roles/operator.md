# The Operator

### Provenance record for the Operations pillar of ACORDIA

**Version 1.1 · revised for distribution 3.0.0**

**Agent renamed in 4.0.0.** This file keeps its name because it is a provenance record of an
upstream artifact that really was called *the operator*, and because the analyst competency grid
anchors line numbers into its sibling. The shipped agent, however, is now `cyber-operator`
(wrapper `/cyber-operator`, short handle `/operator`). Read every "operator" below as the role;
read `cyber-operator` as the file on disk. Where this document once said "the operator pillar" it
now says "the operations pillar", so that the pillar and the agent are no longer the same word.

This is the operations pillar's source of truth, and it is shaped differently from `docs/roles/operational-analyst.md`. The analyst pillar derives its agents and skills from a competency grid — rows of skills scored `●`/`○` against columns of specialisations, compiled forward into files by an openspec contract. The operations pillar has no such grid, and this document does not manufacture one. `acordia-operators/` is a **port**: five agents and thirty skills carried over verbatim in methodology from an existing offensive fork, CyberStrike (`~/git/CyberStrike`, commit `359655518`, 2026-07-27), rather than a role derived from ACORDIA source material. Its source of truth is therefore provenance — which CyberStrike file each artifact came from, and which CyberStrike artifacts were deliberately left behind — not a skill-to-agent derivation.

## What the pillar is

`acordia-operators/` is the execution counterpart to `acordia-analysts/`. Every analyst prompt in this repo ends on the same guardrail — *"execution belongs to the operators you advise"* — and until this pillar existed, that advice had nowhere to land. CyberStrike is a fork of opencode carrying a compiled offensive agent roster and a large skill library authored in the same markdown contract this repo already writes to, which is what makes the transferable part of it portable here: five agents whose value is methodology, not fork-specific plumbing, plus thirty hand-authored technique skills.

When this pillar landed it was the first **write-capable** pillar in the repository — it writes scripts, evidence, and its own operation journal — against an analyst pillar that was then read-only by design. Since 3.0.0 both pillars are write-capable and the distinction is gone; see Posture below. The substitution contract that makes the ported prompts portable is recorded in the workbook, referenced below rather than restated here.

## Agent provenance

Five agent files under `acordia-operators/agents/`, each derived from the correspondingly named CyberStrike agent. Native agent definitions live in `packages/cyberstrike/src/agent/agent.ts`; prompt bodies live under `packages/cyberstrike/src/agent/prompt/`.

| ACORDIA agent | CyberStrike agent | Prompt source | Native definition |
| --- | --- | --- | --- |
| `cyber-operator` (orchestrator) | `cyberstrike` | `prompt/cyberstrike.txt` + `prompt/methodology/common-methodology.txt` | `agent.ts` |
| `web-application` (specialist) | `web-application` | `prompt/web-application.txt` | `agent.ts` |
| `mobile-application` (specialist) | `mobile-application` | `prompt/mobile-application.txt` | `agent.ts` |
| `cloud-security` (specialist) | `cloud-security` | `prompt/cloud-security.txt` | `agent.ts` |
| `internal-network` (specialist) | `internal-network` | `prompt/internal-network.txt` | `agent.ts` |

`cyber-operator` dispatches these four specialists and names them in its prompt; each specialist is a leaf agent that dispatches nothing. Since 3.0.0 that routing is prompt discipline rather than a `task` permission map — the frontmatter carries no spawn allowlist.

## Skill provenance

Thirty-one skills under `acordia-operators/skills/` carry CyberStrike provenance, each with a `metadata.cyberstrike.source` naming the `.cyberstrike/skill/<path>/SKILL.md` it was cloned from (the per-skill source path is mechanical: the skill's own slug under that root, or under `.cyberstrike/skill/WEB/OWASP_WSTG_4.2/` for the WSTG material). Thirty were cloned directly; the thirty-first, `attack-sqli`, was split in 3.2.0 out of the `wstg-injection` bundle and carries that bundle's source path, because its payloads are the bundle's upstream SQL-injection text moved rather than authored.

**Attack family — 17:** `attack-cache-poison`, `attack-cors`, `attack-graphql`, `attack-host-header`, `attack-idor-automation`, `attack-jwt`, `attack-open-redirect`, `attack-prototype-pollution`, `attack-race-condition`, `attack-rate-limit-bypass`, `attack-request-smuggling`, `attack-sqli`, `attack-ssrf`, `attack-ssti`, `attack-subdomain-takeover`, `attack-websocket`, `attack-xxe`.

**Infrastructure — 10:** `ad-security`, `kerberos-attacks`, `ebpf-attacks`, `cicd-attacks`, `recon-methodology`, `aws-postexploit`, `azure-postexploit`, `k8s-postexploit`, `windows-postexploit`, `macos-postexploit`.

**WSTG bundles — 4:** `wstg-recon-config`, `wstg-auth-session`, `wstg-injection`, `wstg-logic-client-api`.

17 + 10 + 4 = 31. Each carries `metadata.cyberstrike.source`, so a re-port against a newer CyberStrike commit is a diff, not an archaeology exercise. Frontmatter is reduced to the skill contract (`name`, `description`, optional `metadata`); bodies keep upstream payloads, commands, tables, and phase order — cloning is not an occasion to rewrite methodology.

## Authored here, not ported — 8 (as of 3.2.0)

Eight operations skills were written in this repository rather than cloned from CyberStrike, so they carry **no `metadata.cyberstrike`** block — claiming upstream attribution for local text would corrupt the port record above. They are recorded here so this document stays a complete account of the pillar, not only of its ported half.

- `operation-journal` — the `.acordia/ops/` recording contract (file layout, severity/confidence scales, evidence and chaining rules) that the five operations prompts previously each restated. Written from `cyber-operator`'s own journal section, the fullest of the five.
- `gcp-postexploit` — Google Cloud post-exploitation, on the pattern of the ported `aws-`/`azure-`/`k8s-postexploit`. Added because `cloud-security` claimed GCP with no skill behind it.
- `mobile-data-storage`, `mobile-crypto-keys`, `mobile-platform-ipc`, `mobile-resilience-bypass`, `mobile-instrumentation` — the mobile technique library `mobile-application` previously admitted it lacked, lifted from that prompt's own `## Key techniques by area`.
- `linux-postexploit` — ordinary-userland Linux post-exploitation (SUID/sudo/capabilities, cron and systemd persistence, credential and key theft, container-escape triage), added in 3.2.0. Its boundary with the ported `ebpf-attacks` is stated in both bodies: `ebpf-attacks` owns the `CAP_BPF` loaded-program path, `linux-postexploit` owns what an ordinary shell reaches.

The operations library is therefore **31 ported + 8 authored = 39** as of 3.2.0.

## What was not ported, and why

- **The web-proxy pipeline** — `proxy-agent`, `proxy-analyzer`, and the eight `proxy-tester-*` agents. They read from CyberStrike's own proxy database through `web_get_*`/`web_write_*` tools, which have no substitution outside CyberStrike; without that database the agents have nothing to read.
- **Harness-internal CyberStrike agents** — `general`, `explore`, `compaction`, `title`, `summary`, `normalize-request`. Both omp and Claude Code already do this work natively; porting them would duplicate harness plumbing, not add methodology.
- **`bun-file-io`** — CyberStrike's own skill for developing CyberStrike itself (Bun file APIs), not a security capability.
- **The four generated corpora** — CIS benchmarks (5,000 skills), NIST control families (1,606), MITRE ATT&CK enterprise/mobile/ICS (898 combined), and the 121 individual WSTG leaf skills. Both target harnesses list every discovered skill's name and description in the system prompt; publishing the corpora would add roughly 190,000 tokens to every session, more than most context windows. This is a token-cost decision, not a value judgement on the corpora.
- **The Python attack scripts** under `packages/cyberstrike/data/scripts/`. This repository is markdown-only; every scripted technique that survives the port is expressed as a standard-tool invocation or an explicit inline command instead.

## Posture

Operators are write-capable, and since 3.0.0 so is every other agent in the distribution: an agent file's frontmatter is exactly `name`, `description` and `color`, so capability is granted by omission rather than by an `edit: allow` declaration. The analyst pillar's former `edit: deny` is gone too, which removes the contrast this section used to draw.

**The destructive-`bash` deny map was dropped in 3.0.0.** All five operations agents carried a 24-glob `permission.bash` map denying SQL DDL, `INTO OUTFILE`/`DUMPFILE`, `xp_cmdshell` and siblings, and `sqlmap --os-*`/`--file-write`/`--reg-*`, ported from CyberStrike's `injectionAgentPermission` ruleset. It was enforced only by opencode's `permission` map; omp and Claude Code have no per-pattern `bash` enforcement, so under both of them the map was already inert, and every generated file said so. With opencode no longer a target the map specified nothing, and a rule that enforces nothing while reading as a sandbox guarantee is worse than no rule.

What replaces it is the guardrails paragraph in each of the five prompts — no destructive action beyond what a proof of concept requires, no exfiltration beyond proof, no persistence, least privilege — which is what the map amounted to under omp anyway. This is a **deliberate divergence from upstream**, recorded here because a port losing a documented element without its record changing is drift. The source, should the map ever be wanted back: `injectionAgentPermission` in `packages/cyberstrike/src/agent/agent.ts:598-623` at commit `359655518`. The upstream gap noted while it was still present — that `*xp_cmdshell*`, `*sp_OACreate*`, `*sys_exec*` and `*sys_eval*` are listed in one case only, while SQL is case-insensitive server-side — is moot locally and remains upstream's to fix.

## Where the substitution table lives

The twelve CyberStrike platform tools these prompts and skills used to call, their fixed portable substitutions, and the `.acordia/ops/` operation-journal layout are documented once, in `docs/agents-skills-extension-workbook.md` (§8). This document does not restate that table — read it there before touching a ported artifact or porting a new pillar from the same fork.
