---
name: attack-subdomain-takeover
description: Claim a dangling subdomain — enumerate names passively and from certificate transparency, resolve each CNAME to its third-party service, match the unclaimed-resource fingerprint such as NoSuchBucket or a missing Pages site, then register the resource and serve proof content under the target's own name. Reach for it when DNS still points at a cloud service that no longer answers for it.
metadata:
  acordia:
    family: web-attack
  cyberstrike:
    source: .cyberstrike/skill/attack-subdomain-takeover/SKILL.md
    commit: 359655518
---

# Subdomain Takeover

## Objective

Identify subdomains with dangling DNS records (CNAME pointing to unclaimed cloud resources) and claim them to serve attacker content.

## Testing Methodology

### Phase 1: Subdomain Enumeration

```bash
# Passive enumeration
subfinder -d TARGET.com -silent | tee subdomains.txt

# Certificate transparency
curl -s "https://crt.sh/?q=%25.TARGET.com&output=json" | jq -r '.[].name_value' | sort -u >> subdomains.txt

# DNS brute force
puredns bruteforce wordlist.txt TARGET.com -r resolvers.txt >> subdomains.txt
```

### Phase 2: Automated Takeover Check

```bash
# Check all subdomains for takeover — resolve CNAME then fingerprint the response
while read -r sub; do
  cname=$(dig +short CNAME "$sub")
  [ -z "$cname" ] && continue
  body=$(curl -s -m 5 "https://$sub")
  case "$cname" in
    *github.io*)        echo "$body" | grep -qi "There isn't a GitHub Pages site here" && echo "TAKEOVER $sub -> $cname (GitHub Pages)" ;;
    *herokuapp.com*)    echo "$body" | grep -qi "No such app" && echo "TAKEOVER $sub -> $cname (Heroku)" ;;
    *myshopify.com*)    echo "$body" | grep -qi "Sorry, this shop is currently unavailable" && echo "TAKEOVER $sub -> $cname (Shopify)" ;;
    *tumblr.com*)       echo "$body" | grep -qi "there's nothing here" && echo "TAKEOVER $sub -> $cname (Tumblr)" ;;
    *wordpress.com*)    echo "$body" | grep -qi "Do you want to register" && echo "TAKEOVER $sub -> $cname (WordPress)" ;;
    *s3.amazonaws.com*|*s3-website*) echo "$body" | grep -qi "NoSuchBucket" && echo "TAKEOVER $sub -> $cname (AWS S3)" ;;
    *elasticbeanstalk.com*) echo "$body" | grep -qi "404 Not Found" && echo "CHECK $sub -> $cname (AWS Elastic Beanstalk)" ;;
    *azurewebsites.net*) echo "$body" | grep -qi "404 Web Site not found" && echo "TAKEOVER $sub -> $cname (Azure Web Apps)" ;;
    *netlify.app*)       echo "$body" | grep -qi "Not Found - Request ID" && echo "TAKEOVER $sub -> $cname (Netlify)" ;;
    *vercel.app*)        echo "$body" | grep -qi "DEPLOYMENT_NOT_FOUND" && echo "TAKEOVER $sub -> $cname (Vercel)" ;;
    *fastly.net*)        echo "$body" | grep -qi "Fastly error: unknown domain" && echo "TAKEOVER $sub -> $cname (Fastly)" ;;
    *fly.dev*)           echo "$body" | grep -qi "404 Not Found" && echo "CHECK $sub -> $cname (Fly.io)" ;;
    *bitbucket.io*)      echo "$body" | grep -qi "Repository not found" && echo "TAKEOVER $sub -> $cname (Bitbucket)" ;;
    *surge.sh*)          echo "$body" | grep -qi "project not found" && echo "TAKEOVER $sub -> $cname (Surge)" ;;
    *ghost.io*)          echo "$body" | grep -qi "The thing you were looking for is no longer here" && echo "TAKEOVER $sub -> $cname (Ghost)" ;;
    *pantheonsite.io*)   echo "$body" | grep -qi "The gods are wise" && echo "TAKEOVER $sub -> $cname (Pantheon)" ;;
    *zendesk.com*)       echo "$body" | grep -qi "Help Center Closed" && echo "TAKEOVER $sub -> $cname (Zendesk)" ;;
    *readme.io*)         echo "$body" | grep -qi "Project doesnt exist" && echo "TAKEOVER $sub -> $cname (README.io)" ;;
    *cargocollective.com*) echo "$body" | grep -qi "404 Not Found" && echo "CHECK $sub -> $cname (Cargo)" ;;
    *feedpress.me*)      echo "$body" | grep -qi "The feed has not been found" && echo "TAKEOVER $sub -> $cname (Feedpress)" ;;
  esac
done < subdomains.txt

# subjack, where installed, fingerprints the same services straight from a list
subjack -w subs.txt -t 100 -o takeover.txt
```

Checks 20 cloud services:
- GitHub Pages, Heroku, Shopify, Tumblr, WordPress
- AWS S3, AWS Elastic Beanstalk, Azure Web Apps
- Netlify, Vercel, Fastly, Fly.io
- Bitbucket, Surge, Ghost, Pantheon
- Zendesk, README.io, Cargo, Feedpress

### Phase 3: Manual CNAME Verification

```bash
# Check CNAME records
dig +short CNAME subdomain.TARGET.com

# Verify the pointed service is unclaimed
curl -s https://subdomain.TARGET.com
# Look for: "There isn't a GitHub Pages site here"
# "No such app" (Heroku)
# "NoSuchBucket" (S3)
```

### Phase 4: Cloud Storage Enumeration

```bash
# Check related cloud buckets for public access
for bucket in "TARGET" "TARGET-backup" "TARGET-assets" "TARGET-static" "www-TARGET"; do
  echo "== $bucket =="
  curl -s -o /dev/null -w "S3 (%{http_code}) " "https://$bucket.s3.amazonaws.com/"
  curl -s -o /dev/null -w "GCS (%{http_code}) " "https://storage.googleapis.com/$bucket/"
  curl -s -o /dev/null -w "Azure (%{http_code})\n" "https://$bucket.blob.core.windows.net/$bucket?restype=container&comp=list"
done
```

### Phase 5: Claim & Verify

After confirming a dangling CNAME:
1. Create the resource on the target service (e.g., GitHub Pages repo, S3 bucket)
2. Serve a harmless proof page (e.g., `cyberstrike-takeover-proof.html`)
3. Verify it's accessible at `subdomain.TARGET.com`

## What Constitutes a Finding

| Finding | Severity |
|---------|----------|
| Subdomain takeover — attacker controls content | High (P2) |
| S3 bucket public write access | Critical (P1) |
| S3 bucket listing enabled | High (P2) |
| Dangling CNAME (service unreachable) | Medium (P3) |
| Cloud storage public read | Medium (P3) |

## Evidence Requirements

- Subdomain with dangling CNAME record
- Target cloud service identified
- Service fingerprint (error message)
- For takeover: proof of content hosting on subdomain
- For buckets: listing output or write proof

## Tools

- `dig` + fingerprint loop (Phase 2) — automated CNAME + fingerprint checker
- `curl` bucket-probe loop (Phase 4) — S3/Azure/GCP enumeration
- `subfinder`, `puredns` — subdomain enumeration
- `subjack -w subs.txt -t 100 -o takeover.txt` (external) — bulk takeover fingerprinting

## References

- [Can I Take Over XYZ](https://github.com/EdOverflow/can-i-take-over-xyz)
- [HackerOne: Subdomain Takeover](https://www.hackerone.com/vulnerability-management/guide-subdomain-takeovers)
