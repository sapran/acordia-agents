## REMOVED Requirements

### Requirement: Source artifacts stay opencode-native

**Reason**: The mechanism is gone. `tools/build-plugins.py` and both generated trees under `plugins/` are deleted, so nothing is generated, translated or gate-checked.

**Migration**: None. One authored tree per pillar is installed as-is; `plugin-distribution` specifies its shape.

### Requirement: Frontmatter translation contract

**Reason**: The mechanism is gone. `tools/build-plugins.py` and both generated trees under `plugins/` are deleted, so nothing is generated, translated or gate-checked.

**Migration**: None. One authored tree per pillar is installed as-is; `plugin-distribution` specifies its shape.

### Requirement: Prompt text corrected for omp's tool set

**Reason**: The mechanism is gone. There is no translation step to correct prompt text during; the authored prompt is the shipped prompt.

**Migration**: `agent-roster` requires a prompt body to name no tool the harness lacks, checked in review rather than at build time.

### Requirement: Unmappable permissions are surfaced, not silently resolved

**Reason**: The mechanism is gone. `tools/build-plugins.py` and both generated trees under `plugins/` are deleted, so nothing is generated, translated or gate-checked.

**Migration**: None. One authored tree per pillar is installed as-is; `plugin-distribution` specifies its shape.

### Requirement: Skill autoloading is opt-in

**Reason**: The mechanism is gone. `tools/build-plugins.py` and both generated trees under `plugins/` are deleted, so nothing is generated, translated or gate-checked.

**Migration**: None. One authored tree per pillar is installed as-is; `plugin-distribution` specifies its shape.

### Requirement: Installation is idempotent and inspectable

**Reason**: The mechanism is gone. opencode is no longer a target and `install.sh`/`uninstall.sh` are deleted.

**Migration**: Install through the harness's own plugin system: `omp plugin marketplace add sapran/acordia-agents` then `omp plugin install acordia-analysts@acordia`, or the Claude Code equivalent.

### Requirement: Pillar auto-discovery is limited to distributable directories

**Reason**: The mechanism is gone. opencode is no longer a target and `install.sh`/`uninstall.sh` are deleted.

**Migration**: Install through the harness's own plugin system: `omp plugin marketplace add sapran/acordia-agents` then `omp plugin install acordia-analysts@acordia`, or the Claude Code equivalent.

### Requirement: Write-capable pillars are translated without a false read-only claim

**Reason**: Nothing is translated, and no read-only claim is made anywhere: every agent in both pillars holds the full tool set.

**Migration**: `agent-roster`'s write-posture requirement is the replacement.

### Requirement: Ownership evidence is defined once for install and uninstall

**Reason**: The mechanism is gone. opencode is no longer a target and `install.sh`/`uninstall.sh` are deleted.

**Migration**: Install through the harness's own plugin system: `omp plugin marketplace add sapran/acordia-agents` then `omp plugin install acordia-analysts@acordia`, or the Claude Code equivalent.

### Requirement: Installation refuses to overwrite an artifact it does not own

**Reason**: The mechanism is gone. opencode is no longer a target and `install.sh`/`uninstall.sh` are deleted.

**Migration**: Install through the harness's own plugin system: `omp plugin marketplace add sapran/acordia-agents` then `omp plugin install acordia-analysts@acordia`, or the Claude Code equivalent.

### Requirement: Overwriting an unowned artifact requires an explicit flag

**Reason**: The mechanism is gone. opencode is no longer a target and `install.sh`/`uninstall.sh` are deleted.

**Migration**: Install through the harness's own plugin system: `omp plugin marketplace add sapran/acordia-agents` then `omp plugin install acordia-analysts@acordia`, or the Claude Code equivalent.
