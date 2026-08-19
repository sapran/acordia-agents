## Why

Each pillar's lead agent was named with the same word as the pillar it leads, and the repository paid
for it in prose. `operator` was three different things depending on the sentence: the orchestrating
agent, the whole Operations pillar ("the operator pillar holds 39 skills", "the five operator
prompts"), and the human or session driving the engagement ("an operator session asks", "belonging to
the operator or the human"). Of 82 live occurrences of the bare word, only about 20 meant the agent.
A reader could not tell which sense was meant without resolving it from context every time, and a
find-and-replace on the word would have corrupted roughly sixty sites.

`operational-analyst` had the opposite problem. It was unambiguous as a slug, but it collided with the
role name in the source competency map, *The Operational Analyst* — so the agent, the role model and
the doctrinal role all read identically while meaning three different things.

Renaming both leads fixes the ambiguity at its root: no lead agent shares a word with its pillar.

## What Changes

- `operational-analyst` → **`cyber-analyst`**; `operator` → **`cyber-operator`**. Four files move
  (agent and canonical wrapper in each pillar), and filename stem still equals frontmatter `name`.
- `/operator` becomes the short alias for `/cyber-operator`, mirroring the alias convention every
  other multi-word command already follows. `/analyst` continues to alias the analyst lead. No
  existing invocation breaks. Wrapper count 17 → 18, operations wrappers 9 → 10.
- The 34 prose sites that meant the *pillar* are normalised to "operations pillar / library / skills /
  prompts / agents / wrappers / artifacts / files / specialist". The pillar and the agent are no
  longer the same word.
- The sites that meant a **human or session** keep the word `operator`, because that is what they
  mean: the guardrail quote *"execution belongs to the operators you advise"*, `operator journal`,
  `operator session`, `operator-deployed`, and the default-credential table row in
  `wstg-auth-session` (`| operator | operator | Industrial systems |`).
- Version 3.2.0 → **4.0.0** in all four version files. Renaming a dispatchable agent is breaking for
  any caller that names it.

## What does NOT change

- **`openspec/changes/archive/**` is untouched** — 112 files, 419 occurrences. An archived change
  records what was true when it shipped; rewriting it would be falsifying history.
- **`docs/roles/operator.md` and `docs/roles/operational-analyst.md` keep their filenames.** They are
  provenance records of upstream artifacts that really were called that, and the analyst file is
  line-anchored: 39 skills carry `source: docs/roles/operational-analyst.md#L<n>` into rows L67–L108.
  Nothing may be inserted above that grid, so the rename note is appended at the end of the file.
  Each document instead records the upstream-name → agent-name mapping.
- The role name *The Operational Analyst* stays in the competency map. A grid row describes a
  competency, not an agent.
- Plugin directory names `acordia-analysts/` and `acordia-operators/` are unchanged; the install
  source paths are stable, so this is not a distribution-path major per `plugin-distribution`.

## Impact

- Affected specs: `agent-roster` (agent filenames, orchestrator names, wrapper count and aliases,
  plus one new naming invariant); `skill-library`, `competency-map-derivation` and
  `plugin-distribution` take the terminology sweep only, with no change to what they require.
- Affected code: none. This distribution has no runtime.
