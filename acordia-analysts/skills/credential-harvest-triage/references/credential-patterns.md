# Credential pattern library

Portable prefixes and shapes that survive most provider rotations. Anchor detection
on the prefix; **verify the current format at the provider's docs before acting** —
lengths and checksum rules change more often than prefixes do.

This file is the single source of truth for credential detection patterns across the
analyst skill set. It is referenced by `credential-harvest-triage/SKILL.md` (first-pass
scan) and by the `## Credential extraction` sections of the pattern-citing skills
(`log-artefact-interpretation`, `web-api-authflow-analysis`, `implant-payload-re`).
Add a new provider prefix here once; every consumer inherits it.

Detection is passive: match to classify, never to validate. Record the pattern that
matched and the source location — never the raw value.

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
