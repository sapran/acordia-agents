## ADDED Requirements

### Requirement: Operator agents carry the pillar and role anchor

Every operator agent's `metadata.acordia` block SHALL declare `pillar: operators` and `role` — `orchestrator` for `operator`, `specialist` for the four domain agents — and SHALL carry no `leg` key. The block is validated at build time, because the generator derives each agent's `color` from `role` and a malformed anchor otherwise produces a mislabelled agent in the picker rather than a failure.

The separate `metadata.cyberstrike` provenance block is unaffected.

#### Scenario: The anchor agrees with the mode

- **WHEN** an operator agent declares `mode: primary`
- **THEN** its `role` is `orchestrator`, and every `mode: subagent` operator declares `role: specialist`

## MODIFIED Requirements

### Requirement: Destructive and RCE primitives denied in bash

Every operator agent SHALL set `bash: allow` with per-pattern `deny` rules covering destructive SQL DDL (`DROP TABLE`, `DROP DATABASE`, `DROP SCHEMA`, `TRUNCATE TABLE`), SQL-based file writes (`INTO OUTFILE`, `INTO DUMPFILE`), SQL-to-RCE primitives (`xp_cmdshell`, `sp_OACreate`, `sys_exec`, `sys_eval`, `COPY … TO PROGRAM`), and `sqlmap` flags that write files or execute commands (`--os-shell`, `--os-cmd`, `--os-pwn`, `--file-write`, `--reg-add`, `--reg-del`).

Because opencode resolves these rules by literal glob match and not case-insensitively, every SQL keyword and every SQL-to-RCE identifier SHALL be listed in both an all-upper-case and an all-lower-case form. SQL is case-insensitive on the server, so a single-cased pattern is no guard: `EXEC XP_CMDSHELL` and `SELECT SYS_EXEC(...)` are accepted by SQL Server and MySQL respectively and would pass a lower-case-only glob. `sp_OACreate` SHALL additionally keep its mixed-case vendor spelling, which neither the all-upper nor the all-lower pattern matches. The six `sqlmap` flags SHALL be listed in lower case only, because that CLI's option parsing is case-sensitive and no other spelling of a flag reaches it. The canonical set that results contains **29** patterns.

The deny set SHALL be identical across all five agents, and that identity SHALL be enforced at build time against a canonical set declared once in the generator. Five hand-synced copies of a safety list is a bypass waiting for the next edit: a pattern removed from one file and not the others leaves four agents guarded and one not, with nothing to report the difference. The rules SHALL nonetheless remain present in every source file, because opencode enforces them by reading the source, and only omp and Claude Code reduce them to prompt-level notes.

#### Scenario: The five deny sets cannot diverge

- **WHEN** one operator agent's deny set differs from the canonical set by any pattern
- **THEN** the build fails naming that agent and that pattern

#### Scenario: The source remains the enforced artifact

- **WHEN** an operator agent is deployed to opencode
- **THEN** its own frontmatter carries the full deny map, so enforcement does not depend on the generator having run

#### Scenario: Destructive SQL denied

- **WHEN** an operator agent attempts a bash command containing `DROP TABLE` or `drop table`
- **THEN** the resolved `bash` permission for that command is `deny` and the command does not run

#### Scenario: SQL-to-RCE identifiers denied in either case

- **WHEN** an operator agent attempts a bash command containing `xp_cmdshell`, `XP_CMDSHELL`, `sp_OACreate`, `sp_oacreate`, `SP_OACREATE`, `sys_exec`, `SYS_EXEC`, `sys_eval`, or `SYS_EVAL`
- **THEN** the resolved `bash` permission for that command is `deny` and the command does not run

#### Scenario: sqlmap OS-interaction flags denied

- **WHEN** an operator agent attempts a bash command containing `--os-shell`, `--os-cmd`, `--os-pwn`, `--file-write`, `--reg-add`, or `--reg-del`
- **THEN** the resolved `bash` permission for that command is `deny`

#### Scenario: Ordinary security tooling still runs

- **WHEN** an operator agent runs a non-matching command such as `nmap`, `ffuf`, `curl`, or a read-only CLI tool
- **THEN** the resolved `bash` permission is `allow`
