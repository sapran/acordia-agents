## 1. Amend the spec first

- [x] 1.1 Modify `acordia-command-namespace`'s "A namespaced command wrapper for every dispatchable agent" requirement: canonical stem wrapper still required per agent; aliases permitted; alias names may not collide with an agent stem; every wrapper must name a live agent.
- [x] 1.2 Sync the delta into `openspec/specs/acordia-command-namespace/spec.md` and run `openspec validate --all --strict`.

## 2. Add the aliases

- [x] 2.1 Generate eight alias wrappers from their canonical counterparts — `analyst`, `target`, `defender`, `fusion`, `webapp`, `mobile`, `cloud`, `internal` — copying description, argument hint, and dispatch body, changing only `name` and adding a comment naming the canonical wrapper.
- [x] 2.2 Give `operator` no alias; its stem is already the short handle.

## 3. Documentation

- [x] 3.1 Update the `CLAUDE.md` command contract: canonical wrapper per agent, aliases permitted, no stem collisions, every wrapper names a live agent.
- [x] 3.2 Update the `README.md` invocation section to show the short handles.

## 4. Verify

- [x] 4.1 Every wrapper's dispatched agent name resolves to a live agent file.
- [x] 4.2 No alias name equals any agent filename stem.
- [x] 4.3 Every agent still has a canonical wrapper named for its stem.
- [x] 4.4 Alias frontmatter matches its canonical counterpart except for `name` and the comment.
- [x] 4.5 An install into temp roots deploys all 17 wrappers in both shapes, with no installer change.
- [x] 4.6 `openspec validate --all --strict` passes.
