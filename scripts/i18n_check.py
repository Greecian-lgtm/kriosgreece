"""Check the site-wide translation tables in data/i18n/ before a release.
Fails on: invalid JSON, a draft page with a missing Greek or Spanish entry, html entries whose links differ from the
English or a different number of text pieces, a site.json page list that differs from the files, em dashes, or text in the private-terms list (KRIOS_PRIVATE_TERMS, comma separated). Run: python3 scripts/i18n_check.py"""
import glob, json, os, re, sys
fails = []; warn = []
priv = [t.strip() for t in os.environ.get("KRIOS_PRIVATE_TERMS", "").split(",") if t.strip()]
def segs(h): return len([t for t in re.split(r'<[^>]+>', h) if t.strip()])
files = ["data/i18n/site.json"] + sorted(glob.glob("data/i18n/pages/*.json"))
for f in files:
    try: d = json.load(open(f, encoding="utf-8"))
    except Exception as e: fails.append(f"{f}: invalid JSON ({e})"); continue
    status = d.get("_status", "draft")
    for i, s in enumerate(d.get("strings", []) + d.get("attrs", [])):
        for l in ("el", "es"):
            v = s.get(l)
            if status != "source" and not v: fails.append(f"{f}: entry {i} missing {l}: {s.get('en','')[:50]}")
            if v and "—" in v: fails.append(f"{f}: em dash in {l}: {v[:50]}")
            for t in priv:
                if v and t.lower() in v.lower(): fails.append(f"{f}: private term in {l}")
            if s.get("html") and status != "source":
                h = s.get(f"{l}_html")
                if not h: fails.append(f"{f}: entry {i} missing {l}_html")
                elif sorted(re.findall(r'href="[^"]*"', h)) != sorted(re.findall(r'href="[^"]*"', s["html"])):
                    fails.append(f"{f}: links differ in {l}_html: {s['en'][:50]}")
                elif segs(h) != segs(s["html"]):
                    fails.append(f"{f}: entry {i} {l}_html has {segs(h)} text pieces, English has {segs(s['html'])} (page would stay English)")
    if status == "source": warn.append(f"{f}: not translated yet (shows English with a notice)")
try:
    listed = set(json.load(open("data/i18n/site.json", encoding="utf-8")).get("pages", []))
    have = {os.path.basename(f)[:-5] for f in files[1:]}
    if listed != have: fails.append(f"site.json pages list differs from data/i18n/pages: missing {sorted(have-listed)}, extra {sorted(listed-have)}")
except Exception: pass
for w in warn: print("note:", w)
for x in fails: print("FAIL", x)
print(f"i18n check: {len(files)} files, {len(fails)} failures")
sys.exit(1 if fails else 0)
