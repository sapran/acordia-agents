## Why

A shipped skill body names its reference files only by a path relative to itself. No harness read
tool resolves such a path, so a session that wants the file has to invent an absolute one — and the
invented path is wrong in a way nothing corrects.

It happened twice in three days on the operator's `mini` host, both times to
`credential-harvest-triage`'s two reference files, and the second time is recorded end to end in the
session log of a live sweep (`opwe` profile, 2026-09-14T10:35:01Z). At 10:32:43 the analyst read
`skill://credential-harvest-triage` correctly, served from the profile's plugin cache at 6.13.0. Two
minutes later it wanted `references/report-layout.md` and `references/credential-patterns.md`, had no
address for either, and globbed `~/.omp/agent/skills/credential-harvest-triage/**` — omp's native
skills root, empty on that host — producing `Path not found`. It recovered by running `find /` and
reading both files out of a stale Claude Code marketplace clone sitting four commits behind the
installed version. On 2026-09-12 the same two files failed for the other reason: the correct
`skill://` form resolved into a native symlink farm that shadowed the plugin.

Three costs, none of which the harness reports:

1. **The reference is silently lost.** A `Path not found` on a skill's own reference file reads to an
   operator as a broken install, and the shipped diagnosis — check the version — is wrong, because the
   version was current both times.
2. **The recovery is worse than the failure.** A filesystem-wide search resolves to whichever copy of
   the distribution happens to exist on the host. Here it was a clone of `develop` at 6.12.0; the two
   files happened to be byte-identical, so the sweep was unharmed by luck rather than by design.
3. **A cross-skill pointer is worse still.** Four bodies point at
   `credential-harvest-triage/references/credential-patterns.md`, three of them through
   `../credential-harvest-triage/…`. That form presumes a sibling directory on disk and a resolver
   that reads relative to a skill body; neither harness offers the second.

Nothing in the tree used the resolvable form: `skill://` appeared zero times across 45 skills, 5
agents and 10 wrappers before this change.

## What Changes

- All **eight** reference pointers, across five skill bodies, gain the resolvable address
  `skill://credential-harvest-triage/references/<file>.md` as their link target, keeping the relative
  filename as the visible text so both addresses are stated in one construct:
  `credential-harvest-triage` (4 — step 3's pattern-library pointer, the report-layout pointer in
  step 9, and the `## Pattern library` and `## Report layout` paragraphs), `implant-payload-re`,
  `web-api-authflow-analysis`, `log-artefact-interpretation` and `aleph-entity-graph` (1 each). The
  three `../credential-harvest-triage/…` targets and the one bare-code-span mention are gone.
- `credential-harvest-triage`'s `## Cross-cutting notice` states where its reference files ship, the
  two addresses that open them, and that a path into a harness skills directory is never
  reconstructed — the failure actually observed, named so it is refused rather than repeated.
- Version `6.13.0` → `6.14.0` across the three JSON files; `acordia-map.html` regenerated.

Capability touched: `skill-library` — one MODIFIED requirement. The published scenario *Skill body
names each reference file* asserts that a pointer states the file's path relative to `SKILL.md`,
which the dual form still satisfies; the requirement is modified because it currently **permits** a
pointer that gives only that path, so without the change an author closes these eight and reopens the
ninth.

## Impact

`acordia-analysts/skills/{credential-harvest-triage,implant-payload-re,web-api-authflow-analysis,log-artefact-interpretation,aleph-entity-graph}/SKILL.md`,
`openspec/specs/skill-library/spec.md`, the three version literals, `acordia-map.html`.

The competency grid does not move, and no column gains or loses a mark. Four of the five edited
skills are grid-row skills whose `row` ids, `grid_deep_in` and `grid_working_in` are untouched; the
fifth is procedural with `grid_row: null`. This changes how a body addresses a file, not what any
analyst is competent in.

No reference file's content changes, so nothing about what may be disclosed moves. No credential
value was read to produce this change: the evidence is a `Path not found` line, a tool record naming
a resolved path, and a `cmp` of two copies of a layout file.
