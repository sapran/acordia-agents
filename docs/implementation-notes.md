# Implementation notes

Out-of-scope findings recorded during work on other changes. Nothing here has been acted on.

## Dev-tooling skills leak into the global install

Found while adding the omp harness target (`omp-harness-target`, 2026-07).

`install.sh` treats every top-level directory carrying an `agents/` or `skills/` subdirectory as a deployable pillar. That includes `.opencode/` and `.claude/`, which hold this repository's own OpenSpec workflow skills — `openspec-apply-change`, `openspec-archive-change`, `openspec-explore`, `openspec-propose`, `openspec-sync-specs`. Those five are development tooling for maintaining this repo, not ACORDIA distribution artifacts, yet a plain `./install.sh` deploys them into `~/.config/opencode/skills/` (and now, with `--harness omp`, into `~/.omp/agent/skills/` as well), where they appear in every unrelated project's session.

The behaviour predates the omp work: the original `install.sh` excluded only `.git` and `.github`. Adding the omp target doubles the blast radius rather than creating it.

Possible fix: exclude dot-directories from pillar auto-discovery, so a pillar must be a visible top-level directory. That matches how `README.md` describes the layout. It is a behaviour change for existing opencode installs, so it wants its own change rather than a drive-by edit.

## `todo` does not appear in a translated agent's tool inventory

Found in the same work.

`tools/translate-omp.py` puts `todo` in the generated allowlist, but a running translated leg agent reported a tool inventory of `read`, `grep`, `glob`, `bash`, `web_search`, `yield`, `hub`, `write` — no `todo`. The other allowlisted names all appeared, and `edit`/`task` were correctly absent, so the allowlist is being honoured; why `todo` specifically does not materialise was not established. Harmless either way: an analyst agent has no use for a task tracker. Worth resolving if the allowlist is ever relied on as an exact description of the runtime tool set.
