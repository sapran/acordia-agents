## Context

Each of the four analyst agents carries a multi-line `bash` permission block:

```yaml
bash:
  "*": allow
  "cat*": deny
  "head*": deny
  "tail*": deny
  "less*": deny
  "more*": deny
  "ls*": deny
  "grep*": ask
  "egrep*": ask
  "rg*": ask
  "find*": ask
  "fd*": ask
```

opencode resolves bash permissions last-match-wins. The block therefore *denies* the read-only viewers/listers and *prompts* on the read-only searchers, while `"*": allow` leaves every other command — including destructive ones (`rm`, `dd`, `curl … | sh`) — ungated. The gating's sole purpose is to steer analysts toward opencode-native `read`/`grep`/`glob`/`list`; it is a nudge, not a sandbox.

The roster spec (`analyst-agent-roster`) already states that bash "remains allowed by opencode's default" — the artifacts are currently *stricter* than the spec. The gating is recorded as convention in `openspec/config.yaml` (L22–24) and `CLAUDE.md` (L61), not as a normative spec requirement.

The user's decision (recorded at propose time): collapse the block to `bash: allow` on all four agents — allow every read-only CLI tool, no gating.

## Goals / Non-Goals

**Goals:**
- Every read-only CLI tool used for file/data analysis (`cat`, `head`, `tail`, `less`, `more`, `ls`, `grep`, `egrep`, `rg`, `find`, `fd`) is `allow` on all four analyst agents.
- The new posture is spec-anchored (a normative requirement), not a silent artifact edit.
- The convention record (`config.yaml`, `CLAUDE.md`) matches the artifacts — no source-of-truth drift.

**Non-Goals:**
- No change to `edit` posture (`edit: deny` + the `.acordia/reports/**` scoped-write exception on the two reporting agents stay exactly as-is).
- No change to `task` (leg `task: deny`; orchestrator three-leg whitelist).
- No change to any prompt body, skill set, description, or the credential-harvest / what-to-return / output-discipline sections.
- Not weakening a security boundary — `bash: "*": allow` already permitted destructive commands; this touches only the read-only-tool gates.

## Decisions

**D1 — Collapse to `bash: allow`, don't keep explicit `allow` entries.**
Because the block was already `"*": allow` with only the read-only substitutes overridden, setting each to `allow` is redundant with the wildcard. The minimal, unambiguous end state is a single `bash: allow`. Alternatives considered: (a) keep named `allow` entries for documentation — rejected as noise that re-states the wildcard; (b) keep `less`/`more` as `ask` because interactive pagers can hang — rejected: opencode runs bash non-interactively (no TTY), so a pager reading a redirected/piped stream exits immediately; gating them buys nothing and reintroduces a prompt.

**D2 — ADD a new requirement rather than MODIFY the existing read-only requirement.**
The existing "Read-only file access via `edit: deny`" requirement already says bash stays allowed by default and is otherwise about `edit`/`task`; it needs no edit. A new requirement — "Bash analysis fully allowed; read-only CLI tools ungated" — cleanly anchors the collapsed block and traces to the four agent files. This keeps the `edit`/`task` requirement untouched and avoids the MODIFIED-partial-content pitfall.

**D3 — Update convention records in the same change.**
`config.yaml` L22–24 and `CLAUDE.md` L61 describe the now-removed gating. Left stale, they become source-of-truth-drift bugs the next regeneration would re-introduce. Both are reworded to `bash: allow` in this change so spec, convention, and artifacts agree.

**D4 — Prompt-level preference for native tools is retained where it already lives.**
Removing the hard gate does not require deleting the "prefer opencode native `read`/`grep`/`glob`/`list`" guidance from agent prompts / `CLAUDE.md`; the preference survives as advice, only the coercive permission is dropped. (Agent prompt bodies are Non-Goals here; only the convention wording that claimed a *permission* gate is corrected.)

## Risks / Trade-offs

- **Loss of steering toward native tools** → Mitigation: the native-first preference remains as prompt/CLAUDE.md advice (D4); only the permission coercion is removed. Analysts still see the recommendation.
- **Interactive pager hang (`less`/`more`)** → Mitigation: opencode bash has no TTY, so pagers exit non-interactively (D1). Native `read` remains the recommended path.
- **Source-of-truth drift if convention records missed** → Mitigation: `config.yaml` and `CLAUDE.md` edits are explicit tasks; `openspec validate --all --strict` gates the spec delta (D3).
- **Perceived security loosening** → Mitigation: proposal + this doc make explicit that `"*": allow` already permitted destructive commands; the change only ungates read-only tools. No boundary moves.

## Migration Plan

1. Edit the four agent files: replace the multi-line `bash:` block with `bash: allow`. Leave `edit`, `task`, and all prompt sections byte-for-byte otherwise.
2. Add the delta requirement to `analyst-agent-roster`; run `openspec validate --all --strict`.
3. Reword `config.yaml` L22–24 and `CLAUDE.md` L61 to describe `bash: allow`.
4. (If available) `opencode debug agent <name>` to confirm each resolves `bash: allow` and unchanged `edit`/`task`.

Rollback: revert the branch — the prior multi-line block is restored verbatim.

## Open Questions

None. Scope and end-state fixed at propose time.
