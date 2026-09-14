## Why

A shipped skill body named its reference files only by a path relative to itself. No harness read
tool resolves such a path, so a session that wanted the file had to invent an absolute one — and the
invented path is wrong in a way nothing corrects.

It happened twice in three days on the operator's workstation, both times to
`credential-harvest-triage`'s two reference files, and the second time is recorded end to end in a
live sweep's session log (2026-09-14). The analyst read `skill://credential-harvest-triage`
correctly, served from the profile's plugin cache at 6.13.0. Two minutes later it wanted
`references/report-layout.md` and `references/credential-patterns.md`, had no address for either, and
globbed a guessed path under omp's native skills root — empty on that host — producing
`Path not found`. It recovered by running `find /` and reading both files out of a stale marketplace
clone sitting four commits behind the installed version. Two days earlier the same two files failed
for the other reason: the correct `skill://` form resolved into a native symlink farm that shadowed
the plugin.

Three costs, none of which the harness reports:

1. **The reference is silently lost.** A `Path not found` on a skill's own reference file reads to an
   operator as a broken install, and the shipped diagnosis — check the version — is wrong, because the
   version was current both times.
2. **The recovery is worse than the failure.** A filesystem-wide search resolves to whichever copy of
   the distribution happens to exist on the host. Here it was a clone four commits behind; the two
   files happened to be byte-identical, so the sweep was unharmed by luck rather than by design.
3. **A cross-skill pointer is worse still.** Four bodies point at
   `credential-harvest-triage/references/credential-patterns.md`, three of them through
   `../credential-harvest-triage/…`, and seven more point at the triage skill itself the same way.
   That form presumes a sibling directory on disk and a resolver that reads relative to a skill body;
   neither harness offers the second.

Nothing in the tree used the resolvable form: `skill://` appeared zero times across 45 skills, 5
agents and 10 wrappers before this change.

## What Changes

- All **eight** reference pointers, across five skill bodies, gain the resolvable address
  `skill://credential-harvest-triage/references/<file>.md` as their link target, keeping the file's
  own name as the visible text so both are stated in one construct: `credential-harvest-triage` (4 —
  step 3's pattern-library pointer, the report-layout pointer in step 9, and the `## Pattern library`
  and `## Report layout` paragraphs), `implant-payload-re`, `web-api-authflow-analysis`,
  `log-artefact-interpretation` and `aleph-entity-graph` (1 each). The three
  `../credential-harvest-triage/…` targets and the one bare code-span mention are gone.
- The **seven** remaining relative pointers at the triage skill itself —
  `[`credential-harvest-triage`](../credential-harvest-triage/SKILL.md)` in the credential-extraction
  section of `cloud-controlplane-analysis`, `disk-memory-forensics`, `identity-directory-trust`,
  `implant-payload-re`, `log-artefact-interpretation`, `os-host-internals` and
  `web-api-authflow-analysis` — become `skill://credential-harvest-triage`. They are the same defect
  in the same class: six of the seven route a finding to the ownership and disclosure doctrine, so the
  pointer that failed to open was the pointer to the rules deciding what may be written down. After
  this change no link target under `acordia-analysts/skills/` is a relative path.
- `credential-harvest-triage`'s `## Cross-cutting notice` states both addresses literally, refuses a
  reconstructed path into a harness skills directory — the failure actually observed — and names the
  terminal behaviour when neither address opens: say so and ask the operator, never search the
  filesystem for a copy of unknown vintage.
- Version `6.13.0` → `6.14.0` across the three JSON files. `acordia-map.html` is regenerated from the
  merged tree as a follow-up `docs:` commit on the integration branch, which is how every previous
  release of this repository has moved it.

Capability touched: `skill-library` — one MODIFIED requirement. The published scenario *Skill body
names each reference file* asserted that a pointer states the file's path relative to `SKILL.md`,
which the pointers still do; the requirement is modified because it **permitted** a pointer that gives
only that path, so without the change an author closes these eight and reopens the ninth. The
modified text separates the two roles a pointer's parts play — the URI is the address measured to
resolve, the filename is identification — rather than calling both openable.

## Impact

`acordia-analysts/skills/*/SKILL.md` — nine bodies in total: five carrying reference pointers
(`credential-harvest-triage`, `implant-payload-re`, `web-api-authflow-analysis`,
`log-artefact-interpretation`, `aleph-entity-graph`) and four more carrying only the pointer at the
triage skill (`cloud-controlplane-analysis`, `disk-memory-forensics`, `identity-directory-trust`,
`os-host-internals`) — the other three of the seven skill-to-skill pointers sit in bodies already in
the first set. Plus `openspec/specs/skill-library/spec.md`, the three version literals, and
`acordia-map.html` in the follow-up commit, whose rebuilt model is what established this count: nine
skill records changed and no other.

The competency grid does not move, and no column gains or loses a mark. Seven of the nine edited
skills are grid-row skills whose `row` ids, `grid_deep_in` and `grid_working_in` are untouched; the
other two — `credential-harvest-triage` and `aleph-entity-graph` — are procedural with
`grid_row: null`. This changes how a body addresses a file, not what any analyst is competent in.

No reference file's content changes, so nothing about what may be disclosed moves, and
`credential-harvest-triage`'s `## Guardrails` block is byte-identical. No credential value was read to
produce this change: the evidence is a `Path not found` line, a tool record naming a resolved path,
and a `cmp` of two copies of a layout file.
