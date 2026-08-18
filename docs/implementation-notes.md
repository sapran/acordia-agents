# Implementation notes

Out-of-scope findings recorded during work on other changes. Nothing here has been acted on.

## `todo` does not appear in a generated omp agent's tool inventory

Found while adding the omp harness target (`omp-harness-target`, 2026-07); re-checked against the current build.

`tools/build-plugins.py` lists `todo` in `BASE_TOOLS`, so every generated omp agent under `plugins/omp/*/agents/` carries `todo` in its `tools` list. A running omp agent nonetheless reported an inventory without it, while every other allowlisted name appeared and `edit`/`task` were correctly absent — so the list is honoured and `todo` specifically does not materialise. Why was never established. Parked because it is harmless: no agent in either pillar needs a task tracker. Worth resolving if the generated `tools` list is ever relied on as an exact description of the runtime tool set.

## Four SQL-to-RCE deny patterns are single-cased upstream

Found by a security review of `remediate-review-defects` (2026-08).

The ported deny map lists SQL keywords in both cases (`*DROP TABLE*` and `*drop table*`) but lists four SQL-to-RCE identifiers in one case only: `*xp_cmdshell*`, `*sp_OACreate*`, `*sys_exec*`, `*sys_eval*`. opencode resolves these by literal glob match, and SQL is case-insensitive on the server, so `EXEC XP_CMDSHELL` and `SELECT SYS_EXEC(...)` are accepted by SQL Server and MySQL respectively and match none of those patterns.

This is upstream's gap, not a port defect: the patterns are verbatim from `injectionAgentPermission` in `packages/cyberstrike/src/agent/agent.ts:598-623` at commit `359655518`, whose own comment states "common variants listed for both upper and lower case". Parked rather than patched because the operator pillar is a provenance-tracked port — adding case variants here diverges the port from its source, and `docs/roles/operator.md` is the record that would have to change first. The right sequence is upstream, or a deliberate documented divergence, not a quiet local edit.

## No rule tells any agent that retrieved content is data, not instructions

Found by the same review.

Nothing in either pillar instructs an agent to treat fetched pages, tool output, document text, or collected artefacts as data rather than as instructions. The nearest artifact is the `deception-detection` skill, which all four analysts carry, and it is about planted *intelligence* steering an analytic judgement — not about instructions embedded in retrieved content driving tool calls. Every analyst holds `bash: allow` and reads target-controlled material by design, so the gap is real.

Parked because it is prompt content: the fix belongs either in the analyst and operator prompts, in a skill both pillars name, or as a normative requirement in the roster specs, and choosing between those is a design decision rather than a defect repair. It should be settled alongside the prompt-slimming phase, which is already rewriting the sections it would land in.
