## 1. Author the command set

- [x] 1.1 Create `commands/acordia/<stem>.md` for each of the nine agents across `analysts/agents/` and `operators/agents/`, with `<stem>` equal to the agent filename stem.
- [x] 1.2 Give each wrapper `name`, `description` (the agent's operating question), `argument-hint`, and `category` frontmatter, and a body that dispatches that agent with `$ARGUMENTS` as the brief.
- [x] 1.3 Word the two orchestrator wrappers (`operational-analyst`, `operator`) to dispatch where the harness allows it and to name the session-switch fallback where it does not.

## 2. Extend ownership evidence

- [x] 2.1 Add a `command` kind to `tools/ownership.sh`: a symlink resolving inside the repository, or a byte-identical copy. Keep the shared-definition property — no second ownership test in either script.

## 3. Wire the installer

- [x] 3.1 Add `--no-commands` and `--commands-target DIR` to `install.sh`, defaulting to deploying commands.
- [x] 3.2 Resolve the command root per harness: opencode → `<root>/commands` with flat `acordia-<stem>.md`; omp → `~/.claude/commands/acordia/<stem>.md`. Print the omp destination, since it lies outside `$OMP_ROOT`.
- [x] 3.3 Skip the command step with an explanatory message when `--target` was given for omp without `--commands-target`, because the command root cannot be inferred from an overridden harness root.
- [x] 3.4 Extend `preflight` so a command destination this repository does not own aborts the run before anything is written, honouring `--force` identically.
- [x] 3.5 Include commands in the deployed count and in `--dry-run` output.

## 4. Wire the uninstaller

- [x] 4.1 Remove owned command files for the selected harness, skip and count unowned ones, and remove the `acordia/` namespace directory only when it is left empty.
- [x] 4.2 Mirror `--no-commands`, `--commands-target`, and the `--target` skip rule so install and uninstall stay symmetrical.

## 5. Documentation

- [x] 5.1 Add the command contract to `CLAUDE.md`: source location, the 1:1 stem rule, and the two namespace shapes.
- [x] 5.2 Correct the stale `CLAUDE.md` claim that the OpenSpec commands are available under `.opencode/commands/opsx/` — that tree is flat (`opsx-apply.md`), because opencode command discovery is not recursive.
- [x] 5.3 Record the invocation surface in `README.md`, including that slugs stay unprefixed on purpose.

## 6. Verify

- [x] 6.1 The wrapper set is exactly 1:1 with the union of `analysts/agents/*.md` and `operators/agents/*.md`.
- [x] 6.2 `./install.sh --harness opencode --target <tmp> --commands-target <tmp2> --dry-run` prints the command actions and writes nothing.
- [x] 6.3 A real install into temp roots produces `acordia-<stem>.md` (opencode shape) and `acordia/<stem>.md` (Claude shape).
- [x] 6.4 Re-running the install is idempotent — the second run leaves the same file set.
- [x] 6.5 A foreign file at a command destination aborts the install naming the path, and `--force` replaces it.
- [x] 6.6 `./uninstall.sh` removes the owned commands, leaves a foreign name-match in place, and removes the emptied `acordia/` directory.
- [x] 6.7 Pillar auto-discovery still yields exactly `analysts` and `operators` — `commands/` is not treated as a pillar.
- [x] 6.8 `openspec validate --all --strict` passes.
