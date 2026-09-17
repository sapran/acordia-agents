## 1. Shared reporting contract

- [x] 1.1 Add the selected reader-facing reporting rationale and four repository-directed practices to the competency-map source; verify the `briefing-reporting` row and marks remain unchanged.
- [x] 1.2 Add the shared first-use, glossary, table and claim-traceability contract plus reader check to `briefing-reporting`; verify existing working-directory, rendering, identifier and credential boundaries remain intact.

## 2. Specialist layout integration

- [x] 2.1 Add the acronym chapter, shared table form, local-source locator form and claim-local reference rules to the credential HTML layout; verify the existing disclosure variants and no-target-contact rules remain intact.
- [x] 2.2 Narrow the layout self-check to parsed Aleph entity paths and add content-free malformed-URL handling; syntax-compile it and exercise its clean and mutation cases.

## 3. Distribution and specifications

- [x] 3.1 Add the human-readable reporting requirement and scenarios in the `skill-library` delta; validate the active OpenSpec change.
- [x] 3.2 Record the retired ACORDIA identifier recovery as a parked note without repairing the source register; verify only the intended note is added.
- [x] 3.3 Bump all three version declarations and regenerate `acordia-map.html` from the completed worktree tree; validate model drift and cold-load the map.

## 4. Behavioral verification and delivery

- [x] 4.1 Run matched before/after fresh analyst report cases with the fixed model and synthetic local evidence; inspect actual tool events and score every output against the frozen rubric.
- [x] 4.2 Run structural gates, JSON parsing, grid and skill-set checks, rendered layout/browser checks, and OpenSpec validation; record attributable results in this change.
- [x] 4.3 Sync and archive the completed change after independently proving that no published requirement, scenario or purpose was lost.
- [x] 4.4 Obtain independent reporting and safety-boundary reviews, resolve findings, rerun integrated gates, commit the change, and open a reviewed pull request to `develop`.

## Verification record

- At the pre-archive change tip, `check-acordia.sh` passed all eight checks: version `6.16.0` appears exactly three times, the catalogs are byte-identical, all prompt slugs and 41 grid anchors resolve, all 23 doctrine keys resolve, lead wrappers remain identical, and every prompt remains below its ceiling.
- `openspec validate --all --strict` passed: five published capabilities and the two active changes (`human-readable-reports`, `positive-dispatch-guard`) validated with zero failures. All four JSON files parse, and the two marketplace catalogs are byte-identical.
- The matched fresh runs used `openai-codex/gpt-5.6-terra` with low thinking and only local synthetic evidence: 5 baseline + 5 changed English finished reports; 5 baseline + 5 changed Russian specialist HTML reports; and one baseline + one changed run for each negative control. Session tool results prove the intended baseline or changed `briefing-reporting` bytes were read in every main run; every Russian main run also read the intended layout bytes.
- The baseline had no dedicated acronym chapter in either main case. The changed English reports all contained the chapter, first-use explanations or an explicit unestablished status, a three-system comparison table, local evidence locators, and bounded continuity claims. The changed Russian reports all retained classified disclosure rules, the fixed dossier and coverage tables, the Russian acronym chapter after Hand-off and before the footer, and usable URL or local path references. The acronym-free changed control retained `None used.` without a comparison table; the changed two-sentence hand-back retained a local reference without a chapter.
- The extracted self-check compiled. Its clean fixture returned zero violation counts; a shortened `/entities/<id>` with a long query returned one short-Aleph violation; an href-less anchor changed only its own count; and a malformed URL returned only `Malformed evidence URL`, without the value. After the safety review, the final checker also returned `unsafe = 0` for the rendered report and `unsafe = 1` for both non-HTTPS and query-bearing anchor mutations, without printing their values.
- Browser checks cold-loaded the map with populated `#main`, rendered its final `v6.16.0` badge and the `briefing-reporting` route, swept 68 supported routes with no `Not found`, and confirmed an unknown skill route 404s. The map payload was re-derived from the final five agents, 45 skills and 10 commands. The Russian HTML report rendered eight tables, visible source locators and its acronym chapter, with zero `<details>` elements.
- An independent reporting review found no in-scope clarity, source-of-truth, delta-spec or map defect. The independent safety review found and then re-read the resolved raw/signed/target URL, classified local-path and unsafe-scheme protections; its final read found no disclosure, parser-error, target-contact or source-verification regression.
- `openspec archive human-readable-reports --yes` added the requirement to the published `skill-library` specification and archived the change as `2026-09-17-human-readable-reports`. A post-archive parse comparison preserved the purpose, all 24 prior requirements and 124 prior scenarios byte-for-byte, and added one requirement with 10 scenarios.