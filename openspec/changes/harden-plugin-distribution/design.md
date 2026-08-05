## Context

Three defects in a freshly archived change, all the same family: a normative claim with nothing behind it. The version was declared and not derivable; the Claude posture was declared and not tested; the dispatch form was documented and wrong.

## Goals / Non-Goals

**Goals.** Make the version shippable. Verify the posture against a live harness. Correct the documentation to what was observed.

**Non-Goals.** No CI, no hooks, no lint automation — this repository is markdown plus one generator, and it has deliberately had no build pipeline. No change to any agent prompt, skill, or wrapper body. No attempt to give Claude Code an upgrade mechanism it may not have.

## Decisions

### Version: content hash, non-semver, epoch by hand

Four candidates. Three fail:

- **`git describe` / commit SHA.** Fatal fixpoint. The version lands in 6 committed files; committing the rebuild changes HEAD; a rebuild then embeds the new HEAD; `--check` never passes.
- **Git SHA scoped to source paths** converges, since the rebuild commit touches only `plugins/`. But it embeds a stale SHA when sources are edited and uncommitted, and breaks in a shallow clone or an export.
- **`1.0.0+<hash>`.** Valid semver, lint-clean, and it *never upgrades* — build metadata is excluded from precedence. Strictly worse than the frozen `1.0.0` it would replace, because it looks like it works.

Content hashing has no fixpoint (the output carries the hash, the inputs do not), needs no git, is correct in a dirty tree, and is deterministic given sorted traversal.

The hash covers the generator as well as the sources. Without that, a change to emitted output — a new provenance comment, a reordered key — would ship to nobody, which is the original defect in a narrower form. A pure refactor of the generator therefore bumps the version; that is the right trade, since the generator's output *is* the product.

The epoch stays human because a hash conveys nothing to a person reading `plugin details`. Nothing forces the bump; accepted, since automating it would mean inventing semantics for what counts as a roster change.

**A simpler option exists and was weighed:** a hand-edited version string, bumped when you remember. Proportionate to a markdown repo, and it survives on the same argument that killed the CI. It lost on one point only — the failure mode is silent. A forgotten bump means users keep running old prompts with no signal, which is the exact defect being fixed, reintroduced as a habit. Deriving it costs ~20 lines in a script that is already the single source of plugin identity, and the epoch keeps the human-readable half a person can still bump on purpose.

### Only shipped files feed the hash

The first implementation walked every file under the version inputs. A gitignored `.DS_Store` inside `analysts/` was present locally and absent from a clone — 101 files against 100 — so the version depended on whose checkout built it, and a fresh clone disagreed with the committed tree. Paths with a dot-prefixed component or a `__pycache__` segment are now skipped. Verified by building in a clean clone and comparing the hash.

### Evidence for the non-semver choice, and a trap in gathering it

Established empirically, and the first attempt was **wrong in a way worth recording**. Using `omp plugin upgrade <name>@<marketplace>` with an explicit target, every transition appeared to upgrade — including identical versions and downgrades. That command reinstalls unconditionally and compares nothing. Controls (equal version, older semver) exposed it. The comparing path is bare `omp plugin upgrade`, exactly as `omp://marketplace.md` states: "Upgrading all plugins compares only catalog entries that declare `version`."

Re-run properly against omp 17.1.8:

| transition | result |
| --- | --- |
| equal → equal | skip |
| `1.0-abc1234` → `1.0-def5678` | **upgrade** |
| `1.0.0+aaa` → `1.0.0+bbb` | **skip** |
| non-semver → `1.0.0` | skip |
| `2.0.0` → `1.5.0` | skip |

Hash-to-hash propagates in either direction, so hex ordering is irrelevant. The build-metadata form does not propagate at all.

### Migration is uninstall-then-install

The retired `--harness omp` path left translated agents under `~/.omp/agent/agents/`, which omp resolves before plugin roots and dedups first-wins, so they shadow the plugin silently. A script was written for this and then deleted: removing a directory is not worth 140 lines of provenance checking in a prose repository. It is documented as a step in `README.md` instead.

## Risks / Trade-offs

- **Every source edit now dirties 6 generated files.** Inherent to embedding a content version in committed output.
- **The epoch can rot.** Human-kept by choice.
- **`--check` is still run by hand.** No automation enforces it, deliberately. Drift is caught by whoever next runs the generator.
- **Claude upgrade propagation is unresolved.** Documented as unverified rather than assumed. If Claude Code turns out to need semver ordering, the version has to diverge per harness — non-semver in the omp catalog, semver in the Claude tree — which would break the "two catalogs differ only in `source`" property and need its own change.

## Open Questions

Whether Claude Code auto-upgrades marketplace plugins at all. Testable once this branch is the default branch; until then `README.md` states the limit rather than guessing.
