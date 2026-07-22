## Context

Every analyst carries a blanket `edit: deny` (roster spec, "Requirement: Read-only file access via `edit: deny`"). The "Briefing & written reporting" competency exists in the role grid (`docs/roles/operational-analyst.md` L76) — `●` for Core (`operational-analyst`), `○` for Fus (`fusion-analyst`), and absent for the T&N and Def legs — but the read-only posture leaves it with nowhere to write. The user decided: the reporting agents should write their report to a single sanctioned directory, everything else stays read-only.

Constraint that shaped the design: opencode skills carry **no** permissions (composition is by prompt reference; there is no per-agent `skills:` binding), and legs carry `task: deny` so they cannot dispatch a helper agent.

## Goals / Non-Goals

**Goals**
- Let the two reporting-competency agents persist a report to disk.
- Keep every other analyst, and every non-report path for the reporting agents, read-only.
- Keep the change grid-derived (only rows with the competency get the exception) and source-of-truth-first (spec + contract before artifacts).

**Non-Goals**
- Not a hard sandbox. `bash: "*": allow` already permits scripted writes; this change does not close that and does not claim to.
- No change to the `briefing-reporting` skill's method content.
- No install-script change; `.acordia/reports/` is created at runtime under the opencode working root.
- No new agent and no reporting capability for the T&N or Def legs.

## Decisions

### Decision: Path-scoped `edit` on the reporting agents, not a separate writer agent or a skill

opencode's `edit` permission accepts path globs with last-match-wins precedence (same mechanic as `bash`), so `{ "*": deny, ".acordia/reports/**": allow }` denies everything except the sink. Chosen because it is the minimal, self-contained expression that keeps each agent's capability in its own frontmatter.

**Alternatives considered:**
- **Separate report-writer agent with edit rights.** Rejected: (a) the three legs carry `task: deny`, so only the orchestrator could reach it; (b) a writer agent has no grid column, breaking the roster's normative grid→agent bijection — it would need its own exception carve-out, more machinery than the problem warrants; (c) report content lives in the analyst's context and would have to be re-passed to the writer.
- **A skill that grants write.** Rejected as architecturally impossible: opencode skills carry no permissions; tool access comes only from the agent's frontmatter. A skill can teach report *format* (and `briefing-reporting` already does) but cannot grant `edit`.
- **Return the report as the agent's final message, keep `edit: deny`.** Viable and purest, but the user explicitly chose "agent writes the file."

### Decision: Grant the exception only to the two agents with the reporting competency

Scoping follows the grid: `●`/`○` on the "Briefing & written reporting" row = eligible; blank = stays `edit: deny`. Granting write to the T&N or Def legs would itself be grid drift (they feed findings up; they do not author reports).

### Decision: Single fixed sink `.acordia/reports/**`

One well-known directory keeps the glob crisp, keeps reports out of the source tree, and gives consumers a predictable location. A dotted directory signals tool-managed output.

## Risks / Trade-offs

- **[Posture vs. sandbox confusion]** A reader may think `edit: deny` guaranteed no writes. → The spec and workbook §6 state explicitly that bash scripting already allowed writes, so this is a posture signal; the change narrows, not widens, the honest guarantee.
- **[Scope creep of the sink]** Future agents copy the scoped block for non-report writes. → The requirement ties the exception to the grid competency, so any copy without a grid basis is a reviewable drift bug.
- **[Path-glob semantics]** Wrong glob could allow more than intended. → `"*": deny` first, `".acordia/reports/**": allow` last; last-match-wins means only paths under that prefix resolve to allow. Covered by two spec scenarios (inside allowed, outside denied).

## Migration Plan

1. Amend the roster spec requirement (delta) — source of truth first.
2. Update `docs/agents-skills-extension-workbook.md` §6 and `CLAUDE.md` to describe the scoped-write exception.
3. Edit the two reporting agent frontmatters; leave the two legs untouched.
4. `openspec validate --all --strict`; `opencode debug agent operational-analyst` / `fusion-analyst` to confirm the resolved `edit` permission.

Rollback: revert the two agent frontmatters to `edit: deny` and archive/revert the delta — no runtime state to unwind.

## Open Questions

- None blocking. Directory name `.acordia/reports/` is the user's stated choice.
