## Context

See proposal.md — Why. Two constraints shape the approach.

The generator already holds the machinery. `split_frontmatter()` parses a frontmatter block and raises `TranslationError` on a non-mapping; `read_agent()` calls it and the error propagates out of `main()` to a non-zero exit. Agents therefore cannot ship malformed. Skills reach `shutil.copytree` without ever being opened, on the recorded rationale that a skill is valid unchanged across all three harnesses — true of the body, but the frontmatter is the part each harness parses differently, and it is the part that broke.

The repository has a standing exclusion on new automation. `harden-plugin-distribution` recorded it explicitly: no CI, no hooks, no lint automation, `--check` run by hand. That rules out the obvious shapes — a pre-commit hook, a workflow, a standalone linter — and leaves the gate inside the generator that already runs.

Measured before designing: all 73 source skills across both pillars parse except one, every skill's top-level keys are exactly `name`/`description`/`metadata`, zero slug/name mismatches, zero descriptions outside 1–1024. The gate's blast radius on today's tree is precisely the one file this change repairs.

## Goals / Non-Goals

**Goals:**

- A malformed skill frontmatter fails the build, at the same severity and through the same path as a malformed agent.
- The check reads sources, so it is not defeated by a defect being present identically in the committed output.
- No new file, command, or execution surface: the gate runs whenever the generator already runs.

**Non-Goals:**

- Validating skill *bodies*. Section-shape requirements (the four-section doctrine shell, credential-extraction sections, the `Method` contract) are real requirements in the skill-library specs, but they are prose contracts with judgement in them; mechanising them is a much larger change and would misfire. This gate stops at frontmatter, which is machine-checkable without interpretation.
- Enforcing the `VERSION`-bump obligation. Same class of unenforced invariant, deliberately separate — it needs git state rather than file content, which is a different mechanism and a different argument about what the generator should know.
- Reformatting or re-quoting the other 72 skills. They parse; churning them would bury the one real fix in noise.

## Decisions

**The gate lives in `tools/build-plugins.py`, invoked from `build()` before the skill tree is copied.** Alternatives considered: a standalone `tools/validate-skills.py`, rejected because a validator nobody runs is exactly the failure being fixed — the whole defect is a contract stated in three places and executed in none, so a fourth optional surface makes it worse; a pre-commit hook or CI job, rejected against the repository's recorded no-automation exclusion. Placing it in the generator means the check cannot be skipped by anyone who builds, and it inherits the staged-build guarantee that a failure leaves the committed trees untouched.

**Validation runs against sources, before staging, not against the staged output.** This is the load-bearing decision. `--check` diffs staged bytes against committed bytes, so a defect that exists in both compares equal and the gate reports success — which is precisely how the current file passes today. Checking sources is the only placement that detects a defect already committed to the output trees.

**Failure is a raised `TranslationError`, not a warning.** The repository already treats a malformed agent and a wrapper naming a dead agent as build failures. A warning would preserve the current outcome, since the defect has been sitting in the tree unnoticed through several builds; the evidence is that nothing short of a hard failure gets acted on.

**The rule set is exactly the intersection of what the two skill-library specs already require**, rather than a new opinion about frontmatter: parses as a mapping; `name` kebab-case, ≤64 chars, equal to the folder slug; `description` 1–1024; keys limited to `name`/`description`/`metadata`; no `sha256`/`signature`/`signed_by`. Nothing here is invented by this change — each clause traces to `analyst-skill-library` (opencode frontmatter contract, slug-equals-name) or `operator-skill-library` (frontmatter reduction, signing-triple removal). `metadata` is checked for presence and type only; its interior (`metadata.acordia.*`) is provenance data the specs shape elsewhere and this gate does not police.

**The malformed description is repaired by single-quoting the existing value, not by rewording it.** The value contains no apostrophe, so single quotes are the minimal escape; verified that the quoted form parses and yields the description byte-for-byte identical at 345 characters. Rewording was rejected because `analyst-skill-library` requires that description to be authored for trigger quality and the current wording satisfies it — the YAML is broken, the prose is not.

**One requirement is added rather than modifying the existing gate requirement.** `plugin-packaging`'s existing scenario "A failed build leaves the committed tree intact" already reads *"WHEN a source artifact is malformed and the generator runs THEN it exits non-zero naming that source file."* That scenario is simply untrue for skills today. The added requirement makes the existing one honest, so the existing text needs no edit.

## Risks / Trade-offs

**The gate rejects a skill that ships today, blocking an unrelated build.** → Measured rather than assumed: 73 skills, one failure, and that one is repaired in this change. A build failing on any other skill after this lands is new information and should be handled as a finding, not silenced by loosening the gate.

**A future skill legitimately needs a new top-level key, and the closed key set blocks it.** → The key set is not this change's invention; it is what both skill-library specs already mandate, so a new key is a spec change first and a gate change second. That ordering is the intended friction, not a side effect.

**PyYAML is a hard dependency of the build.** → Already true: `split_frontmatter()` uses `yaml.safe_load` for every agent, so the generator cannot run without it. The gate adds no dependency.

**The gate gives false confidence that skills are validated.** → It validates frontmatter only. The body contracts stay unenforced and remain open findings; this change should not be read as closing them, which is why they are listed as Non-Goals above and left in the review's outstanding set.

## Migration Plan

No migration. The change is source edits plus a regeneration: repair the description, add the gate, bump `VERSION` to `2.3.0`, rebuild, and confirm `--check` is clean. Rollback is a revert of the commit; nothing is installed, persisted, or stateful, and the generated trees are reproduced from source by construction.
