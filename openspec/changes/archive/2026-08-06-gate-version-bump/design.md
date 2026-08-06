## Context

See proposal.md — Why. The constraint that shapes everything here is that version-bump enforcement is inherently history-aware: unlike frontmatter validity, "was this bumped?" cannot be answered from the working tree alone. Some git comparison is unavoidable, and the design question is only which one.

The generator currently knows nothing about git. `check()` builds to a tempdir and diffs file bytes; `main()` catches `TranslationError`. Adding history-awareness is therefore a genuine new dependency on the environment, not a refactor — which is why the degradation path matters as much as the check.

## Goals / Non-Goals

**Goals:**

- The `cc7339a` mistake — a source edit committed with no bump — fails a gate the author already runs.
- One bump per release, not one per commit; the gate must not nag a branch that has already bumped.
- Absence of evidence never fails. A tree with no git, no remote, or no base branch is not a violation.

**Non-Goals:**

- Enforcing *which* level moved. MINOR-versus-MAJOR is the judgement `plugin-packaging` assigns to the author (roster and distribution-shape changes are MAJOR), and it is not mechanically derivable from a file diff. The gate checks that the version increased, not that it increased correctly.
- Blocking the commit itself. That needs a hook, which the repository has ruled out; the gate lives where the existing discipline lives.
- Bumping the version automatically. A derived version is explicitly rejected by `plugin-packaging`, and auto-bumping would reintroduce it by the back door.

## Decisions

**The base is the merge base with the integration branch, not `HEAD`.** This is the load-bearing decision. Comparing against `HEAD` implements "bump on every commit": a branch that correctly bumps once and then edits a second skill would fail, and the author's only remedy is a second bump — producing a version per commit and a changelog nobody wants. Comparing against the merge base implements "bump once per release," which is what the version actually means, since users see one version per install. Base resolution tries `origin/develop`, `origin/main`, `develop`, `main` in order, matching the repository's actual branch layout (`develop` is the integration branch; `origin/HEAD` points at `main`).

**Skip, never fail, when the base cannot be resolved.** A shallow clone, a marketplace clone with no remotes, a CI-less fresh checkout, or a detached state must not produce a spurious failure — a false positive here blocks the only pre-commit gate the project has, which would train the author to stop running it. The asymmetry is deliberate: a missed bump is a silent no-op the next release corrects, while a wedged `--check` costs trust in every gate it carries, including the frontmatter one.

**The gate runs in `--check` only.** A plain build runs constantly during authoring, often before any bump decision is sensible. Failing it would make the generator unusable for its primary purpose and would push authors toward editing `plugins/` by hand, which is the drift bug `plugin-packaging` most wants to prevent. `--check` is already the pre-commit gate, so this is where the obligation belongs.

**Source scope is the three paths `CLAUDE.md` already names**: `analysts/`, `operators/`, `commands/acordia/`. Not `tools/`, because changing the generator without changing its output reaches no user, and requiring a bump for a comment edit would be noise; when a generator change does alter emitted bytes, `--check`'s existing drift comparison catches it independently. Not `docs/` or `openspec/`, which reach no installed user at all.

**Versions compare as integer tuples, not strings.** `"2.10.0" > "2.9.0"` is false lexicographically and true numerically, and the library is already past `2.2.0`. Parsing is a strict `MAJOR.MINOR.PATCH` split; anything that fails to parse is treated as a skip rather than a failure, consistent with the degradation stance, since `plugin-packaging` separately forbids non-semver forms and the frontmatter of that rule is not this gate's job.

**Git is invoked through `subprocess` with an explicit argument list and a repo-root `cwd`.** No shell string interpolation, so a branch name can never be interpreted. Failures are caught as `subprocess.CalledProcessError`/`OSError` and routed to the skip path rather than raising.

## Risks / Trade-offs

**The gate is skipped exactly when it would have caught something — a fresh clone with no remote.** → Accepted deliberately. The alternative is failing builds in environments that have no way to satisfy the check. The gate targets the authoring loop, which always has a base.

**One bump per branch means a long-lived branch ships many changes under one MINOR.** → Correct by the version's own semantics: it signals "something changed, reinstall," not "how much changed." `plugin-packaging` already treats it as an update signal rather than a changelog.

**An author can satisfy the gate with a PATCH bump where MINOR was required.** → Out of scope by design; the gate proves movement, not correctness of level. Stated as a Non-Goal rather than silently implied.

**New environmental dependency in a previously hermetic script.** → Confined to one function that cannot raise: every git failure resolves to a skip, so the generator remains runnable anywhere it ran before.

## Migration Plan

None. The gate reads git and emits no artifact, so there is nothing to migrate and nothing to roll back beyond reverting the commit. The change is inert on any tree whose sources match the base.
