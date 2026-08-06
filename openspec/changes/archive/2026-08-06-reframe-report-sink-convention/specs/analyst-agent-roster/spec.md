## MODIFIED Requirements

### Requirement: Read-only file access via `edit: deny`

opencode's permission default is **allow**, and the `edit` permission governs the edit, write, and patch tools collectively (there is no separate `write` key; a top-level `"*": deny` is accepted but overridden by per-tool built-in defaults, so it does not produce a deny-default). The `edit` permission additionally accepts **path-scoped rules with last-match-wins precedence**, exactly like `bash` (documented in `docs/agents-skills-extension-workbook.md` §6).

Every analyst agent SHALL deny file modification by default. The two analysts that hold the **Briefing & written reporting** competency in the role grid (`docs/roles/operational-analyst.md` L76 — `●` Core `operational-analyst`, `○` Fus `fusion-analyst`) SHALL set a path-scoped `edit` permission that denies every path except a single report sink:

```yaml
edit:
  "*": deny
  ".acordia/reports/**": allow
```

Every other analyst — `target-network-analyst` and `defender-detection-analyst`, which carry no reporting competency in the grid — SHALL set a blanket `edit: deny`. Analysis capability (read, grep, glob, bash, webfetch, websearch, skill) remains allowed by opencode's default. Each leg subagent SHALL additionally set `task: deny` (leaf specialist — does not dispatch).

**The report sink is a convention, not a boundary, in every harness including opencode.** Because every analyst carries `bash: allow` (`analysts/agents/*.md`), file creation via scripting (`python`, `jq`, a shell redirection) is permitted at any path, and the path-scoped `edit` rule does not constrain it. `edit: deny` therefore expresses read-only **posture** — the agent holds no file-editing tool — and the scoped rule **declares** the one sanctioned report destination rather than enforcing it. The scoped rule is retained because it is the clearest available expression of that convention in opencode's vocabulary, not because it confines anything.

Documentation, generated notes, and prompt guardrails SHALL NOT describe the sink as enforced in opencode and unenforced elsewhere. The non-enforcement is universal and follows from `bash: allow`, which is retained because `analytic-tooling-scripting` and `exhaustive-data-processing` depend on it.

#### Scenario: File modification denied

- **WHEN** an analyst agent attempts to edit, write, or patch a file outside its sanctioned report sink
- **THEN** the resolved `edit` permission is `deny` and the action is refused

#### Scenario: Reporting agents may write to the report sink

- **WHEN** `operational-analyst` or `fusion-analyst` writes or edits a file under `.acordia/reports/`
- **THEN** the resolved `edit` permission is `allow` (last-match-wins on the `.acordia/reports/**` rule) and the write proceeds

#### Scenario: Non-reporting legs are fully read-only

- **WHEN** `target-network-analyst` or `defender-detection-analyst` attempts to edit, write, or patch any file
- **THEN** the resolved `edit` permission is `deny` and the action is refused

#### Scenario: A scripted write outside the sink is refused by no harness

- **WHEN** any analyst agent writes a file outside `.acordia/reports/` using `bash`
- **THEN** the write succeeds, in opencode as in omp and Claude Code
- **AND** the scoped `edit` rule does not apply to it, because `bash: allow` is a separate and unrestricted write channel

#### Scenario: The sink is documented as a convention

- **WHEN** the repository's documentation, the generated agent notes, or an analyst's guardrails describe the report sink
- **THEN** the confinement is stated as prompt discipline holding in every harness
- **AND** no harness is credited with enforcing it

#### Scenario: Analysis allowed by default

- **WHEN** an analyst agent reads a file or fetches a web resource
- **THEN** the action is allowed (opencode default)

#### Scenario: Legs do not dispatch

- **WHEN** a leg subagent is inspected
- **THEN** its resolved `task` permission is `deny`

## ADDED Requirements

### Requirement: Analyst guardrails state the product destination uniformly

Each analyst's `## Guardrails` section SHALL state, in wording consistent across all four agents, where that agent's written product goes and that the destination is prompt discipline rather than an enforced scope.

The two reporting analysts (`operational-analyst`, `fusion-analyst`) SHALL name `.acordia/reports/` as the sink. The two non-reporting legs (`target-network-analyst`, `defender-detection-analyst`) SHALL state that they return their product in-message, because they hold no write tool — a fact their guardrails currently omit entirely, leaving the destination unstated.

The guardrails SHALL NOT attribute the non-enforcement to a specific harness. The current per-agent divergence — `defender-detection-analyst` and `target-network-analyst` naming only "Under OMP, write access is prompt-level only", against `operational-analyst` and `fusion-analyst` naming "Under OMP … confine writes to `.acordia/reports/`" — is the drift this requirement removes.

#### Scenario: All four guardrails share one wording

- **WHEN** the `## Guardrails` sections of the four analyst agents are compared
- **THEN** each states the sink or the in-message destination in the same form
- **AND** none names a single harness as the reason the confinement is prompt-level

#### Scenario: Read-only legs state where the product goes

- **WHEN** `target-network-analyst` or `defender-detection-analyst` guardrails are read
- **THEN** they state that the product is returned in-message
