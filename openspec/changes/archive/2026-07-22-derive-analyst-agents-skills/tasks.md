## 1. Preparation

- [x] 1.1 Re-read the appendix grid in `docs/roles/operational-analyst.md` and confirm the 39-row inventory + marks in `design.md` still match (grid is source of truth)
- [x] 1.2 Create the skill root `~/.config/opencode/skills/` and agent root `~/.config/opencode/agents/` if absent

## 2. Author the skill library (39 skills, one per grid row)

- [x] 2.1 Author the 11 analytic-spine skills (`reasoning-under-uncertainty` … `human-automation-teaming`) as `~/.config/opencode/skills/<slug>/SKILL.md`, opencode frontmatter (`name` + triggering `description`)
- [x] 2.2 Author the 11 target-understanding skills (`target-mission-analysis` … `vuln-attacksurface-mapping`)
- [x] 2.3 Author the 9 defender-footprint skills (`detection-capability-analysis` … `disk-memory-forensics`)
- [x] 2.4 Author the 5 fusion skills (`multi-source-fusion` … `data-integration-tooling`)
- [x] 2.5 Author the 3 cross-cutting skills (`log-artefact-interpretation`, `analytic-tooling-scripting`, `ot-embedded`)
- [x] 2.6 Confirm slugs are plain (no prefix), each `name` matches its slug, and no `SKILL.md` carries CyberStrike-only fields or `sha256`
- [x] 2.7 State the RE (`implant-payload-re`) and OT (`ot-embedded`) attach-to-a-leg relationship in prose within those skill bodies

## 3. Author the agent roster (4 agents)

- [x] 3.1 Write `~/.config/opencode/agents/operational-analyst.md` — `mode: primary`, body from role-doc line 22, prompt names the resolved Core skill set, `edit: deny`
- [x] 3.2 Write `~/.config/opencode/agents/target-network-analyst.md` — `mode: subagent`, `description` = T&N italic question, body from lines 30–34, prompt names the resolved T&N skill set
- [x] 3.3 Write `~/.config/opencode/agents/defender-detection-analyst.md` — `mode: subagent`, `description` = Def italic question, body from lines 36–40, prompt names the resolved Def skill set
- [x] 3.4 Write `~/.config/opencode/agents/fusion-analyst.md` — `mode: subagent`, `description` = Fus italic question, body from lines 42–46, prompt names the resolved Fus skill set
- [x] 3.5 Confirm read-only posture per opencode's model: `edit: deny` on all four (opencode `edit` governs edit/write/patch); `task: deny` on the three legs — verified via `opencode debug agent`
- [x] 3.6 Confirm the `Core ●` spine skills are named in all four agents' prompts

## 4. Verify wiring against the grid

- [x] 4.1 Diff each agent's named skill set against its grid column (Core/T&N/Def/Fus); every marked row present, no unmarked row present
- [x] 4.2 Assert the row↔skill bijection: 39 grid rows ↔ 39 `SKILL.md` files, no orphans either side
- [x] 4.3 Confirm each subagent `description` conveys its leg's italic operating question

## 5. Load-test in opencode

- [x] 5.1 `opencode agent list` shows the four agents with correct modes (operational-analyst primary; three legs subagent)
- [x] 5.2 `opencode debug skill` discovers all 39 skills (39/39 unique slugs present)
- [x] 5.3 `operational-analyst` resolves as primary with `task` allowed (can dispatch); the three legs load as dispatchable subagents with distinct descriptions
- [x] 5.4 `opencode debug agent` resolves `edit: deny` on every analyst (file modification blocked)
