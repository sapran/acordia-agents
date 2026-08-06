## Why

`analyst-skill-library`'s Method contract opens with a criterion — skills "whose `Objective` involves reading collected material (files, memory dumps, logs, packet captures, configuration archives)" must carry an inventory step, a bounded-and-exhaustive reading discipline, a `<path>:<offset>` citation shape, and a per-tool degradation policy — and then closes it off: "The requirement applies to the following fifteen skills only."

The library has 39 grid skills. Fifteen are bound; 24 are not. A classification pass over all 24 against the spec's own criterion found seven that read collected material and are bound by nothing: `ot-embedded` reads firmware, HMI projects, ladder logic, and historian data; `overwatch` reads SIEM and EDR consoles, alert queues, and SOAR tickets; `effect-on-target-verification` gathers independent observables from the target; `assessing-take-value` inspects an artefact for truncation, corruption, and planting; `analytic-tooling-scripting` and `data-integration-tooling` parse and normalise raw take; `change-cycle-forecasting` reads version and release evidence. None of the seven names a tool, states a coverage discipline, gives a citation shape, or says what to do when a tool is missing.

The closed list is the defect, not the criterion. A skill that reads evidence is bound or unbound according to whether someone remembered to add its name, so the next artefact-reading skill will be unanchored by default. Two of the fifteen were checked as controls and genuinely carry all four elements, so the contract is a real standard being applied to an arbitrary subset rather than an aspiration nobody meets.

Current behavior: seven skills direct the reading of collected material with no verifiability anchor of any kind, and the requirement's own criterion does not reach them. Desired behavior: the criterion governs, the enumeration follows it, and every skill that reads evidence carries the four elements.

## What Changes

### The spec — the criterion governs and the list follows it

The Method contract requirement is modified so the criterion is normative and the enumeration is a statement of which skills currently satisfy it, not a limit on which skills it reaches. The list grows from fifteen to twenty-two. A scenario is added requiring that a skill meeting the criterion be bound whether or not it appears in the list, so the enumeration can never again silently define the scope.

### The skill bodies — seven skills gain the four elements

Each of the seven gains, in its existing `## Method` section and in the established style of the bound fifteen: an inventory step naming the enumeration tool, bounded-and-exhaustive reading language, a citation shape appropriate to its artefact type, and a degradation policy for each optional tool it names. Wording stays in each skill's own idiom; the elements are woven into the existing bullets rather than bolted on as a labelled block.

### The version

`VERSION` moves to `2.4.0` — MINOR, seven skill bodies reach users. The version gate added in `gate-version-bump` now enforces this.

**Not in scope:** the seventeen skills classified as analytic spine keep their exemption, which the requirement already provides for and which the classification pass confirmed for each. No body contract beyond the four elements is mechanised; the Method contract remains a prose requirement verified by reading, as it is for the existing fifteen.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `analyst-skill-library`: the requirement "Method contract for evidence-reading skills" is modified so its criterion is normative rather than decorative, its enumeration grows from fifteen skills to twenty-two, and a new scenario forbids the list from narrowing the criterion.

## Impact

- **Modified:** seven `analysts/skills/<slug>/SKILL.md` bodies, plus `VERSION`.
- **Regenerated:** both `plugins/` trees carry the seven bodies and the six version-carrying files.
- **Unchanged:** every agent prompt, every command wrapper, the seventeen spine skills, and the fifteen already-bound skills.
- **Classification evidence:** all 24 unbound skills were classified against the spec's criterion by four independent passes, with two already-bound skills used as controls to confirm the contract describes real content. Seven came back evidence-reading; seventeen analytic spine.
- **Corrected while classifying:** an earlier review had named `cloud-identity-log-analysis` and `detection-capability-analysis` as unanchored evidence-reading skills. Both are predictive — they reason about what a provider *would* log and what a defender *could* detect, without opening an artefact — so both stay exempt and neither is touched.
