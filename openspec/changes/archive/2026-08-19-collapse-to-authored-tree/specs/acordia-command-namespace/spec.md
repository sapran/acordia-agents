## REMOVED Requirements

### Requirement: A namespaced command wrapper for every dispatchable agent

**Reason**: Subsumed by `agent-roster`, which specifies the 17 wrappers alongside the agents they dispatch.

**Migration**: Read `agent-roster`'s command-wrapper requirement.

### Requirement: Namespace shape is per harness, because discovery differs

**Reason**: Only one discovery shape remains. Both harnesses read `<pluginRoot>/commands/*.md` non-recursively and namespace by plugin name; the opencode flat-namespace branch is gone with opencode.

**Migration**: `agent-roster` states the single layout: eight wrappers in `acordia-analysts/commands/`, nine in `acordia-operators/commands/`.

### Requirement: Agent names and skill slugs stay unprefixed

**Reason**: Subsumed by the new `agent-roster` capability, which specifies all nine agents in one place instead of one capability per pillar.

**Migration**: Read the equivalent requirement in `agent-roster`; the behaviour it protects is unchanged.

### Requirement: Commands deploy under the same guarantees as agents and skills

**Reason**: The mechanism is gone. opencode is no longer a target and `install.sh`/`uninstall.sh` are deleted.

**Migration**: Install through the harness's own plugin system: `omp plugin marketplace add sapran/acordia-agents` then `omp plugin install acordia-analysts@acordia`, or the Claude Code equivalent.

### Requirement: The command directory is not a pillar

**Reason**: The mechanism is gone. There is no pillar auto-discovery to exclude a directory from, and `commands/` no longer exists at the repository root — each pillar carries its own.

**Migration**: None. `plugin-distribution` fixes each plugin's layout explicitly.
