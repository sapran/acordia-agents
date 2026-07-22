## Why

Across multiple runs the primary `operational-analyst` answers operational questions itself instead of dispatching its three legs. This was traced (against opencode 1.18.4 source and the live install) to a **prompt-behaviour gap, not a permission or wiring fault**: the `task` tool resolves visible, dispatch to all three legs resolves `allow`, and the legs are enumerated to the model with their descriptions. Delegation is fully available — nothing compels it.

The role model defines the orchestrator's recommended course of action as **"three technical reads feeding one analytic judgement"** (`docs/roles/operational-analyst.md` L52). An orchestrator that forms a course of action without first obtaining the legs' reads is under-encoding that model. In opencode a custom agent prompt **replaces** the base agent prompt (`session/llm/request.ts`: `input.agent.prompt ? [input.agent.prompt] : SystemPrompt.provider(...)`), so the prompt body is the *entire* behavioural spec — and the current body makes delegation optional and explicitly authorises self-service ("if a piece of work fits none of them, do it yourself"), which the model reads as licence to answer directly.

## What Changes

- **Current behaviour**: `operational-analyst`'s prompt presents leg dispatch as one option among several and offers a co-equal self-service path; nothing in the body requires dispatch before a course of action is delivered. Result: the model usually does the analysis inline.
- **Desired behaviour**: the prompt body **compels** the orchestrator to dispatch every leg whose operating question the task touches **before** delivering a recommended course of action, and **narrows** self-service to work that genuinely matches no leg's question plus trivial single-artefact lookups.
- Rewrite is confined to the **prompt body** of `analysts/agents/operational-analyst.md` — strengthen the existing "You direct three specialists" dispatch prose and reframe the self-service clause as a narrow exception. Additive/rephrasing only; no new H2 topology.
- **No frontmatter change**: the `edit` / `bash` / `task` permission blocks, `mode`, and the three-leg whitelist are untouched.
- **No leg change**: the three subagent files are untouched. Leg `description`s remain the italic operating questions per the existing roster requirement (they are already the routing signal that `describeTask` surfaces).
- **No new capability, no grid change**: the mandate is a faithful re-derivation of role-doc L52 / "How the pieces fit", encoded as a normative requirement — not a new competency.

## Capabilities

### New Capabilities
<!-- none -->

### Modified Capabilities
- `analyst-agent-roster`: add a requirement that the primary orchestrator's **prompt body** compels leg dispatch before delivering a recommended course of action, and bounds self-service to work matching no leg. Complements the existing permissive "Orchestrator dispatches a leg" scenario (which established that it *can* dispatch) with a behavioural mandate on the prompt.

## Impact

- **Edited artifact**: `analysts/agents/operational-analyst.md` — prompt body only.
- **Spec**: `openspec/specs/analyst-agent-roster/spec.md` — one added requirement (synced from the delta on archive).
- **Not touched**: `install.sh`, `uninstall.sh`, all skill files, the three leg agents, every permission block, and `docs/roles/operational-analyst.md` (the mandate traces to existing prose, so the source map does not change).
- **Verification**: no runtime/test suite exists; validate via `openspec validate --all --strict` and `opencode debug agent operational-analyst` (frontmatter/permissions unchanged), plus a read-through that the body now names dispatch as a precondition of the course of action.
