## Context

`docs/roles/operational-analyst.md` (v1.1) defines the Analysis pillar of ACORDIA as a human role: a general **operational analyst** carrying a shared analytic **spine**, three **specialisations** (Target & Network, Defender & Detection, Fusion), and two cross-cutting deep skills (reverse-engineering, operational-technology). Its appendix "skills at a glance" grid maps ~39 skills across four columns (Core, T&N, Def, Fus) using `●` (deep/defining) and `○` (working) marks.

The deployment target is **opencode**. Verified from opencode's docs (opencode.ai/docs/agents, /skills):
- **Agents** load from `~/.config/opencode/agents/<name>.md` (global) and `.opencode/agents/` (project). Frontmatter: `description`, `mode` (subagent/primary/all), `model`, `temperature`, `permission`, `steps`. The filename is the agent name; the body is the system prompt. There is **no `skills:` field** — opencode discovers skills globally and triggers them by description.
- **Skills** load as `SKILL.md` from `~/.config/opencode/skills/<name>/` (among other dirs). Required frontmatter: `name` (lowercase-hyphen, 1–64) and `description` (1–1024). Optional `license`, `compatibility`, `metadata`. Unknown fields are ignored.

The grid is already an agent↔skill wiring table. This change compiles it: rows → skills, columns → each agent's prompt skill set, marks → deep/working membership. The exploration that produced this change is captured in the session; the decisions below are settled.

## Goals / Non-Goals

**Goals:**
- Turn the competency map into runnable opencode artifacts: 4 agents + ~39 skills.
- Keep the grid the single source of truth; make the wiring mechanically regenerable from it.
- Give analysts a decision-support shape (read/model/judge), distinct from the attack-executor agents.

**Non-Goals:**
- No application code; markdown + config only.
- No symlinks, canonical-source repo, per-tool wrappers, commands, `oa-` prefix, or cross-tool (Codex / Claude Code) placement. opencode is the sole target.
- Not authoring skill *bodies* to publishable depth here; the change fixes structure, wiring, and frontmatter. Body depth can iterate.
- Not committing artifacts to this repo — they live in the user's opencode config.

## Decisions

### D1 — Skills live in `~/.config/opencode/skills/<slug>/SKILL.md`
opencode-native, plain kebab-case slug matching `name`. No prefix. Frontmatter is opencode's schema: `name` + `description` required; `metadata` optional if grouping is wanted. No CyberStrike-only fields.
- **Alternative — a portable dir opencode also reads (`~/.agents/skills` / `~/.claude/skills`):** would let other tools see the skills, but adds cross-tool concerns the user explicitly rejected. opencode-only is the target.

### D2 — Agents live in `~/.config/opencode/agents/<name>.md`
opencode-native. Frontmatter: `description`, `mode`, `permission` (+ `steps`/`temperature` if wanted). Filename = agent name.

### D3 — `operational-analyst` is `mode: primary`
It is the senior/orchestrator: holds the spine's judgement and the end-neutral loop, dispatches the three legs, fuses their reads into one recommended course of action. This mirrors the role doc's "three technical reads feeding one analytic judgement" and fills a real gap (no decision-support role exists among the attack agents). opencode supports `mode: primary`.

### D4 — Composition is prompt-level, not a `skills:` list
opencode has no per-agent `skills:` binding; skills fire by description. So each agent's **prompt** names the skill set it draws on (resolved from its grid column), and the skills' descriptions must be triggering-quality. The `Core ●` spine skills are named in all four agents' prompts — that is how the shared spine is realised.

### D5 — Skills 1:1 with grid rows
39 rows → 39 skills, no merging. Keeps the grid the master and the wiring mechanically checkable (bijection). Thin rows (e.g. *naming-the-gaps*) get thin skills; acceptable.

### D6 — Read-only file access via `edit: deny`
opencode's permission default is **allow**, and (verified against opencode.ai/docs/permissions) `edit` governs the edit/write/patch tools collectively — there is no separate `write` key. A top-level `"*": deny` in agent frontmatter is *accepted* (it resolves as `*=deny`) but is **overridden by per-tool built-in defaults** — e.g. `read` still resolves to `allow` — so `"*": deny` does **not** produce a deny-default (verified empirically with a wildcard-only test agent). The read-only posture is therefore expressed as `edit: deny` on all four agents (blocks all file modification via built-in tools), plus `task: deny` on the three legs (leaf specialists). Analysis tools (read, grep, glob, bash, webfetch, websearch, skill) stay allowed by default.
- **Note (soft boundary):** `bash` is allowed for inspection, so shell-level file writes are technically possible; the guardrail is "no file-modification *tools*", not a hard sandbox. This matches the approved "read + web + shell for inspection" intent.
- **Verified:** `opencode debug agent <name>` resolves `edit=deny` on all four and `task=deny` on the legs.

### Resolved wiring — skill inventory (39 rows)

`slug` — grid group — marks `[Core/T&N/Def/Fus]` (● deep, ○ working, · none). The group is documentation (opencode has no `category`); it mirrors the grid's section headers.

**analytic spine**
1. `reasoning-under-uncertainty` [●···]
2. `naming-the-gaps` [●··○]
3. `hypothesis-testing` [●·○·]
4. `key-assumptions-check` [●···]
5. `deception-detection` [●·●·]
6. `calibrated-confidence` [●··○]
7. `method-timing-risk-decision` [●○○○]
8. `outcome-judgement` [●○·○]
9. `gain-loss-calculus` [●···]
10. `briefing-reporting` [●··○]
11. `human-automation-teaming` [●···]

**target understanding**
12. `target-mission-analysis` [○●··]
13. `pattern-of-life-baselining` [○●··]
14. `change-cycle-forecasting` [·●··]
15. `effect-on-target-verification` [○●··]
16. `packet-traffic-analysis` [○●●·]
17. `protocol-routing-architecture` [·●○·]
18. `os-host-internals` [○●●·]
19. `web-api-authflow-analysis` [·●○·]
20. `cloud-controlplane-analysis` [·●○○]
21. `identity-directory-trust` [·●○·]
22. `vuln-attacksurface-mapping` [○●○·]

**reading the defender & our own footprint**
23. `detection-capability-analysis` [○·●·]
24. `endpoint-telemetry-edr` [·○●·]
25. `cloud-identity-log-analysis` [·○●○]
26. `evasion-antianalysis` [·○●·]
27. `own-footprint-analysis` [··●·]
28. `overwatch` [○·●·]
29. `c2-beacon-exfil-analysis` [··●○]
30. `implant-payload-re` [·○●·]  ← cross-cutting **RE** (attaches to the legs that draw on it; stated in prose)
31. `disk-memory-forensics` [·○●·]

**pulling it together**
32. `multi-source-fusion` [○··●]
33. `nontechnical-context-integration` [···●]
34. `maintaining-operating-picture` [○··●]
35. `assessing-take-value` [○··●]
36. `data-integration-tooling` [○··●]

**cross-cutting technical**
37. `log-artefact-interpretation` [○●●●]
38. `analytic-tooling-scripting` [●○○○]
39. `ot-embedded` [·○○·]  ← cross-cutting **OT** (attaches to the legs that draw on it; stated in prose)

### Resolved wiring — per-agent prompt skill set

Read down each column; `●`+`○` both include the skill. Each agent's prompt names these.

- **operational-analyst** (Core): deep 1–11, 38; working 12,13,15,16,18,22,23,28,32,34,35,36,37 — 25 skills (the spine + baseline). Prompt emphasises the spine deeply; delegates deep technical reads to legs.
- **target-network-analyst** (T&N): deep 12–22, 37; working 7,8,24,25,26,30,31,38,39 — 21 skills.
- **defender-detection-analyst** (Def): deep 5,16,18,23,24,25,26,27,28,29,30,31,37; working 3,7,17,19,20,21,22,38,39 — 22 skills.
- **fusion-analyst** (Fus): deep 32–37; working 2,6,7,8,10,20,25,29,38 — 15 skills.

### Resolved wiring — agent frontmatter

- `mode`: primary (operational-analyst), subagent (three legs).
- `description`: legs use the role doc's italic operating questions (lines 32, 38, 44); the primary uses a one-line "senior analyst; directs specialists; runs the end-neutral loop" signal.
- `permission`: the D6 deny-default read-only posture on all four.
- Body: primary from line 22 (spine paragraph); legs from lines 30–34 / 36–40 / 42–46, each ending with an explicit list of the skills that agent draws on.

## Risks / Trade-offs

- **Drift between grid and artifacts** → hand-editing an agent's prompt skill set without touching the grid breaks D5/source-of-truth. Mitigation: a verification task diffs each agent's named skill set against its grid column and asserts the 39-row bijection.
- **Thin skills** → 1:1 fidelity yields some sparse `SKILL.md` bodies. Accepted; bodies iterate, structure is fixed now.
- **No explicit binding** → because opencode triggers skills by description, a weak description means the right skill never fires for the right agent. Mitigation: descriptions are triggering-quality (a spec requirement), and the agent prompt names its set as a backstop.
- **Fit risk** → analysts are decision-support, unlike the attack agents. Mitigation: read-only permissions (D6) and the primary/dispatch model make the difference explicit rather than papering over it.

## Open Questions

- Should the primary's prompt name all 25 (spine + baseline `○`) or a lean 12 (spine `●` only), delegating the `○` baselines to the legs? Design lists the faithful 25; a lean variant is a one-line trim at apply time.
- Do we want a tiny verification script (bijection + column-diff) committed alongside, or is manual verification at apply enough?
