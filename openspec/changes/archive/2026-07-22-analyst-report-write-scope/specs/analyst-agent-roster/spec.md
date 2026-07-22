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

Because `bash: "*": allow` already permits file creation via scripting (`python`, `jq`), `edit: deny` expresses read-only **posture**, not a hard sandbox; the path-scoped exception declares the one sanctioned report destination for the reporting agents rather than granting a new capability class.

#### Scenario: File modification denied
- **WHEN** an analyst agent attempts to edit, write, or patch a file outside its sanctioned report sink
- **THEN** the resolved `edit` permission is `deny` and the action is refused

#### Scenario: Reporting agents may write to the report sink
- **WHEN** `operational-analyst` or `fusion-analyst` writes or edits a file under `.acordia/reports/`
- **THEN** the resolved `edit` permission is `allow` (last-match-wins on the `.acordia/reports/**` rule) and the write proceeds

#### Scenario: Non-reporting legs are fully read-only
- **WHEN** `target-network-analyst` or `defender-detection-analyst` attempts to edit, write, or patch any file
- **THEN** the resolved `edit` permission is `deny` and the action is refused

#### Scenario: Analysis allowed by default
- **WHEN** an analyst agent reads a file or fetches a web resource
- **THEN** the action is allowed (opencode default)

#### Scenario: Legs do not dispatch
- **WHEN** a leg subagent is inspected
- **THEN** its resolved `task` permission is `deny`
