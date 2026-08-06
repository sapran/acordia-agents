## ADDED Requirements

### Requirement: Skill frontmatter is parsed and validated before packaging

The generator SHALL parse the frontmatter of every `SKILL.md` it packages, from both pillars, before that skill tree is copied into a staged plugin tree, and SHALL fail the build on any violation rather than packaging the file.

This closes an asymmetry in the generator's own validation surface. Agent files are read through a frontmatter parse that raises on a non-mapping and fails the build; skill trees are copied verbatim, so nothing opens them. The contract being enforced is not new — `analyst-skill-library` already requires each `SKILL.md` to declare a valid `name` and `description` and to exclude `sha256`/`signature`, and `operator-skill-library` already requires the reduced frontmatter and the removal of the signing triple. Those requirements were stated and never executed, which is how a skill with unparseable YAML reached both committed plugin trees.

Byte-level drift detection SHALL NOT be treated as a substitute. `--check` compares the staged tree against the committed tree, so a defect present in both compares equal and reports no drift; only parsing the source detects it.

The validation SHALL cover, for each skill:

- the frontmatter block parses as a YAML mapping;
- `name` matches `^[a-z0-9]+(-[a-z0-9]+)*$`, is at most 64 characters, and equals the name of the containing directory;
- `description` is between 1 and 1024 characters;
- no key is present other than `name`, `description`, and `metadata`;
- none of `sha256`, `signature`, or `signed_by` is present.

The failure SHALL name the offending source file and the specific violation, because the generator's purpose in failing is to send the author back to the source artifact.

#### Scenario: Unparseable skill frontmatter fails the build

- **WHEN** a `SKILL.md` carries frontmatter that is not a valid YAML mapping — for example a `description` whose unquoted value contains a colon-space sequence — and the generator runs
- **THEN** the generator exits non-zero naming that source file
- **AND** neither plugin tree is modified, because the build is staged and swapped rather than written in place

#### Scenario: Folder slug and frontmatter name must agree

- **WHEN** a skill directory's name differs from its frontmatter `name`
- **THEN** the generator exits non-zero naming both values

#### Scenario: A forbidden or unknown frontmatter key fails the build

- **WHEN** a `SKILL.md` declares `sha256`, `signature`, `signed_by`, or any key outside `name`, `description`, and `metadata`
- **THEN** the generator exits non-zero naming that key and that source file

#### Scenario: An out-of-range description fails the build

- **WHEN** a `SKILL.md` declares an empty `description`, or one longer than 1024 characters
- **THEN** the generator exits non-zero naming that source file

#### Scenario: Validation precedes packaging

- **WHEN** any skill in either pillar violates the contract
- **THEN** the generator fails before a staged tree is swapped into place, so no violating skill is ever written to `plugins/`

#### Scenario: A conforming library builds unchanged

- **WHEN** every skill in both pillars satisfies the contract and the generator runs
- **THEN** the build succeeds and the generated trees are byte-identical to those produced before the gate existed, because the gate inspects sources and changes no output

#### Scenario: The gate catches what byte comparison cannot

- **WHEN** a malformed skill is present identically in the source tree and in the committed plugin trees, so that a byte diff of staged output against committed output finds no difference
- **THEN** `tools/build-plugins.py --check` exits non-zero naming that source file, because it builds through the same source validation before it diffs anything
- **AND** the plain build exits non-zero on the same file, so neither entry point can package the defect
