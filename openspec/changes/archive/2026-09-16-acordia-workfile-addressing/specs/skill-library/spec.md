## ADDED Requirements

### Requirement: `briefing-reporting` states the workfile addressing scheme

`briefing-reporting` is the skill every prompt defers to for the task directory's shape, so it SHALL
carry the addressing scheme rather than leaving each prompt to restate it. It SHALL state all four of
the following.

**The parent.** Where a dispatch names no working directory, the task directory is created under
`.acordia/work/` — not in the current directory and not under a bare slug. The skill SHALL state the
reason with the rule: the current directory is where the corpus lives, and a working file written
there is exactly what `.acordia/` exists to keep out of the material under analysis.

**The stem.** The directory is named `<corpus>-<YYYY-MM-DD>-<task-slug>`, and the product written
from it takes the same stem under `.acordia/reports/`. The skill SHALL state that a date alone does
not identify a corpus, and that two corpora swept on one day therefore resolve to one name.

**The corpus token.** It is derived from the material rather than from the request — an Aleph
collection's `foreign_id`, falling back to a slug of its label, and for a file corpus a slug of the
analysed directory or archive name. The skill SHALL state why the derivation runs that way round: a
token taken from the request text splits one corpus across two directories whenever two dispatches
word the same work differently.

**The collision rule.** A stem already taken takes a numeric suffix (`-2`, `-3`) for both the
directory and its product. The skill SHALL state that a colliding write **succeeds** — nothing in
either harness reports it — so the suffix is the only thing standing between a second run and the
silent replacement of the first run's product.

The directory SHALL continue to hold a `README.md` carrying the request **verbatim**, its date and
one line on what is being settled, as it does today; the addressing scheme names that directory and
does not change what it holds.

The scheme SHALL be stated as a convention. No part of it is enforced by either harness, and the
skill SHALL NOT present it as a restriction on where a write can land.

#### Scenario: The parent is named for the unbriefed case

- **WHEN** `briefing-reporting` states what to do where a dispatch names no working directory
- **THEN** it names `.acordia/work/` as the parent, and neither instructs nor permits creating the
  directory in the current directory or under a bare dated slug

#### Scenario: The stem is stated with its report counterpart

- **WHEN** the naming rule is read
- **THEN** it gives `<corpus>-<YYYY-MM-DD>-<task-slug>` for the directory and the same stem for the
  product under `.acordia/reports/`

#### Scenario: The derivation is stated, not assumed

- **WHEN** the corpus token's derivation is read
- **THEN** it names the Aleph `foreign_id`, the label slug as fallback, and the analysed directory or
  archive name for a file corpus, and states that the token comes from the material rather than the
  request

#### Scenario: The collision rule states the silent failure

- **WHEN** the collision rule is read
- **THEN** it gives the numeric suffix for both directory and product, and states that a colliding
  write succeeds without any harness reporting it

#### Scenario: The scheme is a convention

- **WHEN** the scheme is read end to end
- **THEN** it is presented as a convention every analyst follows, with no claim that a harness
  enforces any part of it

### Requirement: A credential file is addressed by the directory that holds it

`credential-harvest-triage` SHALL continue to require a credential file separate from the notes,
placed beside them in the task directory and named in them. It SHALL NOT restate the addressing
scheme: the file's address follows from the directory's, so the skill names the placement and defers
the naming to `briefing-reporting`.

Where `credential-harvest-triage` or its `references/report-layout.md` describes a working file or a
product as "named relative to the working directory", that directory SHALL be the addressed task
directory, so a credential file produced by two sweeps on one day is held apart by its parent rather
than by its own name.

#### Scenario: The credential file inherits the address

- **WHEN** `credential-harvest-triage` states where the credential file goes
- **THEN** it places the file beside the notes in the task directory without restating the stem
  rule, which `briefing-reporting` carries

#### Scenario: Two sweeps keep separate credential files

- **WHEN** two credential sweeps run on one date against two different corpora
- **THEN** each writes its credential file into its own addressed task directory, and neither
  overwrites the other
