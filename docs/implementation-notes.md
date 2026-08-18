# Implementation notes

Out-of-scope findings recorded during work on other changes. Nothing here has been acted on.

## `todo` does not appear in a generated omp agent's tool inventory

Found while adding the omp harness target (`omp-harness-target`, 2026-07); re-checked against the current build.

`tools/build-plugins.py` lists `todo` in `BASE_TOOLS`, so every generated omp agent under `plugins/omp/*/agents/` carries `todo` in its `tools` list. A running omp agent nonetheless reported an inventory without it, while every other allowlisted name appeared and `edit`/`task` were correctly absent — so the list is honoured and `todo` specifically does not materialise. Why was never established. Parked because it is harmless: no agent in either pillar needs a task tracker. Worth resolving if the generated `tools` list is ever relied on as an exact description of the runtime tool set.
