## Why

Both harnesses load agents and skills from a single flat namespace shared with their own built-ins and with anything else the user installed — `~/.omp/agent/agents/` currently holds this repo's four analyst agents beside omp's `task`, `scout`, `reviewer`, `designer` and `sonic`. Two problems follow. `install.sh` deploys into that namespace by unconditionally removing whatever occupies the destination path (`deploy_file` and `deploy_dir` both `rm` first), so a name collision silently destroys a foreign artifact — while `uninstall.sh` already refuses exactly that kind of removal via its `owned_by_repo` predicate. And once deployed, nothing in the list a user or model reads identifies which agents came from this repo, because the roster is presented as bare slug plus `description`.

## What Changes

- **Install-time ownership guard.** `install.sh` SHALL refuse to overwrite a destination that this repository did not deploy, reusing the same ownership evidence `uninstall.sh` already applies, with `--force` as the explicit override. The `owned_by_repo` predicate moves into a shared file both scripts source, so install and uninstall cannot drift apart in what they consider owned.
- **Pillar provenance in the dispatch description.** Every agent `description` in `analysts/` and `operators/` gains a leading `ACORDIA Analysis —` / `ACORDIA Operations —` tag, so the pillar is visible wherever a harness renders the roster. The routing sentence after the tag is unchanged; agent names, filenames, `task:` whitelists and skill slugs are all untouched.
- **Skill names and slugs are deliberately not prefixed.** Skills are selected by `description` match, so a name prefix buys no isolation while breaking the normative folder-slug/`name` bijection and the `·`-separated autoload lines that `tools/translate-omp.py --autoload deep` parses. Recorded here so the decision is not relitigated.

## Capabilities

### New Capabilities

None. All three changes tighten requirements in capabilities that already exist.

### Modified Capabilities

- `omp-harness-distribution`: installation gains an ownership precondition — deploying over an unowned path is an error, not a silent overwrite — and the ownership predicate becomes shared between the two scripts.
- `analyst-agent-roster`: the dispatch-description requirement additionally mandates the `ACORDIA Analysis —` provenance tag ahead of the leg question.
- `operator-agent-roster`: the dispatch-description requirement additionally mandates the `ACORDIA Operations —` provenance tag ahead of the domain sentence.

## Impact

- `install.sh` — ownership check in `deploy_file`/`deploy_dir`, new `--force` flag, sourcing the shared predicate.
- `uninstall.sh` — `owned_by_repo` extracted, behaviour unchanged.
- `tools/ownership.sh` — new shared file (shell library, not an artifact deployed to any harness; pillar auto-discovery already ignores `tools/`).
- `analysts/agents/*.md`, `operators/agents/*.md` — nine `description` lines.
- `README.md`, `CLAUDE.md` — the description format contract and the `--force` flag.
- No skill file, agent name, or permission block changes. No behaviour change for a first-time install into an empty harness root.
