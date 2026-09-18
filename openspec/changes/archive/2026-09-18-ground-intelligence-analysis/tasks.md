## 1. Source doctrine

- [x] 1.1 Add the selected Clark and Cvetko-Davydiuk records to `docs/roles/sources.md`; verify each key and document identifier resolves through the repository provenance check.
- [x] 1.2 Update the operational-analyst prose with the selected target-model, explicit-gap, human–automation, and access-versus-outcome framing; verify the grid table rows and marks are unchanged.

## 2. Analytic-spine skills

- [x] 2.1 Update `human-automation-teaming` with the automation-hypothesis versus analyst-conclusion boundary and its claim-specific provenance; verify its grid anchor remains unchanged.
- [x] 2.2 Update `naming-the-gaps` and `outcome-judgement` with the selected model/gap and access/outcome framing; verify only doctrinal claims receive `doctrine_source`.

## 3. Distribution and verification

- [x] 3.1 Bump the MINOR version in the three required distribution JSON locations and keep the marketplace catalogs byte-identical; verify with `~/ai/checks/check-acordia.sh`.
- [x] 3.2 Regenerate `acordia-map.html` from the changed tree and prove its data model matches source metadata, including a cold-load landing-page check.
- [x] 3.3 Validate OpenSpec, sync the delta specifications, archive the completed change, and revalidate; review the final diff and record resolution of every finding.
