# omp-harness-distribution Specification

## Purpose

How the opencode-native source artifacts under `<pillar>/` reach omp (`oh-my-pi`): the agent frontmatter translation contract, the committed plugin tree the translated agents are generated into, and the permission-model gaps that translation cannot close.

## Requirements

### Requirement: Source artifacts stay opencode-native

The files under `<pillar>/agents/` and `<pillar>/skills/` SHALL remain written to the opencode contract and SHALL be the only editable source for every harness. Distribution to omp SHALL be produced by translating those files, never by maintaining a parallel set.

The translated form is no longer transient. It is generated into the committed plugin tree at `plugins/omp/<plugin>/agents/`, because a marketplace install clones the repository and performs no build on the installing machine. That tree is build output all the same: it is regenerated wholesale on every build and gated by `tools/build-plugins.py --check`, so editing it is a drift bug rather than a change.

#### Scenario: Committed omp agent copies are generated, never authored

- **WHEN** the repository is inspected for tracked agent files
- **THEN** the only editable agent prompts are `<pillar>/agents/*.md` in opencode frontmatter form
- **AND** every omp-form agent file lives under `plugins/omp/`, is committed, and declares in its generated metadata the source path it came from
- **AND** `tools/build-plugins.py --check` reproduces every one of them byte-for-byte

#### Scenario: Source edit reaches every harness

- **WHEN** a prompt body in `<pillar>/agents/*.md` is edited
- **THEN** rebuilding the plugin trees carries the edited body into both the omp and the Claude agent files
- **AND** reinstalling for opencode carries it into the opencode deployment

#### Scenario: Editing the generated tree is caught

- **WHEN** a file under `plugins/omp/` is edited without editing its source
- **THEN** `tools/build-plugins.py --check` exits non-zero naming that path

### Requirement: Frontmatter translation contract

The translator SHALL convert one opencode agent file into one omp task-agent file according to a fixed mapping. The generated file SHALL carry a `name` field equal to the source filename stem and SHALL preserve the source `description` verbatim, because omp skips any agent file lacking either field.

The emitted `tools` allowlist SHALL be derived from the source `permission` map rather than from a fixed list, so that a write-capable pillar translates as faithfully as a read-only one. The derivation is:

- always present: `read`, `grep`, `glob`, `bash`, `web_search`, `todo`, and `yield` (omp appends `yield` itself; naming it keeps the generated file honest)
- `edit` and `write` are present when the source `permission.edit` is not a denial — that is, when it is `allow`, or a path map with at least one `allow`
- `browser` is present when the source `permission.browser` is `allow`
- `task` is present, and `spawns` lists the allowed agent names, when the source `permission.task` map names at least one allowed agent

The generated file SHALL additionally carry a `color`, because omp renders every agent in one flat picker shared with its own built-ins and the user's own agents — the same visual-namespace problem the `ACORDIA <pillar> — ` description tag solves for text. The colour SHALL be derived from the `metadata.acordia` block the source already declares rather than from a filename table, so the pillar keeps one source of truth for which agent is the orchestrator: the analyst pillar names it in `leg`, the operators pillar in `role`, and either field reading `orchestrator` emits `cyan`. Every other value — and a source carrying no `metadata.acordia` block at all — emits `blue`, the specialist default.

#### Scenario: Required fields emitted

- **WHEN** any `<pillar>/agents/<stem>.md` is translated
- **THEN** the output frontmatter contains `name: <stem>`
- **AND** the output frontmatter contains the source `description` unchanged

#### Scenario: Orchestrator and legs are visually distinguishable

- **WHEN** an agent declaring `metadata.acordia.leg: orchestrator` (analyst pillar) or `metadata.acordia.role: orchestrator` (operators pillar) is translated alongside an agent declaring any other value
- **THEN** the orchestrator's output carries `color: cyan` and the other carries `color: blue`

#### Scenario: Colour falls back for an agent with no orchestrator declaration

- **WHEN** an agent carrying no `metadata.acordia` block, or one naming neither `leg` nor `role` as `orchestrator`, is translated
- **THEN** the output frontmatter carries `color: blue`

#### Scenario: Read-only posture becomes an absent tool

- **WHEN** a source agent carries `permission.edit` denying `"*"`
- **THEN** the output `tools` allowlist contains neither `edit` nor `write`
- **AND** the running agent has no `edit` tool

#### Scenario: Write-capable posture becomes present tools

- **WHEN** a source agent carries `permission.edit: allow`
- **THEN** the output `tools` allowlist contains both `edit` and `write`

#### Scenario: Browser capability carried over

- **WHEN** a source agent carries `permission.browser: allow`
- **THEN** the output `tools` allowlist contains `browser`

#### Scenario: Analysis shell preserved

- **WHEN** a source agent carries `permission.bash: allow`
- **THEN** the output `tools` allowlist contains `bash`

#### Scenario: Per-command bash denies do not remove the shell

- **WHEN** a source agent carries `bash: allow` together with per-pattern `deny` rules
- **THEN** the output `tools` allowlist still contains `bash`
- **AND** the generated metadata records that omp has no per-command equivalent, so those denies are prompt-level under omp

#### Scenario: Leaf specialist cannot dispatch

- **WHEN** a source agent carries `mode: subagent` and `permission.task: deny`
- **THEN** the output `tools` allowlist does not contain `task`
- **AND** the output frontmatter declares no `spawns`

#### Scenario: Orchestrator dispatches exactly its named legs

- **WHEN** a source agent carries `mode: primary` and a `permission.task` map allowing named agents
- **THEN** the output `tools` allowlist contains `task`
- **AND** the output `spawns` lists exactly those names

#### Scenario: Provenance metadata preserved

- **WHEN** a source agent carries a `metadata.acordia` or `metadata.cyberstrike` block
- **THEN** the output frontmatter carries that block unchanged
- **AND** the output frontmatter records that the file is generated, naming its source path

### Requirement: Prompt text corrected for omp's tool set

omp provides no `list` tool; a directory path given to `read` enumerates it. The translator SHALL fail rather than emit a prompt naming a `list` tool, and that check — a `list` token surviving in the body after rewriting — is the enforced guarantee, whichever pillar the prompt comes from.

Two rewrites feed that check. The translator SHALL replace the inline `` `read`/`grep`/`glob`/`list` `` token wherever it appears, and SHALL replace the legacy analyst Tool-discipline paragraph, byte-exact, with an omp-correct version naming no `list`. Both rewrites are **best-effort fallbacks for wording that still names the tool**: their absence from a prompt is not an error, because a prompt that never names `list` needs no correction. In particular, a prompt carrying a `## Tool discipline` section in wording the rewrite does not recognise SHALL translate cleanly so long as no `list` token survives — the translator SHALL NOT require a Tool-discipline paragraph to match a fixed text.

#### Scenario: Legacy paragraph rewritten

- **WHEN** an agent file whose Tool-discipline paragraph matches the legacy wording naming `list` is translated
- **THEN** the emitted paragraph does not name a `list` tool
- **AND** the emitted paragraph states that `read` on a directory path lists its entries

#### Scenario: Prompt without the paragraph translates cleanly

- **WHEN** an agent file carrying no Tool-discipline paragraph and no `list` reference is translated
- **THEN** translation succeeds and the body is emitted unchanged

#### Scenario: Unrecognised Tool-discipline wording is not an error

- **WHEN** an agent file carrying a `## Tool discipline` section in wording other than the legacy paragraph, and naming no `list` tool, is translated
- **THEN** translation succeeds and the section is emitted unchanged

#### Scenario: Surviving `list` reference aborts translation

- **WHEN** a source prompt names a `list` tool in wording the translator cannot rewrite
- **THEN** the translator exits non-zero naming the offending file
- **AND** no output file is written for it

### Requirement: Unmappable permissions are surfaced, not silently resolved

omp allowlists whole tools, cannot scope a tool to a path, and cannot remove `write` at all while its `tools.xdev` setting is on, because `read` and `write` are the transport for every `xd://` device. The source files' `".acordia/reports/**": allow` write exception therefore has no faithful translation.

Where a source declares a path-scoped `edit`, the translator SHALL emit `write` and SHALL NOT emit `edit`, and SHALL record in the generated file that the path scope is a prompt-level convention no harness enforces. This resolves a divergence in which one source posture produced opposite capability in the two plugin harnesses: the omp emitter withheld every write tool while the Claude emitter kept `Write` allowed, so an agent whose prompt requires it to produce a report held the means to do so in one harness and not the other.

The emitted capability is the honest one. `write` survives in omp as an `xd://` transport tool whenever `tools.xdev` is on, and `bash: allow` is an open write channel at any path in all three harnesses, so an agent with a scoped `edit` can already write anywhere; the generated note SHALL state that outcome rather than imply a boundary the harness keeps.

A blanket `edit: deny` SHALL continue to emit neither `edit` nor `write`, with the note recording that omp exposes `write` regardless while `tools.xdev` is on.

#### Scenario: A path-scoped edit yields a write tool

- **WHEN** a source agent declares `edit` as `"*": deny` followed by a path-scoped `allow`
- **THEN** the generated omp agent's `tools` list includes `write` and excludes `edit`
- **AND** the generated note states that the path scope is an unenforced convention and that the agent can write anywhere

#### Scenario: The two plugin harnesses agree on the posture

- **WHEN** the same path-scoped source is translated for both harnesses
- **THEN** both generated agents hold a write capability and neither holds a general edit capability, so one source posture yields one capability

#### Scenario: A blanket denial is unchanged

- **WHEN** a source agent declares a bare `edit: deny`
- **THEN** the generated omp agent's `tools` list contains neither `edit` nor `write`, and the note records that omp exposes `write` anyway while `tools.xdev` is on

#### Scenario: Write access is never silently claimed

- **WHEN** any agent is translated
- **THEN** the output frontmatter records, under generated metadata, that omp exposes `write` as an `xd://` transport tool irrespective of the allowlist

#### Scenario: Scoped report sink is reported as an unenforced convention

- **WHEN** an agent carrying the scoped report-sink exception is translated
- **THEN** the output frontmatter records that the sink is a prompt-level convention enforced by no harness
- **AND** the record states that the agent can write anywhere
- **AND** the record does not present the gap as specific to omp

#### Scenario: Dispatch denial is enforced

- **WHEN** a translated leaf agent runs in omp
- **THEN** it has no `task` tool and cannot dispatch any agent

### Requirement: Skill autoloading is opt-in

omp can inject named skill bodies into a subagent at start via `autoloadSkills`. Because opencode has no equivalent and binds skills by prose reference, the generated omp agent files SHALL leave `autoloadSkills` unset, so that every harness behaves alike. There is no flag to enable it: a prebuilt plugin is installed by the harness rather than by a user-invoked command, so there is no invocation to carry one.

The `(deep)` skill heading in each prompt SHALL nonetheless still be parsed on every build, and a heading that is missing or names no skills SHALL fail the build, because the one-line shape remains normative in the roster specifications.

#### Scenario: Generated agents declare no autoloading

- **WHEN** any agent is generated for the omp tree
- **THEN** the output frontmatter declares no `autoloadSkills`

#### Scenario: A broken deep heading still fails the build

- **WHEN** an agent prompt's `(deep)` heading is followed by a blank line, or is absent
- **THEN** the generator exits non-zero naming that source file

### Requirement: Installation is idempotent and inspectable

`install.sh` SHALL support repeated invocation without accumulating state, and SHALL support previewing an invocation without touching the filesystem. Because it now serves opencode alone, the guarantee is stated for one destination rather than for a harness selector.

The dry run no longer exercises a translator: nothing is translated at install time, so a dry run's fidelity is the destination list it prints, not a parse it performs. Translation failures surface at build time instead, where `tools/build-plugins.py` fails the build.

#### Scenario: Re-running changes nothing

- **WHEN** `./install.sh` runs twice in succession
- **THEN** the second run leaves the same set of deployed files as the first

#### Scenario: Dry run writes nothing

- **WHEN** `./install.sh --dry-run` runs
- **THEN** the intended actions are printed
- **AND** no file is created, removed, or modified anywhere on disk

#### Scenario: The dry run names only opencode destinations

- **WHEN** `./install.sh --dry-run` runs
- **THEN** every destination printed lies under the opencode root or the command target
- **AND** no path under `~/.omp/` is named

### Requirement: Pillar auto-discovery is limited to distributable directories

When no pillar is named explicitly, `install.sh` and `uninstall.sh` SHALL treat a top-level directory as a pillar only if it is not dot-prefixed and carries an `agents/` or `skills/` subdirectory. Dot-prefixed directories hold tooling configuration for this repository rather than distributable artifacts, and SHALL NOT be swept into a default install.

#### Scenario: Repository tooling is not published

- **WHEN** `./install.sh` runs with no `--pillar` argument
- **THEN** the OpenSpec workflow skills under `.opencode/skills/` and `.claude/skills/` are not deployed
- **AND** no dot-prefixed directory contributes artifacts to the deployment

#### Scenario: Non-artifact directories are still skipped

- **WHEN** pillar auto-discovery runs
- **THEN** a visible top-level directory carrying neither `agents/` nor `skills/` is not treated as a pillar

#### Scenario: Analyst pillar is unaffected

- **WHEN** `./install.sh` runs with no `--pillar` argument
- **THEN** every agent under `analysts/agents/` and every skill under `analysts/skills/` is deployed

#### Scenario: Explicit selection overrides the filter

- **WHEN** a dot-prefixed directory carrying artifacts is named with `--pillar`
- **THEN** its artifacts are deployed
- **AND** the same holds for `uninstall.sh`, so an already-published dot-directory pillar can still be removed

### Requirement: Write-capable pillars are translated without a false read-only claim

Because omp cannot deny `write` while `tools.xdev` is on, the generated metadata note about write access SHALL distinguish three source postures: a blanket denial, a path-scoped exception, and an outright `allow`. A write-capable source SHALL NOT be stamped with the read-only note.

The path-scoped note's wording is **no longer frozen**. `harden-plugin-distribution` fixed a scenario requiring the analysts' generated write-access note to be unchanged from before that change; its purpose was to prove that change did not disturb the note, not to make the wording permanent. `reframe-report-sink-convention` rewords it deliberately, per the reframing requirement above.

#### Scenario: Write-capable source stamped accurately

- **WHEN** an agent whose source grants `edit: allow` is translated
- **THEN** the generated metadata states that the source granted write access and that the allowlist carries `edit` and `write`
- **AND** it does not claim a read-only posture

#### Scenario: Blanket read-only note is unchanged by this change

- **WHEN** an agent whose source denies `edit` outright is translated
- **THEN** its generated write-access note still states that omp exposes `write` as an `xd://` transport tool and that read-only is prompt-level for writes

#### Scenario: Path-scoped note is reworded

- **WHEN** an agent whose source carries the scoped report-sink exception is translated
- **THEN** its generated write-access note differs from the pre-change wording
- **AND** it no longer attributes the gap to omp's inability to express a path scope

### Requirement: Ownership evidence is defined once for install and uninstall

The evidence that this repository deployed a given artifact SHALL be defined in exactly one place, sourced by both `install.sh` and `uninstall.sh`, because a destination the uninstaller declines to remove is by definition a destination the installer must decline to overwrite. The evidence SHALL be: a symlink resolving inside this repository, a copied file byte-identical to its source, or a copied skill whose `SKILL.md` is byte-identical to its source's.

The translated-agent branch is gone. It existed because `install.sh` deployed generated omp agents, which differ from their source by construction and so could only be recognised by the provenance line naming that source. No opencode deployment is ever a translated file — the plugin trees are the only generated form, and the harnesses' own plugin machinery installs them — so byte-identity is now the whole agent test.

#### Scenario: Both scripts consult the same definition

- **WHEN** `install.sh` and `uninstall.sh` are inspected
- **THEN** neither defines its own ownership test
- **AND** both obtain it from a single shared shell file under `tools/`

#### Scenario: Shared file is not a distributable artifact

- **WHEN** `./install.sh` runs with pillars auto-discovered
- **THEN** the shared ownership file is not deployed to any harness root

#### Scenario: A generated agent is not recognised by provenance

- **WHEN** a file carrying a generated provenance line occupies an opencode agent destination but is not byte-identical to its source
- **THEN** `install.sh` refuses to overwrite it and `uninstall.sh` declines to remove it

### Requirement: Installation refuses to overwrite an artifact it does not own

`install.sh` SHALL, before removing or replacing any destination path, require ownership evidence for that path, and SHALL exit non-zero naming the path when the evidence is absent, because the opencode root is a flat namespace shared with the harness's built-ins and with the user's own artifacts.

A destination deployed by a previous run SHALL still test as owned after its source is edited, on the strength of the symlink resolving into this repository or of byte-identity in copy mode. The generated-provenance route to ownership is gone with the translated agents it existed for.

#### Scenario: Foreign agent of the same name is refused

- **WHEN** an agent file this repository did not deploy already occupies a destination agent path
- **AND** `./install.sh` runs for the pillar containing that agent name
- **THEN** the run exits non-zero
- **AND** the message names the conflicting destination path
- **AND** the foreign file is left byte-for-byte unchanged

#### Scenario: Foreign skill directory of the same slug is refused

- **WHEN** a skill directory this repository did not deploy already occupies a destination skill path
- **AND** `./install.sh` runs for the pillar containing that slug
- **THEN** the run exits non-zero
- **AND** the foreign directory is left in place

#### Scenario: A refused run deploys nothing at all

- **WHEN** a foreign artifact occupies one destination path among many
- **AND** `./install.sh` runs for the pillar containing that name
- **THEN** every destination is checked before any file is written
- **AND** no artifact of any pillar is deployed, including those whose destinations were free

#### Scenario: A previous deployment is owned and is replaced

- **WHEN** `./install.sh` runs twice in succession in any mode
- **THEN** the second run replaces its own artifacts without error
- **AND** the deployed set is the same as after the first run

#### Scenario: Dry run detects the collision

- **WHEN** a foreign artifact occupies a destination path
- **AND** `./install.sh --dry-run` runs
- **THEN** the run exits non-zero
- **AND** no file is created, removed, or modified anywhere on disk

### Requirement: Overwriting an unowned artifact requires an explicit flag

`install.sh` SHALL accept `--force`, which replaces unowned destinations instead of refusing them, because a user who deliberately keeps a modified copy of a shipped artifact must retain a way to return to the shipped one.

#### Scenario: Forced install replaces the foreign artifact

- **WHEN** a foreign artifact occupies a destination path
- **AND** `./install.sh --force` runs
- **THEN** the destination is replaced with this repository's artifact
- **AND** the run exits zero

#### Scenario: Force is announced

- **WHEN** `./install.sh --force` replaces an unowned destination
- **THEN** the run reports each unowned path it overwrote
