## Why

The distribution has been shipping half a methodology under one name, and the halves do not compose.

`docs/roles/operational-analyst.md` is a genuine derivation. It opens by naming Analysis as the
ACORDIA core pillar, quotes Monte p. 60 in full as its load-bearing claim, and closes with fourteen
works cited to the page. `docs/roles/operator.md` is provenance, not derivation: it records where the
text came from and says nothing about why those four agents are the right four. They are not the right
four. **"Operations" is not an ACORDIA pillar** — the framework's operational tier is Access, Control
and Analysis — and `web-application` / `mobile-application` / `cloud-security` / `internal-network` is a
commercial pentest service catalogue organised by target surface, which is the exploit-and-surface
framing the source paper was written to argue against.

The two orchestrators say it themselves. `cyber-analyst` is "the primary brain for an offensive
operation" running an end-neutral effect-or-collection loop; `cyber-operator` runs "an authorized
penetration test or red-team engagement", routing "recon-through-exploitation phases". They share no
objective concept, no life cycle and no state file, so they cannot be in one operation.

Underneath that is a category error. Analysis agents consume evidence and make no target contact;
operations agents make target contact. One `## Guardrails` posture has been stretched over two risk
classes, which is why it reads as an evidence-integrity rule bolted onto agents that run exploits.

Removing the pillar is not a reduction in ambition. ACORDIA's own resource-allocation finding is that
overinvestment in supporting functions at the expense of core functions, *particularly analysis*,
"produces capability without effectiveness", and that operators frequently hold access they cannot
turn into outcomes. Shipping Analysis alone is that argument executed rather than a gap in it.

The second defect is inside the analysis pillar. `fusion-analyst` fails the separation criterion the
grid itself states — a specialist is made "by the technical substrate they command deeply enough to
take apart from the inside" — and the grid then describes Fusion as "shallow-but-wide". The marks
agree: deep (`●`) counts are Core 12, T&N 12, Def 13, **Fus 6**, of which one is shared with both other
legs, leaving five unique and all five in a single grid section. Worse, the source of truth
contradicts itself: the grid gives `Maintaining the operating picture ●` to Fusion while the
`cyber-analyst` description says the lead "holds the target picture". Fusion is not a leg. It is three
things wearing one hat.

## What Changes

- **`acordia-operators/` is deleted** — five agents, forty skills, ten command wrappers and its
  manifest. `acordia-analysts/` becomes the only plugin.
- **Five analyst agents, up from four.** `cyber-analyst` (lead, cyan) keeps its name and gains the
  operating picture and multi-source correlation. `target-analyst` **splits**: `mission-analyst` takes
  the organisational half — what the target is for, what it depends on, crown-jewels and mission-thread
  work, and the target's procedures, redundancy and reporting culture — and `terrain-analyst` takes the
  technical half. `overwatch-analyst` is unchanged. `collection-analyst` is new and holds what actually
  remained of Fusion: the value and quality of the collected take, data integration tooling, and
  working bulk material at volume.
- **`target-analyst` and `fusion-analyst` are retired.** Fusion's five unique skills go three ways —
  operating picture and correlation to the lead, non-technical context to `mission-analyst`, take
  quality and data tooling to `collection-analyst`.
- **Wrappers 18 → 10**: five canonical, five short aliases, all flat in `acordia-analysts/commands/`.
- **The consumer is a human operator.** An analyst product is handed to a person who then acts. The
  lead no longer directs executing agents, and its end-neutral loop judges outcomes from reported
  evidence rather than from its own dispatched action.
- **Grid anchors move from line numbers to stable row ids.** Thirty-eight skills currently carry
  `source: docs/roles/operational-analyst.md#L<n>` into rows L67–L108, and every one of them breaks
  silently on any grid edit. They move to `row: <stable-id>`, minted once in the grid row itself.
- **A fifth capability, `doctrinal-provenance`**, makes the literature grounding checkable the way
  `competency-map-derivation` makes the grid grounding checkable.
- **Version 4.2.0 → 5.0.0.** Removing a pillar is breaking for anyone who installed it.

## What does NOT change

- **The analyst grid is repaired, not rewritten.** Its fourteen-source, page-level grounding is the
  only asset in this repository that already does what `doctrinal-provenance` proposes to mandate.
  Five changes land on it — the Fusion leg, the third end, the operating-logic axis, the anchors, and
  three added rows — and nothing else. The fifth was not in the original scope and was approved
  explicitly: redistributing the retired Fusion column left `collection-analyst` with three deep
  skills against Terrain's nine and Def's thirteen, which is the same thinness that retired Fusion.
  `target-friction-susceptibility`, `take-domain-interpretation` and `operational-memory` are added so
  the two new legs are real rather than nominal, and so the passages selected for them have a skill to
  live in. Grid rows 38 → 41; library 42 → 45.
- **`openspec/changes/archive/**` is untouched.** An archived change records what was true when it
  shipped.
- **`docs/roles/operator.md` is archived, not deleted.** It is the only record of what was ported from
  CyberStrike at commit `359655518` and where it deliberately diverged. Deleting it would destroy the
  provenance rather than retire it.
- **Both marketplace catalogs still ship and stay byte-identical.** omp prefers `.omp-plugin/`, Claude
  Code reads `.claude-plugin/`; each now carries one entry instead of two.
- **`acordia-analysts/` keeps its directory name**, so the install source path is stable and this is
  not a distribution-path major on top of the roster major.
- **Names stay unprefixed.** Provenance is carried by the description tag, the `color` and the plugin
  namespace, never by the agent name or the skill slug.

## Impact

- Affected specs: `agent-roster` (roster, wrappers, dispatch tags, return contract, retired legs);
  `skill-library` (the operations half removed wholesale, `analyst-loop` re-routed);
  `competency-map-derivation` (five columns, stable row ids); `plugin-distribution` (one plugin, three
  version occurrences across three JSON files); `doctrinal-provenance` (new).
- Affected code: none. This distribution has no runtime.
- **External:** `~/ai/checks/check-acordia.sh` asserts one semver at exactly six occurrences across
  four JSON files. After this change it is three across three, so the script fails on a correct
  repository until it is updated in lockstep.
- **In the wild:** removing a plugin from the catalogs does not uninstall it, and Claude Code has no
  working upgrade path for marketplace plugins, so an installed `acordia-operators` stays resident and
  frozen at 4.2.0. The change must say so rather than assume the removal propagates.
