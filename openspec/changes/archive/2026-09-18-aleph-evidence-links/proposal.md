## Why

Aleph-backed reports routinely carry correct `entity_id` values as inert text. The current shared reporting rule permits that form, while the only concrete Aleph link template is limited to credential-sweep HTML; agents therefore have no general, drafting-time instruction for turning a record they read into a safe, resolvable reader link. This leaves a decision-maker unable to inspect the source and makes post-hoc link wrapping incomplete.

## What Changes

**Current behavior:** `briefing-reporting` requires claim-local usable locators and full identifiers, but permits issuer-qualified document/entity locators as inert text. `aleph-entity-graph` records entity IDs and collection provenance but defines no report URL construction. `credential-harvest-triage` supplies the lone `ALEPH_BASE/entities/<id>` template and a lint that cannot detect an inert Aleph ID. No shared rendered-report check compares cited Aleph IDs with report links.

**Desired behavior:**

- State in the competency-map reporting practice that a safe, known evidence-system locator is navigable rather than a bare identifier; retain an explicit, labelled exception when a safe base is unavailable.
- Make `briefing-reporting` require a report to preserve a link-ready source tuple and, for an Aleph-backed claim, defer URL construction and mechanical coverage checking to `aleph-entity-graph`.
- Add an Aleph reporting reference that defines one canonical, safe UI locator for every Aleph entity — including a document or file entity — from the same instance origin that issued the read, plus a verdict-only check that compares the expected entity IDs with the rendered report’s links without printing report content.
- Align the credential-sweep HTML layout with that common form and make its existing self-check reject an unlinked expected Aleph entity, not merely malformed anchors and placeholders.
- Preserve the no-target-contact, credential-disclosure, full-identifier, and safe-link restrictions. A base URL is only taken from the already-used Aleph connection or an explicitly supplied UI origin; it is never copied from collected material.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `skill-library`: shared finished-report traceability, Aleph evidence-link construction, and credential-sweep layout verification gain explicit, mechanically checked behavior.

## Impact

- `docs/roles/operational-analyst.md` — source-of-truth reporting prose.
- `docs/roles/sources.md` — recorded empty literature result for report-link construction.
- `acordia-analysts/skills/briefing-reporting/SKILL.md` — shared finished-report contract.
- `acordia-analysts/skills/aleph-entity-graph/SKILL.md` and a co-located markdown reference — Aleph evidence tuple, UI locator form, and verdict-only coverage check.
- `acordia-analysts/skills/credential-harvest-triage/references/report-layout.md` — specialist HTML form and self-check alignment.
- `openspec/specs/skill-library/spec.md` through a delta spec.
- The three version declarations; `acordia-map.html` is explicitly out of scope and remains independently maintained.

Not affected: agent prompts, command wrappers, `skill-sets.json`, marketplace structure, and `tools/check-acordia.sh`. The selected ACORDIA passage grounds the value of analysis as a core function; the Aleph URL and checking mechanics are procedural technique detail and therefore carry no new doctrine-source attribution.