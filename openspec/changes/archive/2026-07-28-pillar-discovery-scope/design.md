## Context

Pillar auto-discovery has always been a `find -maxdepth 1 -type d` sweep with a hand-written exclusion list. It began as `! -name '.git' ! -name '.github'`, gained `! -name '.build'` with the omp harness, and gained a `[[ -d "$dir/agents" || -d "$dir/skills" ]]` guard at the same time to stop the new `tools/` directory being treated as a pillar.

That guard fixed the symptom it was aimed at and left the real one: `.opencode/` and `.claude/` both carry a `skills/` subdirectory, so they still qualify. Their contents are the OpenSpec workflow skills this repository uses on itself — the very skills driving this change — and a plain `./install.sh` publishes them to the user's global config alongside the analyst library.

## Goals / Non-Goals

**Goals:**

- A default install publishes ACORDIA artifacts and nothing else.
- The rule is legible: someone reading `install.sh` should be able to say what a pillar is without tracing an exclusion list.
- Deliberate deployment of a dot-directory stays possible.

**Non-Goals:**

- Moving or renaming `.opencode/` and `.claude/`. They are where their respective tools look for them.
- A manifest listing pillars explicitly. Convention-over-configuration is working; the convention just needs stating correctly.
- Cleaning already-published skills out of users' config directories from inside `install.sh`. `uninstall.sh --pillar .opencode` already does that, and an installer that deletes things it no longer recognises is a worse failure mode than a stale skill.

## Decisions

**A pillar is a visible top-level directory carrying `agents/` or `skills/`.**
The dot-prefix is doing real work here: every directory in this repository that is *tooling configuration* rather than *distributable content* is dot-prefixed — `.git`, `.github`, `.build`, `.opencode`, `.claude`, `.codex`, `.remember`. That is not a coincidence to be exploited, it is the existing convention of the repository, and encoding it collapses the growing exclusion list into one predicate. `.git`, `.github`, and `.build` no longer need naming individually, though the guard for a directory that carries neither `agents/` nor `skills/` stays, since `docs/`, `openspec/`, and `tools/` are all visible.

The alternative — extending the exclusion list with `.opencode` and `.claude` — was rejected. It is the third patch to the same list, it would need a fourth when `.codex/skills` appears (that directory already exists in the repository and would qualify the moment it gains skills), and it states what a pillar is *not* rather than what it is.

**`--pillar` bypasses the filter entirely.**
Auto-discovery is a default, not a policy. `./install.sh --pillar .opencode` still works, because the explicit list has never gone through the `find` sweep. This keeps the change purely subtractive on the default path and means the fix does not remove a capability, only an accident.

## Risks / Trade-offs

**Someone came to rely on the leaked OpenSpec skills.** → Marked BREAKING in the proposal. The remedy is one command (`./uninstall.sh --pillar .opencode`), and the skills remain installable on purpose with `--pillar`. A user who wants them globally is better served by installing them from their own source than by a side effect of this repository's install script.

**A future pillar authored as a dot-directory would be silently skipped.** → Acceptable and arguably correct: it would violate the repository's own layout convention, and `README.md` documents pillars as visible directories. The failure is also loud in practice — the install prints its per-pillar headers, so a missing pillar is visible in the output.

## Migration Plan

Subtractive and immediate. Existing installs keep the five skills until the user runs `./uninstall.sh --pillar .opencode` (add `--harness omp` or `--harness both` to reach the omp copy). Rollback is reverting one predicate in each script.
