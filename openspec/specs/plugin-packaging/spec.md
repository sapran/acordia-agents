# plugin-packaging Specification

## Purpose

How this distribution is packaged and installed: the two-plugin split into `acordia-analysts` and `acordia-operators`, the two generated plugin trees and the two marketplace catalogs that let one checkout serve both omp and Claude Code, the rule that everything under `plugins/` is committed build output gated by `tools/build-plugins.py --check`, the denylist that carries the read-only posture into Claude Code, and how command wrappers are routed to a plugin.
## Requirements
### Requirement: The repository root is a plugin marketplace

The repository SHALL publish itself as a plugin marketplace carrying exactly two plugins, so that a harness with a plugin system installs the distribution through its own mechanism rather than through a bespoke shell installer. The marketplace SHALL be named `acordia`, and the plugins SHALL be `acordia-analysts` and `acordia-operators`, one per pillar.

The two plugins SHALL be independently installable, because the pillars carry opposite postures: the analysts are read-only decision support and the operators are write-capable offensive tooling. Installing the analytic library SHALL NOT imply installing the offensive one.

#### Scenario: Both plugins are offered separately

- **WHEN** either marketplace catalog is read
- **THEN** it lists exactly the two plugin entries `acordia-analysts` and `acordia-operators`
- **AND** each entry carries its own `source`, `version`, `description`, `category`, and `keywords`

#### Scenario: The analysis pillar installs alone

- **WHEN** `acordia-analysts@acordia` is installed and `acordia-operators@acordia` is not
- **THEN** the four analyst agents, the analyst skill library, and the eight analyst command wrappers are available
- **AND** no operator agent, skill, or command wrapper is installed

#### Scenario: Plugin contents are fixed by pillar

- **WHEN** an installed plugin is inspected
- **THEN** `acordia-analysts` carries the four agents and the skill library of `analysts/`, and `acordia-operators` carries the five agents and the skill library of `operators/`
- **AND** each carries exactly the command wrappers that dispatch its own agents

### Requirement: Two plugin trees, because one agent file cannot serve both harnesses

The distribution SHALL materialise a Claude-shaped tree at `plugins/claude/<plugin>/` and an omp-shaped tree at `plugins/omp/<plugin>/`, both generated from the single opencode-format source under `<pillar>/agents/`, `<pillar>/skills/`, and `commands/acordia/`.

Two trees are required rather than preferred. Both harnesses discover plugin agents at the fixed path `<plugin-root>/agents/`; Claude Code expects a capitalised Claude tool vocabulary while omp expects lowercase omp tool names and additionally requires `spawns` for the orchestrators' delegation allowlists; and Claude Code's manifest `agents` path field supplements the `./agents` default rather than replacing it, so the two harnesses cannot be pointed at different directories inside one plugin. Emitting no tool field at all SHALL NOT be used as an escape, because both harnesses would then inherit every tool and the analysts' read-only posture would be lost in both.

Skills and command wrappers SHALL be byte-identical between the two trees, so that `agents/` is the only directory in which they can differ.

#### Scenario: Only the agent directory differs

- **WHEN** the Claude tree and the omp tree of the same plugin are compared
- **THEN** their `skills/` directories are identical
- **AND** their `commands/` directories are identical
- **AND** their `agents/` directories differ

#### Scenario: Each tree speaks its harness's vocabulary

- **WHEN** an agent file from each tree is read
- **THEN** the omp file carries a lowercase `tools` allowlist, and `spawns` when the source allows dispatch
- **AND** the Claude file carries no `tools` allowlist and no `spawns`

### Requirement: Two marketplace catalogs, one per harness

The repository root SHALL carry `.omp-plugin/marketplace.json` and `.claude-plugin/marketplace.json`. omp reads the former in preference to the latter and falls back only when it is absent, and Claude Code reads the latter, so shipping both is what hands each harness its own tree from one checkout.

The two catalogs SHALL be identical except for the `source` values, which SHALL point at `./plugins/omp/<plugin>` and `./plugins/claude/<plugin>` respectively. Each SHALL carry only keys both catalog schemas document — `name`, `owner`, `metadata`, and per entry `name`, `source`, `version`, `description`, `category`, `keywords` — because omp logs and skips a plugin entry it considers invalid, so a speculative field risks silently dropping a plugin.

#### Scenario: Catalogs differ only in their sources

- **WHEN** the two catalogs are compared
- **THEN** every field is equal except the two `source` values
- **AND** the omp catalog's sources name `./plugins/omp/…` while the Claude catalog's name `./plugins/claude/…`

#### Scenario: Each plugin directory carries a manifest

- **WHEN** a plugin directory in either tree is inspected
- **THEN** it carries `.claude-plugin/plugin.json` naming the plugin, its version, description, author, repository, and keywords
- **AND** the manifest declares no `commands`, `agents`, or `skills` path key, because the defaults are exactly what the tree uses and the fields supplement rather than replace

### Requirement: Generated trees are committed and gate-checked

Everything under `plugins/`, `.claude-plugin/`, and `.omp-plugin/` SHALL be build output produced by `tools/build-plugins.py` from the opencode-native sources, and SHALL be committed, because a marketplace install clones the repository and performs no build on the installing machine.

A plain build SHALL stage the whole tree in a temporary directory and swap it into place only on success, replacing each generated path wholesale, so that a renamed or removed source artifact cannot leave an orphan behind and a failed build cannot leave the committed tree deleted or half-written. `tools/build-plugins.py --check` SHALL build into a temporary directory, diff against the committed tree, name every missing, extra, and differing path, and exit non-zero on any mismatch, without writing anything outside that temporary directory. Editing a file under `plugins/` SHALL be treated as a drift bug rather than as a change.

#### Scenario: The generator is deterministic

- **WHEN** `tools/build-plugins.py` runs twice in succession
- **THEN** the second run leaves the tree byte-identical to the first

#### Scenario: Drift is reported and fails

- **WHEN** a file under `plugins/` is edited by hand and `tools/build-plugins.py --check` runs
- **THEN** the command exits non-zero naming that path as differing
- **AND** no file outside the temporary build directory is modified

#### Scenario: A removed source artifact leaves no orphan

- **WHEN** a skill directory is deleted from a pillar and the generator runs
- **THEN** the corresponding directory is absent from both plugin trees

#### Scenario: A failed build leaves the committed tree intact

- **WHEN** a source artifact is malformed and the generator runs
- **THEN** it exits non-zero naming that source file
- **AND** the previously committed trees are unchanged, because the build is staged and swapped rather than written in place

### Requirement: Claude Code posture is expressed as a denylist

A Claude Code plugin agent SHALL carry `disallowedTools`, never a `tools` allowlist, because an allowlist would have to enumerate the harness's whole tool vocabulary and would silently strip tools this repository never audited. The denylist SHALL be derived from the same source signals the omp emitter reads:

| source signal | contributes to `disallowedTools` |
| --- | --- |
| `permission.edit` denies writing outright | `Edit`, `Write`, `NotebookEdit` |
| `permission.edit` is path-scoped | `Edit`, `NotebookEdit` — `Write` is retained |
| `permission.edit: allow` | nothing |
| `permission.task` allows no agent | `Task` |

`disallowedTools` SHALL be omitted entirely when the derived list is empty.

The path-scoped row deliberately diverges from the omp emitter, which drops the tool. `Write` is retained because denying it outright would leave the two reporting analysts unable to produce the reports the competency grid assigns them, and the report sink they write into is a prompt-level convention rather than an enforced scope — in opencode as much as here, since `bash: allow` is an unrestricted write channel in every harness (see `analyst-agent-roster`). The rationale SHALL be stated in those terms and SHALL NOT read as opencode confining the writes while Claude Code fails to.

#### Scenario: Read-only analyst is denied every write tool

- **WHEN** an agent whose source denies `edit` outright and allows no dispatch is emitted for Claude Code
- **THEN** its `disallowedTools` names `Edit`, `Write`, `NotebookEdit`, and `Task`

#### Scenario: Scoped reporting analyst keeps Write

- **WHEN** an agent whose source scopes `edit` to a report path and allows no dispatch is emitted for Claude Code
- **THEN** its `disallowedTools` names `Edit`, `NotebookEdit`, and `Task`
- **AND** it does not name `Write`

#### Scenario: Write-capable orchestrator is denied nothing

- **WHEN** an agent whose source grants `edit: allow` and allows dispatch is emitted for Claude Code
- **THEN** its frontmatter carries no `disallowedTools` key

### Requirement: Postures Claude Code cannot express are recorded in the generated file

Claude Code plugin agents silently ignore `metadata`, `hooks`, `mcpServers`, and `permissionMode`, so the provenance and permission-gap record the omp emitter places in `metadata.generated` has no frontmatter home. The Claude emitter SHALL therefore write comment lines above the frontmatter keys: always the generating tool and the repo-relative source path, and conditionally one note per posture the harness cannot express — the spawn allowlist, the path-scoped write, and the per-command bash denies.

The path-scoped-write note SHALL describe the report sink as a convention no harness enforces, on the same grounds as the omp emitter's note. It SHALL NOT state or imply that the confinement is prompt-level *here* in contrast to being enforced in the source harness.

#### Scenario: Provenance is always present

- **WHEN** any Claude plugin agent file is read
- **THEN** its first comment line names the repo-relative source path and `tools/build-plugins.py`, and states that the file is not to be edited

#### Scenario: Spawn allowlist gap recorded

- **WHEN** an agent whose source allows dispatch to named agents is emitted for Claude Code
- **THEN** a comment states that plugin agents cannot express a spawn allowlist and that the prompt names the agents this one dispatches

#### Scenario: Path scope gap recorded as a universal convention

- **WHEN** an agent whose source scopes writes to a report path is emitted for Claude Code
- **THEN** a comment states that the sink is a prompt-level convention enforced by no harness
- **AND** the comment does not contrast Claude Code against the source harness

#### Scenario: Bash deny gap recorded

- **WHEN** an agent whose source carries per-pattern bash denies is emitted for Claude Code
- **THEN** a comment states that plugin agents cannot express per-command bash rules and that those denies are prompt-level

### Requirement: Command wrappers are routed by the agent they name

Each `commands/acordia/<stem>.md` SHALL be placed in whichever plugin owns the agent its body names. The agent SHALL be read from the wrapper's opening sentence, which is one of two shapes — a dispatch sentence for a leaf agent, or a hand-the-work sentence for an orchestrator, which must additionally name a session-switch fallback. A wrapper matching neither shape, or naming an agent belonging to no pillar, SHALL fail the build naming that wrapper rather than being guessed at.

The emitted wrapper SHALL carry `description` and `argument-hint` only, preserving their values verbatim along with any trailing comment line, and SHALL drop `name` (the handle is now supplied by the plugin prefix) and `category` (a key in neither plugin schema). The body SHALL be copied unchanged, including `$ARGUMENTS`.

Wrappers SHALL be emitted flat at `<plugin-root>/commands/<stem>.md`, because omp's plugin command provider scans that directory non-recursively and a subdirectory would be invisible to it.

#### Scenario: Wrappers follow their agent's pillar

- **WHEN** the plugin trees are generated
- **THEN** every wrapper naming an analyst agent is in `acordia-analysts` and every wrapper naming an operator agent is in `acordia-operators`

#### Scenario: An unroutable wrapper fails the build

- **WHEN** a wrapper's body names no agent, or names an agent in no pillar
- **THEN** the generator exits non-zero naming that wrapper
- **AND** no plugin tree is left partially written in the repository

#### Scenario: Frontmatter is reduced, not rewritten

- **WHEN** a generated wrapper is compared with its source
- **THEN** its `description` and `argument-hint` values are unchanged, and any trailing comment line is preserved
- **AND** it carries no `name` and no `category`
- **AND** its body is byte-identical to the source body

### Requirement: The plugin version is hand-maintained and bumped on every change

The catalogs and plugin manifests SHALL carry a hand-maintained `MAJOR.MINOR.PATCH` version, declared once in the generator, and it SHALL be bumped by whoever changes a source artifact. MINOR SHALL move for any change that reaches a user — an agent prompt, a skill body, a command wrapper, or the generator's emitted output. MAJOR SHALL move for a change to the roster, to a pillar, or to the shape of the distribution.

The version is the only update signal either plugin harness has. omp compares the catalog version against the installed one and skips when they match, so an unbumped version means an edited artifact never reaches an already-installed user, and it fails silently — no error and no warning distinguishes it from being up to date. The obligation to bump therefore SHALL be stated as a rule in the repository's own contributor guidance, not left implicit in the generator.

The version SHALL be real semantic versioning and SHALL increase monotonically, because a hand-maintained version can be ordered and both harnesses then compare it by precedence. Verified against omp 17.1.8: a newer semver reinstalls and an older one is skipped.

The version SHALL NOT be derived from source content or from a git revision, and SHALL NOT carry semver build metadata. Two versions differing only in build metadata compare **equal** and never upgrade, so a `MAJOR.MINOR.PATCH+<hash>` form would be a silent no-op — accepted by both harnesses and propagating to neither.

A targeted upgrade naming one plugin reinstalls unconditionally and compares nothing. It SHALL NOT be used as evidence of version semantics.

The obligation SHALL additionally be gate-checked, because stating it in contributor guidance did not prevent a source artifact from being committed without a bump. `tools/build-plugins.py --check` SHALL exit non-zero when any generated artifact under `plugins/`, `.claude-plugin/`, or `.omp-plugin/` — the surface that actually reaches an installed user — differs from the git base, whether that artifact is already tracked or newly added, while the declared version does not exceed the published version, compared as a semver tuple. Gating on the generated surface rather than on the source directories is deliberate: a change to the generator itself can alter emitted output without touching any source file, and the drift comparison does not backstop that, because it compares built bytes against committed bytes and both carry the new output once the author rebuilds.

The set of changed artifacts SHALL be diffed against the merge base with the integration branch, so the obligation is one bump per release rather than one per commit; a branch that bumps once and then edits further artefacts SHALL pass. The published version SHALL be read from the integration branch's tip, not from the merge base, because the obligation is relative to what is already released: two branches forking at the same version must not both ship it, and a branch that later merges the integration branch must not regress below it. When git is unavailable, the tree is not a git checkout, no base branch resolves, or a version cannot be parsed, the check SHALL report that the version gate was skipped and SHALL NOT fail — an unresolvable base is not evidence of a missing bump.

The gate SHALL apply to `--check` only and SHALL NOT apply to a plain build, because a plain build runs continuously while editing and failing it on an unbumped version would make the generator unusable for its primary purpose.

#### Scenario: A newer version propagates

- **WHEN** the catalog version is bumped above the installed version
- **AND** the upgrade-all path runs
- **THEN** the plugin is reinstalled at the new version

#### Scenario: An unchanged version is a no-op

- **WHEN** the catalog version equals the installed version
- **AND** the upgrade-all path runs
- **THEN** nothing is reinstalled

#### Scenario: The bump obligation is written down

- **WHEN** the repository's contributor guidance is read
- **THEN** it states that a source change without a version bump is a release bug
- **AND** it gives the MINOR and MAJOR criteria

#### Scenario: Build-metadata versioning is rejected as a design

- **WHEN** the version scheme is inspected
- **THEN** it carries no hash and no build metadata
- **AND** the reason is recorded, because that form is accepted by both harnesses yet never upgrades

#### Scenario: A generated change with no bump fails the check

- **WHEN** a generated artifact under `plugins/`, `.claude-plugin/`, or `.omp-plugin/` differs from the base — whether already tracked or newly added — and the declared version does not exceed the published version
- **THEN** `tools/build-plugins.py --check` exits non-zero naming the changed artifacts and both versions

#### Scenario: A generated change with a bump passes

- **WHEN** generated artifacts differ from the base and the declared version is strictly greater than the published version
- **THEN** the version gate passes and `--check` reports only whatever generated-tree drift it finds independently

#### Scenario: One bump covers a whole branch

- **WHEN** a branch has already bumped the version above the published version and then changes further artefacts without bumping again
- **THEN** the version gate passes, because the obligation is one bump per release rather than one per commit

#### Scenario: A change touching no generated artifact needs no bump

- **WHEN** the only differences from the base leave the generated trees untouched — a documentation or planning-artifact edit, for example
- **THEN** the version gate passes with the version unchanged

#### Scenario: An unresolvable base skips rather than fails

- **WHEN** git is unavailable, the tree is not a git checkout, or no integration branch resolves
- **THEN** `--check` reports that the version gate was skipped
- **AND** the absence of a base does not by itself fail the check

#### Scenario: A plain build is never blocked by the version gate

- **WHEN** source artifacts have changed with no version bump and `tools/build-plugins.py` runs without `--check`
- **THEN** the build succeeds, because the gate is scoped to the check path

### Requirement: Agent-name resolution differs by harness and is documented

A plugin agent's dispatch handle SHALL be documented per harness, because the harnesses disagree and a single documented form would be wrong for one of them. Verified against Claude Code 2.1.220: plugin agents are namespaced there, so the dispatch name is `<plugin>:<agent>` and the bare agent name fails as an unrecognised type. omp and opencode register agents flat, by bare name.

The command wrappers SHALL remain the portable entry point, naming their agent in prose so each harness resolves it in its own idiom.

#### Scenario: Claude Code requires the namespaced handle

- **WHEN** a plugin agent is dispatched in Claude Code by its bare name
- **THEN** the dispatch fails as an unrecognised agent type
- **AND** the same dispatch succeeds as `<plugin>:<agent>`

#### Scenario: Documentation states both forms

- **WHEN** the install documentation is read
- **THEN** it states the namespaced form for Claude Code and the bare form for omp and opencode

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

