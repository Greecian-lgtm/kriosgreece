# Builds the PROPOSED Universe homepage prototype at /prototype/universe/ (design branch only).
# Not linked from the live site, noindex, kept out of the sitemap. Reads the same approved data as the live site;
# nothing here is typed by hand that the film data already says. Run: python3 build_universe.py
import json, os
from site_lib import (ROOT, EP, UP, SUBJ, FILMS, DEDICATION_HTML, e, nice, short, released, film_page_for, featured_film,
                      subjects_of, calendar_entries, film_for_feast, _matches, thumb)
from site_parts import head, footer, SCRIPTS, SUB, YT, menu_button

OUT = "prototype/universe/index.html"
load = lambda p: json.load(open(os.path.join(ROOT, p), encoding="utf-8"))
G, W, FT = load("data/universe/gateways.json"), load("data/universe/why.json"), load("data/universe/featured.json")

TAG = " · proposed"
PROTO = True   # prototype-only labels and banner; set False when the page is promoted

NAVP = [("/films/", "Films"), ("/sacred-days/", "Sacred Days"), ("#gateways", "Themes"), ("#memory-room", "Memory Room"), ("/answers/", "Q&amp;A")]


def film_by_slug(slug):
    return next(f for f in FILMS if f["slug"] == slug)


def published(f):
    """The published episode for an approved film, or None. Prototype content only uses published films."""
    return released(f["match"])


# ---------- header (proposed navigation) ----------
def header(banner=""):
    links = "".join(f'<a href="{h}">{t}</a>' for h, t in NAVP)
    return ('<a class="skip" href="#main">Skip to content</a>\n' + banner + '<header class="top">\n  <div class="wrap">\n'
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
      <h1 id="u-h1"><span>The stories we inherited.</span><span class="u-q2">The questions we never asked.</span></h1>
      <p class="u-sub">Short documentaries on Greek history, faith and family memory. Real archives. Named sources. Made for Greeks in Greece and everywhere else.</p>
      <div class="u-cta">
        <a class="u-btn u-btn-gold" href="#featured">Watch the newest film</a>
        <a class="u-textlink" href="#gateways">Or start with a theme</a>
      </div>
    </div>
    <figure class="u-hero-art">
      <img src="{e(img['src'])}" alt="{e(img['alt'])}" width="1280" height="720" fetchpriority="high">
      <span class="u-chip">Illustration</span>
      <figcaption class="u-cap">Illustration from the film The Greeks Who Left. It is not a historical photograph.</figcaption>
    </figure>
  </div>
</section>'''


# ---------- six gateways ----------
def film_count(subjects):
    keys = set(subjects)
    return sum(1 for x in EP if keys & set(subjects_of(x)))


def gateways():
    tiles = []
    for g in G["gateways"]:
        n = film_count(g["subjects"])
        if g["key"] == "faith-sacred-days":
            status = f'{n} film{"s" if n != 1 else ""} and a calendar'
        elif n:
            status = f'{n} film{"s" if n != 1 else ""}'
        else:
            status = "Coming soon"
        cls = "u-gate" + ("" if n else " u-gate--empty")
        tiles.append(f'''<li class="{cls}">
      <p class="u-gate-el" lang="el">{e(g["el"])}</p>
      <h3><a href="{e(g["href"])}">{e(g["en"])}</a></h3>
      <p>{e(g["line"])}</p>
      <div class="u-gate-foot"><span>{e(status)}</span><span class="u-go" aria-hidden="true">→</span></div>
    </li>''')
    return f'''<section class="u-sec u-gates" id="gateways" aria-labelledby="u-gates-h">
  <div class="u-wrap">
    <h2 id="u-gates-h">Start with what feels closest to home.</h2>
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
        sh = ""
    ups = [f'<li><b>{e(u["title"])}</b><br><span class="u-soft">{e(u["label"])} · premieres {nice(u["date"])}</span></li>' for u in UP]
    chapters = "<ul>" + "".join(ups) + "</ul>"
    return f'''<section class="u-sec u-feat u-dark" id="featured" aria-labelledby="u-feat-h">
  <div class="u-wrap">
    <h2 id="u-feat-h">The newest film</h2>
    <div class="u-feat-grid">
      <article class="u-film">
        <span class="u-film-meta">{e(x["label"])} · {x["mins"]} min · {nice(x["date"])}</span>
        <h3>{e(x["title"])}</h3>
        <p>{e(x.get("tease", ""))}</p>
        <div class="u-cta">
          <a class="u-btn u-btn-gold" href="https://www.youtube.com/watch?v={e(x["id"])}" rel="noopener">Watch on YouTube</a>
          <a class="u-textlink" href="{e(page)}">Open the film page</a>
        </div>
      </article>
      <ul class="u-rail" aria-label="Connected to this film">
        <li><h3>Source material</h3><p>{e(", ".join(parts))}, each with a named source.</p><p><a href="{e(page)}#sources">Read the sources</a> <a href="{e(page)}#credits">Image credits</a></p></li>
        {('<li><h3>Related Shorts</h3>' + sh + '</li>') if sh else ''}
        <li><h3>Coming next</h3>{chapters}</li>
      </ul>
    </div>
  </div>
</section>'''


# ---------- storybook: unlocking memories (published films open, upcoming stay locked) ----------
def storybook():
    pages = []
    for x in sorted((x for x in EP if x["id"] and x.get("date") and film_page_for(x)), key=lambda x: x["date"], reverse=True)[:3]:
        t = thumb(x["id"], "maxresdefault")
        art = (f'<img src="{t}" alt="Thumbnail of the film {e(x["title"])}" width="1280" height="720" loading="lazy" '
               f'onerror="this.onerror=null;this.src=\'{thumb(x["id"])}\'">')
        pages.append(f'''<li class="u-sb-page is-open"><div class="u-sb-art">{art}</div>
      <div class="u-sb-text"><p class="u-label u-sb-tag">Memory unlocked</p><h3>{e(x["title"])}</h3><p>{e(x.get("tease", ""))}</p>
      <a class="u-btn u-btn-gold" href="{e(film_page_for(x))}">Open this memory</a></div></li>''')
    for u in UP:
        pages.append(f'''<li class="u-sb-page is-locked"><div class="u-sb-art u-sb-veil"><img src="{e(u["image"])}" alt="" width="960" height="540" loading="lazy"><div class="u-sb-lock" aria-hidden="true"></div></div>
      <div class="u-sb-text"><p class="u-label u-sb-tag">Opens {nice(u["date"])}</p><h3>{e(u["title"])}</h3><p>This page stays closed until the premiere.</p></div></li>''')
    return f'''<section class="u-sec u-sb u-dark" id="storybook" aria-labelledby="u-sb-h">
  <div class="u-wrap">
    <h2 id="u-sb-h">A storybook of memories{TAG if PROTO else ''}</h2>
    <p class="u-lede">Each film opens one page. Turn through the ones that are open. The next one is waiting.</p>
    <ol class="u-sb-track" tabindex="0" aria-label="Storybook pages, scroll sideways">{"".join(pages)}</ol>
    <div class="u-sb-nav"><button class="u-btn u-btn-line" type="button" id="u-sb-prev">Previous page</button><button class="u-btn u-btn-gold" type="button" id="u-sb-next">Turn the page</button></div>
  </div>
</section>'''


# ---------- Memory Room ----------
def memory_room():
    per = []
    for f in FILMS:
        p = published(f)
        if p and f.get("family_questions"):
            per.append([(q, p["title"]) for q in f["family_questions"]])
    qs = [x for row in zip(*per) for x in row] if len(per) > 1 else [x for r in per for x in r]
    items = "".join(f'<li><p class="u-q-text">{e(q)}</p><p class="u-q-from">From {e(t)}</p></li>' for q, t in qs)
    return f'''<section class="u-sec u-room u-dark" id="memory-room" aria-labelledby="u-room-h">
  <div class="u-wrap">
    <p class="u-label u-kick">Memory Room{TAG if PROTO else ''}</p>
    <h2 id="u-room-h">A question to take to the table</h2>
    <p class="u-lede">Most of what we inherited was never written down. Here is one question for the table. Skip any that feel heavy.</p>
    <div class="u-room-card">
      <ol class="u-qs" aria-live="off">{items}</ol>
      <div class="u-room-actions">
        <button class="u-btn u-btn-gold" type="button" id="u-next">Another question</button>
      </div>
      <p class="u-status" id="u-status" role="status"></p>
      <p class="u-room-note">Maybe write down one thing they say.</p>
    </div>
    <p class="u-room-fine">Nothing here is saved or sent. These questions come from the film pages.</p>
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
            blocks.append(f'<div><h3>What the sources say</h3>{claims("established", it["established"])}</div>')
        if it.get("interpretation"):
            blocks.append(f'<div><h3>Interpretation, not established fact</h3>{claims("interpretation", it["interpretation"])}</div>')
        if it.get("open"):
            blocks.append(f'<div><h3>Still open</h3>{claims("open", it["open"])}</div>')
        quote = "".join("<p>" + e(f['story'][k]).replace("\u03be\u03b5\u03bd\u03b9\u03c4\u03b9\u03ac", '<span lang="el">\u03be\u03b5\u03bd\u03b9\u03c4\u03b9\u03ac</span>') + "</p>" for k in it["quote"])
        blocks.append(f'<blockquote class="u-quote">{quote}<p class="u-quote-from">From the film\u2019s narration.</p></blockquote>')
        blocks.append(f'<div class="u-ask"><a class="u-btn u-btn-ink" href="{page}#family">Questions for your family</a>'
                      f'<a href="{page}">Read the full film page</a></div>')
        out.append(f'<details name="u-why"><summary>{e(it["question"])}</summary><div class="u-why-body">{"".join(blocks)}</div></details>')
    return f'''<section class="u-sec u-why" id="why" aria-labelledby="u-why-h">
  <div class="u-wrap">
    <p class="u-label u-kick" style="color:var(--u-gold-ink)">Why do we do this?{TAG if PROTO else ''}</p>
    <h2 id="u-why-h">Questions the films answer</h2>
    <p class="u-lede">Each answer shows what the sources say and what is still open.</p>
    <div class="u-why-list">{"".join(out)}</div>
  </div>
</section>'''


def know():
    return '''<section class="u-sec u-know" aria-labelledby="u-know-h">
  <div class="u-wrap">
    <h2 id="u-know-h">How we work</h2>
    <ul>
      <li><b>The oldest source, not the most famous</b><span>Primary sources and named scholarship for every historical claim, checked before recording and again on the finished film.</span></li>
      <li><b>Real archives first</b><span>Historical photographs, documents, icons and maps, credited with their licence.</span></li>
      <li><b>Illustration is labelled</b><span>Where no photograph exists, some everyday scenes are illustrated. They are marked and never stand in for sacred or historical evidence.</span></li>
      <li><b>A human voice</b><span>Every film is narrated by a human voice.</span></li>
    </ul>
    <p class="u-more"><a class="u-btn u-btn-ink" href="/how-we-work/">Read how we work</a></p>
  </div>
</section>'''


def close():
    return f'''<section class="u-sec u-ded" aria-label="Dedication"><div class="u-wrap">{DEDICATION_HTML}</div></section>
<section class="u-sec u-close u-dark" aria-labelledby="u-close-h"><div class="u-wrap">
  <h2 id="u-close-h">Who taught you the songs?</h2>
  <p class="u-lede">The films live on YouTube. Subscribe to hear when the next one is out.</p>
  <a class="u-btn u-btn-gold" href="{SUB}" rel="noopener">Subscribe on YouTube</a>
</div></section>'''


def build():
    extra = ('<meta name="robots" content="noindex, nofollow">\n<link rel="stylesheet" href="/assets/universe.css">\n'
             '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap" rel="stylesheet">')
    banner = ('<div class="u-proto" role="note"><span class="u-wrap"><b>Design prototype</b>'
              '<span>Proposed homepage. Not the live site, not approved, not indexed.</span></span></div>') if PROTO else ""
    html = f"""{head("KRIOS · Universe homepage prototype", "Proposed redesign of the KRIOS homepage. Design prototype, not the live site.", "/prototype/universe/", extra=extra)}
<body>
{header(banner)}
<main id="main">
{hero()}
{featured()}
{storybook()}
{gateways()}
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
