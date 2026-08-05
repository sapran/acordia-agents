## Context

The question that produced this change was "could my agents and skills be marked like `/opsx:`, or should I prefix the slugs?" Investigating the harnesses answered it: `/opsx:` is not a naming convention anyone applied to an artifact, it is a *directory*. `.claude/commands/opsx/apply.md` registers as both `apply` and `opsx:apply`. Nothing was renamed to get it.

The three artifact types differ sharply:

| Artifact | Namespace mechanism |
| --- | --- |
| Slash commands | Subdirectory becomes a prefix (`foo/bar.md` → `bar` **and** `foo:bar`); plugin-packaged commands are auto-prefixed `<plugin>:<command>` |
| Skills | None. Discovery is one level under `skills/`, non-recursive; nested `group/skill/SKILL.md` is not discovered. Flat dedup by name |
| Agents | None. Flat, exact-name lookup, first-wins dedup, case-sensitive |

So for agents and skills, "distinguish by name" can only mean a literal slug prefix, and that was measured before being rejected: 941 slug occurrences across 98 files for the analyst pillar alone, plus the grid bijection (`docs/roles/` row → slug → `SKILL.md`), the `·`-separated autoload lines the translator parses, `skill://` references, and per-skill spec requirements. It also buys nothing functionally, because skills are selected by **description match** — a prefix does not make a skill easier for the model to find.

## Goals

- One namespaced entry point per agent, in the harnesses the repository already targets.
- Zero renames: no agent name, no skill slug, no grid row.
- Command names that cannot drift from the agents they wrap.
- The same ownership, idempotence, and dry-run guarantees the agent and skill deployments already carry.

Non-goals: prefixing slugs; packaging the distribution as a plugin (which would grant `<plugin>:<command>` free, but is a distribution-model change, not a naming one); inventing a shorthand vocabulary for agents.

## Decisions

**Command filename equals the agent filename stem.** `/acordia:fusion-analyst`, not `/acordia:fusion`. Short handles read better for about a week, then become a second naming surface that drifts the first time an agent is renamed. The stem is already the dispatch handle wired into both orchestrators' `task` whitelists, so reusing it keeps one source of truth and makes the 1:1 correspondence mechanically checkable. Tab completion makes the extra characters free.

**Two namespace shapes rather than one lowest common denominator.** opencode cannot do the colon form — its command discovery is flat, which this repository already discovered and worked around when it shipped `.opencode/commands/opsx-apply.md` next to `.claude/commands/opsx/apply.md`. Rather than degrade every harness to the hyphen, each gets the best shape it supports. Rejected alternative: hyphen everywhere for uniformity — it throws away the exact affordance that motivated the change on the harness where it works.

**The omp deployment targets the Claude tree, deliberately.** omp's native `commands/` directory is non-recursive, so a namespace is impossible there; its `claude` provider, by contrast, scans `~/.claude/commands/**` recursively and adds the alias. Writing outside `$OMP_ROOT` for an `--harness omp` install is surprising enough to be worth an explicit line of installer output rather than a silent side effect. Where the user overrode the harness root with `--target`, the command root cannot be inferred, so the step is skipped with a message and `--commands-target` is offered.

**Commands are opt-out, not opt-in.** They are additive, cheap, and refuse to overwrite anything unowned; making them opt-in would mean most installs never get the feature that motivated the change. `--no-commands` covers the user who keeps a curated command tree.

**`commands/` is not a pillar.** Pillar auto-discovery requires a visible top-level directory carrying `agents/` or `skills/`. `commands/` carries neither, so the existing rule already excludes it — no exclusion list grows, and a scenario pins that behaviour so a future refactor cannot quietly sweep it in.

**Ownership gets a `command` kind rather than reusing `agent`.** The `agent` kind falls back to grepping generated provenance, which a command file does not carry. A distinct kind keeps the evidence honest: symlink resolving inside the repository, or a byte-identical copy.

## Risks

- **Wrapper rot.** A new agent without a matching wrapper is invisible to the namespace. Mitigated by the 1:1 requirement and a verification step that diffs the wrapper set against the agent set; the failure is a missing convenience, never a broken agent.
- **`$ARGUMENTS` semantics differ per harness.** omp supports `$ARGUMENTS`, `$@`, and positionals; Claude Code supports `$ARGUMENTS`. Only `$ARGUMENTS` is used, which both honour.
- **Primary agents may not be dispatchable as subagents in every harness.** The two orchestrator wrappers say so and name the fallback (switch the session agent) rather than assuming.
- **A user's own `~/.claude/commands/acordia/` directory.** Ownership evidence applies per file, so a foreign file of the same name aborts the install rather than being replaced, exactly as for agents and skills.
- **Colon-prefixed names and built-in reservation.** omp filters extension command names whose prefix parses as a built-in (e.g. `model:foo`). `acordia` is not a built-in command name, so the alias survives; a future built-in by that name would shadow it, which is a rename away from fixed.
