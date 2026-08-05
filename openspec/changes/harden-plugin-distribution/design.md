## Context

Four defects in a freshly archived change, all of the same family: a normative claim with nothing behind it. The gate was declared and not run; the version was declared and not derivable; the Claude posture was declared and not tested; the retired deployment was removed from the installer and not from users' machines.

## Goals / Non-Goals

**Goals.** Make each declared property actually hold, and verify the ones that were only asserted.

**Non-Goals.** No change to any agent prompt, skill, or wrapper body. No attempt to give Claude Code an upgrade mechanism it may not have.

## Decisions

### Version: content hash, non-semver, epoch by hand

Four candidates were considered. Three fail:

- **`git describe` / commit SHA.** Fatal fixpoint. The version lands in 6 committed files; committing the rebuild changes HEAD; a rebuild then embeds the new HEAD; `--check` fails; committing that changes HEAD again. Never converges.
- **Git SHA scoped to source paths** (`git log -1 -- analysts operators commands`) converges, since the rebuild commit touches only `plugins/`. But it embeds a stale SHA when sources are edited and uncommitted, and breaks in a shallow clone or an export.
- **`1.0.0+<hash>`.** Valid semver and lint-clean, and it *never upgrades* — build metadata is excluded from precedence, so `+aaa` and `+bbb` compare equal. Strictly worse than the frozen `1.0.0` it would replace, because it looks like it works.

Content hashing wins on every axis: no fixpoint (output carries the hash, inputs do not), no git dependency, correct in a dirty tree, and deterministic given sorted traversal.

The hash covers the generator as well as the sources. Without that, a change to emitted output — a new provenance comment, a reordered key — would ship to nobody, which is the original finding in a narrower form. The cost is that a pure refactor of the generator bumps the version; that is the right trade, since the generator's output *is* the product.

The epoch stays human because a hash conveys nothing to a person reading `plugin details`. Nothing forces the bump; that is accepted, since automating it would require inventing semantics for what counts as a roster change.

### Evidence for the non-semver choice, and a trap in gathering it

The version semantics were established empirically, and the first attempt was **wrong in a way worth recording**. Using `omp plugin upgrade <name>@<marketplace>` with an explicit target, every version transition appeared to upgrade — including identical versions and *downgrades*. That command reinstalls unconditionally and compares nothing. Controls (equal version, older semver) exposed it. The comparing path is bare `omp plugin upgrade`, exactly as `omp://marketplace.md` states: "Upgrading all plugins compares only catalog entries that declare `version`."

Re-run properly against omp 17.1.8:

| transition | result |
| --- | --- |
| equal → equal | skip |
| `1.0-abc1234` → `1.0-def5678` | **upgrade** |
| `1.0.0+aaa` → `1.0.0+bbb` | **skip** |
| non-semver → `1.0.0` | skip |
| `2.0.0` → `1.5.0` | skip |

Hash-to-hash propagates in either direction, so hex ordering is irrelevant. The build-metadata form does not propagate at all.

### CI fails rather than auto-commits

Auto-committing a rebuild never blocks a contributor, but lands generated output unreviewed, needs a write-scoped token, and can race a human push. Failing keeps the generated diff inside the reviewed change, which matters precisely because a bad source edit surfaces as a large visible blast radius rather than a quiet bot commit.

### The migration needs its own evidence rule

`reframe-as-plugin` deleted the translated-agent branch from `tools/ownership.sh`, correctly: no opencode deployment is ever a translated file. But the artifacts this migration removes *are* translated files — they never matched their source by construction — so the shared rule would refuse to recognise a single one of them.

`tools/migrate-omp.sh` therefore carries the retired rule, and both halves must hold: `by: tools/translate-omp.py` **and** a `from:` path that resolves to a real file in this repository. The old tool name is the migration's fingerprint, which is the one place its continued existence is useful. Skills are byte-identical and use the shared rule unchanged.

## Risks / Trade-offs

- **Every source edit now dirties 6 generated files.** Inherent to embedding a content version in committed output. `--check` makes forgetting it a CI failure rather than silent drift.
- **The epoch can rot.** Human-kept by choice.
- **Claude upgrade propagation is unresolved.** Documented as unverified rather than assumed. If Claude Code turns out to require semver ordering to upgrade, the version has to diverge per harness — non-semver in the omp catalog, semver in the Claude tree — which would break the "two catalogs differ only in `source`" property and need its own change.
- **CI is new surface for a repo that had none.** Kept to four commands, all of which already had to pass locally.

## Open Questions

Whether Claude Code auto-upgrades marketplace plugins at all. Testable once this branch is the default branch; until then the README states the limit rather than guessing.
