## Context

One question drove this change: what does a user do when the marketplace install reports success and delivers nothing. The answer had to satisfy three constraints at once — it must not depend on the provider that is switched off, it must not touch the user's configuration, and it must not fork the authored tree. What follows is the set of decisions that fell out of those constraints, and the alternatives each one rejected.

The measurements behind the constraints are in the proposal. The two that shape every decision below: the native roots are gated by no discovery provider (discovery inputs 1 and 2), and no packaging of the pillar reaches the agents through any other surface — `extensions:` with or without a `package.json`, and a registered `omp plugin link` plugin, all load the skills and drop the agents, and only CLI `omp -e` does not.

## Symlinks, not copies

The install links each agent file and each skill directory rather than copying them. Two reasons.

A copy needs an upgrade path, and this route has no version signal. The marketplace route has one — the catalog version is what a harness compares to decide whether to reinstall — but a script that copied files into a user's agent directory would have nothing to compare and no way to know it was stale. It would need a manifest, a recorded version, a diff, and a reinstall command, which is a package manager written badly. A symlink has no staleness: `git pull` in the checkout changes what omp serves on the next start, with no second step.

A copy also forks the authored tree, which is the thing `plugin-distribution` exists to prevent. Its first requirement is one authored directory serving every harness with no generated or translated copy of any agent, skill or command. A copy under `~/.omp/agent/` would be exactly such a second tree, differing from the source the moment either moves. A symlink is a pointer to the authored file; there is still one tree.

The cost is that a deleted or moved checkout leaves dangling links. That is real, and it is why the uninstaller is written the way it is below.

## The native roots, not a configuration edit

The `extensions:` setting was the obvious candidate and it is measurably wrong: with `claude-plugins` disabled, a user `extensions:` entry loads the pillar's skills and does not load its agents, with or without a `package.json` in the directory. So the setting cannot deliver the thing the user is missing.

Even if it worked, a script that edits a user's `config.yml` is a worse citizen than one that does not. It has to parse YAML it did not write, preserve comments it does not understand, decide what to do about an existing `extensions:` array, and reverse all of that on uninstall. Failure modes there damage a file that governs every session, not just this pillar. The native roots need none of it: `mkdir -p`, `ln -s`, and nothing outside those two directories is read or written. Uninstall is a matched `rm` of links the installer made.

The `omp -e <absolute path>` flag does serve agents from such a root, and was rejected as the primary route for a different reason: it is per-invocation. It makes the pillar available to a session that remembered to pass the flag, which is a standing instruction to the user rather than an install.

## No `package.json` is added to the pillar

Adding one would be the natural packaging fix and it buys nothing, measured. A directory carrying a `package.json` behaves identically to a bare one under `extensions:` — skills load, agents do not — and a properly registered `omp plugin link` npm plugin behaves the same way, while reporting perfect health: `npm Plugins: ● acordia-analysts@5.0.0`, `enabled: true` in the lockfile, symlinked into `~/.omp/plugins/node_modules/`. The failure is in omp's agent discovery, which contradicts its own documented input 3, not in how the pillar is packaged. Adding a manifest to work around a harness bug would leave a permanent artefact in the tree that stops being necessary the day the bug is fixed and never announces that it has.

## The collision preflight aborts the whole run

The installer refuses to proceed when any single target already exists and is not one of our own symlinks. It prints every collision and changes nothing — not the colliding entry, and not the 49 entries that would have been fine.

Skipping the collision and linking the rest was considered and rejected. A collision on `cyber-analyst.md` means the user already has an agent by that name, and the interesting question is which one omp will dispatch. A partial install answers it by accident: the user's own file survives, our other four agents install, and the roster is now a silent mixture of two sources that nobody chose. Worse, the failure is reported as a warning in the middle of a success message, which is the shape of message people scroll past. Aborting makes the user resolve the name clash deliberately — rename theirs, or point `--agent-dir` somewhere else — before anything is in place.

The all-or-nothing property is also what makes the script safe to run speculatively, which matters for a script whose whole purpose is to be tried by a user who has just discovered their install was inert. Verified: a single planted real `cyber-analyst.md` aborted the run and left all 45 skills unlinked.

An entry that *is* one of our own symlinks is not a collision, which is what makes a re-run idempotent.

## Uninstall matches the recorded target, not a manifest

The uninstaller removes a symlink when its `readlink` target contains `/acordia-analysts/agents/` or `/acordia-analysts/skills/`. It does not read a manifest and it does not compare against the current checkout's contents.

A manifest file was rejected: it is state that can disagree with the filesystem. If the user removes one link by hand the manifest is now wrong, and the uninstaller either refuses or deletes something it should not. The symlink itself is the record — self-describing, and impossible to desynchronise from what is actually installed.

Matching against the current checkout's contents was rejected for a sharper reason: it fails in the case that most needs to work. A user who deleted or renamed the checkout has no way to remove the links from it — every match would come back empty, and the links would stay in the roots forever, dangling and unowned. A `readlink` on a dangling symlink still returns its recorded target, so matching on the target cleans exactly that case. Verified: with 50 ACORDIA links plus a planted real `mine.md` and a planted foreign symlink `decoy` present, the run reported `Removed 50 ACORDIA links` and `Left 2 entries that are not ours`, and both planted entries survived.

The two roots are removed only when the script emptied them itself, because a directory the user populated is theirs. Both scripts also tell the user to restart omp: a running session holds the roster it started with, so a successful install that appears to have done nothing is the predictable next confusion.

## Command wrappers are out of scope

A wrapper's invocation name comes from the plugin namespace, so `/acordia-analysts:analyst` exists because a plugin root supplied that prefix. There is no namespace in a native root to give it one, and inventing a flat `/analyst` would collide with whatever the user has and would differ from the name the same wrapper has under the marketplace route — two names for one artefact, depending on how it was installed. The scripts therefore install agents and skills only, and say so in their own output rather than leaving the user to notice.

This is a genuine reduction against the marketplace route, and it is the honest one: the wrappers are convenience over `@agent-name` dispatch, which works from a native root.

## The shadowing consequence, accepted

omp's native roots dedup first-wins by exact agent name and resolve before plugin roots. A user who runs the installer while a marketplace install is live therefore gets the native copies of all five agents, silently, with the plugin's copies shadowed and no notice that it happened.

This is accepted rather than guarded. Detecting it would mean reading the plugin registries the script deliberately does not touch, and the harm is bounded: both sides point at authored files from this distribution, so the practical difference is which checkout wins, not whether the user gets ACORDIA. Attempting to detect and warn would couple the script to the exact registry files whose provider gating is the reason it exists. It is documented in the requirement, in `README.md` and in the script header, which is the correct place for a cost you have decided to pay.

## Why reintroducing a shell script is not a reversal

3.0.0 deleted this distribution's shell installer on purpose, along with the generator that expressed opencode's permission maps, and `openspec/config.yaml` still records "no shell installer" as a property of the design. Adding two scripts needs to answer that.

The deleted installer and these scripts are different objects. That one was the **only** route in for its harness: it deployed the whole tree, it was what a user had to run, and every user of that harness depended on a shell script executing correctly for the distribution to exist at all. It also carried the generator's output, which is what made it a fork of the authored tree rather than a pointer to it. These scripts are an **alternative** route for one gated case. The marketplace route remains the documented default and is unchanged. They deploy nothing the marketplace route does not deploy — the same five agent files and the same 45 skill directories, by reference rather than by copy — they generate nothing, and they edit no configuration. A user who never hits the `claude-plugins` gate never runs them and loses nothing by their existence.

The property 3.0.0 was protecting was *one authored tree, no generated copy, no build step between checkout and install*. All three still hold. What 3.0.0 removed was a script that was load-bearing; what this adds is a script that is optional.

## Deferred deliberately

**A Claude Code equivalent is not written.** Claude Code has native `~/.claude/agents/` and `~/.claude/skills/` roots and the same symlink approach would very likely work there, but nothing here has measured it, and the failure this change exists to fix is specific to omp's provider gating. Writing an unmeasured second script would ship exactly the kind of claim this repository's verification discipline is meant to stop. The scripts are named `install-omp.sh` and `uninstall-omp.sh` so that a future harness gets its own pair rather than a flag on these.

**The omp discovery bug is not worked around further.** The right fix for input 3 dropping agents from `extensions:` and from linked npm plugins is upstream in omp. This change routes around it at the one surface that works; it does not attempt to make the broken surfaces work.
