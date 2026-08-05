# Implementation notes

Out-of-scope findings recorded during work on other changes. Nothing here has been acted on.

## `todo` does not appear in a translated agent's tool inventory

Found while adding the omp harness target (`omp-harness-target`, 2026-07).

`tools/build-plugins.py` (then named `tools/translate-omp.py`) puts `todo` in the generated omp allowlist, but a running translated leg agent reported a tool inventory of `read`, `grep`, `glob`, `bash`, `web_search`, `yield`, `hub`, `write` — no `todo`. The other allowlisted names all appeared, and `edit`/`task` were correctly absent, so the allowlist is being honoured; why `todo` specifically does not materialise was not established. Harmless either way: an analyst agent has no use for a task tracker. Worth resolving if the allowlist is ever relied on as an exact description of the runtime tool set.
