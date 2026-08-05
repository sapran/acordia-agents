## MODIFIED Requirements

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
