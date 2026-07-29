## Why

This repository ships one pillar — `analysts/` — and every analyst prompt ends on the same guardrail: *"Execution belongs to the operators you advise."* Those operators do not exist here, so the advice has no counterpart to hand work to.

They do exist elsewhere. CyberStrike (`~/git/CyberStrike`, a fork of opencode) carries a compiled offensive roster and a 7,656-file skill library in the same markdown contract this repo authors to. None of it runs under omp: omp does not discover CyberStrike agents, its skill discovery is non-recursive, and the platform tools the CyberStrike prompts call (`report_vulnerability`, `add_intel`, `methodology_status`, `attack_script`, `hackbrowser`, the `skill` CLI) exist only inside that fork. Porting the transferable part gives this repo its execution pillar and makes the CyberStrike methodology runnable in both harnesses.

## What Changes

Layered so each layer reviews independently.

**Layer 1 — agent prompts (new `operators/agents/`, 5 files)**

- `operator` — `mode: primary`, the orchestrating offensive brain. Dispatches only the four specialists below. Derived from `packages/cyberstrike/src/agent/prompt/cyberstrike.txt` plus `prompt/methodology/common-methodology.txt`.
- `web-application` — OWASP WSTG / API testing specialist (`prompt/web-application.txt`).
- `mobile-application` — Android/iOS, MASTG/MASVS (`prompt/mobile-application.txt`).
- `cloud-security` — AWS/Azure/GCP/K8s, IAM and CIS posture (`prompt/cloud-security.txt`).
- `internal-network` — AD, Kerberos, lateral movement (`prompt/internal-network.txt`).

**Layer 2 — skill library (new `operators/skills/`, 30 skills)**

- 26 standalone technique skills cloned from `.cyberstrike/skill/<name>/SKILL.md` (the `attack-*` family, `ad-security`, `kerberos-attacks`, `ebpf-attacks`, `cicd-attacks`, `recon-methodology`, and the four `*-postexploit` skills). `bun-file-io` is excluded — it is CyberStrike's own repo-development skill, not a security capability.
- 4 OWASP WSTG bundle skills cloned from `.cyberstrike/skill/WEB/OWASP_WSTG_4.2/`: `wstg-recon-config`, `wstg-auth-session`, `wstg-injection`, `wstg-logic-client-api` — the aggregates the CyberStrike specialists already reference.
- Frontmatter reduced to opencode's contract (`name`, `description`, optional `metadata`): CyberStrike-only fields (`category`, `version`, `author`, `tags`, `owasp_id`, `cwe_ids`, `chains_with`, `prerequisites`, `severity_boost`) and any `sha256`/`signature`/`signed_by` pair are dropped, the last because a stale hash silently drops the skill as `tampered`.

**Layer 3 — harness-tool translation (new capability)**

CyberStrike prompts and skill bodies call twelve platform tools that neither opencode nor omp provides. Each gets one fixed, documented substitution — a file-based operation journal under `.acordia/ops/` plus native tools — so no ported artifact names a tool that does not exist:

| CyberStrike tool | Portable substitution |
| --- | --- |
| `add_intel` | append to `.acordia/ops/intel.md` |
| `update_vrt_check`, `record_coverage_note` | append to `.acordia/ops/coverage.md` |
| `methodology_status`, `get_coverage_notes` | read those two files |
| `scope_check` | read `.acordia/ops/scope.md`; absent file means untested, not in-scope |
| `report_vulnerability`, `triage_vulnerability` | write `.acordia/ops/findings/<slug>.md` |
| `generate_report` | compose from the journal into `.acordia/ops/reports/` |
| `ensure_tools` | `bash` install, with the user asked first |
| `attack_script <name>` | the named standard tool or an explicit inline command |
| `hackbrowser` | `browser` where the harness has it (omp), else scripted HTTP |
| `skill search`/`load`/`unload` | prompt-named skills; skills fire by description |

**Layer 4 — permission posture (new for this repo)**

Operators are the first **write-capable** pillar: `edit: allow`, because an operator writes scripts, evidence, and its own journal. `bash: allow` carries a deny list for destructive and RCE primitives (SQL DDL, `INTO OUTFILE`, `xp_cmdshell`, `sqlmap --os-*`/`--file-write`), ported from CyberStrike's injection-tester ruleset. The primary whitelists exactly its four specialists in `permission.task`; every specialist sets `task: deny`.

**Layer 5 — translator (modified `tools/translate-omp.py`)**

- `tools` is derived from the source `permission` map instead of a hard-coded read-only list: `edit`+`write` appear when `edit` is not denied, `browser` when the source allows it, `task` when the source names spawnable agents.
- The exact-match "Tool discipline" paragraph rewrite becomes conditional (analyst prompts carry it, operator prompts do not); the assertion that no `` `list` `` token survives stays unconditional.

**Layer 6 — docs**

`docs/roles/operator.md` records the provenance map (each operator artifact → its CyberStrike source path and commit) as this pillar's source of truth. `README.md` and `CLAUDE.md` gain the pillar and its write-capable posture.

**Explicitly deferred — recorded, not silently dropped**

- The CyberStrike web-proxy pipeline (`proxy-agent`, `proxy-analyzer`, and the eight `proxy-tester-*` agents): they are driven by the fork's proxy database through `web_get_*` / `web_write_*` tools, which have no substitution outside CyberStrike.
- The 7,626 generated corpus skills (CIS benchmarks 5,000, NIST 1,606, MITRE ATT&CK enterprise/mobile/ICS 898, WSTG leaves 121): both harnesses list every discovered skill's name and description in the system prompt, so publishing them would cost roughly 190k tokens per session. A corpus-access design belongs to its own change.

## Capabilities

### New Capabilities

- `operator-agent-roster`: the five operator agents — modes, dispatch descriptions, prompt bodies, write-capable permissions with destructive-command denies, and the prompt-named skill sets.
- `operator-skill-library`: the 30-skill operator library — membership, provenance, opencode-only frontmatter, and the rules for what is dropped from a cloned CyberStrike skill.
- `harness-tool-translation`: the fixed substitution contract for CyberStrike platform tools, the `.acordia/ops/` journal layout, and the rule that no shipped artifact may name a tool the target harness lacks.

### Modified Capabilities

- `omp-harness-distribution`: the translated `tools` allowlist becomes a function of the source permission map rather than a fixed read-only list, and the Tool-discipline paragraph rewrite becomes conditional on the paragraph being present.

## Out of Scope

- Any change to the `analysts/` pillar's artifacts, permissions, or prompts.
- Porting CyberStrike's Python attack scripts (`packages/cyberstrike/data/scripts/*.py`) — this repository stays markdown-only.
- Corpus skill publication (CIS / NIST / MITRE / WSTG leaves) and the proxy-pipeline agents, both deferred above.
- Any `SYSTEM.md` session-persona install for the primary; `operator` lands in omp as a spawnable orchestrator like `operational-analyst` does.
