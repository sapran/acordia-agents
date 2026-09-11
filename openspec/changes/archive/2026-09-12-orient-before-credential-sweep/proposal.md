## Why

The current credential workflow begins with generic artefact inventory and credential-pattern scanning before the operation has refreshed its carried knowledge or built a current model of the target infrastructure. In an Aleph corpus this biases collection toward salient VPN and SSH material while under-searching databases, file shares, object storage, Kubernetes, CI/CD and other systems that the collection actually describes.

This change makes infrastructure orientation and prior-knowledge refresh a lead-controlled precondition for directed credential collection. It follows the repository's operational model: Monte describes operational analysis as directing every movement while identifying information gaps and synthesising technical and nontechnical data (Monte, *Network Attacks & Exploitation: A Framework*, document `c159a333`, p. 60); Styran and Yashchuk describe systematic knowledge acquisition of target systems and analysis as a core operational pillar (document `1152d85c`, pp. 21–22).

## What Changes

- Add a collection-planning preflight to the existing end-neutral analyst loop: refresh memory, orient technical terrain, assess mission value, build a credential hypothesis register, then collect.
- Require `cyber-analyst` to read and fuse the orientation returns before issuing credential-sweep instructions.
- Make `collection-analyst` produce a prior-knowledge and Aleph-corpus orientation return before credential work.
- Make `terrain-analyst` produce a non-secret technical asset register before credential extraction.
- Make `mission-analyst` map discovered assets to mission threads, crown jewels and organisational value before credential priorities are fixed.
- Change `credential-harvest-triage` to consume an Aleph orientation packet, associate findings with assets and mission relevance, and run targeted extraction before a residual sweep.
- Add non-secret asset fingerprints for MinIO/S3-compatible storage, databases, file shares, Kubernetes/container systems, CI/CD, VPN/remote access, identity systems and SSH to the existing pattern reference.
- Preserve passive handling, ownership-first classification, separate credential files, exhaustive coverage, bounded notes, and the rule that no credential is validated against a live provider.
- Update the normative role and OpenSpec requirements without adding an agent, skill, competency-grid row, permission boundary or install route.
- Bump the analyst plugin version from `6.9.0` to `6.10.0` in the three hand-maintained version files.

## Capabilities

### New Capabilities

None. The orientation gate composes existing analyst competencies and procedural skills.

### Modified Capabilities

- `agent-roster`: add the lead-controlled orientation precondition and the required orientation returns from Collection, Terrain and Mission.
- `skill-library`: modify `analyst-loop` and `credential-harvest-triage` to carry the orientation gate, orientation-packet input, asset-aware prioritisation, and targeted-then-residual ordering.

## Impact

Affected authored prompts and skills are the existing analyst loop, cyber, collection, terrain, mission, operational-memory and credential-triage surfaces, plus the credential pattern reference and the role-model prose. The competency grid remains unchanged because this is workflow composition rather than a new specialist competency. The change is passive: it reads already-collected material and produces plans and reports; it does not validate credentials or contact target systems.

The Lindsay search required by the repository grounding procedure produced no direct passage on carried operational memory. That mechanism therefore remains grounded in the existing `operational-memory` skill and its evidence, freshness, supersession and no-secrets contract rather than in an unsupported literature claim.
