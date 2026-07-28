## Context

Two harnesses now matter for this repo. opencode is the original target; omp (`oh-my-pi`, currently 17.1.8) is the second. They agree on skills and disagree on agents.

**Skills already work in omp, unchanged.** omp registers an `opencode` skill provider at priority 55 that scans `~/.config/opencode/skills` with the same non-recursive `<name>/SKILL.md` layout `install.sh` already produces. Verified: all 47 skill directories symlinked by `install.sh` are present in a live omp session's skill list. Nothing about the skill half needs translating.

**Agents do not.** omp discovers task agents from `<project>/.omp/agents`, `~/.omp/agent/agents`, and Claude plugin `agents/` directories, and it explicitly filters out `.claude/agents`, `.codex/agents`, and `.gemini/agents` on the grounds that their frontmatter is not the omp task-agent contract. `~/.config/opencode/agents` is not scanned at all. The four analyst files are therefore invisible.

The two frontmatter contracts differ in kind, not just in spelling:

| Concern | opencode | omp |
|---|---|---|
| Agent name | filename stem | required `name:` field; a file missing `name` or `description` is skipped with a warning |
| Role | `mode: primary` / `mode: subagent` | no modes; every file-defined agent is a subagent reached through the `task` tool |
| Tool access | `permission:` map of allow/deny, deny-by-exception | `tools:` allowlist; absent tools are simply not present |
| Path-scoped writes | supported (`".acordia/reports/**": allow`) | not supported; allowlisting is per tool, never per path |
| Delegation | `permission.task` map naming allowed agents | `tools` must include `task`, and `spawns:` names the allowed agents |
| Skill binding | none — prompts name their skills in prose | `autoloadSkills:` injects named skill bodies at subagent start |

omp also has no `list` tool; a directory path handed to `read` lists it. The analyst prompts' shared "Tool discipline" paragraph names `list` explicitly, so the paragraph is wrong under omp.

## Goals / Non-Goals

**Goals:**

- An omp operator runs one command and gets the four analysts as dispatchable task agents plus the skill library.
- The opencode agent files under `analysts/` remain the single source of truth for both harnesses.
- The read-only posture survives translation, to the same degree it held in opencode.
- Existing `./install.sh` behaviour is unchanged for anyone who does not pass the new flag.

**Non-Goals:**

- Hand-maintained omp copies of the four prompts. A second editable copy of a prompt is exactly the source-of-truth drift the repo's compile contract exists to prevent.
- Closing parity gaps that the omp permission model cannot express (see Risks).
- Making `operational-analyst` the omp session's own persona. That is a `SYSTEM.md` concern, deliberately deferred (see Decisions).
- Translating future pillars. The translator is generic over `<pillar>/agents/*.md`, but only `analysts/` exists.

## Decisions

**Translate at install time into gitignored build output, not into committed files.**
The alternative — a committed `omp/` pillar mirroring `analysts/` — was rejected. It doubles the prompt corpus, and the repo's own doctrine ("Editing the artifacts under `analysts/` without touching the map is a source-of-truth drift bug") would then need a second clause about editing the omp mirror. Build output under `.build/omp/` cannot drift because it is regenerated on every install and is never read by a reviewer.

A consequence: the omp harness cannot use symlink mode. A symlink would point at a build artifact that the next `--dry-run` could invalidate. The omp harness therefore always materialises copies, and `--link` is ignored for it with a notice. Skills, which are not translated, still honour `--link`.

**`operational-analyst` becomes a spawnable orchestrator, not a session persona.**
Two options existed for `mode: primary`. Making it the session itself requires `~/.omp/agent/SYSTEM.md`, which replaces prompt block 0 — and block 0 is where omp injects the discovered-skills list. An operational-analyst session installed that way would lose automatic visibility of the 47 skills it is built to draw on, and would have to hard-code the list, reintroducing drift. `APPEND_SYSTEM.md` avoids the block-0 problem but layers the analyst on top of a coding-agent prompt rather than replacing it, and is global to every omp session in every project.

The spawnable form has none of those problems: the agent keeps its own prompt, inherits the skills list like any subagent, and is dispatched explicitly when wanted. Its `tools` include `task` and its `spawns` names exactly the three legs — a faithful rendering of the opencode `permission.task` map, and the one mapping where omp is actually more precise than opencode, since `spawns` is a positive allowlist rather than a deny-with-exceptions map.

**`permission` maps onto a fixed tools allowlist, derived rather than configured.**
Every analyst gets `read, grep, glob, bash, web_search, todo, yield`; the orchestrator additionally gets `task`. `edit` and `write` are absent, which is the translation of `edit: deny` — and which omp honours for `edit` but not for `write` (see the next decision). `yield` is appended by omp automatically when `tools` is present, but naming it explicitly keeps the generated file honest about what the agent declares.

**The write permission cannot be translated at all, so it is reported instead.**
This decision was rewritten after testing. The original plan was to drop `write` by default and offer a `--reports` opt-in to restore it. Testing the installed agents showed the premise was false: a translated leg agent whose allowlist omits `write` still had a working `write` tool and successfully created a scratch file. omp's `XDEV_TRANSPORT_TOOLS` are `read` and `write` — the channel every `xd://` device is driven through — so both are present whenever `tools.xdev` is on, which is the default. The same agent correctly had no `edit` and no `task`, so the allowlist is enforced in general; `write` is the single exception.

A `--reports` flag would therefore have had no observable effect under stock settings — a control that lies about what it controls is worse than no control. It was removed. The translator emits the narrow allowlist regardless, and stamps `metadata.generated.write_access` with what the harness actually enforces, so the posture is legible from the installed file rather than assumed from the frontmatter.

**`autoloadSkills` is available but off by default.**
omp can inject full skill bodies at subagent start, and the prompts' `(deep)` skill lists are exactly the right input. But the orchestrator's spine is 12 skills and the legs' depth lists run to 12 more; injecting all of them front-loads a large amount of context the agent may never need, and it changes behaviour relative to opencode, where the same names are prose the agent acts on by reading `skill://`. Default off preserves cross-harness behavioural parity. `--autoload deep` turns it on for operators who prefer the front-loaded shape.

**One prompt paragraph is rewritten, by exact-string match on all four files.**
The "Tool discipline" paragraph is byte-identical across the four agents. The translator matches it literally and substitutes an omp-correct version; a file in which the paragraph is not found is a translation failure, not a silent pass-through, because a silent pass-through would ship a prompt telling the agent to use a tool that does not exist.

**`pyyaml` via a PEP 723 inline dependency.**
The frontmatter is nested YAML — `permission.edit` is a map in one file and a scalar in three. A line-oriented bash or `sed` parser would have to special-case that, and would break on the next agent that nests differently. `uv run --script` resolves `pyyaml` into an isolated per-script environment; nothing is installed into any system or project interpreter.

## Risks / Trade-offs

**`bash` remains a write channel.** → Not a regression: `bash: allow` in the opencode files has exactly the same hole. The read-only guarantee in both harnesses is "the agent has no file-editing tool", not "the agent cannot write". Documented in README rather than mitigated, because removing `bash` would gut the analytic-tooling and exhaustive-data-processing skills that the whole library leans on.

**The read-only posture is genuinely weaker in omp.** → Not fully mitigable. `edit` and `task` denial hold; write denial does not. The response is disclosure in three places — README parity gaps, workbook §7.3, and per-file generated metadata — plus the escape hatch for operators who need enforcement: disabling `tools.xdev` restores full allowlist behaviour at the cost of moving every discoverable tool back into the top-level schema.

**Translation drifts if a prompt's structure changes.** → Mitigated by failing loudly: a missing `name`-able filename, an unrecognised `mode`, or an unmatched Tool-discipline paragraph aborts that file's translation with a non-zero exit rather than emitting a subtly wrong agent.

**Name collisions in `~/.omp/agent/agents/`.** → The four analyst names do not collide with omp's bundled agents (`task`, `sonic`, `scout`, `designer`, `reviewer`, `librarian`). Discovery is first-wins by exact name with user agents ahead of bundled, so a future collision would silently shadow a bundled agent. `uninstall.sh` only removes files this repo deployed, tracked by name, so it cannot delete an unrelated agent.

**Two copies of the skill library on disk for a both-harness install.** → Harmless: omp de-duplicates skills by `realpath` before it de-duplicates by name, and both copies are symlinks to the same source directories.

## Migration Plan

Additive. `./install.sh` with no arguments behaves exactly as before. Rollback for the omp side is `./uninstall.sh --harness omp`, which removes the four agent files and the skill symlinks under `~/.omp/agent/` and touches nothing else.

## Open Questions

None blocking. Whether to ship a `SYSTEM.md` variant of the orchestrator for operators who want an analyst-first omp session is deferred until someone asks for it; the spawnable form covers the dispatch case, which is the one the role model describes.
