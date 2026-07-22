## Why

The analyst roster is uniformly read-only (`edit: deny`), so no analyst can persist a written report — the "Briefing & written reporting" competency (role grid `docs/roles/operational-analyst.md` L76) exists as a method but has no place to land its output. Consumers must copy the report out of the agent's final message by hand. The two agents that actually hold the reporting competency should be able to write their report to a single, sanctioned location without gaining any broader edit capability.

## What Changes

- **Current behaviour:** `analyst-agent-roster` requires *every* analyst to set `edit: deny` (roster spec, "Requirement: Read-only file access via `edit: deny`"). All four agent files carry a blanket `edit: deny`.
- **Desired behaviour:** the two reporting-competency agents — `operational-analyst` (● Core) and `fusion-analyst` (○ Fus) — carry a **path-scoped** edit permission that denies edit everywhere except a single report directory:

  ```yaml
  edit:
    "*": deny
    ".acordia/reports/**": allow
  ```

  The two non-reporting legs — `target-network-analyst` and `defender-detection-analyst` — keep the blanket `edit: deny` unchanged.
- The scoped exception is derived from the grid, not invented: only rows with the reporting competency receive it. Grid columns without it stay fully read-only.
- Rationale note carried into the contract: `bash: "*": allow` already lets any analyst write files via `python`/`jq`, so `edit: deny` is a **posture/intent** signal rather than a hard sandbox. This change does not grant a new capability class — it declares the sanctioned output path for the two agents that are supposed to produce reports.
- The `briefing-reporting` skill (the report "how") is unchanged; the report destination `.acordia/reports/` is referenced as its landing zone.

Not breaking: the two non-reporting legs are unaffected; existing invocations that never wrote files continue to work.

## Capabilities

### New Capabilities
<!-- none -->

### Modified Capabilities
- `analyst-agent-roster`: the read-only requirement changes from "every analyst SHALL set `edit: deny`" to "non-reporting analysts SHALL set `edit: deny`; the two reporting-competency analysts SHALL set a path-scoped `edit` that denies all paths except `.acordia/reports/**`."

## Impact

- **Spec:** `openspec/specs/analyst-agent-roster/spec.md` — read-only requirement amended (delta).
- **Agent files:** `analysts/agents/operational-analyst.md`, `analysts/agents/fusion-analyst.md` — `edit: deny` → path-scoped block. `analysts/agents/target-network-analyst.md`, `analysts/agents/defender-detection-analyst.md` — unchanged (assert in spec).
- **Docs:** `docs/agents-skills-extension-workbook.md` §6 — document the path-scoped reporting-write convention. `CLAUDE.md` — update the "Read-only posture is mandatory. Every analyst carries `edit: deny`" line to reflect the two-agent scoped exception.
- **Runtime:** the `.acordia/reports/` directory becomes the sanctioned report sink under the opencode working root; no install-script change (the installer symlinks agents/skills only).
- **No** application code, build, or test surface affected (repo has none).
