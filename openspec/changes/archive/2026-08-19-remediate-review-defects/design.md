## Context

The review that motivated this change measured the distribution rather than reading it: nine agent bodies sized in characters, 73 skill descriptions scored pairwise, both plugin registries read, and the generator's gate list enumerated against what each gate can and cannot catch. Two things came out of that which shape the design here.

First, the repository's enforcement surface is one file. There is no CI, no hook, no lint, and by deliberate precedent (`harden-plugin-distribution`, `gate-skill-frontmatter`) none is being added. Every gate in this change therefore lives inside `tools/build-plugins.py` and runs the way everything else here runs — by hand.

Second, the most damaging failure was invisible to that file by construction. The generator's inputs are sources and its outputs are trees; what a workstation actually loads is neither. That is why `--doctor` exists as a separate mode rather than as more gates: it reads machine state, it cannot fail a build honestly, and its findings are advisory by nature.

## Goals / Non-Goals

**Goals**

- Execute contracts already stated: metadata anchors, prompt skill-set declarations, the destructive-bash denylist.
- Make one source posture mean one capability across both plugin harnesses.
- Give a maintainer one command that answers "is what I am running what this repository says".
- Leave the content phase a measured baseline to work against.

**Non-Goals**

- Any prompt or skill body content change beyond three heading casings and one skill-list line.
- Making the prompt-ceiling or duplication findings fatal. Three operator prompts breach the ceiling today and the phase that fixes them has not run; a gate that fails on the current tree would be turned off rather than obeyed.
- Restructuring the spec set. `omp-harness-distribution` is half opencode install mechanics under an omp name, and the wrapper-routing requirement is split across two specs. Both are real and neither is urgent.

## Decisions

**The bash denylist stays in all five sources.** The obvious fix — one fragment, injected at build time — would be wrong. opencode is the only harness that *enforces* these patterns, and it enforces them by reading the source file; under omp and Claude Code they are prompt-level notes. Hoisting the list out of the sources would trade a drift risk for a capability regression in the one harness where the list bites. So the canonical list lives in the generator as a constant and the gate asserts equality. Five copies remain, and they can no longer diverge.

**A path-scoped `edit` grants `write`, not nothing.** Two coherent semantics existed. Deny the write tool everywhere and the two reporting analysts cannot produce the reports their prompts require — which is why the Claude side kept `Write` in the first place. Grant it everywhere and the declaration reads honestly: the agent holds a write tool, and the path scope is a convention no harness enforces. The second is chosen because it is what was measured to be true — an omp agent whose allowlist omitted `write` still wrote a file when asked, verified against omp 17.1.8 — and because `bash: allow` is an open write channel at any path in all three harnesses. omp's documentation describes a narrower mechanism than "omission does not remove a tool", so this rests on the observation and is not generalised past it. The generated note now states the capability rather than implying a boundary.

**`role`, not `leg`.** The two pillars had converged on the same distinction under different key names, and `agent_color()` accepted either. `leg` also carried an identity (`fusion`, `target-network`) that the filename already establishes, and the filename is the dispatch handle. So `role` survives, `leg` goes, and the grid provenance that is genuinely analyst-specific — `column`, `source_paragraph` — stays where it is.

**Skill lines are recognised by shape.** The generator could match the five heading strings the prompts use today. It matches the line shape instead — kebab-case slugs joined by ` · ` — so a sixth heading cannot silently escape the resolution check. This is the same reasoning `gate-skill-frontmatter` applied when it parsed every skill rather than the ones a list named.

**`--doctor` exits 0.** A report that fails the build teaches maintainers to skip it. `--strict` exists for a caller that wants install skew and shadowing to be fatal; the four measurement sections stay advisory in every mode, because they measure the deferred phase's backlog rather than a defect in this one.

## Risks / Trade-offs

- **The gates run against never-checked sources.** Mitigated by having measured the current tree first: the expected failure set is exactly what this change repairs.
- **`--doctor` reads outside the repository.** It touches `~/.omp` and `~/.claude` read-only, tolerates their absence, and prints paths rather than contents, so it reveals nothing a maintainer cannot already see.
- **Granting `webfetch`/`websearch` widens nothing; it states a posture.** opencode's permission default is `allow`, so the analysts already fetch and search there, and omp's `BASE_TOOLS` already carries `web_search`. What the declaration buys is an explicit source contract, and survival: an agent that names the permission keeps it under a deployer's restrictive global `opencode.json`, where silence would not. Read-only in this distribution has always meant "holds no file-editing tool", and fetching is collection, not modification. The alternative — narrowing `fusion-analyst`'s body claim about open sources — would have made the prompt describe less than the role model does.
- **Five gates and a report add roughly 200 lines to a single-file generator that is already the repository's most complex artifact.** Accepted: the alternative is a second tool, and the same precedent that refused CI refuses that too.

## Migration Plan

Source edits land together, because the metadata gate and the metadata schema are two halves of one contract. Then one rebuild, then `--check`, then the sync and archive in the same PR as the code. `--doctor` is run once on the maintainer's workstation as the acceptance evidence for the shadow removal that preceded this change.

## Open Questions

- The `ollama` omp profile lists `claude-plugins` in `disabledProviders`, so ACORDIA cannot load there at all now that the shadow is gone. Enabling the provider would also pull every other user-scoped Claude Code plugin into that profile. Left as a maintainer decision; `--doctor` cannot see it, since a disabled provider is a profile setting rather than an install state.
- Whether `--doctor` should eventually read the opencode deployment under `~/.config/opencode/` as a third install surface. Deferred until someone runs `install.sh` again.
