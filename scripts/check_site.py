"""KRIOS publishing safeguards for kriosgreece.com (Gate C plan, section 4).

Run from the repo root:  python3 scripts/check_site.py
Exit 1 if any BLOCKING check fails; WARNINGS are printed but do not fail the run.
Until after the Oct 26, 2026 release this runs only in .github/workflows/site-checks.yml
(pushes and pull requests). It is not part of the YouTube sync yet.
"""
import glob, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)
from site_lib import DEDICATION_LINES  # noqa: E402

errors, warnings = [], []
err = lambda m: errors.append(m)
warn = lambda m: warnings.append(m)

GENERATED = ["index.html", "films/index.html", "sacred-days/index.html", "how-we-work/index.html",
             "blog/index.html", "answers/index.html", "tools/index.html"]
PUBLIC = sorted(set(GENERATED + glob.glob("blog/**/*.html", recursive=True) + glob.glob("answers/**/*.html", recursive=True)
                    + glob.glob("tools/**/*.html", recursive=True) + ["links.html", "links/index.html"]))
PUBLIC = [p for p in PUBLIC if os.path.exists(p)]


def visible_text(s):
    s = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(re.sub(r"\s+", " ", s))


# Explicit episode/season labels only. Plain numbers and years (1821, 1922, "300 Spartans", dates) never match.
EP_RX = re.compile(r"\b(?:EP|Ep)\s?0*\d{1,3}\b|\bEpisode\s+\d{1,3}\b|\bSeason\s+\d{1,2}\b|(?<![\w&])#\d{1,3}\b(?=\s*(?:episode|film|documentary)\b)", re.I)


def number_hits(text):
    return [m.group(0) for m in EP_RX.finditer(text)]


def selftest():
    ok = ["In 1821 Diakos stood at Thermopylae.", "The 300 Spartans everyone forgets.", "October 26, 2026 on YouTube",
          "An economic crisis followed the fall in currant prices in 1893.", "After the 1922 Asia Minor Catastrophe",
          "Zorba the Greek (1964)", "5 questions", "from about 430,000 to more than 600,000", "Psalm 23", "Theophany · January 6, 2027"]
    bad = ["EP021 The Greeks Who Left", "Episode 3", "Season 2 · Heroes", "season 3", "Ep 14"]
    for t in ok:
        if number_hits(t):
            err(f"validator self-test: false positive on {t!r}")
    for t in bad:
        if not number_hits(t):
            err(f"validator self-test: missed {t!r}")


selftest()

# 1. Dedication: exact homepage block and footer line on every v2 page
home = open("index.html", encoding="utf-8").read()
for line in DEDICATION_LINES:
    if line not in home:
        err(f"dedication line missing or changed on the homepage: {line!r}")
if '<p class="dgr" lang="el">Αἰωνία σου ἡ μνήμη.</p>' not in home:
    err("Greek dedication line changed (exact text and lang attribute required)")
for p in GENERATED + glob.glob("blog/**/*.html", recursive=True) + glob.glob("answers/**/*.html", recursive=True):
    if os.path.exists(p):
        s = open(p, encoding="utf-8").read()
        if 'http-equiv="refresh"' not in s and "For my father, Peter (Πέτρος)." not in s:
            err(f"footer dedication missing: {p}")

# 2/3/4. Episode numbers, season numbers, em dashes (generated pages: blocking; older pages: warning)
for p in PUBLIC:
    s = open(p, encoding="utf-8").read()
    t = visible_text(s)
    hits = number_hits(t)
    if hits:
        (err if p in GENERATED else warn)(f"episode/season number in {p}: {sorted(set(hits))[:5]}")
    if p in GENERATED and "—" in t:
        err(f"em dash in generated public copy: {p}")

# 5/6. Held content and release gates
up = json.load(open("data/upcoming.json", encoding="utf-8"))["upcoming"]
for u in up:
    for f in u.get("release_files", []):
        if os.path.exists(f):
            err(f"held file is on the site before release: {f} ({u['title']})")
    cred = u.get("credits")
    if cred:
        for p in PUBLIC:
            if f'href="{cred}"' in open(p, encoding="utf-8").read():
                err(f"page links to held credits before release: {p} -> {cred}")
for d in glob.glob("films/*/"):
    slug = d.rstrip("/").split("/")[-1]
    data = f"data/films/{slug}.json"
    if not os.path.exists(data) or not json.load(open(data, encoding="utf-8")).get("approved"):
        err(f"film page exists without director-approved content: {d}")
    else:
        fd = json.load(open(data, encoding="utf-8"))
        if fd.get("opening") and not (fd["opening"] or {}).get("from"):
            err(f"film page opening lacks its narration-master reference: {data}")

# 7. Calendar
sd = json.load(open("data/sacred_days.json", encoding="utf-8"))
for f in sd["feasts"]:
    v = f.get("verified") or {}
    if not v.get("source", "").startswith("http"):
        err(f"Sacred Days entry without a verification source: {f.get('en')}")
cal = open("sacred-days/index.html", encoding="utf-8").read() if os.path.exists("sacred-days/index.html") else ""
for li in re.findall(r"<li class=\"reveal\"><div class=\"m-feast\">.*?</li>", cal, re.S):
    t = visible_text(li)
    if "No KRIOS film scheduled" not in t and "premieres" not in t.lower() and "Watch the KRIOS film" not in t:
        err(f"calendar row has no clear film status: {t[:80]}")

# 8. Privacy blocklist (kept out of the code; supplied as a secret)
terms = [t.strip() for t in os.environ.get("KRIOS_PRIVATE_TERMS", "").split(",") if t.strip()]
if terms:
    for p in PUBLIC:
        low = visible_text(open(p, encoding="utf-8").read()).lower()
        for t in terms:
            if t.lower() in low:
                err(f"private term found in {p}")
else:
    warn("privacy blocklist not configured (KRIOS_PRIVATE_TERMS secret)")

# 9. Internal links on generated pages resolve
for p in GENERATED:
    s = open(p, encoding="utf-8").read()
    for href in re.findall(r'href="(/[^"#?]*)', s):
        target = href.lstrip("/")
        cands = [target, os.path.join(target, "index.html")] if target else ["index.html"]
        if not any(os.path.isfile(c) for c in cands):
            err(f"broken internal link in {p}: {href}")

# 10. Data integrity
eps = json.load(open("data/episodes.json", encoding="utf-8"))
ids = [x["id"] for x in eps["episodes"]] + [x["id"] for x in eps["season1"]]
if len(ids) != len(set(ids)):
    err("duplicate video ids in data/episodes.json")
for x in eps["episodes"]:
    for k in ("id", "date", "title", "label"):
        if not x.get(k):
            err(f"episode missing {k}: {x.get('id')}")
subj = json.load(open("data/subjects.json", encoding="utf-8"))
for x in eps["episodes"]:
    if x.get("label") not in subj["from_label"] and not any(o.get("id") == x["id"] for o in subj["overrides"]):
        warn(f"label not mapped to a subject (still listed under All films): {x['label']} · {x['title'][:50]}")

for w in warnings:
    print("WARNING:", w)
for m in errors:
    print("::error title=site check::" + m if os.environ.get("GITHUB_ACTIONS") else "ERROR: " + m)
print(f"site check: {len(errors)} blocking, {len(warnings)} warnings, {len(PUBLIC)} pages")
sys.exit(1 if errors else 0)
