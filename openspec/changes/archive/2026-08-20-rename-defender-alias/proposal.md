# Rename the /defender alias to /overwatch

## Why

The leg rename left `overwatch-analyst` with a short alias called `defender` — the only alias in the
roster naming a word that does not appear in its own agent's name. Eight of the nine derive from
their agent: `/analyst`, `/fusion`, `/target`, `/cloud`, `/internal`, `/mobile`, `/operator`, and
`/webapp` as a legible contraction of `web-application`. `/defender` derived from
`defender-detection-analyst`, a name the same release deleted.

So the alias was unguessable from the roster, and it kept alive the exact `defender` / `detection`
vocabulary the rename concluded was the wrong framing.

The reasons given for keeping it do not survive inspection:

- *It would collide with the skill `overwatch`.* Sharing a word with a skill is already the norm —
  `analyst`, `cloud`, `fusion`, `mobile`, `target`, `web` and `security` all appear in both an agent
  name and a skill name. Commands and skills are separate namespaces: one is invoked with a slash,
  the other is matched by description. No command name collides with a skill name, and `/overwatch`
  does not collide with a command. The same skill was simultaneously cited as the justification for
  naming the agent `overwatch-analyst`, which cannot both validate and disqualify the word.
- *It would break an existing invocation.* The same release deleted the canonical wrappers
  `/target-network-analyst` and `/defender-detection-analyst` outright, with no alias. This is an
  unreleased major whose purpose is a breaking rename.

The retention rule that covered it was also mis-scoped. It reads "where renaming a **lead** agent
**lengthens** its canonical wrapper" — the `/operator` case. `overwatch-analyst` is a leg, and the
rename *shortened* its name by four characters, so neither precondition held. A second requirement
had been added specifically to cover the case, which made an ad-hoc choice into a rule.

## What Changes

- `acordia-analysts/commands/defender.md` → `acordia-analysts/commands/overwatch.md`. The wrapper's
  body already named `overwatch-analyst`; only the filename, and therefore the handle, changes.
- The three sites that named the handle are updated: the short-handle list in `README.md`, the
  provenance note in `docs/roles/operational-analyst.md`, and the spec scenario.
- The invented leg-alias-retention rule is replaced by the rule that actually holds: a short alias is
  formed from its own agent's name and is renamed when that name changes.
- Wrapper count stays 18: nine canonical, nine short aliases.
- Every other occurrence of the word `defender` is left alone. In 14 skill files, both agent prompts
  and the provenance document it means the adversary's defender, which is the subject matter.

## Impact

- Breaking for a caller invoking `/defender`. There is no aliased wrapper left under that name.
- The lead-agent retention rule at `agent-roster` is unchanged and still governs `/operator` and
  `/analyst`; both remain words of their agents' names, so it is consistent with the new rule.
