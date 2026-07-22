## ADDED Requirements

### Requirement: Bash analysis fully allowed; read-only CLI tools ungated

Every analyst agent SHALL set `bash: allow`, granting every shell command — including the read-only CLI tools used for file and data analysis (`cat`, `head`, `tail`, `less`, `more`, `ls`, `grep`, `egrep`, `rg`, `find`, `fd`) — the `allow` resolution. No read-only CLI tool SHALL be gated with `deny` or `ask`.

This supersedes the prior tool-steering block (which denied `cat`/`head`/`tail`/`less`/`more`/`ls` and prompted on `grep`/`egrep`/`rg`/`find`/`fd` while leaving `"*": allow`). Removing those overrides grants no new command class: `bash: "*": allow` already permitted every non-read-only command, so `bash: allow` only lifts the gate on the read-only tools. The preference for opencode-native `read`/`grep`/`glob`/`list` is retained as prompt-level advice, not as a permission gate.

This requirement governs only the `bash` permission. It does not alter `edit` (read-only file-modification posture: `edit: deny`, plus the `.acordia/reports/**` scoped-write exception on the two reporting agents) or `task` (leg `task: deny`; the orchestrator's three-leg dispatch whitelist).

#### Scenario: Read-only CLI tools resolve to allow

- **WHEN** any analyst agent runs a read-only CLI command (`cat`, `head`, `tail`, `less`, `more`, `ls`, `grep`, `egrep`, `rg`, `find`, or `fd`)
- **THEN** its resolved `bash` permission is `allow` and the command runs without a prompt or denial

#### Scenario: Bash block is a single allow

- **WHEN** any analyst agent's frontmatter is inspected
- **THEN** its `bash` permission is `bash: allow` with no per-command `deny` or `ask` overrides

#### Scenario: edit and task posture unchanged

- **WHEN** an analyst agent's `edit` and `task` blocks are compared before and after this change
- **THEN** they are unchanged — file-modification stays denied outside the sanctioned report sink, legs still set `task: deny`, and the orchestrator still whitelists only its three legs
