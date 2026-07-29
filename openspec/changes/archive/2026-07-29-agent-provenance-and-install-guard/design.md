## Context

`install.sh` deploys into a namespace it does not own. Both harness roots are flat and shared: `~/.config/opencode/agent/` and `~/.omp/agent/agents/` for agents, `.../skill{,s}/<slug>/` for skills. omp ships its own agents there (`task`, `scout`, `reviewer`, `designer`, `sonic`, `librarian`), and a user may have unrelated agents or skills of their own. `deploy_file` and `deploy_dir` begin by removing whatever is at the destination — `rm -f` for a file, `rm -rf` for a skill directory — with no test of what that thing is. A future pillar naming an agent `task`, or a skill slug that already exists elsewhere, therefore destroys it silently.

`uninstall.sh` already solved the mirror-image problem correctly: `owned_by_repo` requires evidence (a symlink resolving inside the repo, a byte-identical copy, or a translated agent carrying `from: <source>` provenance) before removing anything, and reports what it left alone. Install simply never got the same treatment.

Separately, the roster a harness renders is slug plus `description`. Nothing marks an agent as coming from this distribution, and the generic operator names (`operator`, `web-application`, `cloud-security`, `internal-network`, `mobile-application`) are the ones most likely to be mistaken for a harness built-in.

## Goals / Non-Goals

**Goals:**

- No install run can destroy an artifact this repository did not deploy.
- One definition of "owned by this repository", shared by install and uninstall.
- The pillar an agent belongs to is visible wherever a harness shows the roster.
- Nothing about dispatch changes: agent names, filenames, `task:` whitelists, skill slugs and permission blocks are all untouched.

**Non-Goals:**

- Renaming any agent or skill. Prefixing names is rejected below.
- A manifest or any other new state under the harness root.
- Collision detection between the two pillars of this repo (their names are disjoint and both are owned).
- Path-scoped permissions, autoload behaviour, or anything else in the translation contract.

## Decisions

**Reuse `owned_by_repo` rather than write a manifest.** A manifest under the harness root would be new state to keep in sync, would be wrong the moment a user moved or edited a file, and would give install a different notion of ownership than uninstall. The existing predicate needs no new state: it reads the destination and compares it to the source. Extract it verbatim into `tools/ownership.sh`, which both scripts source; each keeps its own `REPO_ROOT`, which the function already reads from the environment.

One case needs care. On re-install the destination is the *previous* deployment, so it must test as owned: a symlink resolves into the repo, a copied artifact is byte-identical, and a translated omp agent carries its `from:` provenance line. Idempotence is therefore preserved for every mode. The one case that would otherwise fail is a translated agent whose source changed since the last install — the copy is neither a symlink nor byte-identical, but its `from:` line still names the source, so the provenance branch accepts it. That is why the predicate must be reused rather than reduced to a byte comparison.

**Refuse, do not skip.** An unowned collision is a configuration problem the user must see, so `install.sh` exits non-zero naming the path, rather than warning and continuing. `--force` restores the old unconditional behaviour for the user who genuinely wants to replace a foreign artifact.

**Check every destination before writing any of them.** Gating the removal inside `deploy_file`/`deploy_dir` was the obvious placement and was wrong: it refuses only when the iteration reaches the collision, having already deployed every artifact that sorts before it — a half-deployed pillar whose orchestrator references legs that never arrived. The check is therefore a `preflight()` pass over all harnesses and pillars, run before the deploy loop, and `deploy_file`/`deploy_dir` stay as they were. That also keeps `--force` accounting single-pass.

**Check in dry-run too.** The existing requirement is that a clean dry run predicts a clean install. The guard must therefore run under `--dry-run` — it only reads the filesystem, so this costs nothing — and a collision must make the dry run exit non-zero.

**Tag the `description`, do not prefix the name.** The name is the dispatch handle: prefixing it would touch the `task:` whitelists in both orchestrators, the roster requirements in two specs, `docs/roles/*`, and the README tree, for no isolation gain. The `description` is rendered next to the name by both harnesses and is free to carry provenance. Chosen form is a leading `ACORDIA Analysis — ` / `ACORDIA Operations — ` tag, em-dash separated, with the existing routing sentence following unchanged, so the requirement that a description *conveys* its leg question or domain still holds verbatim.

**Skills keep bare slugs.** Rejected prefixing all 72 skill slugs. Skill selection is by `description` match, so a name prefix isolates nothing; the cost is the normative slug/`name` bijection in `analyst-skill-library` and `operator-skill-library`, the `·`-separated skill lines that `tools/translate-omp.py --autoload deep` parses out of the operator prompts, and a longer skill list injected into every prompt. Skill descriptions are also left alone: the description *is* the trigger, and diluting its opening words would degrade selection. The operator library already namespaces itself in practice via `attack-*` and `wstg-*`.

## Risks / Trade-offs

- [A user with a hand-edited copy of one of our agents is now blocked from installing] → The error names the path and points at `--force`; the edited file is theirs to keep or discard, and silently overwriting it is exactly the data loss this change exists to prevent.
- [Sourcing a shared shell file couples `tools/` to the two scripts] → `tools/` already holds `translate-omp.py`, which `install.sh` invokes; pillar auto-discovery ignores `tools/` because it is not a pillar directory, so nothing is deployed by accident.
- [The provenance tag lengthens every agent description] → Nine lines, a fixed ~22-character prefix, against descriptions that already carry 200+ characters of routing signal.
- [A future pillar could still collide with *this* repo's own names] → Out of scope and not currently possible; the two pillars' agent and skill names are disjoint.

## Migration Plan

No migration. An existing deployment tests as owned, so the first `./install.sh` after this change behaves as before, then rewrites the nine agent files with their tagged descriptions. Rollback is reverting the commit and re-running install.
