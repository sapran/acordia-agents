## Context

The primary `operational-analyst` was observed, across several runs, to answer operational questions itself rather than dispatching its three legs. The natural suspect was the `task` permission block (`"*": deny` then a three-leg allow-list). It was ruled out by reading opencode 1.18.4 source and confirming against the live install (`opencode debug agent operational-analyst`). Every gate that could block delegation passes:

- **Match order** — `permission/index.ts` `evaluate()` uses `findLast` (last-match-wins). For `pattern = "target-network-analyst"` the last matching rule is the leg's `allow`. Dispatch → **allow**. The `"* : deny"`-first ordering the repo relies on is correct.
- **Tool visibility** — `permission/index.ts` `disabled()` hides a tool only when the `findLast` rule matching its permission has `pattern === "*" && action === "deny"`. The orchestrator's last `task`-matching rule is `{task, fusion-analyst, allow}` (pattern ≠ `*`) → the task tool stays **visible**.
- **Roster surfaced to the model** — `tool/registry.ts` `describeTask()` appends to the task tool description every non-`primary` agent for which `evaluate("task", name, perm) !== "deny"`. All three legs resolve `allow` and are listed with their descriptions; `general`/`explore` resolve `deny` and are excluded.
- **Agents loaded** — all four `.md` are symlinked into `~/.config/opencode/agents/` and load via `config/agent.ts` `Glob.scan("{agent,agents}/**/*.md", { symlink: true })`.

So the wiring permits and advertises delegation. The remaining lever is the prompt. Decisively, `session/llm/request.ts` builds the system prompt as `input.agent.prompt ? [input.agent.prompt] : SystemPrompt.provider(model)` — a custom agent prompt **replaces** opencode's base prompt. The analyst body is therefore the *entire* behavioural spec, and it currently frames dispatch as optional and authorises a co-equal self-service path ("if a piece of work fits none of them, do it yourself"). `task.txt` reinforces the out ("If no available agent is a good fit… use other tools directly"). Given all its own tools, the model defaults to answering inline.

## Goals / Non-Goals

**Goals:**
- Make `operational-analyst` reliably dispatch the relevant legs before delivering a recommended course of action, by encoding that as a precondition in the prompt body.
- Preserve the read-only posture, the three-leg dispatch topology, and every frontmatter contract exactly.
- Keep the change a faithful re-derivation of the role model (role-doc L52 / "How the pieces fit"), not a new competency — so the source map and grid are untouched.

**Non-Goals:**
- No permission, `mode`, or `task`-whitelist change. The block is not the bug; editing it would be cargo-culting.
- No change to the leg agents or their `description`s. Descriptions are locked to the italic operating questions by the existing "Dispatch descriptions are the role doc's leg questions" requirement, and they already route correctly through `describeTask`.
- No opencode config change (`default_agent`, `subagent_depth`, experimental flags). `subagent_depth` default (1) already permits primary→leg.
- No attempt to force dispatch mechanically (opencode has no "must-call-tool-first" hook for a primary); the lever is prose the model follows.

## Decisions

**Decision: fix the prompt body, nothing else.** The permission layer, roster surfacing, and install are all correct and verified; the only under-encoded surface is the prompt. Because the agent prompt replaces the base prompt, strengthening the body is both necessary and sufficient. *Alternatives rejected:* editing the `task` block (not the cause); setting `default_agent`/depth (irrelevant); making legs `mode: all` (changes routing semantics for no benefit).

**Decision: express the mandate as a precondition on the course of action, not a blanket "always call all three."** The role model ties the course of action to the *fused* reads, but not every task touches every leg. So the body compels dispatch of the legs whose **operating question the task touches**, before delivering a recommendation — preserving analytic judgement about which legs are relevant while removing the "just answer it myself" default. *Alternative rejected:* "always dispatch all three legs on every turn" — wasteful round-trips on narrow questions and not what the role model claims.

**Decision: narrow, not delete, the self-service clause.** The orchestrator legitimately carries the Core `○` technical baseline and may do trivial lookups. The reframed clause keeps self-service for work that matches **no** leg plus trivial single-artefact reads, and stops presenting it as co-equal to dispatch for specialist questions. *Alternative rejected:* removing self-service entirely — contradicts the grid (orchestrator has a working technical baseline) and would push trivial reads through a leg.

**Decision: keep the edit additive to the existing dispatch prose.** Strengthen the "You direct three specialists" section and the self-service sentence in place; introduce no new H2, so the credential-harvest / output-discipline / tool-discipline sections and their requirements are undisturbed.

## Risks / Trade-offs

- **[No runtime to prove behaviour change]** There is no test suite and no deterministic way to assert an LLM will dispatch. → Verify structurally: `openspec validate --all --strict`, `opencode debug agent operational-analyst` to confirm frontmatter/permissions are byte-unchanged, and a body read-through confirming dispatch is stated as a precondition. Optionally a manual smoke run.
- **[Over-dispatch on trivial asks]** A strong mandate could push the model to spawn legs for questions it should answer directly. → Mitigated by scoping the mandate to "legs whose operating question the task touches" and keeping the trivial-lookup carve-out.
- **[Prompt drift vs. source map]** The mandate must stay a re-derivation, not a new claim. → It cites role-doc L52 / "How the pieces fit"; no grid row or skill is added, so `docs/roles/operational-analyst.md` needs no edit and the bijection is preserved.
- **[Wording collides with `task.txt`]** opencode's task tool description still offers the "use other tools directly" out, which the body now partly counters. → Acceptable: the agent body is the authoritative spec and takes precedence in practice; the body simply must be unambiguous that specialist questions go to the legs.
