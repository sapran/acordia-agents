## REMOVED Requirements

### Requirement: The repository root is a plugin marketplace

**Reason**: Subsumed by the new `plugin-distribution` capability.

**Migration**: Read the equivalent requirement in `plugin-distribution`.

### Requirement: Two plugin trees, because one agent file cannot serve both harnesses

**Reason**: The premise is measurably false. All 73 skills were byte-identical between the two generated trees and agent bodies were identical; the only difference was the frontmatter line expressing a restriction. Removing the restriction converges the two files.

**Migration**: `plugin-distribution`'s one-authored-tree requirement replaces it.

### Requirement: Two marketplace catalogs, one per harness

**Reason**: Replaced. Both catalogs survive, but they are now byte-identical and hand-maintained, and their sources point at the top-level pillar directories.

**Migration**: Read `plugin-distribution`'s catalog requirement.

### Requirement: Generated trees are committed and gate-checked

**Reason**: The mechanism is gone. `tools/build-plugins.py` and both generated trees under `plugins/` are deleted, so nothing is generated, translated or gate-checked.

**Migration**: None. One authored tree per pillar is installed as-is; `plugin-distribution` specifies its shape.

### Requirement: Claude Code posture is expressed as a denylist

**Reason**: The mechanism is gone. Agent frontmatter is exactly `name`, `description`, `color`, so no permission map, tool allowlist or denylist exists to specify.

**Migration**: None. Capability is granted by omission: an agent with no `tools` key receives the harness's full tool set. Posture that still matters is stated in the prompt body and specified by `agent-roster`.

### Requirement: Postures Claude Code cannot express are recorded in the generated file

**Reason**: The mechanism is gone. `tools/build-plugins.py` and both generated trees under `plugins/` are deleted, so nothing is generated, translated or gate-checked.

**Migration**: None. One authored tree per pillar is installed as-is; `plugin-distribution` specifies its shape.

### Requirement: Command wrappers are routed by the agent they name

**Reason**: Subsumed by `agent-roster`. Routing is no longer computed by a generator: each wrapper is authored in the pillar of the agent it dispatches.

**Migration**: Read `agent-roster`'s command-wrapper requirement.

### Requirement: The plugin version is hand-maintained and bumped on every change

**Reason**: Replaced. The version semantics survive; the `tools/build-plugins.py --check` version gate that enforced them does not, because the generator is deleted.

**Migration**: Read `plugin-distribution`'s version requirement, which keeps semver, monotonicity, the no-build-metadata rule and the written-down bump obligation, and adds that an install-source move is a MAJOR bump.

### Requirement: Agent-name resolution differs by harness and is documented

**Reason**: The divergence is gone. One authored agent file is discovered by name in both harnesses, and command namespacing is the plugin name in both.

**Migration**: `agent-roster` states that names are bare and provenance rides on the description tag, the plugin name and the colour.

### Requirement: Skill frontmatter is parsed and validated before packaging

**Reason**: The mechanism is gone. `tools/build-plugins.py` and both generated trees under `plugins/` are deleted, so nothing is generated, translated or gate-checked.

**Migration**: None. One authored tree per pillar is installed as-is; `plugin-distribution` specifies its shape.

### Requirement: Agent metadata anchors are validated before packaging

**Reason**: The mechanism is gone with the generator, and there is no longer an agent anchor to validate.

**Migration**: `competency-map-derivation` keeps the skill-side anchor requirement; nothing validates it automatically, and a wrong anchor is caught in review.

### Requirement: Every skill an agent names resolves in its own pillar

**Reason**: The gate is gone with the generator. The invariant is kept as a requirement rather than as a build failure.

**Migration**: `agent-roster` requires every named slug to resolve; the change's verification section gives the one-liner that checks it by hand.

### Requirement: The destructive-bash denylist has one canonical source

**Reason**: The denylist is gone with opencode, so there is nothing left to keep canonical.

**Migration**: `docs/roles/operator.md` records the removal and names the upstream source.

### Requirement: Generated-tree drift ignores operating-system artefacts

**Reason**: The mechanism is gone. `tools/build-plugins.py` and both generated trees under `plugins/` are deleted, so nothing is generated, translated or gate-checked.

**Migration**: None. One authored tree per pillar is installed as-is; `plugin-distribution` specifies its shape.

### Requirement: The generator reports install state and prompt measurements

**Reason**: The mechanism is gone. `tools/build-plugins.py` and both generated trees under `plugins/` are deleted, so nothing is generated, translated or gate-checked.

**Migration**: None. One authored tree per pillar is installed as-is; `plugin-distribution` specifies its shape.
