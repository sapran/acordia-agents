## ADDED Requirements

### Requirement: The retired omp filesystem deployment has a migration

The distribution SHALL ship a migration that removes the artifacts the retired `--harness omp` install path left under the omp agent root, because those artifacts do not merely go stale — they **shadow the plugin**. omp resolves task agents from the user's own agent directory before it reaches plugin roots and deduplicates by name first-wins, so a translated file left from the old path silently supersedes the plugin's agent of the same name, and the user runs superseded prompts with no indication that they are.

The migration SHALL default to reporting rather than deleting, and SHALL require an explicit flag to remove anything.

The migration SHALL remove only artifacts for which this repository's provenance can be demonstrated, and SHALL report and leave in place anything else, on the same principle that governs the installer and uninstaller: a name match is not proof of origin.

Its evidence rule for an agent SHALL be the retired provenance rule, not the shared one. The shared ownership evidence now tests a copied agent by byte-identity with its source, which no translated agent has ever satisfied by construction; applying it here would refuse to recognise every artifact the migration exists to remove. Both halves SHALL hold: the generated block naming the tool that produced the file, and a recorded source path that resolves to a file that really exists in this repository. Skills SHALL use the shared rule unchanged.

#### Scenario: Shadowing artifacts are identified

- **WHEN** the migration runs against an omp agent root carrying a previous deployment
- **THEN** it names every translated agent and deployed skill it would remove

#### Scenario: Reporting is the default

- **WHEN** the migration runs with no flag
- **THEN** nothing is created, removed, or modified
- **AND** it states which flag performs the removal

#### Scenario: A stranger's file is left alone

- **WHEN** a file whose name matches a repository agent occupies the omp agent root but carries no provenance from this repository
- **THEN** the migration leaves it in place
- **AND** reports how many such artifacts it declined to remove

#### Scenario: A translated agent is recognised despite differing from its source

- **WHEN** the migration considers a translated agent that is not byte-identical to its opencode source
- **THEN** it is recognised as this repository's artifact on the strength of its generated provenance
- **AND** the shared byte-identity rule is not what decides it
