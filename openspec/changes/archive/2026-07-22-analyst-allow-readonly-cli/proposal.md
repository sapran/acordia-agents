## Why

The four analyst agents gate the *safe* read-only shell commands: `cat`/`head`/`tail`/`less`/`more`/`ls` resolve to `deny` and `grep`/`egrep`/`rg`/`find`/`fd` resolve to `ask`, while `bash: "*": allow` leaves genuinely destructive commands ungated. The gating exists only to steer analysts toward the opencode-native `read`/`grep`/`glob`/`list` tools — it is a nudge, not a security boundary. In practice it obstructs ordinary file-and-data analysis: an analyst inspecting a collected dump, `.env` archive, or log bundle hits a permission prompt (or a hard `deny`) on the exact read-only tools that analysis depends on, and gains nothing in return because `bash: "*": allow` already permits any write or destructive command. The nudge costs more than it buys.

## What Changes

- **Collapse the per-tool `bash` block to `bash: allow` on all four analyst agents** (`operational-analyst`, `target-network-analyst`, `defender-detection-analyst`, `fusion-analyst`). Every read-only CLI tool used for file and data analysis (`cat`, `head`, `tail`, `less`, `more`, `ls`, `grep`, `egrep`, `rg`, `find`, `fd`) becomes allowed. Because the block was already `"*": allow` with only these read-only substitutes gated, removing the gates leaves a plain `bash: allow` — no new command class is granted beyond what `"*": allow` already permitted.
- **Current behavior:** `cat`/`head`/`tail`/`less`/`more`/`ls` → `deny`; `grep`/`egrep`/`rg`/`find`/`fd` → `ask`; everything else `allow`.
- **Desired behavior:** all bash commands `allow`; no read-only CLI tool is gated.
- `edit`, `task`, and the orchestrator's three-leg dispatch whitelist are **unchanged**. Read-only *file-modification* posture (`edit: deny`, plus the `.acordia/reports/**` scoped-write exception) and the leaf-specialist `task: deny` are untouched. This change concerns only the `bash` tool-steering gates.
- **Update the convention record** so the source of truth stops describing gating that no longer exists: `openspec/config.yaml` context text and the `CLAUDE.md` "Bash discipline" bullet.

## Capabilities

### New Capabilities
<!-- none -->

### Modified Capabilities
- `analyst-agent-roster`: adds a normative requirement stating the `bash` posture — analysis via bash is fully allowed (`bash: allow`), read-only CLI tools are not gated — so the collapsed block is spec-anchored rather than a silent artifact edit. Existing `edit`/`task` requirements are unchanged.

## Impact

- **Agent files (4):** `analysts/agents/operational-analyst.md`, `target-network-analyst.md`, `defender-detection-analyst.md`, `fusion-analyst.md` — the multi-line `bash:` gating block becomes `bash: allow`. The `edit` and `task` blocks and every prompt body section are untouched.
- **Spec:** `openspec/specs/analyst-agent-roster/spec.md` — new "Bash analysis fully allowed" requirement (via delta).
- **Convention record:** `openspec/config.yaml` (context text, L22–24) and `CLAUDE.md` (Bash-discipline bullet, L61) reworded to describe `bash: allow`.
- **No behavioral risk added:** `bash: "*": allow` already permitted destructive commands; this only stops prompting on / denying read-only viewers and searchers. No security boundary is weakened.
