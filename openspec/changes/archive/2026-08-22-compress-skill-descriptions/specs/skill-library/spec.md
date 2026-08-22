## MODIFIED Requirements

### Requirement: The description is the selection surface

Because both harnesses select a skill by matching its `description`, each `description` SHALL open
with an imperative naming the work only that skill does, and SHALL then give the trigger — the
situation in which that work is wanted. It SHALL be 1–200 characters.

The ceiling is a budget obligation, not a style preference. A host renders the library as a
*catalogue* in the system prompt — one entry per skill, costing `97 + len(name) + len(description) +
len(location)` characters — and that catalogue has a finite budget, 18,000 characters on OpenClaw
2026.7.1. A host that exceeds the budget does not drop the overrunning skill and does not fail: it
drops **every** description in the catalogue and renders names and paths alone. An overlong
description therefore costs every *other* skill its selection surface, which is why the bound is
per-description and hard rather than an aggregate the library could average its way past.

Across the library the mean `description` length SHALL be at most 180 characters, so that the
catalogue for any single analyst's skill set stays under 12,000 characters and leaves a host room for
skills of its own.

A description SHALL NOT open with a selection-boilerplate clause: `Use when`, `Apply when`, `Use to`,
`Use this skill`, and their variants are prohibited openings, because they are common to every skill
and therefore discriminate between none of them. A bare topic label SHALL NOT be used either.

Within a family, no two descriptions SHALL compete: each SHALL name work its siblings do not cover.
Where two are inseparable, the two skills SHALL be merged rather than shipped as competing siblings.

Compression SHALL NOT be achieved by dropping the trigger. Where a description must lose material to
reach the ceiling, what goes is enumeration — worked examples, lists of artefact types, restatements
of the body — and what stays is the pair a selecting model needs: the work only this skill does, and
the situation that calls for it.

#### Scenario: Description states applicability

- **WHEN** any skill's description is read
- **THEN** it states the situation the skill applies to, not merely its topic

#### Scenario: Description discriminates between siblings

- **WHEN** two skills in the same family are compared
- **THEN** each description names work the other does not cover

#### Scenario: Boilerplate openings are absent

- **WHEN** every description under `acordia-analysts/skills/` is read
- **THEN** none begins with `Use when`, `Apply when`, `Use to`, `Use this skill` or an equivalent selection-boilerplate clause

#### Scenario: Every description is within the ceiling

- **WHEN** every `description` under `acordia-analysts/skills/` is measured as characters after YAML folding
- **THEN** none exceeds 200 characters, and the mean across the library is at most 180

#### Scenario: A role-scoped catalogue renders with descriptions

- **WHEN** a host loads the skill set named in any one analyst's prompt and renders its catalogue at `97 + len(name) + len(description) + len(location)` per entry
- **THEN** the total is under 12,000 characters, so the catalogue renders with descriptions intact rather than degrading to the names-and-paths compact format

#### Scenario: The worked collision is separated

- **WHEN** `multi-source-fusion` and `maintaining-operating-picture` descriptions are compared
- **THEN** one names consolidating disconnected strands into one coherent picture and the other names stopping an already-fused picture from rotting — timestamping, decay on perishable facts, re-verification before reliance — rather than a shared "target picture" phrasing

### Requirement: Skill frontmatter contract

Each `SKILL.md` SHALL declare `name` (lowercase-hyphen, 1-64 characters) and `description` (1-200
characters, per *The description is the selection surface*), and MAY declare `metadata`. It SHALL
declare no other key. A `metadata` block SHALL carry the `acordia` key alone: with the ported library
gone, no `metadata.cyberstrike` block remains anywhere in the tree, and one SHALL NOT be reintroduced
except by a change that ports material and needs a provenance record for it.

Every CyberStrike-only field SHALL stay dropped: `category`, `version`, `author`, `tags`, `owasp_id`,
`cis_id`, `cis_benchmark`, `tech_stack`, `cwe_ids`, `chains_with`, `prerequisites`, `severity_boost`.
The prohibition outlives the port that brought these keys in. The contract has room for exactly three
keys and no harness reads any of the twelve, so the list is what distinguishes a field that is merely
unused from one that is excluded: deleting it along with the library that introduced it would leave
nothing standing between a future import and twelve keys nothing consumes.

The signing triple `sha256` / `signature` / `signed_by` SHALL stay dropped. Every body here is
hand-edited and no step recomputes a digest, so a retained hash is stale on its first edit; a stale
digest is worse than none, because any verifier that honours it reads a legitimately edited skill as
tampered and drops it without saying so, while the body sits intact on disk.

No skill SHALL declare a tool list, a permission map, or any harness-restriction field.

#### Scenario: Only contract fields present

- **WHEN** any skill's frontmatter is parsed
- **THEN** its keys are a subset of `name`, `description`, `metadata`

#### Scenario: Field values are within the contract

- **WHEN** any skill's frontmatter is validated
- **THEN** `name` matches the kebab-case pattern and is at most 64 characters, `description` is 1-200 characters, and the body is non-empty

#### Scenario: No signing or restriction fields

- **WHEN** any skill's frontmatter is inspected
- **THEN** it carries no `sha256`, `signature`, `signed_by`, `tools`, or `permission` key

#### Scenario: No provenance block survives the strip

- **WHEN** any skill's `metadata` block is read
- **THEN** it carries `acordia` and no `cyberstrike` key, because the library that recorded upstream attribution is gone
