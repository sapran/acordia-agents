## Context

The stem-only rule came from a real failure mode: a short handle is a second naming surface, so renaming an agent leaves `/acordia:fusion` pointing at nothing while the file still looks fine. Binding the wrapper name to the agent stem made that impossible by construction.

It also made the namespace worse at its job. The namespace was added because agent names are dispatched from a flat picker shared with the harness's built-ins, and the ask behind it was explicitly about handle length. Stem naming produces the longest spelling available — and the maintenance risk it defends against is a rename that happens rarely, is visible in review, and is already covered by the fact that both orchestrators' `task` whitelists name the same stems.

## Goals

- Short handles for daily use.
- Canonical stem wrappers retained as the source of truth.
- Rename drift caught by a check rather than prevented by prohibition.
- No installer, uninstaller, or ownership change.

Non-goals: removing the canonical wrappers; prefixing any slug; a handle for every conceivable abbreviation of an agent.

## Decisions

**Keep both, rather than swap.** Deleting the stem wrappers would make the short handle the only entry point and reintroduce the drift risk with nothing to catch it; keeping only stems is what prompted this change. Both cost nothing at runtime — a wrapper is an eight-line file, and the harness lists them from one directory.

**Aliases are generated from the canonical wrapper, never authored twice.** Description, argument hint, and dispatch body are copied; only `name` differs, plus a frontmatter comment naming the canonical wrapper. Two hand-written copies of the same brief would drift in wording, which is the same class of defect this change is trying to make impossible.

**Alias names may not collide with an agent stem.** Otherwise an alias could shadow a canonical wrapper for a *different* agent — `/acordia:operator` meaning one thing as a stem and another as an alias. A collision check is cheap and removes the ambiguity entirely.

**The drift guard is "every wrapper names a live agent".** That check covers both directions: a renamed agent breaks its alias *and* its canonical wrapper identically, and both surface as the same failure. It is strictly stronger than the prohibition it replaces, because the prohibition never protected the canonical wrapper from a rename either — it only prevented a second name from existing.

**`operator` gets no alias.** Its stem is already the handle. Minting `op` beside it would add a name for nothing.

**Handle choices avoid skill slugs.** `defender`, not `overwatch` — `overwatch` is a live skill slug, and a command handle that shadows a skill name in conversation invites the wrong mental model. Handles name the *agent's domain* (`target`, `cloud`, `internal`), not one of its skills.

## Risks

- **Two ways to invoke one agent.** Mild autocomplete noise: 17 entries where 9 would do. Accepted — the alternative is 9 long entries or 9 drift-prone short ones.
- **A future agent whose stem collides with an existing alias.** The collision rule catches it at authoring time; the fix is renaming the alias, not the agent.
- **Alias descriptions duplicate the canonical ones in the picker.** Two entries with identical descriptions is honest — they do the same thing — but a user scanning the list sees the pair. Naming the canonical wrapper in the alias's frontmatter comment keeps the relationship discoverable in the file if not in the picker.
