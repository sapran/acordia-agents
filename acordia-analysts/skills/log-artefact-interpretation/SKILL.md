---
name: log-artefact-interpretation
description: Reconstruct an ordered account of events from raw logs and artefacts across host, network and cloud, establishing first what each source actually records and its fidelity, retention and blind spots, then correlating the matched line ranges into one timeline, to answer what happened, what the environment contains, and what marks your own activity wrote.
metadata:
  acordia:
    family: evidence-forensics
    grid_row: log-artefact-interpretation
    grid_deep_in: ['T&N', Def, Fus]
    grid_working_in: [Core]
    source: docs/roles/operational-analyst.md#L107
---

# Log / Artefact Interpretation

## Objective
Read logs and artefacts across host, network, and cloud to reconstruct events, understand the environment, and see the target — and your own footprint — the way a defender's telemetry would.

## When to use
- When on-box or collected logs and artefacts hold the answer to what happened, what exists, or who did it.
- When assessing your own detectability — what evidence your actions wrote, and where it lives.

## Method
- Inventory the log corpus with `ls` / `find` / `glob` first — list every collected log source (path, size, first/last timestamp) before opening any single file.
- Identify the artefact and its semantics: know what each log/event actually records, its fidelity, retention, and blind spots before trusting it.
- Read with bounded context, exhaustive coverage: drive an exhaustive `grep`/`rg`/`jq` pass over the whole file for known indicators or timestamps, then open only the matched line-ranges — every match, not just the first — with a few lines of context. Never slurp gigabyte-scale JSON or `.evtx` files whole into context — use the parser's native pagination or offset-limited reads, and confirm the pass covered the whole file (record counts reconcile).
- Reconstruct timelines by correlating artefacts across host, network, and cloud into one ordered account of events.
- Read the environment from its exhaust — installed tooling, agents, logging config, and coverage gaps revealed by what is and isn't recorded.
- Turn the lens on yourself: locate the artefacts your own operation generated and judge what a hunter reading them would conclude.
- Distinguish signal from routine noise, and flag artefacts that have been cleared, tampered, or are conspicuously absent.
- Cite every claim by `<log-path>@L<line>` (or `<log-path>:<byte-offset>` for binary event-log formats after parser conversion) so the corroborating record is re-openable.
- If a named parser (`evtx_dump`, `jq`, `zeek-cut`, cloud-provider log CLIs) is unavailable, either substitute a documented equivalent or flag the gap and stop — never reason from a truncated `head`/`tail` alone.

## Signals / outputs
- A reconstructed timeline of events from correlated artefacts.
- A map of the environment's logging coverage, fidelity, and blind spots.
- Own-footprint assessment: what you left behind, where, and how visible it is.

## Credential extraction

Credentials leak into logs constantly. Extraction here is grep-shaped across collected log corpora; no live log-source polling.

**Application / debug logs**
- Stack traces printing config objects — search for `password=`, `token=`, `secret=`, `apiKey=`, `Authorization: `. Case-insensitive; multi-line context (`grep -B2 -A10`).
- Request logs with URLs — query-string tokens (`?api_key=`, `?access_token=`, `?sig=`); reverse-proxy access logs (`nginx`, `apache`, `envoy`) commonly hold JWTs in the query string when clients ignore the header contract.
- Debug/verbose modes (Rails logger, Django DEBUG, Spring Boot `logging.level.root=DEBUG`) — HTTP request bodies including `password` fields, session cookies, OIDC id_tokens.

**CI/CD and build logs**
- GitHub Actions/GitLab CI/Jenkins output — masked secrets *sometimes* fail to mask (env vars printed by `env` step, secrets echoed via `set -x`, base64-encoded before mask). Search for the [pattern-library](../credential-harvest-triage/references/credential-patterns.md) prefixes (`ghp_`, `AKIA`, `xox`, `eyJ`) even in logs marked "secrets masked".
- Docker build logs — `ARG` credentials leaked into image layers or build output.
- Terraform apply/plan output — resource creation surfaces secrets in `sensitive = false` outputs.

**Connection strings and config leaks**
- Full DSN patterns (`postgres://user:pass@host`, `mongodb+srv://`, `Server=...;Password=...;`) appear in ORM debug logs, migration output, health-check probes.
- Kubernetes event logs and `describe pod` output — image-pull-secret refs (safe) vs env-var secret values printed when a container crashloops (unsafe).

**System / audit logs**
- Windows Security event 4688 (process creation) with command-line auditing on — full command lines including `-Password`, `-Credential`, `net use ... /user:...`.
- Linux `auth.log` / `secure` — pam_ldap or `sudo` reads that logged the wrong field; `bash_history` shipped via syslog.

**Cross-cutting**
- Log-sourced credentials often have unknown freshness (log retention window) and unknown revocation status. Mark `freshness: unknown` unless the log line carries a timestamp inside the retention SLA. Classification and reporting via [`credential-harvest-triage`](../credential-harvest-triage/SKILL.md); source path in the report references the log file, not the credential value.
