# Data and card helpers shared by build_home.py and build_films.py.
# Public pages never show episode numbers ("n") or season numbers ("season"); both stay internal.
import datetime, html, json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
load = lambda p: json.load(open(os.path.join(ROOT, p), encoding="utf-8"))
DATA = load("data/episodes.json")
EP = sorted(DATA["episodes"], key=lambda x: x["date"], reverse=True)       # newest first
S1 = DATA["season1"]
UP = load("data/upcoming.json")["upcoming"]
SUBJ = load("data/subjects.json")
SD = load("data/sacred_days.json")
TODAY = datetime.date.today().isoformat()

MONTHS = "January February March April May June July August September October November December".split()
e = lambda s: html.escape(str(s), quote=True)
watch = lambda v: f"https://www.youtube.com/watch?v={v}"
thumb = lambda v, q="hqdefault": f"https://i.ytimg.com/vi/{v}/{q}.jpg"
nice = lambda d: f"{MONTHS[int(d[5:7]) - 1]} {int(d[8:10])}, {d[:4]}"
short = lambda d: f"{MONTHS[int(d[5:7]) - 1][:3]} {int(d[8:10])}"
weekday = lambda d: datetime.date.fromisoformat(d).strftime("%A")


def subjects_of(x):
    """Subjects for a film: an approved override (by id or title text), else the label mapping."""
    for o in SUBJ.get("overrides", []):
        if ("id" in o and o["id"] == x.get("id")) or ("title" in o and o["title"].lower() in x.get("title", "").lower()):
            return list(o["subjects"])
    return list(SUBJ["from_label"].get(x.get("label", ""), []))


def tags(x):
    return " ".join(subjects_of(x))


def card(x, d=0.0, compact=False):
    meta = f'{e(x["label"])} · {short(x["date"])} · {x["mins"]} min'
    tease = "" if compact else f'<span class="m-ctext">{e(x.get("tease", ""))}</span>'
    return (f'<a class="m-card reveal" style="--d:{d:.2f}s" href="{watch(x["id"])}" rel="noopener" data-tags="{tags(x)}">'
            f'<span class="m-thumb"><img src="{thumb(x["id"])}" alt="" loading="lazy" width="480" height="270"></span>'
            f'<span class="m-cbody"><span class="label m-kick">{meta}</span><span class="m-ctitle">{e(x["title"])}</span>{tease}</span></a>')


def s1card(x):
    return (f'<a class="m-card m-card--s1 reveal" href="{watch(x["id"])}" rel="noopener" data-tags="myth">'
            f'<span class="m-thumb"><img src="{thumb(x["id"])}" alt="" loading="lazy" width="480" height="270"></span>'
            f'<span class="m-cbody"><span class="label m-kick">Where KRIOS began</span><span class="m-ctitle">{e(x["title"])}</span></span></a>')


def upcoming_card(u):
    return (f'<a class="m-card m-card--soon reveal" href="/sacred-days/" data-tags="{tags(u)}">'
            f'<span class="m-thumb"><img src="{u["image"]}" alt="" width="480" height="270"><span class="m-badge">Premieres {short(u["date"])}</span></span>'
            f'<span class="m-cbody"><span class="label m-kick">{e(u["label"])} · {nice(u["date"])}</span><span class="m-ctitle">{e(u["title"])}</span>'
            f'<span class="m-ctext">{e(u.get("tease", ""))}</span></span></a>')


def featured_film():
    return next((x for x in EP if x.get("featured")), EP[0])


def featured(x):
    return (f'<a class="m-feat reveal" href="{watch(x["id"])}" rel="noopener" data-tags="{tags(x)}"><span class="m-feat-img">'
            f'<img src="{thumb(x["id"], "maxresdefault")}" onerror="this.onerror=null;this.src=\'{thumb(x["id"])}\'" alt="" width="960" height="540">'
            f'<span class="m-play">▶ {x["mins"]} min</span></span><span class="m-feat-body"><span class="label m-kick">Featured · {e(x["label"])} · {nice(x["date"])}</span>'
            f'<span class="m-feat-title">{e(x["title"])}</span><span class="m-feat-text">{e(x.get("tease", ""))}</span>'
            f'<span class="m-cta">Watch the film →</span></span></a>')


def sacred_next():
    """The next scheduled Sacred Days film, else the latest released one from the last 30 days, else None."""
    up = next((u for u in UP if u.get("label") == "Sacred Days"), None)
    if up:
        return "upcoming", up
    cutoff = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
    rel = next((x for x in EP if x.get("label") == "Sacred Days" and x["date"] >= cutoff), None)
    return ("released", rel) if rel else (None, None)


def sacred_films():
    return [x for x in EP if x.get("label") == "Sacred Days"]


def calendar_entries():
    """Curated feasts from today onward. Fixed feasts roll to next year once passed; a passed moveable feast drops off."""
    out = []
    for f in SD["feasts"]:
        d = f["date"]
        if d < TODAY:
            if f.get("moveable"):
                continue
            y = int(TODAY[:4])
            d = f"{y}{d[4:]}"
            if d < TODAY:
                d = f"{y + 1}{d[4:]}"
        out.append(dict(f, date=d))
    return sorted(out, key=lambda f: f["date"])


def film_for_feast(f):
    """Release status for a feast comes only from upcoming.json (scheduled) or episodes.json (published)."""
    m = f.get("film_match")
    if not m:
        return None, None
    up = next((u for u in UP if m.lower() in u["title"].lower()), None)
    if up:
        return "scheduled", up
    rel = next((x for x in EP if m.lower() in x["title"].lower()), None)
    return ("published", rel) if rel else (None, None)


XR = ('<svg class="xr" viewBox="0 0 18 26" aria-hidden="true"><rect x="7.6" y="2" width="2.8" height="22"/>'
      '<rect x="1.5" y="7.6" width="15" height="2.8"/><circle cx="9" cy="2.2" r="2"/><circle cx="9" cy="23.8" r="2"/>'
      '<circle cx="1.8" cy="9" r="2"/><circle cx="16.2" cy="9" r="2"/></svg>')

# The approved dedication (director, Oct 19, 2026). Do not edit; check_site.py verifies it byte for byte.
DEDICATION_LINES = ["For my father, Peter (Πέτρος).", "He led by example.",
                    "A piece of you will forever remain in our hearts.", "Αἰωνία σου ἡ μνήμη."]
DEDICATION_HTML = (
    '<div class="m-dedication reveal">\n'
    f'      <p class="dname"><span aria-hidden="true"></span>{XR}<i>{DEDICATION_LINES[0]}</i>{XR}<span aria-hidden="true"></span></p>\n'
    f'      <p>{DEDICATION_LINES[1]}</p>\n'
    f'      <p>{DEDICATION_LINES[2]}</p>\n'
    f'      <p class="dgr" lang="el">{DEDICATION_LINES[3]}</p>\n'
    '    </div>')

ILLUSTRATION_NOTE = "Thumbnail artwork is an illustration, not a historical image."
