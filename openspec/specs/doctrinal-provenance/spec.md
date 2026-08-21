# doctrinal-provenance Specification

## Purpose
Makes the distribution's literature grounding checkable, the way `competency-map-derivation` makes
its grid grounding checkable. A source register names every work the doctrine draws on together with
its lib.ai document id; a doctrinal claim traces to a work and a section rather than to recall; and an
empty search is recorded instead of filled in.

## Requirements

### Requirement: One source register introduces every work

`docs/roles/sources.md` SHALL be the single register of the works the distribution's doctrine draws
on. Each entry SHALL carry a short **key** used to cite it elsewhere, the author, the title, and the
lib.ai library document id, so any claim attributed to it can be re-read at its source rather than
argued from memory.

The register SHALL be the only place a work is introduced. Every other document SHALL cite a work by
its register key plus the section or pages it draws on, never by restating the bibliographic entry.
The `### Sources (library)` list in `docs/roles/operational-analyst.md` SHALL accordingly be reduced
to register keys with the sections each row's prose rests on; the fourteen works it currently spells
out, and the eight in `docs/methodology-alignment-proposal.md` §1, are the register's initial content.

A work that is not in the library SHALL still be registered, with the document id recorded as absent
and a note stating where the text can be obtained and whether it can be ingested. An attribution to a
work with no document id is permitted only where the register carries that note, because otherwise the
claim cannot be re-read by anyone.

#### Scenario: A work is introduced once

- **WHEN** `docs/roles/sources.md` is read
- **THEN** every work the doctrine cites appears exactly once, with a key, author, title and lib.ai document id

#### Scenario: A citing document carries no bibliography

- **WHEN** a competency grid paragraph, an agent prompt or a doctrine skill cites a work
- **THEN** it names the register key and the section, and does not repeat the author, title or document id

#### Scenario: An unavailable work is registered rather than cited loosely

- **WHEN** a work the doctrine rests on is absent from the library
- **THEN** the register still holds its entry, with the document id marked absent and a note on where the text can be obtained

### Requirement: A doctrinal claim traces to a work and a section

Any normative or methodological claim — a claim about *how the work is divided, why a judgement is
made this way, or what an operation is for* — appearing in a competency grid paragraph, an agent
prompt, or a doctrine skill SHALL be attributable to a named register key and a section or page range
within it. The attribution SHALL be readable in the citing document; a claim whose only support is
the author's recollection is not grounded.

Technique detail SHALL NOT be attributed to the literature. A procedure, tool behaviour, artefact
format, protocol quirk or triage rule traces to its grid row through the `row` / `source` anchor
that `competency-map-derivation` defines — the stable row identifier being owned by the grid row
itself — and adding a literature citation to it would falsely imply a work prescribes it.

#### Scenario: A doctrinal paragraph names its source

- **WHEN** a grid leg's prose paragraph asserts why a leg exists or how its judgement is framed
- **THEN** it names the register key and section that claim is drawn from

#### Scenario: Technique detail stays anchored to the grid

- **WHEN** a skill's Method section describes a procedure or an artefact format
- **THEN** it traces to its grid row and carries no literature attribution

### Requirement: A doctrinal skill names its work in frontmatter

Where a skill body rests on a specific work rather than on general practice, its `metadata.acordia`
block SHALL carry `doctrine_source`: a list of register references, each `<key>` or
`<key>#<section>`, where `<key>` is a key defined in `docs/roles/sources.md`. It sits alongside
`family`, `row` and `source`, and follows their style: a short machine-readable value naming where the
content came from, not a citation string.

`doctrine_source` SHALL be present only where the dependency is real. A skill that codifies common
practice SHALL omit the field entirely rather than carry an empty list, so its presence means
something. The field records grounding and SHALL NOT replace `row` / `source`: a grid-row skill keeps
its grid anchor whether or not it also rests on a work.

#### Scenario: A doctrinal skill declares its work

- **WHEN** a skill whose body rests on a specific work is inspected
- **THEN** its `metadata.acordia.doctrine_source` lists one or more register references, each resolving to a key in `docs/roles/sources.md`

#### Scenario: A practice skill carries no field

- **WHEN** a skill that codifies general practice is inspected
- **THEN** it has no `doctrine_source` key, and its grid anchor is unchanged

### Requirement: An empty literature search is a recorded finding

Where the library was searched for support on a point and holds nothing, that SHALL be recorded — in
the register's gaps section or in the change's design document — naming what was searched for and
which works were searched. The claim SHALL then either be restated as practice and anchored to a grid
row, or dropped. It SHALL NOT be filled from recall and presented as grounded.

This is the invariant that stops invented content, which is this repository's characteristic defect:
an agent that cannot find a citation is far more likely to write a plausible one than to report the
absence.

#### Scenario: A gap is written down

- **WHEN** a search for support on a doctrinal point returns nothing
- **THEN** the point and the searched works are recorded as a gap, and the claim is either re-anchored to a grid row or removed

#### Scenario: A confident citation with no register entry is rejected

- **WHEN** a citation names a work, page or passage that no register entry supports
- **THEN** it is treated as invented and removed, not verified after the fact by adding a register entry to match it

### Requirement: Every attribution resolves, and is checked

The external check script `~/ai/checks/check-acordia.sh` SHALL gain a check that every register
reference in the repository resolves to an entry in `docs/roles/sources.md` — every
`doctrine_source` item in every skill's frontmatter, and every register key cited in prose. There is
no build and no test suite here; that script and a reviewer are the only gates, so the check is where
the invariant becomes enforceable rather than aspirational.

An unresolvable attribution SHALL be a defect of the same class as a `·`-separated prompt skill slug
that resolves to no skill: the script names the offending file and value, and the change does not
ship until it resolves.

#### Scenario: Unresolvable attribution fails the check

- **WHEN** a skill carries `doctrine_source` naming a key absent from `docs/roles/sources.md`
- **THEN** the check script fails, naming the skill file and the unresolved key

#### Scenario: A clean tree passes

- **WHEN** the check script runs against a tree whose every register reference resolves
- **THEN** it reports no provenance failure, alongside the version-lockstep, catalog-identity and prompt-slug checks
