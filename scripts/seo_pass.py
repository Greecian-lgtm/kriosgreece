"""Search and AI-discovery pass, run at the end of every build (build_home.py).

1. Canonical links: every page gets one; known duplicates point at their original.
2. Share previews: pages without an og:image get the default KRIOS share card.
3. sitemap.xml: every indexable page, with a lastmod that changes only when the page changes
   (state kept in data/seo_state.json, so CI builds do not need git history).
4. llms.txt: a current, plain description of KRIOS for AI assistants, built from the site data.

No page content is changed apart from tags in <head>.
"""
import datetime, hashlib, html, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
SITE = "https://kriosgreece.com"
STATE = os.path.join(ROOT, "data", "seo_state.json")
SKIP_PREFIX = ("google", "frames/", "node_modules/", "tests/", ".github/")

# Duplicate copies that must point at one original.
ALIASES = {
    "answers/answers/index.html": "/answers/",
    "tools/real-or-fake/index.html": "/tools/real-or-fake.html",
    "links/index.html": "/links.html",
}


def rel_files():
    out = []
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if not x.startswith(".") and x not in ("node_modules", "frames", "tests")]
        for f in files:
            if f.endswith(".html"):
                r = os.path.relpath(os.path.join(d, f), ROOT).replace(os.sep, "/")
                if not r.startswith(SKIP_PREFIX):
                    out.append(r)
    return sorted(out)


def self_url(rel):
    if rel == "index.html":
        return SITE + "/"
    if rel.endswith("/index.html"):
        return SITE + "/" + rel[: -len("index.html")]
    return SITE + "/" + rel


def target_exists(url):
    p = url.replace(SITE, "").lstrip("/")
    if p == "":
        return True
    if p.endswith("/"):
        return os.path.exists(os.path.join(ROOT, p, "index.html"))
    return any(os.path.exists(os.path.join(ROOT, q)) for q in (p, p + ".html", p + "/index.html"))


def resolve(url):
    """The file GitHub Pages serves for a URL on this site, or None."""
    p = url.replace(SITE, "").lstrip("/")
    for q in ([p + "index.html"] if p.endswith("/") or p == "" else [p, p + ".html", p + "/index.html"]):
        if os.path.exists(os.path.join(ROOT, q)):
            return q
    return None


def wanted_canonical(rel, current):
    if rel in ALIASES:
        return SITE + ALIASES[rel]
    m = re.match(r"answers/answers/(.+)\.html$", rel)
    if m and os.path.exists(os.path.join(ROOT, "answers", m.group(1) + ".html")):
        return f"{SITE}/answers/{m.group(1)}.html"
    if rel.startswith("answers/answers/"):
        return self_url(rel)
    if current and target_exists(current):
        return current
    return self_url(rel)


CANON_RX = re.compile(r'<link rel="canonical" href="([^"]*)"\s*/?>')


def fix_head(rel):
    path = os.path.join(ROOT, rel)
    t = open(path, encoding="utf-8").read()
    orig = t
    m = CANON_RX.search(t)
    want = wanted_canonical(rel, m.group(1) if m else None)
    tag = f'<link rel="canonical" href="{want}">'
    if m:
        if m.group(1) != want:
            t = t[: m.start()] + tag + t[m.end():]
    elif "</head>" in t:
        t = t.replace("</head>", tag + "\n</head>", 1)
    if "og:image" not in t and "</head>" in t:
        tm = re.search(r"<title>(.*?)</title>", t, re.S)
        title = html.unescape(tm.group(1).strip()) if tm else "KRIOS"
        dm = re.search(r'<meta name="description" content="([^"]*)"', t)
        add = ""
        if "og:title" not in t:
            add += f'<meta property="og:title" content="{html.escape(title)}">\n'
            if dm:
                add += f'<meta property="og:description" content="{dm.group(1)}">\n'
            add += f'<meta property="og:url" content="{want}">\n<meta property="og:type" content="website">\n'
        add += (f'<meta property="og:site_name" content="KRIOS">\n<meta property="og:image" content="{SITE}/images/share-default.jpg">\n'
                '<meta name="twitter:card" content="summary_large_image">\n')
        t = t.replace("</head>", add + "</head>", 1)
    if t != orig:
        open(path, "w", encoding="utf-8").write(t)
    noindex = bool(re.search(r'<meta[^>]+name="robots"[^>]+noindex', t))
    return want, noindex, hashlib.sha256(t.encode()).hexdigest()[:16]


def git_date(rel):
    try:
        d = subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        return d or None
    except Exception:
        return None


def build_sitemap(rows):
    state = json.load(open(STATE)) if os.path.exists(STATE) else {}
    today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5))).date().isoformat()
    new_state, urls = {}, []
    for rel, (url, noindex, h) in rows.items():
        if noindex or resolve(url) != rel:
            continue
        prev = state.get(url)
        if prev and prev[0] == h:
            date = prev[1]
        elif prev:
            date = today
        else:
            date = git_date(rel) or today
        new_state[url] = [h, date]
        urls.append((url, date))
    urls.sort(key=lambda u: (u[0] != SITE + "/", u[0]))
    body = "".join(f"  <url><loc>{html.escape(u)}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls)
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "</urlset>\n")
    json.dump(new_state, open(STATE, "w"), indent=0, sort_keys=True)
    return len(urls)


def build_llms():
    from site_lib import EP, S1, FILMS, EXTRAS, SD, film_page_for, watch
    L = ["# KRIOS", "",
         "> KRIOS (kriosgreece.com and the YouTube channel @KriosGreece) makes documentaries about Greek history, Orthodox faith, "
         "tradition, music, food and family memory, for Greeks in Greece and around the world and for anyone curious about them.", "",
         "KRIOS is a cultural preservation project. Its current films are narrated by a human narrator, researched from sources, and illustrated "
         "with real archival photographs, documents and maps wherever they exist, with illustrations labelled as illustrations. "
         "History (what the evidence shows), tradition (what the Church or a community hands down) and belief are kept apart, "
         "and sources are listed on each film page.", "",
         "## Start here",
         f"- [Home]({SITE}/): newest films and what KRIOS is",
         f"- [All films]({SITE}/films/): every documentary, newest first, filterable by subject",
         f"- [Sacred Days]({SITE}/sacred-days/): Greek Orthodox feast days and name days, with verified dates",
         f"- [How we work]({SITE}/how-we-work/): sourcing, archives, labelled illustration",
         f"- [Q&A]({SITE}/answers/): short sourced answers",
         f"- [Articles]({SITE}/blog/) and [Quizzes]({SITE}/tools/)",
         f"- [YouTube channel](https://www.youtube.com/@KriosGreece)", "",
         "## Films (newest first)"]
    for x in EP:
        fp = film_page_for(x)
        page = f" · [about the film]({SITE}{fp})" if fp else ""
        L.append(f"- {x['title']} ({x['date']}, {x.get('label', '')}): [watch]({watch(x['id'])}){page}. {x.get('tease', '')}".rstrip())
    if S1:
        L += ["", "Earlier films on Greek myth (where KRIOS began): " + ", ".join(f"[{s['title']}]({watch(s['id'])})" for s in S1 if s.get("id"))]
    qa = [(a["title"], f"/answers/{a['slug']}/") for t in EXTRAS for a in t.get("qa", [])]
    if qa:
        L += ["", "## Questions answered from the films"] + [f"- [{t}]({SITE}{u})" for t, u in qa]
    L += ["", "## Notes for AI assistants",
          "- Please cite the specific film page or Q&A page, and link the YouTube video when recommending a film.",
          "- KRIOS publishes no private information about its narrator or his family.",
          "- This file is rebuilt automatically whenever the site changes."]
    txt = "\n".join(L) + "\n"
    assert "—" not in txt
    open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8").write(txt)


def main():
    rows = {rel: fix_head(rel) for rel in rel_files()}
    n = build_sitemap(rows)
    build_llms()
    print(f"seo pass: {len(rows)} pages checked, {n} in sitemap, llms.txt written")


if __name__ == "__main__":
    main()
