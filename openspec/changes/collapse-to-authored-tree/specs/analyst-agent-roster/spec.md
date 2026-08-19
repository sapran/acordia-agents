## REMOVED Requirements

### Requirement: Four analyst agents mirroring the role model

**Reason**: Subsumed by the new `agent-roster` capability, which specifies all nine agents in one place instead of one capability per pillar.

**Migration**: Read the equivalent requirement in `agent-roster`; the behaviour it protects is unchanged.

### Requirement: Primary orchestrator, subagent legs

**Reason**: Subsumed by `agent-roster`. The `mode` key is gone with the rest of the restriction frontmatter; orchestrator versus leg is now carried by the prompt body and by which agents each prompt names.

**Migration**: Read `agent-roster`'s routing requirement: an orchestrator names its own specialists in its prompt.

### Requirement: Dispatch descriptions are the role doc's leg questions

**Reason**: Subsumed by the new `agent-roster` capability, which specifies all nine agents in one place instead of one capability per pillar.

**Migration**: Read the equivalent requirement in `agent-roster`; the behaviour it protects is unchanged.

### Requirement: Portable prompt bodies

**Reason**: Subsumed by the new `agent-roster` capability, which specifies all nine agents in one place instead of one capability per pillar.

**Migration**: Read the equivalent requirement in `agent-roster`; the behaviour it protects is unchanged.

### Requirement: Read-only file access via `edit: deny`

**Reason**: The posture was wrong and is reversed by this change. An analyst that cannot write its own notes is restricted at the wrong boundary; the material under analysis is what must stay untouched.

**Migration**: `agent-roster`'s write-posture requirement replaces it: every analyst holds the full tool set, writes freely, and does not modify the material it was given to analyse.

### Requirement: Analyst guardrails state the product destination uniformly

**Reason**: Replaced. The uniform paragraph it mandated claimed the agent holds no file-editing tool, which is no longer true and was the defect this change fixes.

**Migration**: `agent-roster` mandates the replacement paragraph, and keeps `.acordia/reports/` as a convention rather than a permission.

### Requirement: Prompt names the skill set from the grid column

**Reason**: Subsumed by the new `agent-roster` capability, which specifies all nine agents in one place instead of one capability per pillar.

**Migration**: Read the equivalent requirement in `agent-roster`; the behaviour it protects is unchanged.

### Requirement: Shared spine named in all four agents

**Reason**: Subsumed by the new `agent-roster` capability, which specifies all nine agents in one place instead of one capability per pillar.

**Migration**: Read the equivalent requirement in `agent-roster`; the behaviour it protects is unchanged.

### Requirement: Credential-harvest dispatch section in every agent prompt

**Reason**: Subsumed by the new `agent-roster` capability, which specifies all nine agents in one place instead of one capability per pillar.

**Migration**: Read the equivalent requirement in `agent-roster`; the behaviour it protects is unchanged.

### Requirement: Triage skill named in agent prompts that draw on it

**Reason**: Subsumed by the new `agent-roster` capability, which specifies all nine agents in one place instead of one capability per pillar.

**Migration**: Read the equivalent requirement in `agent-roster`; the behaviour it protects is unchanged.

### Requirement: Leg subagents declare what they return

**Reason**: Subsumed by the new `agent-roster` capability, which specifies all nine agents in one place instead of one capability per pillar.

**Migration**: Read the equivalent requirement in `agent-roster`; the behaviour it protects is unchanged.

### Requirement: Primary declares output discipline

**Reason**: Subsumed by the new `agent-roster` capability, which specifies all nine agents in one place instead of one capability per pillar.

**Migration**: Read the equivalent requirement in `agent-roster`; the behaviour it protects is unchanged.

### Requirement: Primary prompt defaults to leg dispatch

**Reason**: Subsumed by the new `agent-roster` capability, which specifies all nine agents in one place instead of one capability per pillar.

**Migration**: Read the equivalent requirement in `agent-roster`; the behaviour it protects is unchanged.

### Requirement: Bash analysis fully allowed; read-only CLI tools ungated

**Reason**: The mechanism is gone. Agent frontmatter is exactly `name`, `description`, `color`, so no permission map, tool allowlist or denylist exists to specify.

**Migration**: None. Capability is granted by omission: an agent with no `tools` key receives the harness's full tool set. Posture that still matters is stated in the prompt body and specified by `agent-roster`.

### Requirement: Exhaustive-processing section in every agent prompt

**Reason**: Subsumed by the new `agent-roster` capability, which specifies all nine agents in one place instead of one capability per pillar.

**Migration**: Read the equivalent requirement in `agent-roster`; the behaviour it protects is unchanged.

### Requirement: Aleph-corpora section in every agent prompt

**Reason**: Subsumed by the new `agent-roster` capability, which specifies all nine agents in one place instead of one capability per pillar.

**Migration**: Read the equivalent requirement in `agent-roster`; the behaviour it protects is unchanged.

### Requirement: Analyst agents carry the pillar and role anchor

**Reason**: Agent frontmatter is now exactly `name`, `description`, `color`. The anchor existed so a generator could read an artifact's provenance without knowing its pillar; the generator is gone.

**Migration**: Provenance for an analyst agent is read from `docs/roles/operational-analyst.md` and the prompt body. `competency-map-derivation` records that agents carry no anchor while skills keep theirs.
