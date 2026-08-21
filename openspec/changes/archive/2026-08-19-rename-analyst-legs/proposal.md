# Rename the two named analyst legs

## Why

Two of the three analyst legs were named after the competency-grid column they were derived from
rather than after the work they do. `target-network-analyst` carried `network` from the grid's
**T&N** (Target & Network) column, but the agent's own prompt leads with the target's *mission* —
what the target is for and what it depends on — and treats terrain as the second half. The name
advertised the smaller half. `defender-detection-analyst` stacked two near-synonyms and still missed
the register the prompt calls defining: **overwatch**, the live read of the defender's own security
operations that drives the go-quiet / move / pull-out call.

The names were also the longest in the roster at 22 and 26 characters, and a caller in Claude Code
must type the namespaced form `acordia-analysts:defender-detection-analyst` to dispatch one.

Renaming them to `target-analyst` and `overwatch-analyst` completes the naming pass begun in the
lead-agent rename: every agent is now named for the question it answers.

## What Changes

- `target-network-analyst` → `target-analyst`; agent and canonical wrapper files renamed.
- `defender-detection-analyst` → `overwatch-analyst`; agent and canonical wrapper files renamed.
- Every live reference updated: pillar docs, `CLAUDE.md`, `README.md`, `openspec/config.yaml`, three
  spec files, and four skill files that route material to a leg by name.
- Short aliases `/target` and `/defender` keep their filenames, so no existing invocation breaks.
  The wrapper count stays 18.
- The competency grid's column letters **T&N**, **Def** and **Fus** are unchanged. They label the
  legs of the role described in `docs/roles/operational-analyst.md`, not the agent files that
  implement it. The provenance note at the end of that document records the new mapping.
- No version bump. 4.0.0 is unreleased and already carries the lead-agent rename; this joins it.

## Impact

- Breaking for any caller that dispatches either leg by its old name. Both old names disappear from
  the live tree entirely — there is no aliased agent file, only the renamed one.
- `openspec/changes/archive/**` is untouched. It records the names that were true when it shipped.
