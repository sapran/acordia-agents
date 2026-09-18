## MODIFIED Requirements

### Requirement: A shared task directory gives each file an owner

A task directory is written by the lead and by every leg it dispatched, and legs dispatched in parallel write into it at the same time. A single-instance file SHALL carry its analyst's name: `notes-<agent>.md`, and `credentials-<agent>.md` where the work produces one.

When the lead dispatches more than one concurrent instance of the same analyst, it SHALL give each assignment a unique brief slug. Those instances SHALL write `notes-<agent>-<brief-slug>.md` and `credentials-<agent>-<brief-slug>.md`, as applicable. `briefing-reporting` SHALL state both forms, name the silent overwrite failure they prevent, and require the hand-back to name the actual file. A direct or single-leg dispatch with no supplied brief slug SHALL use the single-instance form rather than block.

#### Scenario: Parallel instances receive unique filenames

- **WHEN** the lead partitions one analyst's work into concurrent bounded slices
- **THEN** every slice receives a distinct brief slug and writes notes and credential material using the agent-and-slug filename form

#### Scenario: A single-instance dispatch has a safe fallback

- **WHEN** an analyst has no brief slug because it was dispatched directly or as a single leg
- **THEN** it writes the agent-only filename form and identifies that file in its hand-back

#### Scenario: The collision is stated as ordinary, not unlucky

- **WHEN** the rule's reason is read
- **THEN** it states that the second write succeeds, the first working is lost, and the lead can fuse one survivor believing it has both


#### Scenario: A file one analyst owns carries that analyst's name

- **WHEN** `briefing-reporting` states how a parallel assignment file is named
- **THEN** it gives `notes-<agent>-<brief-slug>.md` and `credentials-<agent>-<brief-slug>.md`, while retaining agent-only filenames for a single instance

#### Scenario: The leg prompts and the credential skill carry it too

- **WHEN** a leg prompt or `credential-harvest-triage` addresses working files
- **THEN** it defers filename addressing to the shared-directory rule

#### Scenario: The hand-back names the file

- **WHEN** a leg returns its bounded summary
- **THEN** it identifies the actual notes file it wrote