## Context

See `proposal.md` — Why. The design-relevant constraint is that the defect is entirely in **prose**, spread across four layers that each restate the same false contrast:

| layer | site | current framing |
| --- | --- | --- |
| agent prompts | `analysts/agents/*.md` guardrails | "Under OMP, write access is prompt-level" — names one harness, three different wordings |
| generator | `tools/build-plugins.py:327-337` (omp note), `:409-411` (Claude comment) | "omp cannot express a path-scoped permission"; "Claude Code cannot express a path scope, so the confinement is prompt-level here" |
| docs | `README.md:164-167`, `CLAUDE.md:86` | "opencode confines … writes to `.acordia/reports/**`"; "**Scoped-write exception**" |
| spec context | `openspec/config.yaml:37-49` | "enforced to different depths per harness: fully in Claude Code and opencode, partially in omp" |

`README.md:166` already states the fact that invalidates all four ("`bash` is still a write channel … all three harnesses"), which is why this is a wording change rather than a discovery.

Two constraints bound the design. First, the generated trees under `plugins/` are committed build output gated by `--check`, so any generator string change is a two-step edit-then-regenerate. Second, `omp-harness-distribution` line 231 currently fixes a scenario reading "its generated write-access note is **unchanged** from before the change" — a prior change deliberately froze that note. This change unfreezes it, which is why the requirement is edited rather than worked around.

## Goals / Non-Goals

**Goals:**

- One statement of the report-sink convention, reused verbatim in meaning across all four layers.
- Preserve every mechanically accurate disclosure already present (omp's `xd://` transport `write`, Claude Code's retained `Write`).
- Keep all three specs' derivation tables and emitted tool names byte-identical in effect — this change must move no tool.
- Make the two read-only legs state their product destination, which they currently omit.

**Non-Goals:**

- No enforcement of the sink. Explicitly rejected below.
- No permission-map edits. The scoped `edit` block stays.
- No change to the operators pillar or to `harness-tool-translation`, whose line 34 already carries the target wording.
- No renaming of either sink path.

## Decisions

### Retain the scoped `edit` block rather than flatten it to `edit: deny`

**Considered:** if the scope enforces nothing, delete it and give the two reporting analysts a blanket `edit: deny`, relying on prompts alone.

**Rejected.** The scoped rule is the only machine-readable record of *which* agents hold the reporting competency and *where* their product goes. Flattening it would lose that, break the `plugin-packaging` derivation table's path-scoped row (which is what keeps `Write` for those two agents in Claude Code), and leave the two reporting analysts unable to write in opencode at all. The rule earns its place as documentation-in-frontmatter; only the claim about its effect is wrong.

### Reject the enforcement hook

**Considered:** a `PreToolUse` hook, supported by both plugin harnesses, rejecting `Write`/`Edit` outside `.acordia/reports/` and pattern-matching shell redirection.

**Rejected on four grounds.** It is executable code in a markdown distribution with no test surface. Its `bash` arm is bypassable by `python -c`, `tee`, or a heredoc, so it would buy partial coverage while reading as complete — strictly worse than an honest convention. It would block the scratch files `analytic-tooling-scripting` and `exhaustive-data-processing` legitimately need. And there is no adversary: the failure it prevents is a misfiled report.

### Keep `bash: allow`

**Considered:** deny `bash` on the two read-only legs to make the scope genuine.

**Rejected.** It trades two load-bearing skills for a cosmetic boundary, and would still leave the two reporting analysts — the ones the sink is about — with an open shell.

### State non-enforcement as universal, not per-harness

The replacement wording attributes the gap to `bash: allow`, a property of the **source** permission maps, rather than to any harness's frontmatter vocabulary. This is what makes one sentence serviceable in all four layers, and it survives a future harness gaining path-scoped permissions.

Retained per-harness facts stay where they are mechanically true and separately consequential: omp exposing `write` via `tools.xdev` is a real divergence from the emitted allowlist and is disclosed independently of the sink.

### Order the edits source-first, then regenerate

Agent prompts, generator strings, and docs are edited before `tools/build-plugins.py` runs. The generated trees are never hand-edited — doing so is a drift bug per `openspec/config.yaml:16-18`. `--check` then gates the result.

### Version: MINOR

`VERSION` `2.1.0` → `2.2.0`. Agent prompt bodies reach users, which `plugin-packaging`'s hand-maintained-version requirement fixes as the MINOR criterion. Not MAJOR: the roster is untouched and the shape of the distribution is unchanged.

## Risks / Trade-offs

**The convention now rests entirely on prompt adherence, and says so.** That is the honest position rather than a new risk — adherence was already the only thing holding — but the change removes the false comfort of the previous wording. Accepted: the consequence of a miss is a misfiled markdown file in the user's own repository.

**Reduced deterrence.** A reader who believed the scope was enforced might have been more careful than one told it is a convention. Judged not worth preserving: a guarantee the repository cannot keep is a worse artifact than an accurate convention, and `README.md:166` already contradicted the guarantee for anyone reading two lines further.

**Spec churn against a recently frozen note.** Editing `omp-harness-distribution`'s "note is unchanged from before the change" scenario reverses a decision from `harden-plugin-distribution`. Deliberate and narrow: that scenario existed to prove a *different* change did not disturb the note, not to make the wording permanent.

**Overlap with an active change.** `harden-plugin-distribution` also modifies `plugin-packaging` and `tools/build-plugins.py`. The requirements touched are disjoint (version derivation and the wrapper bijection there; the denylist rationale and the path-scope note here), but both bump `VERSION`, so whichever applies second must reconcile the number rather than assume `2.2.0`.
