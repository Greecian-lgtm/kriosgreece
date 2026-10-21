# Builds the PROPOSED Universe homepage prototype at /prototype/universe/ (design branch only).
# Not linked from the live site, noindex, kept out of the sitemap. Reads the same approved data as the live site;
# nothing here is typed by hand that the film data already says. Run: python3 build_universe.py
import json, os
from site_lib import (ROOT, EP, UP, SUBJ, FILMS, DEDICATION_HTML, e, nice, short, released, film_page_for, featured_film,
                      subjects_of, calendar_entries, film_for_feast, _matches)
from site_parts import head, footer, SCRIPTS, SUB, YT, menu_button

OUT = "prototype/universe/index.html"
load = lambda p: json.load(open(os.path.join(ROOT, p), encoding="utf-8"))
G, W, FT = load("data/universe/gateways.json"), load("data/universe/why.json"), load("data/universe/featured.json")

TAG = " · proposed"
PROTO = True   # prototype-only labels and banner; set False when the page is promoted

NAVP = [("/films/", "Films"), ("/sacred-days/", "Sacred Days"), ("#gateways", "Explore"), ("#memory-room", "Memory Room"), ("/answers/", "Q&amp;A")]


def film_by_slug(slug):
    return next(f for f in FILMS if f["slug"] == slug)


def published(f):
    """The published episode for an approved film, or None. Prototype content only uses published films."""
    return released(f["match"])


# ---------- header (proposed navigation) ----------
def header():
    links = "".join(f'<a href="{h}">{t}</a>' for h, t in NAVP)
    return ('<a class="skip" href="#main">Skip to content</a>\n<header class="top">\n  <div class="wrap">\n'
            '    <a class="brand" href="/"><b>KRIOS</b><span>Greek cultural preservation</span></a>\n'
            f'    <nav class="nav" aria-label="Main">{menu_button()}<div class="nav-links" id="site-menu">{links}</div>'
            f'<a class="btn btn-gold" href="{SUB}" rel="noopener">Subscribe<span class="m-hide-sm">&nbsp;on YouTube</span></a></nav>\n'
            '  </div>\n</header>')


# ---------- hero ----------
def hero():
    f = film_by_slug("the-greeks-who-left")
    img = f["hero_image"]
    return f'''<section class="u-hero" aria-labelledby="u-h1">
  <div class="u-hero-grid">
    <div class="u-hero-copy">
      <p class="u-label u-kick">KRIOS · The living story of Greek civilization</p>
      <h1 id="u-h1"><span>The stories we inherited.</span><span class="u-q2">The questions we never asked.</span></h1>
      <p class="u-sub">Documentaries on Greek history, faith, tradition and family memory, for Greeks in Greece and around the world. Real archives, sourced claims, and the stories families carried with them.</p>
      <div class="u-cta">
        <a class="u-btn u-btn-gold" href="#featured">Watch the newest film</a>
        <a class="u-btn u-btn-line" href="#gateways">Choose where to begin</a>
      </div>
    </div>
    <figure class="u-hero-art">
      <img src="{e(img['src'])}" alt="{e(img['alt'])}" width="1280" height="720" fetchpriority="high">
      <span class="u-chip">AI-generated illustration</span>
      <figcaption class="u-cap">Illustration from the film The Greeks Who Left. It is not a historical photograph.</figcaption>
    </figure>
  </div>
</section>
<div class="u-strip"><ul aria-label="What KRIOS does"><li>Preserve</li><li>Teach</li><li>Understand</li><li>Connect</li><li>Pass forward</li></ul></div>'''


# ---------- six gateways ----------
def film_count(subjects):
    keys = set(subjects)
    return sum(1 for x in EP if keys & set(subjects_of(x)))


def gateways():
    tiles = []
    for g in G["gateways"]:
        n = film_count(g["subjects"])
        if g["key"] == "faith-sacred-days":
            status = f'{n} film{"s" if n != 1 else ""} · calendar'
        elif n:
            status = f'{n} film{"s" if n != 1 else ""}'
        else:
            status = "No film yet"
        cls = "u-gate" + ("" if n else " u-gate--empty")
        tiles.append(f'''<li class="{cls}">
      <div class="u-gate-top"><span class="u-gate-num">{e(g["num"])}</span><span class="u-gate-el" lang="el">{e(g["el"])}</span></div>
      <h3><a href="{e(g["href"])}">{e(g["en"])}</a></h3>
      <p>{e(g["line"])}</p>
      <div class="u-gate-foot"><span>{e(status)}</span><span class="u-go" aria-hidden="true">→</span></div>
    </li>''')
    return f'''<section class="u-sec u-gates" id="gateways" aria-labelledby="u-gates-h">
  <div class="u-wrap">
    <p class="u-label u-kick" style="color:var(--u-gold-ink)">Six ways in</p>
    <h2 id="u-gates-h">Where would you like to begin?</h2>
    <p class="u-lede">Every film belongs to more than one door. Pick the one that feels closest to your own family.</p>
    <ul class="u-gate-grid">
      {"".join(tiles)}
    </ul>
  </div>
</section>'''


# ---------- featured documentary ----------
def featured():
    x = next((x for x in EP if x["id"] and FT.get("slug") and film_page_for(x) == f'/films/{FT["slug"]}/'), None) or featured_film()
    page = film_page_for(x)
    f = next(f for f in FILMS if _matches(f["match"], x))
    src = f["sources"]
    n_est, n_open, n_int = len(src.get("established", [])), len(src.get("open", [])), len(src.get("interpretation", []))
    parts = [f'{n_est} established claim{"s" if n_est != 1 else ""}']
    if n_int:
        parts.append(f'{n_int} marked as interpretation')
    if n_open:
        parts.append(f'{n_open} still open')
    shorts = FT.get("shorts") or []
    if shorts:
        sh = "<ul>" + "".join(f'<li><a href="https://www.youtube.com/watch?v={e(s["id"])}" rel="noopener">{e(s["title"])}</a></li>' for s in shorts) + "</ul>"
    else:
        sh = '<p class="u-soft">No Shorts are public for this film yet. They will appear here once they are.</p>'
    ups = [f'<li><b>{e(u["title"])}</b><br><span class="u-soft">{e(u["label"])} · premieres {nice(u["date"])}</span></li>' for u in UP]
    feasts = []
    for fe in calendar_entries()[:3]:
        st, _ = film_for_feast(fe)
        if st == "scheduled":
            continue
        feasts.append(f'<li>{e(fe["en"])} <span class="u-soft">· {nice(fe["date"])} · No KRIOS film scheduled</span></li>')
    chapters = "<ul>" + "".join(ups + feasts) + "</ul>"
    return f'''<section class="u-sec u-feat u-dark" id="featured" aria-labelledby="u-feat-h">
  <div class="u-wrap">
    <p class="u-label u-kick">Featured documentary</p>
    <h2 id="u-feat-h">One film, and everything around it</h2>
    <p class="u-lede">Each documentary connects to its sources, its Shorts and the chapters that follow, so the story can keep going after the credits.</p>
    <div class="u-feat-grid">
      <article class="u-film">
        <span class="u-film-meta">{e(x["label"])} · {x["mins"]} min · {nice(x["date"])}</span>
        <h3>{e(x["title"])}</h3>
        <p>{e(x.get("tease", ""))}</p>
        <div class="u-cta">
          <a class="u-btn u-btn-gold" href="{e(page)}">Open the film page</a>
          <a class="u-btn u-btn-line" href="https://www.youtube.com/watch?v={e(x["id"])}" rel="noopener">Watch on YouTube</a>
        </div>
      </article>
      <ul class="u-rail" aria-label="Connected to this film">
        <li><h3>Source material</h3><p>{e(", ".join(parts))}, each with a named source.</p><p><a href="{e(page)}#sources">Read the sources</a> · <a href="{e(page)}#credits">Image credits</a></p></li>
        <li><h3>Related Shorts</h3>{sh}</li>
        <li><h3>Future chapters</h3>{chapters}</li>
      </ul>
    </div>
  </div>
</section>'''


# ---------- Memory Room ----------
def memory_room():
    qs = []
    for f in FILMS:
        p = published(f)
        if p and f.get("family_questions"):
            for q in f["family_questions"]:
                qs.append((q, p["title"]))
    items = "".join(f'<li><p class="u-q-text">{e(q)}</p><p class="u-q-from">From the film {e(t)}</p></li>' for q, t in qs)
    return f'''<section class="u-sec u-room u-dark" id="memory-room" aria-labelledby="u-room-h">
  <div class="u-wrap">
    <p class="u-label u-kick">Memory Room{TAG if PROTO else ''}</p>
    <h2 id="u-room-h">A question to take to the table</h2>
    <p class="u-lede">Most of what we inherited was never written down. Take one question, ask someone in your family, and listen for the answer.</p>
    <div class="u-room-card">
      <ol class="u-qs" aria-live="off">{items}</ol>
      <div class="u-room-actions">
        <button class="u-btn u-btn-gold" type="button" id="u-next">Another question</button>
        <button class="u-btn u-btn-line" type="button" id="u-copy">Copy this question</button>
      </div>
      <p class="u-status" id="u-status" role="status"></p>
      <p class="u-room-note">Write down one thing they say, in their own words.</p>
    </div>
    <p class="u-room-fine">Nothing on this page is saved or sent. The questions come from the approved film pages. Sharing family stories with KRIOS is not part of this prototype.</p>
  </div>
</section>'''


# ---------- Why do we do this? ----------
def why():
    out = []
    for it in W["items"]:
        f = film_by_slug(it["film"])
        p = published(f)
        assert p, f"film not published: {it['film']}"
        page = f"/films/{f['slug']}/"
        s = f["sources"]

        def claims(key, idx):
            lis = []
            for k in idx:
                c = s[key][k]
                cite = (f'<a href="{e(c["url"])}" rel="noopener">{e(c["cite"])}</a>' if c.get("url") else e(c["cite"]))
                lis.append(f'<li>{e(c["text"])}<cite>{cite}</cite></li>')
            return '<ul class="u-claims">' + "".join(lis) + "</ul>"

        blocks = []
        if it.get("established"):
            blocks.append(f'<div><h3>What the sources show</h3>{claims("established", it["established"])}</div>')
        if it.get("interpretation"):
            blocks.append(f'<div><h3>Interpretation, not established fact</h3>{claims("interpretation", it["interpretation"])}</div>')
        if it.get("open"):
            blocks.append(f'<div><h3>Still open</h3>{claims("open", it["open"])}</div>')
        quote = "".join(f"<p>{e(f['story'][k])}</p>" for k in it["quote"])
        blocks.append(f'<blockquote class="u-quote">{quote}<p class="u-quote-from">{e(f["story_from"])}</p></blockquote>')
        blocks.append(f'<div class="u-ask"><a class="u-btn u-btn-ink" href="{page}#family">Questions for your family</a>'
                      f'<a href="{page}">Read the full film page</a></div>')
        out.append(f'<details name="u-why"><summary>{e(it["question"])}</summary><div class="u-why-body">{"".join(blocks)}</div></details>')
    return f'''<section class="u-sec u-why" id="why" aria-labelledby="u-why-h">
  <div class="u-wrap">
    <p class="u-label u-kick" style="color:var(--u-gold-ink)">Why do we do this?{TAG if PROTO else ''}</p>
    <h2 id="u-why-h">The questions behind the customs</h2>
    <p class="u-lede">{e(W["intro"])}</p>
    <div class="u-why-list">{"".join(out)}</div>
  </div>
</section>'''


def know():
    return '''<section class="u-sec u-know" aria-labelledby="u-know-h">
  <div class="u-wrap">
    <p class="u-label u-kick" style="color:var(--u-gold-ink)">How we work</p>
    <h2 id="u-know-h">Built on evidence, told by people</h2>
    <ul>
      <li><b>The oldest source, not the most famous</b><span>Primary sources and named scholarship for every historical claim, checked before recording and again on the finished film.</span></li>
      <li><b>Real archives first</b><span>Historical photographs, documents, icons and maps, credited with their licence.</span></li>
      <li><b>Illustration is labelled</b><span>Where no photograph exists, some everyday scenes are illustrated. They are marked and never stand in for sacred or historical evidence.</span></li>
      <li><b>A human voice</b><span>Every documentary today is narrated in a human voice.</span></li>
    </ul>
    <p class="u-more"><a class="u-btn u-btn-ink" href="/how-we-work/">How we work</a></p>
  </div>
</section>'''


def close():
    return f'''<section class="u-sec u-ded" aria-label="Dedication"><div class="u-wrap">{DEDICATION_HTML}</div></section>
<section class="u-sec u-close u-dark" aria-labelledby="u-close-h"><div class="u-wrap">
  <h2 id="u-close-h">Who taught you yours?</h2>
  <a class="u-btn u-btn-gold" href="{SUB}" rel="noopener">Subscribe on YouTube</a>
</div></section>'''


def build():
    extra = ('<meta name="robots" content="noindex, nofollow">\n<link rel="stylesheet" href="/assets/universe.css">\n'
             '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap" rel="stylesheet">')
    banner = ('<div class="u-proto" role="note"><span class="u-wrap"><b>Design prototype</b>'
              '<span>Proposed homepage. Not the live site, not approved, not indexed.</span></span></div>') if PROTO else ""
    html = f"""{head("KRIOS · Universe homepage prototype", "Proposed redesign of the KRIOS homepage. Design prototype, not the live site.", "/prototype/universe/", extra=extra)}
<body>
{banner}
{header()}
<main id="main">
{hero()}
{gateways()}
{featured()}
{memory_room()}
{why()}
{know()}
{close()}
</main>
{footer()}
{SCRIPTS}
<script src="/assets/universe.js" defer></script>
</body>
</html>
"""
    full = os.path.join(ROOT, OUT)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(html)
    print("wrote", OUT, len(html), "bytes")


if __name__ == "__main__":
    build()
