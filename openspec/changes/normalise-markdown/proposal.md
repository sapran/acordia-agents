# Normalise markdown across the authored tree

## Why

Opening any file in this repository in VS Code produces a wall of markdownlint warnings. There is no
lint configuration, so the editor applies stock defaults that know nothing about how this distribution
is written. Measured with markdownlint-cli2 0.23.2 (markdownlint 0.41.1) over the 120 files in scope on
`develop`, with `{"default": true}`, there are **2,984** violations:

| Rule | Count | Rule | Count |
|---|---|---|---|
| MD013 line-length | 2,097 | MD024 no-duplicate-heading | 6 |
| MD060 table-column-style | 411 | MD056 table-column-count | 3 |
| MD022 blanks-around-headings | 271 | MD001 heading-increment | 3 |
| MD032 blanks-around-lists | 244 | MD050 strong-style | 2 |
| MD040 fenced-code-language | 39 | MD049 emphasis-style | 2 |
| MD036 no-emphasis-as-heading | 37 | MD033 no-inline-html | 2 |
| MD041 first-line-heading | 27 | MD058, MD047, MD028, MD012 | 1 each |
| MD031 blanks-around-fences | 26 | | |

Four of these fire on things this repository does on purpose. MD013 wants 80-column prose, but one
paragraph per line is what keeps a prose diff to the paragraph that changed. MD036 reads a standalone
bold label as a botched heading; the 37 occurrences are in seven analyst skills and both role
documents, where a bold lead-in introduces a list rather than opening a section. MD038 objects to a
code span with a trailing space, but the agent description prefix is exactly `ACORDIA Analysis — `,
space included, and quoting it without the space would misstate the contract the roster requires.
MD060 demands that table pipes line up visually; 55 of its 411 cannot be auto-fixed, and every one of
those is in a ported operations skill whose cells hold em dashes and inline code, where padding to
align by character count is churn no reader benefits from.

Left unconfigured this costs more than irritation. An editor reporting 2,984 violations trains its
reader to treat warnings as noise, so a real one arrives in the same colour as the 2,097 that are not.
It also produced the accident that prompted this change: an author fixing what the editor flagged, in
good faith, and disturbing a convention nobody had documented as load-bearing.

## What changes

- **A committed lint policy** in `.markdownlint-cli2.jsonc`, disabling those four rules with the reason
  recorded beside each, configuring three more to match how this repository is written, and excluding
  the immutable archive and vendored tooling. The file is read both by markdownlint-cli2 and by the
  `DavidAnson.vscode-markdownlint` extension, which is the same engine — so the editor and the tree
  finally agree.
- **Every remaining violation fixed**, taking the in-scope tree to zero. 2,937 by markdownlint's own
  `--fix`; the 47 it cannot fix by hand: 39 fence languages, 3 heading levels, 3 broken table rows,
  1 blockquote separator, 1 inline-HTML placeholder.
- **Three shipped skills stop dropping data.** MD056 found three table rows whose inline code contains
  an unescaped shell pipe, so the renderer reads it as a cell separator: the command renders truncated
  at the first `|` and the description column disappears. `k8s-postexploit` loses "Extract and decode
  all Kubernetes Secrets"; `linux-postexploit` loses two. Escaping the pipes as `\|` makes the existing
  cells render without changing a word.
- **A lead heading in all nine agent prompts**, formed from the prompt's opening sentence, matching what
  two already carried. This is a style choice, not a lint fix: MD041 is satisfied by the `description`
  frontmatter key.

## What the official fixer got wrong

`markdownlint --fix` is not safe to run unaudited on this tree, and two of its edits had to be reverted:

- **MD050 rewrote a payload.** In `attack-prototype-pollution` it read `__proto__` as strong emphasis
  and replaced it with `**proto**` — destroying the literal JavaScript property that the entire skill
  is about. Now a code span, which is what it always should have been.
- **MD049 and MD050 rewrite emphasis markers**, which is harmless in prose and not harmless next to
  identifiers that use underscores. Every added line carrying emphasis was inspected, not sampled.

Verification for this change is therefore twofold: the linter reports zero, **and** every changed line
is classified. Of 472 changed lines outside the JSON manifests, 378 are blank, 78 are fence markers,
15 are headings, 1 is a blockquote marker, and all 34 remaining are individually accounted for — the
nine lead-sentence splits, three escaped table rows, one restored `__proto__`, one repaired code span,
and the documentation edits this change makes deliberately.

## Impact

- 85 files change. `openspec/changes/archive/`, `.claude/` and `.codex/` are untouched.
- `cyber-operator`'s prompt body grows 24 characters, 9,960 → 9,984 of its 10,000 ceiling. That spends
  24 of the 40 characters that were free — 60% of the remaining headroom on the most pressured artefact
  in the distribution, for a change that alters no prose. 16 characters remain, which still admits a
  slug of up to 13 characters plus its separator but no prose at all.
- Version 4.1.0 → 4.2.0. Every prompt and skill body a user receives changes, so without the bump an
  installed plugin never sees it.
- No agent, skill, command, family or count changes, which is why this is MINOR.

## A note on the pre-existing markup bug this surfaced

`agent-roster` described a prompt's routing form as `` `- **<situation>** → \`<skill-slug>\`` ``,
using backslash-escaped backticks inside a code span. CommonMark does not honour backslash escapes
inside code spans, so that span ended early and `<skill-slug>` was never code — which is why MD033
flagged it as inline HTML. Re-delimited with double backticks, which is how a code span carrying
backticks is written.
