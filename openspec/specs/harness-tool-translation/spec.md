# harness-tool-translation Specification

## Purpose
TBD - created by archiving change operators-pillar. Update Purpose after archive.
## Requirements
### Requirement: No shipped artifact names a tool the harness lacks

Every agent prompt and skill body distributed by this repository SHALL name only tools that the target harness provides. An artifact ported from a fork — CyberStrike today — SHALL have each of its harness-specific tool references substituted before it is shipped.

This generalises the rule the omp translator already enforces for the `list` tool: naming a nonexistent tool in a prompt produces an agent that calls something that cannot answer.

#### Scenario: Ported artifact carries no fork-only tool

- **WHEN** any file under `operators/` is searched for the CyberStrike platform tool names
- **THEN** none of `add_intel`, `update_vrt_check`, `record_coverage_note`, `get_coverage_notes`, `methodology_status`, `scope_check`, `report_vulnerability`, `triage_vulnerability`, `generate_report`, `ensure_tools`, `attack_script`, `hackbrowser`, `web_get_*`, or `web_write_*` appears

#### Scenario: opencode-only and omp-only tools are handled

- **WHEN** a ported prompt would use a tool present in one harness but not the other (`browser` exists in omp and in CyberStrike, not in stock opencode; `list` exists in opencode, not in omp)
- **THEN** the prompt states the condition rather than assuming the tool, and names the fallback

### Requirement: The `.acordia/ops/` operation journal

Operation state that CyberStrike keeps in its methodology-engine database SHALL be kept as files under `.acordia/ops/`, relative to the working directory, with this fixed layout:

| Path | Content |
| --- | --- |
| `.acordia/ops/scope.md` | authorised targets, exclusions, rules of engagement |
| `.acordia/ops/intel.md` | append-only intel log — endpoints, credentials, technologies, parameters, configuration, auth flows, with severity and confidence |
| `.acordia/ops/coverage.md` | append-only coverage log — what was tested, the request sent, the response summary, and the reasoning |
| `.acordia/ops/findings/<slug>.md` | one confirmed finding per file, with evidence |
| `.acordia/ops/reports/<name>.md` | composed engagement reports |

The journal mirrors the analyst pillar's `.acordia/reports/` convention and SHALL be described in prompts as discipline, not enforced as a permission scope, because omp cannot scope a tool to a path.

#### Scenario: Layout named identically across artifacts

- **WHEN** the journal paths named in the five operator prompts are compared
- **THEN** they agree on the five paths above

#### Scenario: Intel entries carry severity and confidence

- **WHEN** a prompt describes an intel append
- **THEN** it requires a severity (critical / high / medium / low / informational) and a confidence (confirmed / high / medium / low)

#### Scenario: Coverage entries carry evidence

- **WHEN** a prompt describes a coverage append
- **THEN** it requires the request sent, the response summary, and the reasoning that proves or disproves the vulnerability

#### Scenario: Journal is not a permission scope

- **WHEN** an operator agent's `edit` permission is inspected
- **THEN** it is an unscoped `allow`, and the journal paths appear only in the prompt body

### Requirement: Fixed substitution table for CyberStrike platform tools

Each CyberStrike tool SHALL be substituted exactly as follows, in every ported prompt and skill body:

| CyberStrike tool | Substitution |
| --- | --- |
| `add_intel` | append an entry to `.acordia/ops/intel.md` |
| `update_vrt_check`, `record_coverage_note` | append an entry to `.acordia/ops/coverage.md` |
| `methodology_status`, `get_coverage_notes` | read `.acordia/ops/coverage.md` and `.acordia/ops/intel.md` |
| `scope_check` | read `.acordia/ops/scope.md` before touching a new host, domain, account, or subnet |
| `report_vulnerability`, `triage_vulnerability` | write `.acordia/ops/findings/<slug>.md` |
| `generate_report` | compose the report from the journal into `.acordia/ops/reports/` |
| `ensure_tools` | install with `bash` after asking the user |
| `attack_script <name>` | the equivalent standard tool or an explicit inline command |
| `hackbrowser` | `browser` where the harness provides it, otherwise scripted HTTP requests |
| `skill search` / `load` / `unload` | rely on description-matched skills and the skill names the prompt already lists |

A substitution SHALL preserve the upstream intent — the same information recorded, the same test performed — rather than deleting the step.

#### Scenario: Every ported reference is substituted, not deleted

- **WHEN** a ported artifact's upstream version calls a platform tool
- **THEN** the ported version performs the equivalent action from the table at the same point in the procedure

#### Scenario: Tool installation asks first

- **WHEN** a prompt describes installing a missing security tool
- **THEN** it requires asking the user before installing

#### Scenario: Crawling asks first

- **WHEN** a prompt describes automated crawling of a target
- **THEN** it requires explicit user go-ahead before the crawl starts, preserving CyberStrike's approval gate on `hackbrowser`

### Requirement: Substitution table is documented once and referenced

The substitution table and the journal layout SHALL be documented in `docs/agents-skills-extension-workbook.md`, so a future pillar ported from CyberStrike applies the same mapping instead of inventing a second one.

#### Scenario: Workbook carries the mapping

- **WHEN** `docs/agents-skills-extension-workbook.md` is read
- **THEN** it contains the CyberStrike-to-portable substitution table and the `.acordia/ops/` layout

#### Scenario: Pillar docs point at the workbook

- **WHEN** `docs/roles/operator.md` describes the translation
- **THEN** it references the workbook section rather than restating the table as a second source of truth

