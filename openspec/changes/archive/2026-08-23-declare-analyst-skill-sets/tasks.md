## 1. Establish the true skill sets

- [x] 1.1 Scan all five prompts for both bindings — `·`-separated skill lines located by heading text,
      and slugs in backticks inside procedural sections.
- [x] 1.2 Confirm the three procedural skills are named in all five prompts, correcting the `6.1.0`
      finding that they were named in none.
- [x] 1.3 Recompute each analyst's catalogue cost on its true set: 22, 25, 29, 31, 33 skills.
- [x] 1.4 Confirm `overwatch-analyst` was over the 12,000 target at 12,211, not under it at 11,114.

## 2. Bring the largest analyst under the target

- [x] 2.1 Trim descriptions in `overwatch-analyst`'s true set, preferring skills shared across roles
      so every role benefits, until it clears 12,000.
- [x] 2.2 Re-check the ceiling after trimming: none over 200, library mean at or under 180.
- [x] 2.3 Re-check that no trim removed a trigger clause or a platform term — the two defects the
      `6.1.0` review caught, which a second round of trimming can reintroduce.

## 3. Declare the sets

- [x] 3.1 Write `acordia-analysts/skill-sets.json` with each agent's set grouped `spine` / `deep` /
      `working` / `procedural`, transcribed from the prompts.
- [x] 3.2 Carry no version field, so the three-occurrence version count is untouched.
- [x] 3.3 Confirm the orchestrator carries no `spine` group and the four legs' spines are identical.

## 4. Prove the check

- [x] 4.1 Run the bidirectional check clean against the authored tree.
- [x] 4.2 Show it fail on a skill named in the prompt but omitted from the declaration.
- [x] 4.3 Show it fail on a skill declared but not named in any prompt.
- [x] 4.4 Show it fail on a typo'd slug that resolves to no skill directory.
- [x] 4.5 Show it fail on a leg whose shared spine diverges from the others.
- [x] 4.6 Restore and confirm clean, so the red results came from the injected defect and nothing else.

## 5. Correct the record

- [x] 5.1 Replace the wrong parked finding in `docs/implementation-notes.md` — the three skills are
      named in every prompt, not in none.
- [x] 5.2 Correct the figures in `docs/handoff-skill-catalogue-prompt-budget.md`, which were computed
      on the undercount, and restate which criteria are met.
- [x] 5.3 Document the declaration check in `CLAUDE.md` beside the slug and catalog checks.

## 6. Release mechanics

- [x] 6.1 Bump `6.1.0` → `6.2.0` in lockstep across the three version occurrences.
- [x] 6.2 Confirm the two catalogs stay byte-identical and all four JSON files parse.
- [x] 6.3 Run `~/ai/checks/check-acordia.sh` and confirm the fourth JSON file does not disturb the
      version-occurrence count.
- [x] 6.4 `openspec validate --all --strict`.
