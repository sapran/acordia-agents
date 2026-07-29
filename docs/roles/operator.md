# The Operator

### Provenance record for the Operations pillar of ACORDIA

**Version 1.0 · 29 July 2026**

This is the operator pillar's source of truth, and it is shaped differently from `docs/roles/operational-analyst.md`. The analyst pillar derives its agents and skills from a competency grid — rows of skills scored `●`/`○` against columns of specialisations, compiled forward into files by an openspec contract. The operator pillar has no such grid, and this document does not manufacture one. `operators/` is a **port plus extension**: five agents and thirty-one skills — thirty carried over verbatim in methodology from an existing offensive fork, CyberStrike (`~/git/CyberStrike`, commit `359655518`, 2026-07-27), and one locally authored. Its source of truth is therefore provenance — which CyberStrike file each cloned artifact came from, which artifacts were not ported and why, and which locally-authored skills extend the library with what ancestry.

## What the pillar is

`operators/` is the execution counterpart to `analysts/`. Every analyst prompt in this repo ends on the same guardrail — *"execution belongs to the operators you advise"* — and until this pillar existed, that advice had nowhere to land. CyberStrike is a fork of opencode carrying a compiled offensive agent roster and a large skill library authored in the same markdown contract this repo already writes to, which is what makes the transferable part of it portable here: five agents whose value is methodology, not fork-specific plumbing, plus thirty hand-authored technique skills and one locally-authored extension.

Where the analyst pillar is read-only by design (`edit: deny`, no target interaction), the operator pillar is the first **write-capable** pillar in this repository: it writes scripts, evidence, and its own operation journal. The substitution and permission contracts that make that posture portable are recorded in the workbook, referenced below rather than restated here.

## Agent provenance

Five agent files under `operators/agents/`, each derived from the correspondingly named CyberStrike agent. Native agent definitions live in `packages/cyberstrike/src/agent/agent.ts`; prompt bodies live under `packages/cyberstrike/src/agent/prompt/`.

| Operator agent | CyberStrike agent | Prompt source | Native definition |
| --- | --- | --- | --- |
| `operator` (`mode: primary`) | `cyberstrike` | `prompt/cyberstrike.txt` + `prompt/methodology/common-methodology.txt` | `agent.ts` |
| `web-application` (`mode: subagent`) | `web-application` | `prompt/web-application.txt` | `agent.ts` |
| `mobile-application` (`mode: subagent`) | `mobile-application` | `prompt/mobile-application.txt` | `agent.ts` |
| `cloud-security` (`mode: subagent`) | `cloud-security` | `prompt/cloud-security.txt` | `agent.ts` |
| `internal-network` (`mode: subagent`) | `internal-network` | `prompt/internal-network.txt` | `agent.ts` |

`operator` dispatches only these four specialists (`permission.task` denies `"*"` then allows exactly those four names); each specialist sets `task: deny` and is a leaf agent.

## Skill provenance

Thirty-one skills under `operators/skills/`. Thirty are cloned from `.cyberstrike/skill/<path>/SKILL.md` (the per-skill source path is mechanical: the skill's own slug under that root, or under `.cyberstrike/skill/WEB/OWASP_WSTG_4.2/` for the four WSTG bundles). One is locally authored.

**Attack family — 16:** `attack-cache-poison`, `attack-cors`, `attack-graphql`, `attack-host-header`, `attack-idor-automation`, `attack-jwt`, `attack-open-redirect`, `attack-prototype-pollution`, `attack-race-condition`, `attack-rate-limit-bypass`, `attack-request-smuggling`, `attack-ssrf`, `attack-ssti`, `attack-subdomain-takeover`, `attack-websocket`, `attack-xxe`.

**Infrastructure — 10:** `ad-security`, `kerberos-attacks`, `ebpf-attacks`, `cicd-attacks`, `recon-methodology`, `aws-postexploit`, `azure-postexploit`, `k8s-postexploit`, `windows-postexploit`, `macos-postexploit`.

**WSTG bundles — 4:** `wstg-recon-config`, `wstg-auth-session`, `wstg-injection`, `wstg-logic-client-api`.

16 + 10 + 4 = 30 cloned. Each cloned skill's `metadata.cyberstrike.source` records the `.cyberstrike/skill/...` path it was cloned from, so a re-port against a newer CyberStrike commit is a diff, not an archaeology exercise. Frontmatter is reduced to opencode's contract (`name`, `description`, optional `metadata`); bodies keep upstream payloads, commands, tables, and phase order — cloning is not an occasion to rewrite methodology.

**Locally authored — 1:** `bolts`. Descended from CyberStrike's Bolt remote tool server concept (Ed25519-paired MCP tool servers managed from the TUI), but not cloned from any CyberStrike source — the mechanism here is plain SSH. Records `metadata.acordia.authored: operator-bolts` and `metadata.acordia.ancestor: CyberStrike Bolt` instead of a `metadata.cyberstrike` block. Introduced by OpenSpec change `operator-bolts`.

30 + 1 = 31 total.

## What was not ported, and why

- **The web-proxy pipeline** — `proxy-agent`, `proxy-analyzer`, and the eight `proxy-tester-*` agents. They read from CyberStrike's own proxy database through `web_get_*`/`web_write_*` tools, which have no substitution outside CyberStrike; without that database the agents have nothing to read.
- **Harness-internal CyberStrike agents** — `general`, `explore`, `compaction`, `title`, `summary`, `normalize-request`. Both opencode and omp already do this work natively; porting them would duplicate harness plumbing, not add methodology.
- **`bun-file-io`** — CyberStrike's own skill for developing CyberStrike itself (Bun file APIs), not a security capability.
- **The four generated corpora** — CIS benchmarks (5,000 skills), NIST control families (1,606), MITRE ATT&CK enterprise/mobile/ICS (898 combined), and the 121 individual WSTG leaf skills. Both target harnesses list every discovered skill's name and description in the system prompt; publishing the corpora would add roughly 190,000 tokens to every session, more than most context windows. This is a token-cost decision, not a value judgement on the corpora.
- **The Python attack scripts** under `packages/cyberstrike/data/scripts/`. This repository is markdown-only; every scripted technique that survives the port is expressed as a standard-tool invocation or an explicit inline command instead.

## Posture

Operators are write-capable: every agent sets `edit: allow`, unscoped — the deliberate opposite of the analyst pillar's `edit: deny`. Destructive and remote-code-execution `bash` primitives are denied by pattern (SQL DDL, `INTO OUTFILE`/`DUMPFILE`, `xp_cmdshell` and siblings, `sqlmap --os-*`/`--file-write`/`--reg-*`), ported from CyberStrike's `injectionAgentPermission` ruleset in `agent.ts`. Under omp those per-command denies are **prompt-level only** — omp has no per-pattern `bash` enforcement the way opencode's `permission` map provides, so the deny list is discipline the model is asked to follow, not a sandboxed guarantee, and the generated metadata says so rather than implying otherwise.

## Where the substitution table lives

The twelve CyberStrike platform tools these prompts and skills used to call, their fixed portable substitutions, and the `.acordia/ops/` operation-journal layout are documented once, in `docs/agents-skills-extension-workbook.md` (§8). This document does not restate that table — read it there before touching a ported artifact or porting a new pillar from the same fork.
