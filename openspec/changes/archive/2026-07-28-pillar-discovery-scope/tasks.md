## 1. Implementation

- [x] 1.1 Narrow `install.sh` pillar auto-discovery to visible directories, collapsing the `.git` / `.github` / `.build` exclusion list into the dot-prefix rule
- [x] 1.2 Mirror the same predicate in `uninstall.sh`
- [x] 1.3 Remove the now-resolved leak finding from `docs/implementation-notes.md`

## 2. Verification

- [x] 2.1 Confirm `./install.sh --dry-run` no longer names `.opencode` or `.claude` and no longer deploys the five `openspec-*` skills
- [x] 2.2 Confirm the analyst pillar still deploys in full for both harnesses
- [x] 2.3 Confirm `--pillar .opencode` still deploys and still uninstalls
- [x] 2.4 Remove the already-published `openspec-*` skills from `~/.config/opencode/skills/` and `~/.omp/agent/skills/`
