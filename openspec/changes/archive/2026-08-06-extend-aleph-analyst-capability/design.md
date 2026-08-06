## Context

Two decisions in this change overturn reasoning recorded in the archived
`2026-07-31-aleph-data-access` design. Both are written up here because a future reader who finds
only the archive will re-derive the old answer and undo this work.

## Goals / Non-Goals

**Goals.** Make the Aleph capability discoverable through the mechanism this library already uses
for non-grid procedural skills. Make the skill accurate against the server it actually drives,
including the parts of Aleph's behaviour that change the method.

**Non-Goals.** No grid change. No agent gains `aleph-entity-graph` in its compiled skill set. No
frontmatter, permission, or distribution-shape change. `aleph-mcp` is not vendored: this
repository is markdown-only by contract.

## Decisions

### An H2 section does not break the grid bijection

The archived design ruled that no agent prompt would name this skill:

> "the prompts' skill lists are compiled from the grid columns, so inserting a non-grid slug into
> one would break the bijection that `competency-map-derivation` and `analyst-agent-roster`
> enforce."
> — `openspec/changes/archive/2026-07-31-aleph-data-access/design.md:34-38`

That reasoning is correct and this change does not contradict it. It binds the **compiled skill
list**, and `analyst-agent-roster`'s bijection requirement is scoped to exactly that: *"exactly
the skills marked (● deep or ○ working) in that agent's grid column"*
(`### Requirement: Prompt names the skill set from the grid column`). Nothing in it constrains
prose sections.

The archived design drew the wrong conclusion from a correct premise — that because the slug
cannot enter the compiled list, it cannot appear in the prompt at all. The library already
disproves that. Two non-grid procedural skills are *required* to appear as their own H2 section in
every analyst prompt:

- `### Requirement: Credential-harvest dispatch section in every agent prompt`
- `### Requirement: Exhaustive-processing section in every agent prompt`

Both are additive, both forbid restating the skill's method, both explicitly cause no permission
change, and neither touches the grid. `analyst-loop` uses the same mechanism in the orchestrator
alone. So an H2 section is not a workaround; it is the established, spec-sanctioned way to make a
non-grid skill reachable, and the new requirement is written to mirror the credential-harvest one
clause for clause.

Rejected alternatives:

1. **Add an Aleph row to the competency grid.** Aleph is a platform, not a competency. A grid row
   would assert that working one instance is an analytic skill on a par with target-mission
   analysis, and it would then propagate into four compiled skill sets by derivation — a much
   larger change to the roster's meaning than the capability warrants.
2. **Leave selection to description-match.** This is the status quo, and it is why the skill is
   effectively unreachable. Description-match is the mechanism of last resort for a harness with
   no per-agent binding, not a substitute for telling the agent the capability exists.
3. **Name it in the orchestrator only,** as `analyst-loop` is. Rejected because all three legs
   have a real and distinct lens on a corpus, and because the orchestrator routes rather than
   queries — a section only it can see would tell the agent to dispatch work whose method the
   recipient was never told about.

### The section goes in all four prompts, each with its own lens

Following the credential-harvest precedent, which permits one agent-specific lens on top of the
shared reference. The lenses are not decoration; each is why that leg would open a corpus at all:
fusion correlates across collections, target-network reads ownership and address edges as target
structure, defender-detection looks for the operation's *own* infrastructure in someone else's
index. That last one is the honest reason that leg carries the section, and it mirrors how its
credential-harvest section already carries an operation-owned-versus-target-owned distinction.

### Reconcile was evaluated and rejected upstream

Recorded here because the skill's limits section is where a reader would expect to find "why not
reconcile", and because the answer required a source read that should not have to be repeated.

Aleph has no bare `/api/2/reconcile`. The real routes build `MatchQuery` from the same engine as
`POST /api/2/match`, under the same permission, and return a worse-shaped result (`r:score`
instead of `score`, `type` as an array, `match` hardcoded false). They duplicate `match_entity`
and buy no capability.

The gain people attribute to reconcile is tolerant name lookup — and that already existed as
`match_entity`. What was actually missing was the *skill saying* that `q` is not that path. So the
fix for the reconcile gap is the query-semantics correction in this change, at no new tool cost.
The upstream decision and its endpoint-by-endpoint rejections live in `aleph-mcp`'s
`extend-profile-tool-surface` design.

### The skill must not assert a tool prefix

The governing requirement mandated the `aleph_*` wording, and `aleph-mcp`'s own spec refuses to
guarantee it:

> "This server SHALL NOT be held to guarantee that prefix, and SHALL NOT add one to compensate;
> the mount configuration is where that expectation is satisfied."

Two specs therefore disagreed, and the skill was correct against ours and wrong against the
server. Editing only the skill would have put it in violation of its own requirement, so the
requirement moves in the same change. The skill now names tool verbs and gives the prefixed form
as an example of what a harness may compose, which also resolves the skill's pre-existing internal
inconsistency between its tooling paragraph and its method.

## Risks / Trade-offs

- **Four more prompt sections is four more things competing for attention in a prompt.** Mitigated
  by holding each to one paragraph and forbidding any restatement of the skill's method — the
  section is a pointer, and the requirement enforces that.
- **The skill now names seventeen tool verbs, which will drift when the server changes.** Accepted
  as the lesser drift: the previous state named four of twelve and asserted a prefix that was
  never true. The server's spec makes its tool set a published contract with a breaking-change
  rule, so drift is detectable there rather than silent here.
- **Nothing in this repository can verify the tool names against a running server**, since
  markdown-only means no test harness. The check is upstream, in `aleph-mcp`'s
  `EXPECTED_TOOLS` enumeration test.
