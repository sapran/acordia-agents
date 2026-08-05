## Why

`acordia-command-namespace` shipped one wrapper per agent, named for the agent's filename stem, and published that 1:1 rule as normative — including a scenario asserting no wrapper exists for a name that is not an agent.

That rule optimised for the wrong thing. It was chosen to prevent drift (a renamed agent leaving a stale short handle), but the namespace exists to be **typed**, and the stem form is the longest possible spelling of every handle: `/acordia:defender-detection-analyst` is 35 characters for a thing invoked many times a day. The requester had explicitly flagged handle length as the concern the namespace was meant to address.

Current behaviour: exactly nine wrappers, each named for its agent, and an alias is spec-forbidden. Desired behaviour: the canonical stem wrapper stays as the source of truth, short aliases are permitted beside it, and the drift risk that justified the restriction is converted from an argument into a check.

## What Changes

### Short aliases become legal, with the canonical wrapper still required

**MODIFY** `acordia-command-namespace`'s requirement "A namespaced command wrapper for every dispatchable agent":

- Every agent SHALL still have a canonical wrapper named for its filename stem. That is unchanged and remains the source of truth.
- A wrapper MAY additionally exist under a short alias, provided it dispatches exactly one live agent and declares which one.
- An alias name SHALL NOT collide with any agent's filename stem, so the canonical set can never be shadowed.
- Every wrapper — canonical or alias — SHALL name a live agent. A wrapper dispatching a name no agent answers to is a defect, which makes the rename-drift risk a detectable failure rather than a rule enforced by prohibition.

### Eight aliases

`analyst`, `target`, `defender`, `fusion` (Analysis) and `webapp`, `mobile`, `cloud`, `internal` (Operations). `operator` needs none — its stem is already the short handle.

Aliases are generated from the canonical wrapper, so the description, argument hint, and dispatch body cannot diverge; the alias declares its canonical counterpart in a frontmatter comment.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `acordia-command-namespace` — one **MODIFIED** requirement. The per-harness namespace shapes, the deployment guarantees, the not-a-pillar rule, and the unprefixed-slugs guarantee are untouched.

## Impact

- **New files:** eight alias wrappers under `commands/acordia/`.
- **Modified docs:** `CLAUDE.md`, `README.md` — the alias rule and the handles.
- **Unchanged:** `install.sh`, `uninstall.sh`, `tools/command-layout.sh`, `tools/ownership.sh` — deployment globs the wrapper directory, so aliases deploy, refuse to overwrite, and uninstall with no code change. Every agent, skill, and slug is untouched.
- **Reversible either way.** Deleting the eight aliases restores the previous state; deleting the eight superseded stem wrappers instead would collapse to short-only, which this requirement permits but does not mandate.
