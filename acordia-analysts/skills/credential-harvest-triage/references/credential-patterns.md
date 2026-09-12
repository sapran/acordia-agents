# Credential pattern library

Portable prefixes and shapes that survive most provider rotations. Anchor detection
on the prefix; **verify the current format at the provider's docs before acting** —
lengths and checksum rules change more often than prefixes do.

This file is the single source of truth for credential detection patterns across the
analyst skill set. It is referenced by `credential-harvest-triage/SKILL.md` (first-pass
scan) and by the `## Credential extraction` sections of the pattern-citing skills
(`log-artefact-interpretation`, `web-api-authflow-analysis`, `implant-payload-re`).
Add a new provider prefix here once; every consumer inherits it.

Detection is passive: match to classify, never to validate. Send a scan's matches to a
file rather than to standard output, and work from the pattern that matched plus the
source location; what the values are is a later question, decided by ownership per
`credential-harvest-triage`. Asset fingerprints below steer search selection; they are
not credentials and never authorise validation or live access.

## Asset fingerprints used to steer searches

Non-secret system indicators that scope a targeted credential search to the system class
the orientation packet names. They identify where credential material is likely to sit;
they carry no secret and confer no permission.

```text
minioadmin|MINIO_ROOT_USER|MINIO_ROOT_PASSWORD          # MinIO server env/config
s3\.amazonaws\.com|S3_ACCESS_KEY|S3_SECRET_KEY          # S3-compatible storage refs
bucket=[A-Za-z0-9._-]+|endpoint_url=.*amazonaws|endpoint_url=.*:9000  # S3/MinIO client config
(mongodb|postgres|postgresql|mysql|mariadb|redis|mssql)://              # database DSN heads
DB_HOST|DB_USER|DB_PASS|DATABASE_URL|connectionString   # database config keys
smb://|\\\\\\\\[A-Za-z0-9.-]+\\\\|mount -t (cifs|nfs)   # SMB/NFS share refs
kubeconfig|kubectl|\.kube/config|serviceaccount|service-account\.yaml  # Kubernetes
image: .*registry|docker (login|pull)|DOCKER_AUTH_CONFIG  # registries/container auth
\.gitlab-ci\.yml|jenkins|JENKINS_URL|GITHUB_ACTIONS|circleci  # CI/CD systems
vault:|VAULT_TOKEN|secretsmanager|aws_secretsmanager_secret  # secret stores
openvpn|wireguard|amneziawg|awg0|anyconnect|forticlient|pptp|l2tp  # VPN / remote access
krb5|kinit|keytab|KRB5CCNAME|ntds\.dit|ntdsutil         # Kerberos / directory
id_rsa|id_ed25519|authorized_keys|known_hosts|ssh-agent # SSH material context
```

## Config-file structural markers

The skeleton a real configuration file carries, as against the name it happens to have. Like the
fingerprints above these are non-secret locators: they identify a file class and confer no
permission. They exist because a filename is not searchable evidence — a `.ovpn` string matches
every document that *mentions* the extension, and a WireGuard or AmneziaWG config carries no
extension at all.

Unlike the value-shaped patterns further down, every marker here sits on the line the secret is on,
so a scan runs with `-l`/`-c` or redirects to a file — never a bare `grep` to the terminal. The two
multi-line patterns need `rg -U` (or `grep -Pz`) to match across a newline at all, and silently
return nothing without it.

```text
\[Interface\][\s\S]{0,255}?PrivateKey\s*=              # WireGuard / AmneziaWG config body
PresharedKey\s*=                                       # WireGuard peer preshared key
\b(Jc|Jmin|Jmax|S1|S2|H1|H2|H3|H4)\s*=\s*[0-9]+        # AmneziaWG DPI-evasion params
auth-user-pass|remote-cert-tls server|key-direction\s+[0-9]|tls-auth  # OpenVPN directives
<(cert|key|tls-auth|tls-crypt)>                        # OpenVPN inline material block (opening tag only)
PuTTY-User-Key-File-[23]:                              # PuTTY .ppk header (formats 2 and 3)
Private-Lines:\s*[0-9]+|Private-MAC:                   # PuTTY .ppk private block
crypto isakmp key|crypto ikev2 keyring|pre-shared-key\s+(local|remote|address|hostname)\b  # IPsec / IKE PSK config
full address:s:|username:s:                            # Windows .rdp profile fields
```

`Jc`/`Jmin`/`Jmax`, `S1`/`S2` and `H1`–`H4` are AmneziaWG's obfuscation parameters — the
DPI-resistant WireGuard fork — and they identify a config **already in hand**. They are not search
terms: `S1`, `H1` and their siblings are two-character tokens that match everything, and pairing one
with a bracketed section name does not rescue the query, because the bracket is discarded.

The inline-block marker stops at the opening tag on purpose, as the PEM markers below do: tying it
to its closing tag would make the private-key body part of the match, and a scan's output file is a
store of locations rather than a second store of keys.

**Two consumption paths, and they behave differently.** Over raw bytes — a slice on disk, per
`exhaustive-data-processing` — the whole pattern applies, punctuation included. As an Aleph `q`
term it does not: the index discards punctuation, so `</key>` reduces to the token `key` and
returns the reported cap, and a hyphenated marker is split into its parts — `auth-user-pass`
unquoted returned 407 where `"auth-user-pass"` quoted returned 1. Search the rare token
(`PrivateKey`, `PresharedKey`, `isakmp`) or the quoted phrase (`"auth-user-pass"`,
`"PuTTY-User-Key-File"`, `"remote-cert-tls server"`), ANDed with a second marker from the same
format. Do not ask for `highlight` on a credential marker: in every format here the secret is the
remainder of the matched line, so the fragment carries the value, and unlike a local scan a tool
result cannot be redirected to a file. Record an Aleph hit as `collection_id` + `entity_id` +
`schema`. `aleph-entity-graph` carries the platform reasoning and the measured figures.

**The passphrase is usually not in the file.** A config arrives in one message and its password in
another, so a config located by marker is the starting point for a pivot to its carrier — the
document's own container, thread or correspondent entity, all of them read-only pivots inside the
corpus — rather than the finding itself. Do not reach for a corpus-wide password-vocabulary query
to close that gap: measured on one collection, `конфиг`
paired with password vocabulary returned 1,911 hits and an attachment-and-password form 7,084, both
effectively pure chat noise, while the specific phrase an analyst expects to find — `"пароль от
конфига"` — returned nothing at all. Pivot from the artefact you have; do not sweep for the sentence
you imagine.

## API keys (prefix anchored)

```text
AKIA[0-9A-Z]{16}                              # AWS access key ID (long-term)
ASIA[0-9A-Z]{16}                              # AWS temp session
AIza[0-9A-Za-z_\-]{35}                        # Google API key
AGQ[A-Za-z0-9_-]{20,}                         # GitHub app installation token (recent)
ghp_[A-Za-z0-9]{36}                           # GitHub personal token
gho_[A-Za-z0-9]{36}                           # GitHub OAuth token
ghs_[A-Za-z0-9]{36}                           # GitHub server-to-server
ghu_[A-Za-z0-9]{36}                           # GitHub user-to-server
glpat-[A-Za-z0-9_\-]{20}                      # GitLab personal token
xox[baprs]-[A-Za-z0-9-]{10,}                  # Slack bot/app/refresh tokens
sk-[A-Za-z0-9]{20,}                           # OpenAI-style secret key
sk-ant-[A-Za-z0-9\-_]{80,}                    # Anthropic API key
npm_[A-Za-z0-9]{36}                           # npm token
pypi-AgEIcHlwaS5vcmc[A-Za-z0-9\-_]+           # PyPI token (macaroon)
dckr_pat_[A-Za-z0-9_\-]{27,}                  # Docker Hub PAT
```

## Auth material shapes

```text
eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+   # JWT (base64 header.payload.signature)
Bearer\s+[A-Za-z0-9_\-\.=]+                    # HTTP bearer header
Authorization:\s*Basic\s+[A-Za-z0-9+/=]+       # HTTP basic (base64 user:pass)
```

## Password hashes

```text
\$1\$[./A-Za-z0-9]{8}\$[./A-Za-z0-9]{22}                # MD5 crypt
\$2[abxy]?\$[0-9]{2}\$[./A-Za-z0-9]{53}                 # bcrypt
\$5\$(rounds=[0-9]+\$)?[./A-Za-z0-9]{16}\$[./A-Za-z0-9]{43}  # SHA-256 crypt
\$6\$(rounds=[0-9]+\$)?[./A-Za-z0-9]{16}\$[./A-Za-z0-9]{86}  # SHA-512 crypt
[a-fA-F0-9]{32}                                          # NTLM / LM (also MD5; disambiguate by source)
[^:]+::[^:]+:[a-fA-F0-9]{16}:[a-fA-F0-9]{32}:[a-fA-F0-9]{32,}  # NetNTLMv2
```

## Connection strings

```text
(mongodb|postgres|mysql|redis)(\+srv)?://[^:@\s]+:[^@\s]+@[^\s/]+  # user:pass DSN
Server=[^;]+;.*Password=[^;]+;                                     # SQL Server ADO
DefaultEndpointsProtocol=https;AccountName=[^;]+;AccountKey=[^;]+  # Azure Storage
```

## Private keys (PEM markers)

```text
-----BEGIN (RSA|EC|OPENSSH|DSA|PGP) PRIVATE KEY(\s+BLOCK)?-----
-----BEGIN ENCRYPTED PRIVATE KEY-----
```

## Cloud service accounts

```text
"type":\s*"service_account"                    # GCP JSON key file marker
"private_key":\s*"-----BEGIN                   # GCP JSON key (embedded PEM)
"clientSecret":\s*"[A-Za-z0-9_\-\.~]+"          # Azure SP JSON
aws_access_key_id\s*=\s*AKIA[0-9A-Z]{16}       # ~/.aws/credentials line
aws_secret_access_key\s*=\s*[A-Za-z0-9/+=]{40} # ~/.aws/credentials line
```

## Kubernetes / secret files

```text
apiVersion:\s*v1[\s\S]*?kind:\s*Secret         # k8s Secret manifest
kubeconfig[\s\S]*?client-key-data:             # kubeconfig with embedded key
```
