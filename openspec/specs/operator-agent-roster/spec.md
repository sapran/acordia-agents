# operator-agent-roster Specification

## Purpose
Defines the five opencode Operations agents ported from the CyberStrike roster recorded in `docs/roles/operator.md` — one primary orchestrator plus four domain specialists — including their modes and dispatch descriptions, the unscoped write-capable `edit: allow` posture and the destructive-bash denylist beside it, the authorization and scope gate every prompt opens with, the prompt-named skill sets, the `.acordia/ops/` operation-journal section, and the delegation discipline retained in the primary.
## Requirements
### Requirement: Five operator agents ported from the CyberStrike roster

The `operators/` pillar SHALL contain exactly five agent files under `operators/agents/`: `operator.md`, `web-application.md`, `mobile-application.md`, `cloud-security.md`, and `internal-network.md`. Each SHALL be derived from the correspondingly named CyberStrike agent recorded in `docs/roles/operator.md`, whose native definitions live in `packages/cyberstrike/src/agent/agent.ts` with prompt bodies under `packages/cyberstrike/src/agent/prompt/`.

The CyberStrike agents that are **not** ported — `proxy-agent`, `proxy-analyzer`, the eight `proxy-tester-*` testers, and the harness-internal `general`, `explore`, `compaction`, `title`, `summary`, `normalize-request` agents — SHALL be named in `docs/roles/operator.md` together with the reason, so an omission is a recorded decision rather than an oversight.

#### Scenario: Roster is complete and named

- **WHEN** the pillar's agent directory is listed
- **THEN** exactly those five `.md` files are present, and each filename is the agent name

#### Scenario: Every ported agent traces to a CyberStrike source

- **WHEN** any operator agent file is inspected
- **THEN** `docs/roles/operator.md` names the CyberStrike prompt file(s) it was derived from

#### Scenario: Non-ported CyberStrike agents are accounted for

- **WHEN** `docs/roles/operator.md` is read
- **THEN** it lists every CyberStrike agent that was not ported, each with its reason

### Requirement: One primary orchestrator, four specialist subagents

`operator` SHALL be `mode: primary` and SHALL dispatch the four specialists. `web-application`, `mobile-application`, `cloud-security`, and `internal-network` SHALL be `mode: subagent`.

`operator`'s `permission.task` SHALL deny `"*"` first and then allow exactly those four names, so no general-purpose or explore agent is reachable from the primary. Each specialist SHALL set `task: deny`.

#### Scenario: Modes assigned per role

- **WHEN** the five agents are loaded
- **THEN** `operator` resolves to `primary` and the four specialists resolve to `subagent`

#### Scenario: Primary dispatches only its four specialists

- **WHEN** `operator`'s `permission.task` block is inspected
- **THEN** it denies `"*"` and allows exactly `web-application`, `mobile-application`, `cloud-security`, and `internal-network`

#### Scenario: Specialists are leaf agents

- **WHEN** any specialist agent is inspected
- **THEN** its resolved `task` permission is `deny` and it declares no dispatchable agent

### Requirement: Dispatch descriptions are the routing signal

Each specialist's `description` SHALL state its domain in one sentence, conveying the same routing signal as its CyberStrike counterpart's description, because `description` is the only routing signal a subagent has. Each agent's `description` SHALL additionally open with the pillar provenance tag `ACORDIA Operations — `, ahead of the domain sentence and without altering it, because these names (`operator`, `web-application`, `mobile-application`, `cloud-security`, `internal-network`) are generic enough to be mistaken for a harness built-in, and a write-capable agent is the one whose origin the user most needs to see.

#### Scenario: Description conveys the domain

- **WHEN** `internal-network` is inspected
- **THEN** its `description` conveys internal-network and Active Directory work — AD attacks, Kerberos, lateral movement

#### Scenario: Description carries the pillar tag

- **WHEN** any agent under `operators/agents/` is inspected
- **THEN** its `description` begins with `ACORDIA Operations — `
- **AND** the domain sentence following the tag is unchanged in meaning

#### Scenario: Provenance is carried by the description, not the name

- **WHEN** the agent files, the primary's `task` whitelist, and the skill slugs are inspected
- **THEN** no agent filename, agent name, or skill slug carries a distribution prefix

### Requirement: Operators are write-capable

Operators execute; they write scripts, evidence, journal entries, and reports. Every operator agent SHALL set `edit: allow`, making this the first write-capable pillar in the repository and the deliberate opposite of the analyst posture (`edit: deny`).

The pillar SHALL NOT rely on path-scoped writes, because **a path-scoped `edit` rule is unenforceable in every harness**. Every operator agent carries `bash: allow`, an open write channel at any path, so a scoped rule would be defeated by a shell redirection in opencode exactly as in omp and Claude Code (see `analyst-agent-roster`, where the analyst pillar's report sink is fixed as a convention on the same grounds). omp additionally cannot express a path scope at all, but that is a secondary limitation, not the reason.

The reason SHALL NOT be stated as a harness asymmetry — "enforced in opencode and silently absent in omp" — because no harness enforces such a rule, and that phrasing has propagated into documentation and into later changes reasoning by analogy. Where an operator is expected to write, the prompt body SHALL name the destination (`.acordia/ops/…`) as discipline rather than as a permission.

An unscoped `edit: allow` is therefore the honest posture rather than a concession: it claims exactly the capability the agent has.

#### Scenario: File modification allowed

- **WHEN** an operator agent writes or edits a file
- **THEN** the resolved `edit` permission is `allow` and the write proceeds

#### Scenario: No path-scoped write rules

- **WHEN** any operator agent's `edit` block is inspected
- **THEN** it is the scalar `allow`, with no path-keyed sub-rules

#### Scenario: The reason given is universal, not per-harness

- **WHEN** the justification for the unscoped `edit: allow` is read in any live spec or document
- **THEN** it attributes the unenforceability of a path scope to `bash: allow` in every harness
- **AND** it does not claim that such a rule would be enforced in opencode

#### Scenario: Journal destination is prompt discipline

- **WHEN** an operator prompt describes recording intel, coverage, findings, or a report
- **THEN** it names the `.acordia/ops/` destination in prose, and no permission rule attempts to confine writes to it

### Requirement: Destructive and RCE primitives denied in bash

Every operator agent SHALL set `bash: allow` with per-pattern `deny` rules covering destructive SQL DDL (`DROP TABLE`, `DROP DATABASE`, `DROP SCHEMA`, `TRUNCATE TABLE`), SQL-based file writes (`INTO OUTFILE`, `INTO DUMPFILE`), SQL-to-RCE primitives (`xp_cmdshell`, `sp_OACreate`, `sys_exec`, `sys_eval`, `COPY … TO PROGRAM`), and `sqlmap` flags that write files or execute commands (`--os-shell`, `--os-cmd`, `--os-pwn`, `--file-write`, `--reg-add`, `--reg-del`). Patterns SHALL be listed in both upper and lower case, because matching is case-sensitive.

This ruleset is ported from the `injectionAgentPermission` block in `packages/cyberstrike/src/agent/agent.ts`, where CyberStrike applies it to its injection tester. It is defence in depth beside the prompt rules, not a substitute for them.

#### Scenario: Destructive SQL denied

- **WHEN** an operator agent attempts a bash command containing `DROP TABLE` or `drop table`
- **THEN** the resolved `bash` permission for that command is `deny` and the command does not run

#### Scenario: sqlmap OS-interaction flags denied

- **WHEN** an operator agent attempts a bash command containing `--os-shell`, `--os-cmd`, `--os-pwn`, `--file-write`, `--reg-add`, or `--reg-del`
- **THEN** the resolved `bash` permission for that command is `deny`

#### Scenario: Ordinary security tooling still runs

- **WHEN** an operator agent runs a non-matching command such as `nmap`, `ffuf`, `curl`, or a read-only CLI tool
- **THEN** the resolved `bash` permission is `allow`

### Requirement: Authorization and scope gate stated in every prompt

Every operator prompt SHALL open with an authorization and scope gate: confirm written authorization for the target, establish in-scope and out-of-scope assets, and never assume authorization. Each prompt SHALL state that scope is read from `.acordia/ops/scope.md` and that an absent or silent scope file means a target is **untested**, never implicitly in scope.

#### Scenario: Gate present in every agent

- **WHEN** any of the five operator prompts is inspected
- **THEN** it contains an authorization and scope section naming `.acordia/ops/scope.md`

#### Scenario: Absent scope is not consent

- **WHEN** the scope clause is read
- **THEN** it states that a target absent from the scope file is out of scope until confirmed, rather than defaulting to allowed

### Requirement: Prompt names its skill set

Because opencode has no per-agent `skills:` field, each operator prompt SHALL name the operator-library skills it draws on, under a `## Your specialist depth (deep)` heading followed by a single `·`-separated line of skill names. The skills named SHALL exist in `operators/skills/`.

The single-line-under-the-heading shape remains load-bearing, but for a different reason than before. No emitter consumes the line any more — the generated omp agents leave `autoloadSkills` unset unconditionally, because a prebuilt plugin is installed by the harness rather than by a user-invoked command and so has no flag to carry. `tools/build-plugins.py` nonetheless parses the line on every build and SHALL fail when the heading is absent or the line names no skills, so the shape this requirement mandates cannot rot unnoticed.

#### Scenario: Deep heading present with a skill line

- **WHEN** any operator agent file is inspected
- **THEN** it contains a `## Your specialist depth (deep)` heading whose immediately following line is a non-empty `·`-separated list of skill names

#### Scenario: Named skills exist

- **WHEN** the skill names in any operator prompt are resolved against `operators/skills/`
- **THEN** every named skill has a directory with a `SKILL.md`

#### Scenario: A broken deep line fails the build

- **WHEN** an operator prompt's `(deep)` heading is removed, or the line beneath it is blanked
- **THEN** `tools/build-plugins.py` exits non-zero naming that source file
- **AND** no plugin tree is regenerated

### Requirement: Journal discipline section in every prompt

Every operator prompt SHALL carry a `## Operation journal` H2 section describing how that agent records intel, coverage, findings, and reports as files under `.acordia/ops/`, per the `harness-tool-translation` capability. The primary's section SHALL additionally state that it composes the final report from the journal and does not delegate reporting.

#### Scenario: Section present in every agent

- **WHEN** any operator prompt is inspected
- **THEN** it contains an `## Operation journal` H2 section naming the `.acordia/ops/` paths it writes

#### Scenario: Primary owns reporting

- **WHEN** `operator`'s journal section is read
- **THEN** it states that the final report is composed by the primary from the journal, not delegated to a specialist

### Requirement: Delegation quality rules retained in the primary

`operator`'s prompt SHALL retain CyberStrike's context-rich delegation discipline: every dispatch names the phase, the discovered intel or endpoints it builds on, the coverage state, and explicit success criteria, and independent work is dispatched in parallel. A bare one-line dispatch SHALL be shown as the counter-example.

#### Scenario: Delegation section present

- **WHEN** `operator`'s prompt is inspected
- **THEN** it contains a delegation section requiring phase, intel, coverage state, and success criteria in each dispatch

#### Scenario: Parallel dispatch stated

- **WHEN** the delegation section is read
- **THEN** it states that independent assets or phases are dispatched in parallel rather than serially

