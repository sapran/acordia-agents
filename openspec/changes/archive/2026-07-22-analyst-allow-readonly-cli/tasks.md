## 1. Agent files — collapse bash block to `bash: allow`

- [x] 1.1 `analysts/agents/operational-analyst.md`: replace the multi-line `bash:` block (`"*": allow` + cat/head/tail/less/more/ls denies + grep/egrep/rg/find/fd asks and inline comments) with `bash: allow`. Leave `edit` and `task` blocks and all prompt sections unchanged.
- [x] 1.2 `analysts/agents/target-network-analyst.md`: same collapse to `bash: allow`; `edit: deny` and `task: deny` unchanged.
- [x] 1.3 `analysts/agents/defender-detection-analyst.md`: same collapse to `bash: allow`; `edit: deny` and `task: deny` unchanged.
- [x] 1.4 `analysts/agents/fusion-analyst.md`: same collapse to `bash: allow`; `edit` block (`"*": deny` + `.acordia/reports/**: allow`) and `task: deny` unchanged.

## 2. Convention record — stop describing the removed gating

- [x] 2.1 `openspec/config.yaml` L22–24: reword the conventions text so it states bash is fully allowed (`bash: allow`) and drops the "`cat`/`head`/`tail`/`ls` denied, `grep`/`find`/`rg`/`fd` gated with `ask`" clause; keep the native-first *preference* as advice.
- [x] 2.2 `CLAUDE.md` L61: reword the "Bash discipline is encoded in permissions" bullet to describe `bash: allow` (native `read`/`grep`/`glob`/`list` still preferred by advice, no permission gate).

## 3. Verify

- [x] 3.1 `openspec validate analyst-allow-readonly-cli --strict` passes.
- [x] 3.2 Confirmed each of the four agent files contains `bash: allow` and no `cat*`/`head*`/`grep*`/`find*` gated keys remain (`grep -rn` returns nothing).
- [x] 3.3 Confirmed `edit` and `task` blocks unchanged — diff shows only the `bash` block collapsed; YAML parse confirms op/fusion scoped edit + orchestrator whitelist and legs' `edit: deny`/`task: deny` intact.
- [x] 3.4 `opencode` resolves the *installed* copy (`~/.config/opencode/`), not this worktree branch — running it would reflect the old installed agents and installing would mutate live user config, so validation was done at file level instead: `python3 yaml.safe_load` on each agent frontmatter confirms `bash: 'allow'` with `edit`/`task` per role.
