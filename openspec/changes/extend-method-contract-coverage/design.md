## Context

See proposal.md — Why. The requirement already contains a correct criterion; the defect is the sentence that closes it to fifteen named skills. Everything here follows from deciding what replaces that sentence.

Two facts from the classification pass shape the approach. First, the contract is real: two already-bound skills were read as controls and genuinely carry all four elements, so this is not an aspiration nobody meets. Second, the boundary is not obvious from a skill's title — the deciding question is whether a skill's own Method directs opening an artefact, or whether it reasons over conclusions another skill produced. Several skills that sound evidence-heavy are predictive, and two that sound like tooling meta-skills in fact take raw take as input.

## Goals / Non-Goals

**Goals:**

- The criterion, not the list, determines who is bound.
- The seven unanchored evidence-reading skills gain the four elements in their own idiom.
- The classification is recorded, so the next reader can see why a skill is in or out rather than re-deriving it.

**Non-Goals:**

- Mechanising the check. The four elements are prose and their adequacy is a judgement — an inventory step is either meaningful or box-ticking, and no parser distinguishes those. The frontmatter gate exists because frontmatter is machine-checkable; this is not.
- Rewriting the seventeen spine skills. Their exemption is correct and already provided for.
- Touching the fifteen bound skills. They were sampled and hold.

## Decisions

**The enumeration stays, but demoted to a record of present membership.** Alternatives considered: delete the list entirely, leaving only the criterion — rejected because the list is what makes the requirement checkable in a repository with no test runner, and a reader would have to classify 39 skills to audit it; or keep a closed list and simply grow it to twenty-two — rejected because that reproduces the exact defect one cycle later, since the next artefact-reading skill is unbound until someone edits the spec. Keeping both, with an explicit scenario that the criterion wins when they disagree, gets the auditability of a list without letting the list define scope.

**The four elements are woven into each skill's existing bullets, not appended as a labelled block.** The bound fifteen do it this way — `endpoint-telemetry-edr` carries its inventory tools, coverage discipline, citation shape, and degradation clause inside prose bullets in its own voice. A bolted-on block would be visibly generated, would read as boilerplate, and would invite skipping.

**The citation shape is per-artefact, not uniform.** `<path>:<offset>` suits a firmware image; `<path>@L<line>` suits a config export; a console-derived observation needs a query-plus-timestamp form because there is no file to anchor to. The requirement already permits both file shapes, and `overwatch` in particular reads consoles rather than files, so forcing a byte offset there would produce a citation nobody can follow.

**The two tooling skills are treated as evidence-reading.** This is the least obvious call. Their output is a script or a pipeline rather than a finding, which argues for exemption; but their input is raw collected take, and the contract exists to stop conclusions resting on a head sample — which is exactly the risk when a parser is written against the first records of a dump. Their anchors emphasise coverage and provenance over citation, since the artefact they produce is a dataset rather than an observation.

**`change-cycle-forecasting` is included at medium-high confidence.** It reads version banners, release notes, and deployment evidence. It is the weakest of the seven, and it is called out here so a later reviewer can reverse it deliberately rather than discovering it as an unexplained inclusion.

## Risks / Trade-offs

**Seven prose edits could dilute each skill's voice.** → Each edit stays inside the existing bullet structure and uses the artefact vocabulary the skill already uses; no shared boilerplate sentence is copied across the seven.

**The enumeration will drift again as skills are added.** → Mitigated, not solved: the criterion now binds regardless, so drift produces an out-of-date list rather than an unbound skill. Solving it fully would need a body-content checker, which is out of scope for the reason given above.

**A borderline classification may be wrong.** → The two genuinely borderline calls (the tooling pair and `change-cycle-forecasting`) are named in this document with their reasoning, so reversing one is an edit to a recorded decision rather than an archaeology exercise.

## Migration Plan

None. Seven skill bodies change and the version moves; the generated trees are rebuilt from source as usual. Rollback is a revert.
