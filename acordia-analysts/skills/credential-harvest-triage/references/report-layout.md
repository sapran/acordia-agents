# Credential Sweep Report Layout

This is the fixed shape of the HTML product that step 9 of `credential-harvest-triage` emits. It
decides presentation only, and adds nothing to what the skill's `## Guardrails` permit to be
disclosed.

## The organising principle

The report is organised by **the system each credential opens** — never by artefact, by file, or by
the collection the material came from. A reader must come away seeing an access, not a list of
strings: an account and a key that open the same endpoint belong in the same section even when they
were recovered from different archives, and two keys from the same archive that open different
systems belong apart. A credential whose system could not be identified goes in the residual section
rather than being filed under a guess, because filing it under a guess asserts an access the
evidence does not support.

## Document order

The spine is fixed. Everything sits inside a single `<div class="wrap">` under `<body>`; the
document is `<html lang="…">` naming the corpus language, carries `<meta charset="utf-8">`, and has
one `<title>` of the form `<Product> — <Target> · <YYYY-MM-DD>`.

0. `<h1>` — the on-page title, `<Product> — <Target>`. The date belongs to the dateline below it,
   not to the heading.
1. `<div class="sub">` — the dateline: organising principle · collections (id + name) · instance URL
   · generated date · report mode.
2. `<div class="banner">` — the bottom line, up front.
3. System sections, numbered `1..N` and ordered by consequence rather than by discovery:
   `<h2>N. <access class> — <system, endpoint></h2>`. Each opens with one `div.cred.sys` dossier
   block, then optionally one count-bearing `<h3>` naming what the following blocks are and how many
   there are (`<h3>7 operator logins recovered</h3>`), then the repeated `div.cred` credential
   blocks.
4. `<h2>N+1. Secrets with no system identified (residual)</h2>` — credential blocks, or a
   `<div class="cv">` stating the negative when there are none.
5. `<h2>N+2. Excluded and borderline</h2>` — `div.cred` blocks carrying a bare `<span class="tag">`.
6. `<h2>N+3. Coverage</h2>` — one `table.grid`, then three `p.meta`.
7. `<h2>N+4. Gaps</h2>` — one `<ol>`.
8. `<h2>N+5. Hand-off</h2>` — one `<p>`, then one `div.alert`.
9. `<div class="footer">`.

A finding whose ownership refuses disclosure is **not** a separate section. It sits in its own
system section as an ordinary credential block with no `<details>` at all — the access is real and
the reader needs to know it exists, so only the value is withheld. The residual section is for a
credential with no identified system; `Excluded and borderline` is for material that is not a
finding. Neither is a place to file something ownership merely refused.

## The stylesheet

```css
:root{--fg:#1a1a1a;--muted:#5a5a5a;--line:#d8d8d8;--accent:#7a1f1f;--bg:#fafafa;--panel:#fff}
*{box-sizing:border-box}
body{font-family:-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans","DejaVu Sans",sans-serif;color:var(--fg);background:var(--bg);margin:0;line-height:1.5}
.wrap{max-width:1000px;margin:0 auto;padding:24px 20px 80px}
h1{font-size:1.6em;border-bottom:3px solid var(--accent);padding-bottom:8px;margin-bottom:4px}
h2{font-size:1.25em;margin-top:34px;border-bottom:1px solid var(--line);padding-bottom:5px}
h3{font-size:1.05em;margin:20px 0 8px}
.sub{color:var(--muted);font-size:.92em;margin-bottom:18px}
.banner{background:#f3e5e5;border-left:4px solid var(--accent);padding:12px 14px;border-radius:4px;margin:16px 0}
.meta{color:var(--muted);font-size:.85em}
table.kv{width:100%;border-collapse:collapse;margin:6px 0 10px;font-size:.9em}
table.kv td{border:1px solid var(--line);padding:5px 8px;vertical-align:top}
table.kv td:first-child{width:150px;font-weight:600;background:#f3f3f3}
table.grid{width:100%;border-collapse:collapse;font-size:.85em;margin:10px 0}
table.grid th,table.grid td{border:1px solid var(--line);padding:5px 7px;text-align:left}
table.grid th{background:#ececec}
.cred{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:10px 12px;margin:12px 0}
.cred.sys{border-left:4px solid var(--accent)}
.credhead{margin-bottom:6px}
.tag{display:inline-block;padding:1px 7px;border-radius:10px;font-size:.78em;margin-left:6px;font-weight:600}
.tag.user{background:#e3ecf7;color:#1f3a5f}
.tag.key{background:#eef2e4;color:#3d5210}
.who{color:var(--muted);font-size:.85em;margin-left:8px}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.9em}
pre.key{background:#0f1115;color:#c9d1d9;padding:10px;border-radius:4px;overflow-x:auto;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.78em;white-space:pre;line-height:1.35}
details{margin:6px 0}
details summary{cursor:pointer;color:var(--accent);font-size:.9em}
.cv{background:#f6f6f6;border:1px dashed var(--line);padding:10px;font-size:.9em}
ul,ol{margin:6px 0 6px 22px;padding:0}
li{margin:3px 0}
.footer{margin-top:40px;border-top:2px solid var(--line);padding-top:12px;color:var(--muted);font-size:.85em}
.alert{background:#fff8e1;border-left:4px solid #b8860b;padding:10px 12px;border-radius:4px;margin:10px 0;font-size:.9em}
```

Three rules differ from the sheet as first delivered, and each exists so the layout is checkable
rather than merely conventional. `.cred.sys` replaces an inline
`style="border-left:4px solid var(--accent)"` that one system block carried and another did not,
which makes "no element carries a `style=` attribute" a property the self-check can assert.
`.mono` was used in the delivered report with no rule behind it, so the span rendered unstyled;
here it has both a rule and a use, the key fingerprint. `ul,ol` replaces a `ul` rule the layout
never reaches — the only list the spine requires is the Gaps `<ol>`, which was falling back to
user-agent margins while every other block used the authored ones.

## Placeholder vocabulary

Every slot in the anatomies below is one of these tokens, and the list is closed. The self-check
carries the same list, so a slot left unsubstituted in a real report is named rather than shipped.
None is braced: a `{BRACED}` token is what a template engine leaves behind, and the check looks for
both.

```text
SYSTEM_OR_ENDPOINT   ACCESS_CLASS_BADGE   ARTEFACT_NAME        ACCOUNT_NAME
HOLDER_ROLE          KEY_FILENAME         KEY_TYPE_LABEL       KEY_FINGERPRINT
WHAT_THIS_DISCLOSES  WHAT_WAS_FOUND_WHERE CREDENTIAL_VALUE     OWNERSHIP_VALUE
ALEPH_BASE           FULL_ENTITY_ID_EXACTLY_AS_ALEPH_RETURNS_IT              FULL_ENTITY_ID_TRUNC
```

## Block anatomies

Four `div.cred` variants, and no others. Every other element in the spine — `div.sub`,
`div.banner`, `div.cv`, `table.grid`, `p.meta`, `ol`, `div.alert`, `div.footer` — is filled by the
rules in the next section rather than by an anatomy.

**System dossier** — exactly one per system section, the first child after its `h2`:

```html
<div class="cred sys">
 <div class="credhead"><strong>SYSTEM_OR_ENDPOINT</strong> <span class="tag key">ACCESS_CLASS_BADGE</span></div>
 <table class="kv">
  <tr><td>System</td><td>What it is, in the target's own words where they exist, and who operates it.</td></tr>
  <tr><td>Address</td><td>Host, ports, mirrors, issuer CN.</td></tr>
  <tr><td>Internet reachability</td><td>Whether it is reachable from outside, and on what evidence.</td></tr>
  <tr><td>Credential</td><td>What kind of credential opens it, and how many were recovered.</td></tr>
  <tr><td>Class</td><td>The access class this grants.</td></tr>
  <tr><td>Holder</td><td>Whose access this is, by role.</td></tr>
  <tr><td>Established</td><td>Dates, and the evidence that fixes them.</td></tr>
  <tr><td>Collection</td><td>Collection id and name.</td></tr>
  <tr><td>Take value</td><td>What this is worth to the operation.</td></tr>
  <tr><td>Confidence</td><td>high / moderate / low, per calibrated-confidence.</td></tr>
 </table>
</div>
```

A dossier omits a row it has nothing for rather than writing "unknown" — except `Confidence`, which
is always present. `Address` becomes `Reached` and `Credential` becomes `What the keys unlock` where
those read more naturally for the system; no other label is renamed. `ACCESS_CLASS_BADGE` takes one
of the access classes the dossier's own `Class` row uses, and the badge is omitted where no class
stands out.

**Credential block, login variant.** `<strong>` is the **artefact**, the tag is the **account**, and
`.who` is the **holder role** — three different things that are easy to collapse into one and must
not be. The holder is named by role, never by individual, matching the dossier's `Holder` row:

```html
<div class="cred">
 <div class="credhead"><strong>ARTEFACT_NAME</strong> <span class="tag user">ACCOUNT_NAME</span> <span class="who">HOLDER_ROLE</span></div>
 <table class="kv">
  <tr><td>Endpoint</td><td>host:port, and any mirror.</td></tr>
  <tr><td>Ownership</td><td>OWNERSHIP_VALUE — target / operation / third-party corporate / third-party personal / unknown.</td></tr>
  <tr><td>Freshness</td><td>Date, and the artefact that dates it.</td></tr>
  <tr><td>Class</td><td>What this credential is, materially.</td></tr>
  <tr><td>Collection</td><td>Collection id.</td></tr>
  <tr><td>Evidence</td><td><a href="ALEPH_BASE/entities/FULL_ENTITY_ID_EXACTLY_AS_ALEPH_RETURNS_IT">FULL_ENTITY_ID_TRUNC…</a></td></tr>
 </table>
 <details><summary>WHAT_THIS_DISCLOSES (exact)</summary><pre class="key">CREDENTIAL_VALUE</pre></details>
</div>
```

**Credential block, key variant.** The tag carries a **derived key-type label** — `RSA private key,
2048-bit`, `JWT, HS256` — so the reader sees what it is without opening anything. The only literal
copied from the artefact that may go there is a PEM `-----BEGIN … PRIVATE KEY-----` armour line,
which is public framing rather than key material. Never the leading bytes of a token-shaped
credential: a JWT's `eyJ…` segment and a vendor key's prefix are part of the secret, and rule 1
forbids them outside the collapse.

```html
<div class="cred">
 <div class="credhead"><strong>KEY_FILENAME</strong> <span class="tag key">KEY_TYPE_LABEL</span></div>
 <table class="kv">
  <tr><td>Size / fingerprint</td><td>Bit length and algorithm, then the content fingerprint as <span class="mono">KEY_FINGERPRINT</span>.</td></tr>
  <tr><td>Ownership</td><td>OWNERSHIP_VALUE — target / operation / third-party corporate / third-party personal / unknown.</td></tr>
  <tr><td>Collection</td><td>Collection id.</td></tr>
  <tr><td>Evidence</td><td><a href="ALEPH_BASE/entities/FULL_ENTITY_ID_EXACTLY_AS_ALEPH_RETURNS_IT">FULL_ENTITY_ID_TRUNC…</a></td></tr>
 </table>
 <details><summary>Private key material (exact)</summary><pre class="key">CREDENTIAL_VALUE</pre></details>
</div>
```

**Excluded / borderline block** — a bare tag, and only two rows:

```html
<div class="cred">
 <div class="credhead"><strong>WHAT_WAS_FOUND_WHERE</strong> <span class="tag">excluded</span></div>
 <table class="kv">
  <tr><td>What</td><td>What it is.</td></tr>
  <tr><td>Verdict</td><td>Why it is not a finding, or why it is only borderline.</td></tr>
 </table>
</div>
```

The bare tag takes `excluded` or `borderline` and nothing else.

## What fills the fixed blocks

**Dateline (`div.sub`).** One line, `·`-separated:
`Organised by the system each credential opens · collections <id (name)> [& <id (name)>] ·
<instance> <url> · generated <YYYY-MM-DD> · report mode = <mode>`.

**Report mode.** Two values, and the choice is made by who receives the product.

- `exact` — the reader is the credential owner's own responder. Values ownership permits are carried
  verbatim inside their `<details>`, and the standing record names the working files.
- `classified` — the reader is anyone else. No `<details>` anywhere in the document, whatever
  ownership would allow, and the standing record states that a credential file exists and where to
  request it without naming its path.

In both modes a working file is named relative to the working directory the brief set, never by
absolute path, so no analyst home directory or workstation name reaches the page. That is the
guardrails' redaction rule applied to the product rather than to the source field.

**Bottom line (`div.banner`).** One paragraph opening `<strong>Bottom line.</strong>`. Every count
and every named system inside it is wrapped in `<strong>`. It states the headline total —
`N distinct credentials opening M named systems` — then one clause per system with its count, then
the count **held back for want of a system**, then an overall confidence word, and closes with
`<strong>Single most consequential:</strong>` naming one access. No credential value appears here,
at any length.

**Coverage.** One `table.grid` with the fixed header row `Probe | Result | Form selected`, one row
per corpus-behaviour probe run before the sweep — what was tried, what came back, and which query
form was chosen as a result. For a non-English corpus the probes are at minimum: stemming,
diacritic and ё-folding, which language strata are present, transliteration, and encoding damage.
Then exactly three `<p class="meta">`:

1. The scoping receipt — what every query was scoped to, that the scope was confirmed on every
   reply, and the readable denominator the coverage figures are against.
2. The sets that exceeded the instance's pagination ceiling, named as `UNENUMERATED, faceted only`
   with their facet totals. A total that was never enumerated must not read as one that was.
3. The legs that ran, and the note file each one wrote, by working-directory-relative name.

**Gaps.** An `<ol>`. Each `<li>` opens with the gap itself in `<b>`, then says what would close it.
A gap is a question someone could answer, not a regret — see `naming-the-gaps` for what makes one
answerable.

**Hand-off.** One `<p>` carrying the ask, with the decision or action required in `<b>`, then a
`<div class="alert">` opening `<b>Standing record:</b>` for what persists after this product is
handed over — that a credential file exists, where it sits (relative to the working directory, and
only in `exact` mode), and when it is destroyed, per the skill's guardrails.

**Footer.** Generation date and author, the author being a role, cell or team designator rather than
an individual; that every credential sits inside a system block naming what it opens; that every
confirmed credential carries a resolving evidence link; that the coverage figures name their
denominator; and the closing assertion that **nothing was authenticated against, cracked, or
used**.

## Rules that are not cosmetic

Each of these changes what the reader believes, so none may be dropped for brevity.

- A credential value appears **only** inside a collapsed `<details>` → `<pre class="key">`. Never in
  a heading, a dateline, the banner, a `kv` cell, a summary, or a tag. The collapse is what lets the
  product carry a value at all: the recipient owns it and can open it, and is not made to read it to
  reach the analysis, which is the "look deliberately" rule of `SKILL.md`'s guardrails rendered on
  the page.
- **A `<details>` is written only where ownership permits the value into the product** — target-owned
  or corporate third-party, and only in `exact` mode. An operation-owned, unadjudicated or personal
  third-party finding is an ordinary credential block with no `<details>` element at all, not an
  empty or elided one. Every credential block carries an `Ownership` row so the omission reads as a
  decision rather than as an oversight.
- A `<summary>` ends in `(exact)` when what it hides is a verbatim secret. A certificate or other
  public artefact carries no `(exact)`.
- An evidence link carries the **whole** identifier in `href`; only the link *text* is shortened,
  with a trailing `…`. Never the reverse — the display may shorten, the record may not.
- No placeholder token survives into the product, braced or from the vocabulary above. The
  2026-09-11 sweep shipped one `{ALEPH}` href: a well-formed link to nothing, which counting links
  does not detect.
- Every class used is defined in the stylesheet, and no element carries a `style=` attribute.
- A count without a denominator is not a coverage figure. A set too large to enumerate is labelled
  unenumerated rather than reported as a total.
- The product is written to disk. It is never returned in a reply, and never read back into the
  session — the self-check below reports a verdict, not content.

Everything above governs presentation. What may be disclosed at all is decided by `## Guardrails` in
`SKILL.md`, gated on ownership, and this layout never widens it. For the discipline of rendering and
citing, see `briefing-reporting`; for the coverage denominator, see `exhaustive-data-processing`;
for what belongs in a gap, see `naming-the-gaps`.

## Self-check before hand-over

Run this against the draft. It reports a verdict — class names, integer counts and truncated section
titles — and never a `pre` body, a `summary` body, an attribute value or an evidence identifier.

```sh
REPORT=${REPORT:-/path/to/the/draft.html}
python3 - "$REPORT" <<'PY'
import re, sys, pathlib
PLACEHOLDERS = ('SYSTEM_OR_ENDPOINT','ACCESS_CLASS_BADGE','ARTEFACT_NAME','ACCOUNT_NAME',
                'HOLDER_ROLE','KEY_FILENAME','KEY_TYPE_LABEL','KEY_FINGERPRINT',
                'WHAT_THIS_DISCLOSES','WHAT_WAS_FOUND_WHERE','CREDENTIAL_VALUE','OWNERSHIP_VALUE',
                'ALEPH_BASE','FULL_ENTITY_ID_EXACTLY_AS_ALEPH_RETURNS_IT','FULL_ENTITY_ID_TRUNC')
KEY = r'<pre\b[^>]*class=["\'][^"\']*\bkey\b[^"\']*["\']'
t = pathlib.Path(sys.argv[1]).read_text()
# blank every <pre> body first: a captured artefact quoted inside one must not
# reach this script's own output through the class or placeholder scans
safe = re.sub(r'(<pre\b[^>]*>).*?</pre>', r'\1</pre>', t, flags=re.S)
css = re.search(r'<style>(.*?)</style>', t, re.S)
defined = set(re.findall(r'\.([A-Za-z][\w-]*)', css.group(1))) if css else set()
used = {c for v in re.findall(r'class=["\']([^"\']+)["\']', safe) for c in v.split()}
keys   = re.findall(KEY, t)
inside = re.findall(r'<details\b[^>]*>(?:(?!</details>).)*?' + KEY, t, re.S)
anchors = re.findall(r'<a\b[^>]*>', t)
hrefs   = re.findall(r'<a\b[^>]*href=["\']([^"\']*)["\']', t)
left = sorted({p for p in PLACEHOLDERS if re.search(r'\b%s\b' % p, safe)} |
              set(re.findall(r'\{[A-Z_]{2,}\}', safe)))
print('undefined classes    :', sorted(used - defined) or 'none')
print('inline style attrs   :', len(re.findall(r'\sstyle=["\']', t)))
print('placeholder tokens   :', left or 'none')
print('pre.key not collapsed:', len(keys) - len(inside))
print('details shipped open :', len(re.findall(r'<details\b[^>]*\bopen\b', t)))
print('anchors/href-less/short:', len(anchors), len(anchors) - len(hrefs),
      sum(1 for h in hrefs if len(h.rsplit("/", 1)[-1]) < 40))
print('sections             :', [re.sub(r'<[^>]+>', '', s)[:40]
                                 for s in re.findall(r'<h2[^>]*>(.*?)</h2>', t, re.S)])
PY
```

Every count must be `0` and both lists `none`, and the section list must end with Coverage, Gaps and
Hand-off. `pre.key not collapsed` above zero means a value is rendered open on the page;
`details shipped open` above zero means one was shipped expanded. The short-link constant is 40
because an Aleph entity identifier is at least that long, so a shorter final path segment is a
display form that was pasted into the `href` — change the constant if the issuing system's
identifiers are shorter.

A clean verdict is a lint result, not a proof. It cannot tell a correct system attribution from a
wrong one, nor a real evidence identifier from a well-formed invention, so a sample of the evidence
references must still be resolved against the issuing system before hand-over, per
`briefing-reporting`.
