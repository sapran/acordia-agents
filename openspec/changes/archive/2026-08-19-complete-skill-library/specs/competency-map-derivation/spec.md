## ADDED Requirements

### Requirement: Merging two rows moves the grid first and preserves both marks

Where two grid rows describe one judgement, they MAY be merged into one row, and the merge SHALL be
performed in the grid before any skill directory or prompt line is touched. The surviving row's marks
SHALL be the union of the two rows' marks, taking the stronger mark per column, because a column that
held `●` on either row still owns the merged competency deeply.

The merge SHALL be a fold, not a deletion: every distinct element of the absorbed skill's Method SHALL
be present in the surviving skill's body afterwards. `Outcome judgement` absorbing
`Effect-on-target verification` is the worked case — the observable-channel inventory, the first-party
versus independent-confirmation split, the `<log>:<offset>` citation form and the honeypot tells all
survive in `outcome-judgement`.

#### Scenario: Grid changes before the artifacts

- **WHEN** two rows are merged
- **THEN** the grid edit and the artifact edits land in the same change, with the grid stated as the reason for the artifact change

#### Scenario: Stronger mark wins per column

- **WHEN** the `Outcome judgement` row absorbs the `Effect-on-target verification` row
- **THEN** the T&N column reads `●` rather than `○`, because that column held the deep mark on the absorbed row

#### Scenario: Nothing is dropped in the fold

- **WHEN** the surviving skill is compared against the absorbed skill's Method
- **THEN** every distinct element of the absorbed Method appears in the survivor, and the absorbed directory no longer exists

#### Scenario: No dangling reference remains

- **WHEN** the repository is searched for the absorbed skill's slug
- **THEN** no prompt, skill body, spec, document or command wrapper names it
