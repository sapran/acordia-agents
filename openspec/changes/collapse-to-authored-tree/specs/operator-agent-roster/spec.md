## REMOVED Requirements

### Requirement: Five operator agents ported from the CyberStrike roster

**Reason**: Subsumed by the new `agent-roster` capability, which specifies all nine agents in one place instead of one capability per pillar.

**Migration**: Read the equivalent requirement in `agent-roster`; the behaviour it protects is unchanged.

### Requirement: One primary orchestrator, four specialist subagents

**Reason**: Subsumed by `agent-roster`. `mode` and the `task` permission map are gone; the orchestrator names its four specialists in its prompt instead.

**Migration**: Read `agent-roster`'s routing requirement.

### Requirement: Dispatch descriptions are the routing signal

**Reason**: Subsumed by the new `agent-roster` capability, which specifies all nine agents in one place instead of one capability per pillar.

**Migration**: Read the equivalent requirement in `agent-roster`; the behaviour it protects is unchanged.

### Requirement: Operators are write-capable

**Reason**: Subsumed by `agent-roster`, and no longer a distinction: with the analyst read-only posture removed, every agent in both pillars holds the full tool set.

**Migration**: Read `agent-roster`'s write-posture requirement, which now covers both pillars.

### Requirement: Destructive and RCE primitives denied in bash

**Reason**: The mechanism is gone. The 24-glob deny map was enforced only by opencode; under omp and Claude Code it was already inert, and every generated file said so. With opencode dropped it specifies nothing.

**Migration**: The guardrails paragraph in each operator prompt carries the discipline (no destructive action, no exfiltration beyond proof, no persistence), and `agent-roster` specifies it. The upstream source of the map, `injectionAgentPermission` in CyberStrike `agent.ts:598-623` at commit 359655518, is recorded in `docs/roles/operator.md` should it ever be wanted back.

### Requirement: Authorization and scope gate stated in every prompt

**Reason**: Subsumed by the new `agent-roster` capability, which specifies all nine agents in one place instead of one capability per pillar.

**Migration**: Read the equivalent requirement in `agent-roster`; the behaviour it protects is unchanged.

### Requirement: Prompt names its skill set

**Reason**: Subsumed by the new `agent-roster` capability, which specifies all nine agents in one place instead of one capability per pillar.

**Migration**: Read the equivalent requirement in `agent-roster`; the behaviour it protects is unchanged.

### Requirement: Journal discipline section in every prompt

**Reason**: Subsumed by the new `agent-roster` capability, which specifies all nine agents in one place instead of one capability per pillar.

**Migration**: Read the equivalent requirement in `agent-roster`; the behaviour it protects is unchanged.

### Requirement: Delegation quality rules retained in the primary

**Reason**: Subsumed by the new `agent-roster` capability, which specifies all nine agents in one place instead of one capability per pillar.

**Migration**: Read the equivalent requirement in `agent-roster`; the behaviour it protects is unchanged.

### Requirement: Operator agents carry the pillar and role anchor

**Reason**: Agent frontmatter is now exactly `name`, `description`, `color`.

**Migration**: Provenance for an operator agent is read from `docs/roles/operator.md`, which records the CyberStrike agent and prompt path each was ported from. Skill-level `metadata.cyberstrike` attribution is untouched.
