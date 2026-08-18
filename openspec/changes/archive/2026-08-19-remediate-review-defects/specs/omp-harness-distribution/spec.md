## MODIFIED Requirements

### Requirement: Unmappable permissions are surfaced, not silently resolved

omp allowlists whole tools and cannot scope a tool to a path. Nor is omitting `write` from the allowlist known to remove it: verified against omp 17.1.8 and recorded in `README.md`, an agent whose allowlist omitted `write` created a scratch file with it anyway, while `edit` and `task` really were absent. This specification asserts that observation and not a mechanism — omp's own documentation states a narrower condition than "always present", and only the observation has been verified here. The source files' `".acordia/reports/**": allow` write exception therefore has no faithful translation.

Where a source declares a path-scoped `edit`, the translator SHALL emit `write` and SHALL NOT emit `edit`, and SHALL record in the generated file that the path scope is a prompt-level convention no harness enforces. This resolves a divergence in which one source posture produced opposite capability in the two plugin harnesses: the omp emitter withheld every write tool while the Claude emitter kept `Write` allowed, so an agent whose prompt requires it to produce a report held the means to do so in one harness and not the other.

The emitted capability is the honest one. A write tool was seen to work in omp from an allowlist that omitted it, and `bash: allow` is an open write channel at any path in all three harnesses, so an agent with a scoped `edit` can already write anywhere; the generated note SHALL state that outcome rather than imply a boundary the harness keeps.

A blanket `edit: deny` SHALL continue to emit neither `edit` nor `write`, with the note recording that the omission is not known to remove `write`, citing the recorded omp 17.1.8 result, and directing that writes be treated as prompt-level rather than blocked.

#### Scenario: A path-scoped edit yields a write tool

- **WHEN** a source agent declares `edit` as `"*": deny` followed by a path-scoped `allow`
- **THEN** the generated omp agent's `tools` list includes `write` and excludes `edit`
- **AND** the generated note states that the path scope is an unenforced convention and that the agent can write anywhere

#### Scenario: The two plugin harnesses agree on the posture

- **WHEN** the same path-scoped source is translated for both harnesses
- **THEN** both generated agents hold a write capability and neither holds a general edit capability, so one source posture yields one capability

#### Scenario: A blanket denial is unchanged

- **WHEN** a source agent declares a bare `edit: deny`
- **THEN** the generated omp agent's `tools` list contains neither `edit` nor `write`, and the note records that the omission is not known to remove `write`, cites the omp 17.1.8 result, and directs that writes be treated as prompt-level rather than blocked

#### Scenario: Write access is never silently claimed

- **WHEN** any agent is translated
- **THEN** the output frontmatter records, under generated metadata, exactly which write capability the agent holds
- **AND** it claims no restriction this repository has not verified the harness to keep

#### Scenario: Scoped report sink is reported as an unenforced convention

- **WHEN** an agent carrying the scoped report-sink exception is translated
- **THEN** the output frontmatter records that the sink is a prompt-level convention enforced by no harness
- **AND** the record states that the agent can write anywhere
- **AND** the record does not present the gap as specific to omp

#### Scenario: Dispatch denial is enforced

- **WHEN** a translated leaf agent runs in omp
- **THEN** it has no `task` tool and cannot dispatch any agent

### Requirement: Write-capable pillars are translated without a false read-only claim

Because omitting `write` from an omp allowlist is not known to remove it, the generated metadata note about write access SHALL distinguish three source postures: a blanket denial, a path-scoped exception, and an outright `allow`. A write-capable source SHALL NOT be stamped with the read-only note.

The path-scoped note's wording is **no longer frozen**. `harden-plugin-distribution` fixed a scenario requiring the analysts' generated write-access note to be unchanged from before that change; its purpose was to prove that change did not disturb the note, not to make the wording permanent. `reframe-report-sink-convention` rewords it deliberately, per the reframing requirement above.

#### Scenario: Write-capable source stamped accurately

- **WHEN** an agent whose source grants `edit: allow` is translated
- **THEN** the generated metadata states that the source granted write access and that the allowlist carries `edit` and `write`
- **AND** it does not claim a read-only posture

#### Scenario: Blanket read-only note claims no restriction it cannot keep

- **WHEN** an agent whose source denies `edit` outright is translated
- **THEN** its generated write-access note states that the omission is not known to remove `write`, cites the recorded omp 17.1.8 result, and directs that writes be treated as prompt-level rather than blocked
- **AND** it asserts no mechanism for why `write` remains available

#### Scenario: Path-scoped note is reworded

- **WHEN** an agent whose source carries the scoped report-sink exception is translated
- **THEN** its generated write-access note differs from the pre-change wording
- **AND** it no longer attributes the gap to omp's inability to express a path scope

### Requirement: Frontmatter translation contract

The translator SHALL convert one opencode agent file into one omp task-agent file according to a fixed mapping. The generated file SHALL carry a `name` field equal to the source filename stem and SHALL preserve the source `description` verbatim, because omp skips any agent file lacking either field.

The emitted `tools` allowlist SHALL be derived from the source `permission` map rather than from a fixed list, so that a write-capable pillar translates as faithfully as a read-only one. The derivation is:

- always present: `read`, `grep`, `glob`, `bash`, `web_search`, `todo`, and `yield` (omp appends `yield` itself; naming it keeps the generated file honest)
- `edit` and `write` are both present when the source `permission.edit` is the scalar `allow`
- `write` alone is present, and `edit` is absent, when the source `permission.edit` is a path map carrying at least one `allow` — the scoped report-sink posture, whose reasoning is stated under *Unmappable permissions are surfaced, not silently resolved* above
- neither is present when the source `permission.edit` is a denial
- `browser` is present when the source `permission.browser` is `allow`
- `task` is present, and `spawns` lists the allowed agent names, when the source `permission.task` map names at least one allowed agent

The generated file SHALL additionally carry a `color`, because omp renders every agent in one flat picker shared with its own built-ins and the user's own agents — the same visual-namespace problem the `ACORDIA <pillar> — ` description tag solves for text. The colour SHALL be derived from the `metadata.acordia` block the source already declares rather than from a filename table, so the pillar keeps one source of truth for which agent is the orchestrator: both pillars declare that standing in one key, `role`, and `role: orchestrator` emits `cyan` while `role: specialist` emits `blue`. There is no colour fallback: a source carrying no `metadata.acordia` block, or declaring no recognised `role`, fails the build under the anchor gate specified in `plugin-packaging`, because a defaulted colour would ship a mislabelled agent in the picker instead of reporting the defect.

#### Scenario: Required fields emitted

- **WHEN** any `<pillar>/agents/<stem>.md` is translated
- **THEN** the output frontmatter contains `name: <stem>`
- **AND** the output frontmatter contains the source `description` unchanged

#### Scenario: Orchestrator and specialists are visually distinguishable

- **WHEN** an agent declaring `metadata.acordia.role: orchestrator` is translated alongside an agent declaring `metadata.acordia.role: specialist`
- **THEN** the orchestrator's output carries `color: cyan` and the specialist's carries `color: blue`

#### Scenario: A missing anchor is a build failure, not a colour default

- **WHEN** an agent carrying no `metadata.acordia` block, or declaring no recognised `role`, is translated
- **THEN** the translator exits non-zero naming that source file, and no colour is defaulted for it

#### Scenario: Read-only posture becomes an absent tool

- **WHEN** a source agent carries `permission.edit` denying `"*"`
- **THEN** the output `tools` allowlist contains neither `edit` nor `write`
- **AND** the running agent has no `edit` tool

#### Scenario: Write-capable posture becomes present tools

- **WHEN** a source agent carries `permission.edit: allow`
- **THEN** the output `tools` allowlist contains both `edit` and `write`

#### Scenario: Scoped posture becomes the write tool alone

- **WHEN** a source agent carries `permission.edit` as a path map denying `"*"` and allowing one path
- **THEN** the output `tools` allowlist contains `write` and does not contain `edit`

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
