# The Operator

### Provenance record for the Operations pillar of ACORDIA

**Version 1.1 · revised for distribution 3.0.0**

This is the operator pillar's source of truth, and it is shaped differently from `docs/roles/operational-analyst.md`. The analyst pillar derives its agents and skills from a competency grid — rows of skills scored `●`/`○` against columns of specialisations, compiled forward into files by an openspec contract. The operator pillar has no such grid, and this document does not manufacture one. `acordia-operators/` is a **port**: five agents and thirty skills carried over verbatim in methodology from an existing offensive fork, CyberStrike (`~/git/CyberStrike`, commit `359655518`, 2026-07-27), rather than a role derived from ACORDIA source material. Its source of truth is therefore provenance — which CyberStrike file each artifact came from, and which CyberStrike artifacts were deliberately left behind — not a skill-to-agent derivation.

## What the pillar is

`acordia-operators/` is the execution counterpart to `acordia-analysts/`. Every analyst prompt in this repo ends on the same guardrail — *"execution belongs to the operators you advise"* — and until this pillar existed, that advice had nowhere to land. CyberStrike is a fork of opencode carrying a compiled offensive agent roster and a large skill library authored in the same markdown contract this repo already writes to, which is what makes the transferable part of it portable here: five agents whose value is methodology, not fork-specific plumbing, plus thirty hand-authored technique skills.

When this pillar landed it was the first **write-capable** pillar in the repository — it writes scripts, evidence, and its own operation journal — against an analyst pillar that was then read-only by design. Since 3.0.0 both pillars are write-capable and the distinction is gone; see Posture below. The substitution contract that makes the ported prompts portable is recorded in the workbook, referenced below rather than restated here.

## Agent provenance

Five agent files under `acordia-operators/agents/`, each derived from the correspondingly named CyberStrike agent. Native agent definitions live in `packages/cyberstrike/src/agent/agent.ts`; prompt bodies live under `packages/cyberstrike/src/agent/prompt/`.

| Operator agent | CyberStrike agent | Prompt source | Native definition |
| --- | --- | --- | --- |
| `operator` (orchestrator) | `cyberstrike` | `prompt/cyberstrike.txt` + `prompt/methodology/common-methodology.txt` | `agent.ts` |
| `web-application` (specialist) | `web-application` | `prompt/web-application.txt` | `agent.ts` |
| `mobile-application` (specialist) | `mobile-application` | `prompt/mobile-application.txt` | `agent.ts` |
| `cloud-security` (specialist) | `cloud-security` | `prompt/cloud-security.txt` | `agent.ts` |
| `internal-network` (specialist) | `internal-network` | `prompt/internal-network.txt` | `agent.ts` |

`operator` dispatches these four specialists and names them in its prompt; each specialist is a leaf agent that dispatches nothing. Since 3.0.0 that routing is prompt discipline rather than a `task` permission map — the frontmatter carries no spawn allowlist.

## Skill provenance

Thirty skills under `acordia-operators/skills/`, each cloned from `.cyberstrike/skill/<path>/SKILL.md` (the per-skill source path is mechanical: the skill's own slug under that root, or under `.cyberstrike/skill/WEB/OWASP_WSTG_4.2/` for the four WSTG bundles).

**Attack family — 16:** `attack-cache-poison`, `attack-cors`, `attack-graphql`, `attack-host-header`, `attack-idor-automation`, `attack-jwt`, `attack-open-redirect`, `attack-prototype-pollution`, `attack-race-condition`, `attack-rate-limit-bypass`, `attack-request-smuggling`, `attack-ssrf`, `attack-ssti`, `attack-subdomain-takeover`, `attack-websocket`, `attack-xxe`.

**Infrastructure — 10:** `ad-security`, `kerberos-attacks`, `ebpf-attacks`, `cicd-attacks`, `recon-methodology`, `aws-postexploit`, `azure-postexploit`, `k8s-postexploit`, `windows-postexploit`, `macos-postexploit`.

**WSTG bundles — 4:** `wstg-recon-config`, `wstg-auth-session`, `wstg-injection`, `wstg-logic-client-api`.

16 + 10 + 4 = 30. Each skill's `metadata.cyberstrike.source` records the `.cyberstrike/skill/...` path it was cloned from, so a re-port against a newer CyberStrike commit is a diff, not an archaeology exercise. Frontmatter is reduced to the skill contract (`name`, `description`, optional `metadata`); bodies keep upstream payloads, commands, tables, and phase order — cloning is not an occasion to rewrite methodology.

## What was not ported, and why

- **The web-proxy pipeline** — `proxy-agent`, `proxy-analyzer`, and the eight `proxy-tester-*` agents. They read from CyberStrike's own proxy database through `web_get_*`/`web_write_*` tools, which have no substitution outside CyberStrike; without that database the agents have nothing to read.
- **Harness-internal CyberStrike agents** — `general`, `explore`, `compaction`, `title`, `summary`, `normalize-request`. Both omp and Claude Code already do this work natively; porting them would duplicate harness plumbing, not add methodology.
- **`bun-file-io`** — CyberStrike's own skill for developing CyberStrike itself (Bun file APIs), not a security capability.
- **The four generated corpora** — CIS benchmarks (5,000 skills), NIST control families (1,606), MITRE ATT&CK enterprise/mobile/ICS (898 combined), and the 121 individual WSTG leaf skills. Both target harnesses list every discovered skill's name and description in the system prompt; publishing the corpora would add roughly 190,000 tokens to every session, more than most context windows. This is a token-cost decision, not a value judgement on the corpora.
- **The Python attack scripts** under `packages/cyberstrike/data/scripts/`. This repository is markdown-only; every scripted technique that survives the port is expressed as a standard-tool invocation or an explicit inline command instead.

## Posture

Operators are write-capable, and since 3.0.0 so is every other agent in the distribution: an agent file's frontmatter is exactly `name`, `description` and `color`, so capability is granted by omission rather than by an `edit: allow` declaration. The analyst pillar's former `edit: deny` is gone too, which removes the contrast this section used to draw.

**The destructive-`bash` deny map was dropped in 3.0.0.** All five operator agents carried a 24-glob `permission.bash` map denying SQL DDL, `INTO OUTFILE`/`DUMPFILE`, `xp_cmdshell` and siblings, and `sqlmap --os-*`/`--file-write`/`--reg-*`, ported from CyberStrike's `injectionAgentPermission` ruleset. It was enforced only by opencode's `permission` map; omp and Claude Code have no per-pattern `bash` enforcement, so under both of them the map was already inert, and every generated file said so. With opencode no longer a target the map specified nothing, and a rule that enforces nothing while reading as a sandbox guarantee is worse than no rule.

What replaces it is the guardrails paragraph in each of the five prompts — no destructive action beyond what a proof of concept requires, no exfiltration beyond proof, no persistence, least privilege — which is what the map amounted to under omp anyway. This is a **deliberate divergence from upstream**, recorded here because a port losing a documented element without its record changing is drift. The source, should the map ever be wanted back: `injectionAgentPermission` in `packages/cyberstrike/src/agent/agent.ts:598-623` at commit `359655518`. The upstream gap noted while it was still present — that `*xp_cmdshell*`, `*sp_OACreate*`, `*sys_exec*` and `*sys_eval*` are listed in one case only, while SQL is case-insensitive server-side — is moot locally and remains upstream's to fix.

## Where the substitution table lives

The twelve CyberStrike platform tools these prompts and skills used to call, their fixed portable substitutions, and the `.acordia/ops/` operation-journal layout are documented once, in `docs/agents-skills-extension-workbook.md` (§8). This document does not restate that table — read it there before touching a ported artifact or porting a new pillar from the same fork.
