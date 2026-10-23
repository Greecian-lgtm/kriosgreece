# Builds the SACRED page at /sacred/ (locked by the director, Oct 23, 2026; released after the Oct 24 to 27 freeze).
# Images are separate files under assets/sacred/ (director-approved; provenance in krios-workspace docs/skills-audit; printed icon artwork rights UNKNOWN, director decision Oct 23).
# Run: python3 build_sacred.py
import json, os
import datetime
from site_lib import ROOT, e, SD
from site_parts import head, footer, SCRIPTS, SUB, menu_button, nav_links

G = json.load(open(os.path.join(ROOT, "data/guide.json"), encoding="utf-8"))
OUT = "sacred/index.html"
GUIDE_IDS = ["sacred-days", "name-day", "history-tradition-belief", "real-or-illustrated"]
ITEMS = {i["id"]: i for g in G["groups"] for i in g["items"]}

PATHS = [
    ("Churches &amp; Monasteries", "The architecture, history and living heritage.", "sacred_churches_v02", None),
    ("Sacred Days", "Feast days, saints and the traditions that unite communities.", "ICON:sacred_icon_theotokos", "/sacred-days/"),
    ("Icons &amp; Art", "The meaning, symbolism and stories behind sacred art.", "sacred_icons_v01", None),
    ("Faith in Daily Life", "How traditions continue today, at home, in the village and around the world.", "sacred_daily_v02", None),
]
CARD_W = {"sacred_icon_theotokos": [380, 600, 940], "sacred_churches_v02": [700, 878], "sacred_icons_v01": [700, 888], "sacred_daily_v02": [700, 899]}


PREVIEW = os.environ.get("GUIDE_PREVIEW") == "1"
SI = json.load(open(os.path.join(ROOT, "data/sacred_i18n.json"), encoding="utf-8"))
GI = json.load(open(os.path.join(ROOT, "data/guide_i18n.json"), encoding="utf-8"))


def langs_allowed():
    """English plus each language marked reviewed (or every drafted language in a staging preview)."""
    return ["en"] + [l for l in ("el", "es") if PREVIEW or GI["review"].get(l) == "reviewed"]


def lang_picker():
    """On-page radio language picker (director, Oct 23). Hidden when only English is available."""
    ls = langs_allowed()
    names = {"en": "English", "el": "Ελληνικά", "es": "Español"}
    radios = "".join(f'<label lang="{l}"><input type="radio" name="s-lang" value="{l}"{" checked" if l == "en" else ""}><span>{names[l]}</span></label>' for l in ls)
    hidden = "" if len(ls) > 1 else " hidden"
    return (f'<div class="s-langbar"{hidden}><fieldset class="s-lang"><legend class="s-sr" data-t="lang_legend">Language</legend>{radios}</fieldset>'
            f'<p class="s-draft" id="s-draft" hidden>Draft translation for review. Not yet approved.</p></div>')


def client_i18n():
    """Strings for the languages allowed in this build only; unreviewed languages never reach the public page."""
    ls = langs_allowed()
    out = {"preview": PREVIEW, "review": GI["review"], "ui": {l: SI["ui"][l] for l in ls}, "feasts_es": SI["feasts_es"] if "es" in ls else {},
           "items": {k: {l: GI["items"][k][l] for l in ls if l != "en" and l in GI["items"].get(k, {})} for k in GUIDE_IDS},
           "status": {l: GI["status"][l] for l in ls if l != "en"}, "terms": {l: GI.get("terms", {}).get(l, {}) for l in ls if l != "en"},
           "draft": {k: v for k, v in {"el": "Πρόχειρη μετάφραση για έλεγχο. Δεν έχει εγκριθεί ακόμη.", "es": "Traducción en borrador para revisión. Todavía no está aprobada."}.items() if k in ls}}
    return json.dumps(out, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def header():
    return ('<a class="skip" href="#main">Skip to content</a>\n<header class="top s-top">\n  <div class="wrap">\n'
            '    <a class="brand" href="/"><b>KRIOS</b><span>Greek cultural preservation</span></a>\n'
            f'    <nav class="nav" aria-label="Main"><a class="s-guide" href="#guide" data-t="guide_h">Page Guide</a>{menu_button()}{nav_links("Sacred")}'
            f'<a class="btn btn-gold" href="{SUB}" rel="noopener">Subscribe<span class="m-hide-sm">&nbsp;on YouTube</span></a></nav>\n'
            '  </div>\n</header>')


def path_card(t, d, img, href, n=0):
    """Pathway card image: decorative (alt=""), sRGB web copies, never enlarged; the page carries one illustration note."""
    base = "/assets/sacred/"
    if img and img.startswith("ICON:"):
        # a real icon from the director's photograph (Track B): shown whole, never cropped, on the card's dark ground
        name = img[5:]; ws = CARD_W[name]; sz = "(max-width: 760px) 36vw, (max-width: 1100px) 18vw, 9vw"
        webp = ", ".join(f"{base}{name}_{w}.webp {w}w" for w in ws); jpg = ", ".join(f"{base}{name}_{w}.jpg {w}w" for w in ws)
        media = (f'<picture class="s-icon"><source type="image/webp" srcset="{webp}" sizes="{sz}">'
                 f'<img src="{base}{name}_{ws[1]}.jpg" srcset="{jpg}" sizes="{sz}" alt="" width="940" height="1264" loading="lazy" decoding="async"></picture>')
    elif img and img.startswith("HOLD:"):
        media = f'<img src="{img[5:]}" alt="" width="350" height="167" loading="lazy" decoding="async">'
    elif img:
        ws = CARD_W[img]
        webp = ", ".join(f"{base}{img}_{w}.webp {w}w" for w in ws)
        jpg = ", ".join(f"{base}{img}_{w}.jpg {w}w" for w in ws)
        media = (f'<picture><source type="image/webp" srcset="{webp}" sizes="(max-width: 760px) 100vw, (max-width: 1100px) 50vw, 25vw">'
                 f'<img src="{base}{img}_{ws[-1]}.jpg" srcset="{jpg}" sizes="(max-width: 760px) 100vw, (max-width: 1100px) 50vw, 25vw" '
                 f'alt="" width="350" height="167" loading="lazy" decoding="async"></picture>')
    else:
        media = '<span class="s-ground" aria-hidden="true"></span>'
    inner = f'<span class="s-pmedia">{media}</span><span class="s-ptext"><h3 data-t="c{n}_t">{t}</h3><p data-t="c{n}_d">{d}</p></span>'
    if href:
        return f'<li><a class="s-path" href="{href}">{inner}<span class="s-arrow" aria-hidden="true">&rarr;</span><span class="s-sr" data-t="open_c{n}">Open {t}</span></a></li>'
    return f'<li><div class="s-path s-soon">{inner}<span class="s-tag" data-t="soon">In preparation</span></div></li>'


def guide_block():
    out = ""
    for k in GUIDE_IDS:
        it = ITEMS[k]
        paras = "".join(f"<p>{e(p)}</p>" for p in it["a"])
        read = "".join(f'<li><a href="{e(u)}" data-term="{e(t)}">{e(t)}</a></li>' for t, u in it["read"])
        out += (f'<li><details><summary data-gq="{k}">{e(it["q"])}</summary><div class="s-ga"><p class="s-gs" data-gs="{it["status"]}">{e(G["status_text"][it["status"]])}</p>'
                f'<div data-ga="{k}">{paras}</div><ul>{read}</ul></div></details></li>')
    return out


def calendar_band():
    """Prominent entry to the existing Sacred Calendar (/sacred-days/#calendar). Dates come from data/sacred_days.json, never duplicated."""
    today = datetime.date.today().isoformat()
    nxt = [f for f in SD["feasts"] if f["date"] >= today][:3] or SD["feasts"][-3:]
    rows = ""
    for f in nxt:
        d = datetime.date.fromisoformat(f["date"])
        rows += (f'<li data-date="{f["date"]}" data-en="{e(f["en"])}"><span class="s-cd" aria-hidden="true"><i>{d.strftime("%b")}</i><b>{d.day}</b></span>'
                 f'<span><b class="s-fn">{e(f["en"])}</b> <span class="s-fel" lang="el">{e(f["el"])}</span><small>{d.strftime("%A, %B")} {d.day}, {d.year}</small></span></li>')
    return (f'<section class="s-cal" aria-labelledby="s-calh"><div class="s-calbox">'
            f'<div><p class="s-kick" data-t="cal_kick">The year ahead</p><h2 id="s-calh" data-t="cal_h">The Sacred Calendar</h2>'
            f'<p data-t="cal_p">Feast days and name days, with the date of each verified against Church sources. Feast dates are listed separately from any KRIOS film release.</p>'
            f'<p><a class="s-calbtn" href="/sacred-days/#calendar" data-t="cal_btn">Explore the Sacred Calendar</a></p></div>'
            f'<ol class="s-calnext" aria-label="Coming up" data-taria="cal_list">{rows}</ol></div></section>')


HERO_ALT = ("A whitewashed village chapel with a blue-trimmed door at the end of a stone lane, bougainvillea on the left "
            "and the sea behind, in morning light. AI-generated illustration of an imagined place, not a real named church.")


def hero_pair():
    """Faith entrance pair (director-approved Night Frame A, corrected Morning Frame B v03), native 1672 px masters,
    web copies at 1600 and 800 px (never enlarged), sRGB tagged. Morning carries the alt text and is the static frame."""
    base = "/assets/sacred/"
    def pic(k, cls, extra_img):
        return (f'<picture class="{cls}"><source type="image/webp" srcset="{base}hero_{k}_800.webp 800w, {base}hero_{k}_1600.webp 1600w" '
                f'sizes="(max-width: 900px) 100vw, 62vw"><img src="{base}hero_{k}_1600.jpg" '
                f'srcset="{base}hero_{k}_800.jpg 800w, {base}hero_{k}_1600.jpg 1600w" sizes="(max-width: 900px) 100vw, 62vw" '
                f'width="1600" height="900" {extra_img}></picture>')
    return (pic("night", "s-hn", 'alt="" aria-hidden="true" loading="lazy" decoding="async"')
            + pic("morning", "s-hm", f'alt="{HERO_ALT}" data-talt="hero_alt" fetchpriority="high" decoding="async"')
            + '<span class="s-ai" data-t="ai_chip">AI illustration &middot; not a photograph</span>')


def build():
    cards = "".join(path_card(*p, n=i + 1) for i, p in enumerate(PATHS))
    desc = "Greek Orthodox faith, places and traditions from KRIOS: Sacred Days feast films, the Sacred Calendar and answers from the Page Guide."
    extra = ('<link rel="stylesheet" href="/assets/universe-fonts.css">\n'
             '<link rel="stylesheet" href="/assets/sacred.css">\n'
             # one entrance moment (web motion standard): night-to-morning crossfade only when motion is welcome;
             # reduced motion, saved data, no JavaScript and print show the morning frame from first paint
             '<script>(function(){try{var r=window.matchMedia("(prefers-reduced-motion: reduce)").matches,'
             'd=navigator.connection&&navigator.connection.saveData;if(!r&&!d)document.documentElement.classList.add("s-anim")}catch(e){}})();</script>')
    html = f'''{head("Sacred · KRIOS", desc, "/sacred/", extra=extra)}
<body class="s-page">
{header()}
{lang_picker()}
<main id="main">
  <section class="s-hero" aria-labelledby="s-h1">
    <div class="s-heroimg">{hero_pair()}</div>
    <div class="s-herotext">
      <p class="s-kick">KRIOS Universe</p>
      <h1 id="s-h1">SACRED</h1>
      <p class="s-sub" data-t="sub">Faith &middot; Traditions &middot; Living Heritage</p>
      <span class="s-rule" aria-hidden="true"></span>
      <p class="s-lede" data-t="lede">Explore the faith, places and traditions that have shaped Greek life for generations, connecting the past, the present and the people who carry these traditions forward.</p>
    </div>
  </section>
  <section class="s-paths" aria-labelledby="s-ph"><h2 id="s-ph" class="s-sr" data-t="four_ways">Four ways in</h2><ul class="s-grid">{cards}</ul><p class="s-illus" data-t="page_note">Sacred Days, and the Archangels Michael and Gabriel beside the closing words: photographs of icons in a Greek Orthodox home (KRIOS). The other images on this page are AI illustrations of imagined places and objects, not photographs.</p></section>
  {calendar_band()}
  <section class="s-quote" aria-label="Closing"><div class="s-qwrap"><picture class="s-angel"><source type="image/webp" srcset="/assets/sacred/sacred_archangel_michael_360.webp 1x, /assets/sacred/sacred_archangel_michael_720.webp 2x"><img src="/assets/sacred/sacred_archangel_michael_360.png" srcset="/assets/sacred/sacred_archangel_michael_720.png 2x" alt="" width="196" height="360" loading="lazy" decoding="async"></picture><div class="s-qbox"><blockquote><p data-t="quote">These traditions are not just history. They are a part of who we are, carried through generations, and still alive today.</p></blockquote>
    <p class="s-mission"><span data-t="mission1">Preserve &middot; Teach &middot; Understand</span><span data-t="mission2">Connect &middot; Pass Forward</span></p></div><picture class="s-angel"><source type="image/webp" srcset="/assets/sacred/sacred_archangel_gabriel_360.webp 1x, /assets/sacred/sacred_archangel_gabriel_720.webp 2x"><img src="/assets/sacred/sacred_archangel_gabriel_360.png" srcset="/assets/sacred/sacred_archangel_gabriel_720.png 2x" alt="" width="196" height="360" loading="lazy" decoding="async"></picture></div></section>
  <section class="s-guidebox" id="guide" aria-labelledby="s-gh">
    <h2 id="s-gh" data-t="guide_h">Page Guide</h2>
    <p data-t="guide_p">Questions about this page, answered from published KRIOS pages with their sources.</p>
    <ul class="s-glist">{guide_block()}</ul>
    <p><a class="s-more" href="/guide/" data-t="guide_more">Open the full Page Guide</a></p>
  </section>
</main>
{footer()}
<script type="application/json" id="s-i18n">{client_i18n()}</script>
<script src="/assets/sacred-i18n.js" defer></script>
{SCRIPTS}
<script>
document.addEventListener("keydown",function(ev){{
  if(ev.key!=="Escape")return;
  var o=document.querySelector("#guide details[open]");if(!o)return;
  o.open=false;var s=o.querySelector("summary");if(s)s.focus();ev.preventDefault();
}});
</script>
</body>
</html>
'''
    full = os.path.join(ROOT, OUT)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(html)
    print("wrote", OUT, len(html), "bytes")


if __name__ == "__main__":
    build()
