## ADDED Requirements

### Requirement: A committed lint policy governs the authored markdown

The repository SHALL carry a `.markdownlint-cli2.jsonc` at its root declaring which markdownlint rules
apply to its own markdown and which paths are out of scope. Applying it to every file it does not
exclude SHALL report zero violations.

The file SHALL be `.markdownlint-cli2.jsonc` and exclusions SHALL live in its `ignores` array. A
`.markdownlintignore` SHALL NOT be used: neither markdownlint-cli2 nor the
`DavidAnson.vscode-markdownlint` extension reads that filename — only the legacy markdownlint-cli v1
does, and nothing here invokes it — so exclusions placed there are silently inert.

A rule this repository violates by intent SHALL be disabled with its reason recorded beside it, rather
than left firing. An editor reporting thousands of violations teaches its reader to ignore the report,
which costs more than the rules were worth: the failure this guards against is an author correcting
what the editor flagged and disturbing a convention the editor knew nothing about.

`openspec/changes/` SHALL be excluded. OpenSpec mandates that a delta spec opens with
`## ADDED Requirements` or `## MODIFIED Requirements`, which can never satisfy a first-line-heading
rule, and archived changes are immutable by contract so a violation there could not be fixed anyway. Vendored tooling under `.claude/` and `.codex/` SHALL be excluded, because it is not
part of the distribution and its upstream owns its formatting.

Because the rule set grows between markdownlint releases, the policy SHALL record the version it was
verified against, and a change that adopts a newer version SHALL re-verify the zero.

The policy SHALL NOT be enforced by a build step or a hook. This repository ships no build, and a lint
gate would be the first. It is an authoring convention.

An automated fix SHALL NOT be trusted without inspecting every line it changed. Verified 2026-08-21:
markdownlint's own `--fix` read the JavaScript property `__proto__` in `attack-prototype-pollution` as
strong emphasis and rewrote it to `**proto**`, destroying the literal payload the skill exists to
document. Emphasis-normalising rules are unsafe next to identifiers that carry underscores.

#### Scenario: The committed tree is clean under its own policy

- **WHEN** the rule set in `.markdownlint-cli2.jsonc` is applied to every file its `ignores` array does not exclude
- **THEN** no violation is reported

#### Scenario: A disabled rule carries its reason

- **WHEN** `.markdownlint-cli2.jsonc` disables a rule
- **THEN** a comment beside it records why this repository violates that rule by intent

#### Scenario: Exclusions live where a tool will read them

- **WHEN** the repository is searched for a `.markdownlintignore`
- **THEN** none exists, and the exclusions are in the `ignores` array of `.markdownlint-cli2.jsonc`

#### Scenario: OpenSpec changes and vendored tooling are out of scope

- **WHEN** the `ignores` array is read
- **THEN** it excludes `openspec/changes/`, `.claude/` and `.codex/`

#### Scenario: The verified tool version is recorded

- **WHEN** the lint policy is read
- **THEN** it names the markdownlint version its zero was verified against

#### Scenario: Adopting a newer linter re-verifies the zero

- **WHEN** a change raises the markdownlint version the policy names
- **THEN** that change re-runs the linter and records the new zero, because a newer release adds rules

#### Scenario: An automated fix is inspected line by line

- **WHEN** an automated fix is applied to this tree
- **THEN** every line it changed is classified before the change is committed, and any edit to prose or to an identifier is reverted

#### Scenario: No gate is introduced

- **WHEN** the repository is searched for a lint invocation in a build script, hook or workflow
- **THEN** none exists
