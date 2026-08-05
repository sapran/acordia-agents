## Context

Three defects in a freshly archived change, all the same family: a normative claim with nothing behind it. The version was declared and not derivable; the Claude posture was declared and not tested; the dispatch form was documented and wrong.

## Goals / Non-Goals

**Goals.** Make the version shippable. Verify the posture against a live harness. Correct the documentation to what was observed.

**Non-Goals.** No CI, no hooks, no lint automation — this repository is markdown plus one generator, and it has deliberately had no build pipeline. No change to any agent prompt, skill, or wrapper body. No attempt to give Claude Code an upgrade mechanism it may not have.

## Decisions

### Version: hand-maintained semver

The version must change when content changes, or omp's upgrade path skips and an edit never reaches an installed user. Two ways: derive it, or type it.

Derivation was implemented first — a sha256 over the sources and the generator — and then removed. It worked, and it was disproportionate: forty lines of hashing plus a checkout-reproducibility bug (a gitignored `.DS_Store` made the version depend on whose machine built it) in a repository that is markdown plus one generator. The same argument that removed the CI removed this.

What remains is `VERSION = "2.0.0"` in the generator, bumped by hand. The failure mode is the honest cost: forgetting is silent, where a stale derived version would have been caught by `--check`. That is mitigated by writing the obligation into `CLAUDE.md` as a top-level rule with explicit MINOR and MAJOR criteria, not by adding machinery.

Hand-maintaining it buys back something the hash could not have: **real semver.** A hash has no ordering, which is why the derived scheme had to be deliberately non-semver to exploit omp's inequality branch — and that left Claude Code, which compares by precedence, with no upgrade path even in principle. A monotonic hand-bumped version is ordered, so both harnesses compare it correctly and the per-harness divergence problem disappears entirely.

Build metadata remains prohibited: `1.0.0+aaa` and `1.0.0+bbb` compare equal and never upgrade.

### Evidence for the version semantics, and a trap in gathering it

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

- **A forgotten bump is silent.** The accepted cost of hand-maintaining it. `CLAUDE.md` carries the rule; nothing enforces it.
- **`--check` is still run by hand.** No automation enforces it, deliberately. Drift is caught by whoever next runs the generator.
- **Claude upgrade propagation is unresolved.** Documented as unverified rather than assumed. Real semver removes the risk that drove this: if Claude Code does compare by precedence, a monotonic hand-bumped version already satisfies it, so no per-harness divergence is needed.

## Open Questions

Whether Claude Code auto-upgrades marketplace plugins at all. Testable once this branch is the default branch; until then `README.md` states the limit rather than guessing.
