## 1. Author the loop skill

- [ ] 1.1 Create `analysts/skills/analyst-loop/SKILL.md` with opencode frontmatter (`name: analyst-loop`, `description` phrased for trigger quality — "when the operator asks for a fresh end-neutral analytic pass over collected material", or equivalent)
- [ ] 1.2 Add a `## Cross-cutting notice` paragraph declaring the skill is procedural, does not correspond to a grid row, and inherits the procedural-skill exception from `analyst-skill-library`
- [ ] 1.3 Add a `## Loop shape` section naming the five steps in one sentence each: target-read (via T&N), defender-read (via Def), fusion (via Fus), judgement (calibrated, via spine skills), next-move (named, end-neutral)
- [ ] 1.4 Add a `## Loop invariants` section naming end-neutrality (every pass reaches a judgement + next move), gap-naming (`naming-the-gaps` on every judgement), calibrated confidence (`calibrated-confidence` on every judgement), and passive posture (loop reads and reasons only)
- [ ] 1.5 Add a `## Where this runs` paragraph stating the loop is the orchestrator's workflow; a leg that matches this skill surfaces the need for a full pass back to the orchestrator rather than attempting the loop itself
- [ ] 1.6 Verify frontmatter validates against opencode contract (`name` matches `^[a-z0-9]+(-[a-z0-9]+)*$`, ≤64 chars; `description` 1–1024 chars)

## 2. Reference from the orchestrator

- [ ] 2.1 In `analysts/agents/operational-analyst.md`, locate the existing paragraph that describes the target → defender → fusion → judgement → next-move loop
- [ ] 2.2 Add one sentence naming `analyst-loop` as the skill that formalises the loop shape and is the pointer for future pillars' orchestrators
- [ ] 2.3 Verify no new section is added and no existing section is modified beyond that sentence
- [ ] 2.4 Verify permission blocks (`edit`, `bash`, `task`) unchanged

## 3. Verify no leg agent is modified

- [ ] 3.1 `git diff analysts/agents/target-network-analyst.md analysts/agents/defender-detection-analyst.md analysts/agents/fusion-analyst.md` shows no changes

## 4. Validate

- [ ] 4.1 `openspec validate --all --strict` passes
- [ ] 4.2 `test -f analysts/skills/analyst-loop/SKILL.md`
- [ ] 4.3 `grep -q '^description:' analysts/skills/analyst-loop/SKILL.md` succeeds
- [ ] 4.4 `grep -q 'procedural' analysts/skills/analyst-loop/SKILL.md` succeeds
- [ ] 4.5 `grep -q 'analyst-loop' analysts/agents/operational-analyst.md` succeeds
- [ ] 4.6 `grep -c 'analyst-loop' analysts/agents/target-network-analyst.md analysts/agents/defender-detection-analyst.md analysts/agents/fusion-analyst.md` reports 0 hits per file
- [ ] 4.7 Skill count invariant: `ls analysts/skills | wc -l` reports 41 (was 40 after the credential-harvest capability landed)
