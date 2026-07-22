---
name: os-host-internals
description: Use when you are on or reasoning about a specific host and need to command Windows/Linux/macOS internals — to understand its state, escalate, persist, and move without tripping the host's own defenses.
metadata:
  acordia:
    grid_row: os-host-internals
    grid_deep_in: ['T&N', Def]
    grid_working_in: [Core]
    source: docs/roles/operational-analyst.md#L85
---

# OS & Host Internals

## Objective
Apply deep operating-system knowledge to a target host so you can read its true state, find privilege and persistence footholds, and operate within its native mechanisms rather than against them.

## When to use
- When you have a foothold and must escalate, persist, or pivot from a specific host.
- When you need to predict how a host will respond to an action — logging, EDR, integrity controls, isolation.

## Method
- Inventory the collected host material with `ls` / `find` / `glob` — mounted image trees, process listings, autoruns exports, service manifests, scheduled-task dumps, `.plist` bundles — before opening any single file.
- Establish host context: OS/version, patch level, privilege model, running processes/services, scheduled tasks/daemons, and installed security tooling. Drive reads with `grep`/`rg` against structured exports (`Get-CimInstance` / WMI output, `systemctl list-unit-files`, `launchctl list`, autoruns CSV); open only the matched entries by line range, not the full multi-megabyte export wholesale.
- Identify escalation vectors native to the platform — token/privilege abuse, SUID/sudo, service and DLL/dylib hijacks, misconfigured ACLs, kernel/driver exposure.
- Locate credential and secret material at rest and in memory (LSASS/keyring/keychain, tokens, caches, config).
- Choose persistence that matches the platform's legitimate mechanisms and survives reboot without standing out.
- Model the host's observation surface: what is logged, what EDR sees, and how to act inside normal process behaviour.
- Cite every finding by `<image-path>@L<line>` for text-like exports (autoruns CSV, `.reg` dumps, `plist` XML, shell histories) or `<image-path>:<byte-offset>` for binary registry hives, raw memory, and keychain files so a peer can re-open the exact key, service, or scheduled task.
- If `impacket-secretsdump`, `regripper`, `evtx_dump`, `plutil`, `chainbreaker`, or a similar named parser is unavailable, either substitute a documented equivalent (`hivex`, `python-registry`, `plistutil`) or flag the gap and stop — never infer registry or keychain contents from a hex dump alone.

## Signals / outputs
- Host state and privilege map with concrete escalation candidates.
- Credential/secret locations and access method.
- Persistence options ranked by durability vs detectability, plus the host's logging/EDR blind spots.

## Credential extraction

Per-OS map of on-disk and in-memory credential stores. Extraction is passive analysis of already-collected material (disk image, memory dump, exfiltrated profile) — never touches the live host beyond collection.

**Windows**
- `SAM` / `SECURITY` / `SYSTEM` hives (`%SYSTEMROOT%\System32\config\`) — local NTLM hashes, LSA secrets (machine account, service credentials, cached DPAPI key). Extract with `impacket-secretsdump -sam SAM -security SECURITY -system SYSTEM LOCAL`.
- DPAPI — user master keys at `%APPDATA%\Microsoft\Protect\<SID>\`; system master keys at `%SYSTEMROOT%\System32\Microsoft\Protect\S-1-5-18\`. Decrypt chain: LSA `DPAPI_SYSTEM` → system master key → user master key → credential blob. Tool: `impacket-dpapi`.
- Credential Manager — `%APPDATA%\Microsoft\Credentials\` (user) and `%SYSTEMROOT%\System32\config\systemprofile\AppData\Local\Microsoft\Credentials\` (system) blobs; unwrap through DPAPI.
- Browser saved passwords — Chrome/Edge `Login Data` SQLite in the profile dir; `password_value` column is DPAPI-encrypted (per-user). Firefox `logins.json` + `key4.db` (NSS-encrypted; primary password may be empty).
- Wi-Fi / VPN / RDP creds — `netsh wlan export profile key=clear` output if pre-collected; `.rdp` files with `password 51:b:` (DPAPI); PuTTY sessions in registry export (`HKCU\Software\SimonTatham\PuTTY\Sessions`).
- Powershell history — `%APPDATA%\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt`. Search `ConvertTo-SecureString -AsPlainText`, `-Credential`, connection-string patterns.

**Linux**
- `/etc/shadow` — password hashes (`$6$` SHA-512, `$y$` yescrypt on newer distros). Requires root at collection time.
- SSH — `~/.ssh/id_*` (private keys; passphrase-protected if the file begins with `-----BEGIN OPENSSH PRIVATE KEY-----` and the next block includes `bcrypt`), `~/.ssh/authorized_keys` (target-side identity map, not a credential per se), `~/.ssh/known_hosts` (lateral-move targets).
- GNOME Keyring — `~/.local/share/keyrings/*.keyring`; encrypted with the login password. KDE `kwallet` files under `~/.local/share/kwalletd/`.
- Shell history — `~/.bash_history`, `~/.zsh_history`, `~/.psql_history`, `~/.mysql_history`, `~/.python_history`. Search for `curl -u`, `git clone https://.*:.*@`, `export ..._TOKEN=`, `mysql -p...`.
- App config — `~/.aws/credentials`, `~/.config/gcloud/`, `~/.kube/config` (client certs and bearer tokens), `~/.docker/config.json` (base64 basic-auth), `~/.netrc`.
- Systemd credentials cache — `/etc/credstore/`, `/etc/credstore.encrypted/`.

**macOS**
- Keychain — `~/Library/Keychains/login.keychain-db` (user) and `/Library/Keychains/System.keychain` (system). Encrypted with the user's login password (or the system key stored under SIP). Offline extraction: `chainbreaker` against a collected keychain file + known password.
- iCloud Keychain sync data — `~/Library/Application Support/com.apple.sbd/`; requires SEP-derived key material, generally not extractable from a plain disk image.
- SSH agent — no on-disk state; capture is memory-only via `disk-memory-forensics`.
- Shell history + app config as Linux.
- Chrome/Safari saved passwords — protected by keychain; requires keychain extraction first.

**Cross-cutting**
- OS-store credentials classify by user scope (`scope: account` or `host`), except LSA/machine-account material which is `scope: host`+ (can pivot to domain via silver-ticket-style analysis — flag for `identity-directory-trust`). Reporting via [`credential-harvest-triage`](../credential-harvest-triage/SKILL.md); source cites path within the collected image, redacting the analyst's own home directory.
