# Credential Sweep Report Layout

This is the fixed shape of the HTML product that step 8 of `credential-harvest-triage` emits. It
decides presentation only, and adds nothing to what the skill's `## Guardrails` permit to be
disclosed.

## The organising principle

The report is organised by **the system each credential opens** — never by artefact, by file, or by
the collection the material came from. A reader must come away seeing an access, not a list of
strings: an account and a key that open the same endpoint belong in the same section even when they
were recovered from different archives, and two keys from the same archive that open different
systems belong apart. A credential whose system could not be identified goes in the residual section
rather than being filed under a guess, because a wrong system attribution is read as an access that
does not exist.

## Document order

The spine is fixed. Everything sits inside a single `<div class="wrap">` under `<body>`; the
document is `<html lang="…">` naming the corpus language, carries `<meta charset="utf-8">`, and has
one `<title>` of the form `<Product> — <Target> · <YYYY-MM-DD>`.

1. `<div class="sub">` — the dateline: organising principle · collections (id + name) · instance URL
   · generated date · report mode.
2. `<div class="banner">` — the bottom line, up front.
3. System sections, numbered `1..N` and ordered by consequence rather than by discovery:
   `<h2>N. <access class> — <system, endpoint></h2>`. Each opens with one `div.cred.sys` dossier
   block, then optionally one count-bearing `<h3>`, then the repeated `div.cred` credential blocks.
4. `<h2>N+1. Secrets with no system identified (residual)</h2>` — credential blocks, or a
   `<div class="cv">` stating the negative when there are none.
5. `<h2>N+2. Excluded and borderline</h2>` — `div.cred` blocks carrying a bare `<span class="tag">`.
6. `<h2>N+3. Coverage</h2>` — one `table.grid`, then three `p.meta`.
7. `<h2>N+4. Gaps</h2>` — one `<ol>`.
8. `<h2>N+5. Hand-off</h2>` — one `<p>`, then one `div.alert`.
9. `<div class="footer">`.

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
ul{margin:6px 0 6px 22px;padding:0}
li{margin:3px 0}
.footer{margin-top:40px;border-top:2px solid var(--line);padding-top:12px;color:var(--muted);font-size:.85em}
.alert{background:#fff8e1;border-left:4px solid #b8860b;padding:10px 12px;border-radius:4px;margin:10px 0;font-size:.9em}
```

Two rules here are additions to the sheet as first delivered, and both exist so the layout is
checkable rather than merely conventional. `.cred.sys` replaces an inline
`style="border-left:4px solid var(--accent)"` that one system block carried and another did not,
which makes "no element carries a `style=` attribute" a check the self-check below can run.
`.mono` was used once in the delivered report with no rule behind it, so the span rendered
unstyled — a class used without a definition is a silent presentation failure, and defining it is
cheaper than removing every use.

## Block anatomies

Four blocks, and no others.

**System dossier** — exactly one per system section, the first child after its `h2`:

```html
<div class="cred sys">
 <div class="credhead"><strong>SYSTEM_OR_ENDPOINT</strong> <span class="tag key">CROWN JEWEL</span></div>
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
is always present, because a dossier with no confidence reads as certain. `Address` becomes
`Reached` and `Credential` becomes `What the keys unlock` where those read more naturally for the
system; no other label is renamed.

**Credential block, login variant.** `<strong>` is the **artefact**, the tag is the **account**, and
`.who` is the **holder** — three different things that are easy to collapse into one and must not be:

```html
<div class="cred">
 <div class="credhead"><strong>ARTEFACT_NAME</strong> <span class="tag user">ACCOUNT</span> <span class="who">HOLDER — ROLE</span></div>
 <table class="kv">
  <tr><td>Endpoint</td><td>host:port, and any mirror.</td></tr>
  <tr><td>Freshness</td><td>Date, and the artefact that dates it.</td></tr>
  <tr><td>Class</td><td>What this credential is, materially.</td></tr>
  <tr><td>Collection</td><td>Collection id.</td></tr>
  <tr><td>Evidence</td><td><a href="ALEPH_BASE/entities/FULL_ENTITY_ID_EXACTLY_AS_ALEPH_RETURNS_IT">FULL_ENTITY_ID_TRUNC…</a></td></tr>
 </table>
 <details><summary>WHAT_THIS_DISCLOSES (exact)</summary><pre class="key">VALUE</pre></details>
</div>
```

**Credential block, key variant.** The tag carries the key's own header line, so the reader sees the
key type without opening anything:

```html
<div class="cred">
 <div class="credhead"><strong>FILENAME</strong> <span class="tag key">-----BEGIN RSA PRIVATE KEY-----</span></div>
 <table class="kv">
  <tr><td>Size / fingerprint</td><td>Bit length, algorithm, content fingerprint.</td></tr>
  <tr><td>Collection</td><td>Collection id.</td></tr>
  <tr><td>Evidence</td><td><a href="ALEPH_BASE/entities/FULL_ENTITY_ID_EXACTLY_AS_ALEPH_RETURNS_IT">FULL_ENTITY_ID_TRUNC…</a></td></tr>
 </table>
 <details><summary>Private key material (exact)</summary><pre class="key">VALUE</pre></details>
</div>
```

**Excluded / borderline block** — a bare tag, and only two rows:

```html
<div class="cred">
 <div class="credhead"><strong>WHAT_WAS_FOUND — WHERE</strong> <span class="tag">excluded</span></div>
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
<instance> <url> · generated <YYYY-MM-DD> · REPORT_MODE = <mode>`.

**Bottom line (`div.banner`).** One paragraph opening `<strong>Bottom line.</strong>`. Every count
and every named system inside it is wrapped in `<strong>`, because this paragraph is the only part
of the report some readers will finish. It states the headline total — `N distinct credentials
opening M named systems` — then one clause per system with its count, then the count **held back for
want of a system**, then an overall confidence word, and closes with
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
3. The legs that ran, and the note file each one wrote.

**Gaps.** An `<ol>`. Each `<li>` opens with the gap itself in `<b>`, then says what would close it.
A gap is a question someone could answer, not a regret.

**Hand-off.** One `<p>` carrying the ask, with the decision or action required in `<b>`, then a
`<div class="alert">` opening `<b>Standing record:</b>` for what persists after this product is
handed over — including where the credential file sits and when it is destroyed, per the skill's
guardrails.

**Footer.** Generation date and author; that every credential sits inside a system block naming what
it opens; that every confirmed credential carries a resolving evidence link; that the coverage
figures name their denominator; and the closing assertion that **nothing was authenticated against,
cracked, or used**.

## Rules that are not cosmetic

Each of these changes what the reader believes, so none may be dropped for brevity.

- A credential value appears **only** inside a collapsed `<details>` → `<pre class="key">`. Never in
  a heading, a dateline, the banner, a `kv` cell, a summary, or a tag. The collapse is the point:
  the recipient owns the value and can open it, and is not made to read it to reach the analysis.
- A `<summary>` ends in `(exact)` when what it hides is a verbatim secret. A certificate or other
  public artefact carries no `(exact)`.
- An evidence link carries the **whole** identifier in `href`; only the link *text* is shortened,
  with a trailing `…`. Never the reverse — the display may shorten, the record may not.
- No placeholder token survives into the product. The 2026-09-11 sweep shipped one `{ALEPH}` href: a
  well-formed link to nothing, which counting links does not detect.
- Every class used is defined in the stylesheet, and no element carries a `style=` attribute.
- A count without a denominator is not a coverage figure. A set too large to enumerate is labelled
  unenumerated rather than reported as a total.
- The product is written to disk. It is never returned in a reply, and never read back into the
  session — the self-check below reports a verdict, not content.

Everything above governs presentation. What may be disclosed at all is decided by `## Guardrails` in
`SKILL.md`, gated on ownership, and this layout never widens it. For the discipline of rendering and
citing, see `briefing-reporting`; for the coverage denominator, see `exhaustive-data-processing`.

## Self-check before hand-over

Run this against the draft. It prints a verdict and never prints report content.

```sh
python3 - "$REPORT" <<'PY'
import re, sys, pathlib
t = pathlib.Path(sys.argv[1]).read_text()
css = re.search(r'<style>(.*?)</style>', t, re.S)
defined = set(re.findall(r'\.([A-Za-z][\w-]*)', css.group(1))) if css else set()
used = {c for v in re.findall(r'class="([^"]+)"', t) for c in v.split()}
keys = re.findall(r'<pre class="key">', t)
inside = re.findall(r'<details>.*?<pre class="key">', t, re.S)
hrefs = re.findall(r'<a href="([^"]*)"', t)
print('undefined classes   :', sorted(used - defined) or 'none')
print('inline style attrs  :', len(re.findall(r'\sstyle="', t)))
print('placeholder tokens  :', sorted({x for x in re.findall(r'\{[A-Z_]{2,}\}', t)}) or 'none')
print('pre.key outside <details>:', len(keys) - len(inside))
print('links, of which short:', len(hrefs), sum(1 for h in hrefs if len(h.rsplit("/",1)[-1]) < 40))
print('sections            :', [re.sub(r'<[^>]+>','',s)[:40] for s in re.findall(r'<h2[^>]*>(.*?)</h2>', t, re.S)])
PY
```

The first four lines must read `none`, `0`, `none`, `0`; the short-link count must be `0`; and the
section list must end with Coverage, Gaps and Hand-off. A `pre.key` outside a `<details>` means a
value is rendered open on the page.
