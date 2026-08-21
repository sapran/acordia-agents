# Tasks

## 1. Lint policy

- [x] 1.1 Write `.markdownlint-cli2.jsonc`: `MD013`, `MD036`, `MD038`, `MD060` off with a reason
      beside each; `MD024` `siblings_only`; `MD033` allowing `<a>`; `MD041` accepting `description:`
      as the front-matter title.
- [x] 1.2 Put exclusions in `ignores`, not a `.markdownlintignore` — neither markdownlint-cli2 nor
      the VS Code extension reads that filename.
- [x] 1.3 Record the markdownlint version the zero was verified against.
- [x] 1.4 Confirm no build script, hook or workflow invokes a linter.

## 2. Fix every violation

- [x] 2.1 Run markdownlint's own `--fix` (548 fixes in 73 files, leaving 47). Do not hand-roll a
      fixer: a fence-unaware one injects blank lines into code blocks, which markdownlint never asks for.
- [x] 2.2 Audit every line `--fix` changed. It rewrote `__proto__` to `**proto**` in
      `attack-prototype-pollution` under MD050; restore it as a code span.
- [x] 2.3 Add a language to all 39 bare fences. Use `text` — inference misclassified 11 of 39.
- [x] 2.4 Fix three heading-level jumps: `README.md` h2→h4, and the h1→h3 subtitle in both role docs.
- [x] 2.5 Escape the shell pipes in three table rows (`k8s-postexploit`, `linux-postexploit` ×2)
      whose cells were being truncated at the first `|` with the description column dropped.
- [x] 2.6 Separate the two blockquotes in the workbook with a `>` line.
- [x] 2.7 Re-delimit `agent-roster`'s routing-form code span with double backticks; backslash-escaped
      backticks do not work inside a code span, which is why its `<skill-slug>` read as inline HTML.
- [x] 2.8 Leave `openspec/changes/archive/`, `.claude/` and `.codex/` untouched.

## 3. Lead headings

- [x] 3.1 Convert each of the nine agent prompts' lead sentence to an `H1`, trailing period stripped,
      remaining sentences kept as prose. Assert each against the original sentence before writing.
- [x] 3.2 Measure every prompt body in characters against the 10,000 ceiling. `cyber-operator` is the
      binding case at 9,984, 16 free.
- [x] 3.3 Correct the ceiling note in `docs/implementation-notes.md`: 40 free before, 24 spent, 60%,
      and a 13-character slug still fits.

## 4. Specs

- [x] 4.1 `plugin-distribution`: add the lint-policy requirement, every clause scenario-bound.
- [x] 4.2 `agent-roster`: modify the skill-line requirement — drop "directly", attribute the adjacency
      to the two generators that actually consumed it and the releases that deleted them, and require
      checks to locate lines by heading text.
- [x] 4.3 `agent-roster`: add the opening-heading requirement, every clause scenario-bound.
- [x] 4.4 Correct the same generator history in `CLAUDE.md`.

## 5. Verify

- [x] 5.1 Linter reports zero across the 120 files in scope, at cli2 0.23.2 and at 0.22.0/0.20.0/0.18.1.
- [x] 5.2 Classify every changed line; account for each one that is not blank, a fence marker, a
      heading or a blockquote marker.
- [x] 5.3 Confirm `--fix` touched no fenced content.
- [x] 5.4 Bump 4.1.0 → 4.2.0 in all four JSON files, six occurrences.
- [x] 5.5 Regenerate `acordia-map.html`, teaching its table renderer to honour `\|`.
- [x] 5.6 `~/ai/checks/check-acordia.sh` green; `openspec validate --all --strict` green.
