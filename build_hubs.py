# Builds the three hub pages: /blog/ (articles), /answers/ (Q&A) and /tools/ (quizzes),
# and restyles the quiz pages onto the KRIOS look. Reads titles from the pages themselves and
# episode data from data/episodes.json, so it can be re-run any time (build_home.py runs it).
import glob, html, json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
DATA = json.load(open("data/episodes.json", encoding="utf-8"))
EP = sorted(DATA["episodes"], key=lambda x: x["date"], reverse=True)
S1 = DATA["season1"]
YT = "https://www.youtube.com/@KriosGreece"
e = lambda s: html.escape(s, quote=True)
watch = lambda vid: f"https://www.youtube.com/watch?v={vid}"
thumb = lambda vid: f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"


def clean(t):
    t = html.unescape(re.sub(r"<[^>]+>|\s+", " ", t)).strip()
    return re.sub(r"\s*—\s*", ", ", t).replace(" ,", ",")      # KRIOS public text: no em dashes


def first(rx, s):
    m = re.search(rx, s, re.S)
    return clean(m.group(1)) if m else ""


def excerpt(s, n=150):
    body = s[s.find("<h1"):] if "<h1" in s else s
    for p in re.findall(r"<p[^>]*>(.*?)</p>", body, re.S):
        t = clean(p)
        if len(t) > 70 and not t.startswith("Stavros") and "©" not in t and "KRIOS ·" not in t:
            return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + "…"
    return ""


FONT = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">'
        '<link rel="stylesheet" href="/assets/krios.css">')


def top(active):
    from site_parts import NAV, menu_button
    links = "".join(f'<a href="{h}"{" aria-current=page" if t == active else ""}>{t}</a>' for h, t in NAV)
    return ('<header class="k-top"><div class="k-in">'
            '<a class="k-brand" href="/"><b>KRIOS</b><span>Greek cultural preservation</span></a>'
            f'<nav class="k-nav" aria-label="Site">{menu_button()}<div class="nav-links" id="site-menu">{links}</div>'
            f'<a class="k-sub" href="{YT}?sub_confirmation=1" rel="noopener">Subscribe</a></nav></div></header>')


FOOT = ('<footer class="k-foot"><div class="k-in"><span>© 2026 KRIOS · '
        f'<a href="/">kriosgreece.com</a> · <a href="{YT}" rel="noopener">YouTube ↗</a></span>'
        '<i>For my father, Peter (Πέτρος).</i></div></footer>')
REVEAL = ("<script>(function(){var d=document.documentElement;d.className+=' js';"
          "if(matchMedia('(prefers-reduced-motion: reduce)').matches||!('IntersectionObserver' in window))return;"
          "var o=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');o.unobserve(x.target)}})},{rootMargin:'0px 0px -8% 0px'});"
          "document.addEventListener('DOMContentLoaded',function(){[].forEach.call(document.querySelectorAll('.reveal'),function(el){o.observe(el)})})})();</script>")


def page(path, title, desc, canonical, active, body, extra_js=""):
    out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="https://kriosgreece.com{canonical}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="https://kriosgreece.com{canonical}"><meta property="og:type" content="website">
{FONT}
{REVEAL}
</head>
<body class="k-hubpage">{top(active)}
<main class="k-wide">
{body}
</main>
{FOOT}
<script src="/assets/site-nav.js" defer></script>
{extra_js}
</body>
</html>
"""
    open(path, "w", encoding="utf-8").write(out)
    return out


def card(href, img, kicker, title, text, cta, ext=False, d=0):
    rel = ' rel="noopener"' if ext else ""
    im = f'<span class="k-img"><img src="{img}" alt="" loading="lazy" width="480" height="360"></span>' if img else ""
    tx = f"<p>{e(text)}</p>" if text else ""
    return (f'<a class="k-card reveal" style="--d:{d:.2f}s" href="{href}"{rel}>{im}<span class="k-cbody">'
            f'<span class="k-kick">{kicker}</span><h3>{e(title)}</h3>{tx}<span class="k-cta">{cta}</span></span></a>')


# ---------- /blog/ ----------
def ep_vid(n):
    if n <= 10:
        return S1[n - 1]["id"]
    m = next((x for x in EP if x.get("n") == n), None)
    return m["id"] if m else None


arts = []
for f in sorted(glob.glob("blog/ep*.html")):
    s = open(f, encoding="utf-8").read()
    n = int(re.search(r"ep(\d+)", f).group(1))
    arts.append(dict(n=n, href="/" + f, title=first(r"<h1[^>]*>(.*?)</h1>", s), text=excerpt(s), vid=ep_vid(n)))
art_n = {a["n"] for a in arts}
s2 = [a for a in arts if a["n"] >= 11][::-1]
s1 = [a for a in arts if a["n"] <= 10][::-1]
newer = [x for x in EP if x.get("n", 99) not in art_n][:3]


def grid(items, fn):
    return '<div class="k-grid">' + "".join(fn(x, i) for i, x in enumerate(items)) + "</div>"


label_of = {x.get("n"): x.get("label", "") for x in EP}
blog_body = f"""<header class="k-hero reveal">
  <span class="k-kick">Articles</span>
  <h1>Read the story behind the film</h1>
  <p class="k-lead">Written companions to KRIOS documentaries, with more of the history and the sources behind it. Newer films are on YouTube first.</p>
</header>

<section class="k-sec">
  <div class="k-sechead reveal"><h2>Newest films</h2><a class="k-more" href="{YT}/videos" rel="noopener">All films on YouTube ↗</a></div>
  {grid(newer, lambda x, i: card(watch(x['id']), thumb(x['id']), e(x.get('label', 'KRIOS')) + ' · ' + str(x.get('mins', '')) + ' min', x['title'], x.get('tease', ''), 'Watch on YouTube ↗', True, i * .08))}
</section>

<section class="k-sec">
  <div class="k-sechead reveal"><h2>Heroes, heroines and forgotten history</h2></div>
  {grid(s2, lambda a, i: card(a['href'], thumb(a['vid']) if a['vid'] else '', e(label_of.get(a['n']) or 'Article'), a['title'], a['text'], 'Read the article', False, i * .08))}
</section>

<section class="k-sec">
  <div class="k-sechead reveal"><h2>Where KRIOS began</h2><p>The first films told the ancient stories.</p></div>
  {grid(s1, lambda a, i: card(a['href'], thumb(a['vid']) if a['vid'] else '', e(S1[a['n'] - 1]['title']), a['title'], a['text'], 'Read the article', False, (i % 3) * .08))}
</section>
"""
page("blog/index.html", "Articles · KRIOS", "Written companions to KRIOS documentaries on Greek history, faith, music and family memory.",
     "/blog/", "Articles", blog_body)

# ---------- /answers/ ----------
seen, qs = {}, []
cands = sorted(glob.glob("answers/*/index.html")) + sorted(glob.glob("answers/*.html")) + sorted(glob.glob("answers/answers/*.html"))
for f in cands:
    if f in ("answers/index.html", "answers/answers/index.html"):
        continue
    s = open(f, encoding="utf-8").read()
    if 'http-equiv="refresh"' in s:
        continue
    t = first(r"<h1[^>]*>(.*?)</h1>", s)
    if not t:
        continue
    key = re.sub(r"[^a-z0-9]", "", t.lower())
    if key in seen:
        continue
    if f.startswith("answers/answers/") and os.path.exists("answers/" + os.path.basename(f)):
        continue
    seen[key] = 1
    href = "/" + (f[:-len("index.html")] if f.endswith("/index.html") else f)
    t = t[0].upper() + t[1:]
    qs.append(dict(t=t, href=href))

import sys as _sys
_sys.path.insert(0, ROOT)
from site_lib import EXTRAS as _EXTRAS, EXTRA_QA_SLUGS as _XQ
new_qs = [q for q in qs if q["href"].strip("/").split("/")[-1] in _XQ]
qs_old = [q for q in qs if q not in new_qs]
TOPICS = [
    ("words", "Greek words and ideas", r"\b(kleos|xenia|ate|hubris|leitourgia|menis|nostos)\b"),
    ("thermopylae", "Thermopylae and the Persian Wars", r"thermopyl|anopaea|leonidas|thespian|marathon|plataea|persian"),
    ("troy", "Achilles, Troy and the Iliad", r"troy|trojan|iliad|helen|achilles|hector"),
    ("odysseus", "Odysseus and the Odyssey", r"odysse|cyclops|suitors"),
    ("theseus", "Theseus and the Minotaur", r"theseus|minotaur|ariadne|aegeus|labyrinth|knossos"),
    ("medusa", "Medusa and Perseus", r"medusa|perseus"),
    ("heracles", "Heracles", r"heracles|hercules|labours"),
    ("islands", "Islands, temples and marble", r"cyclad|paros|parian|naxos|portara|venus|milo|parthenon|acropolis|delos|lion terrace"),
    ("gods", "Gods, myths and mysteries", r"."),
]
groups = {k: [] for k, _, _ in TOPICS}
for q in qs_old:
    for k, _, rx in TOPICS:
        if re.search(rx, q["t"].lower()):
            groups[k].append(q); break
TOPICS = [("newest", "From the newest films", None)] + TOPICS
groups["newest"] = new_qs
chips = "".join(f'<a href="#{k}">{e(n)} <small>{len(groups[k])}</small></a>' for k, n, _ in TOPICS if groups[k])
secs = ""
for k, n, _ in TOPICS:
    if not groups[k]:
        continue
    items = "".join(f'<li><a href="{q["href"]}">{e(q["t"])}</a></li>' for q in sorted(groups[k], key=lambda q: q["t"]))
    secs += f'<section class="k-topic reveal" id="{k}"><h2>{e(n)}</h2><ul class="k-qlist">{items}</ul></section>\n'
ans_body = f"""<header class="k-hero reveal">
  <span class="k-kick">Q&amp;A</span>
  <h1>Questions about Greece, answered</h1>
  <p class="k-lead">Short answers to {len(qs)} questions, from the newest KRIOS films on dance, migration and faith to the ancient stories of the first films.</p>
  <div class="k-find"><label for="qfind">Find a question</label><input id="qfind" type="search" placeholder="Try Medusa, kleos or Thermopylae" autocomplete="off"><span id="qcount" aria-live="polite"></span></div>
  <nav class="k-chips" aria-label="Topics">{chips}</nav>
</header>
<div class="k-topics">
{secs}</div>
<p class="k-empty" id="qempty" hidden>No question matches that yet. <a href="{YT}" rel="noopener">Ask it in the comments on YouTube</a>.</p>
<div class="k-note reveal">More questions from the newer films are added as each film is released. <a href="/films/">See every film</a>.</div>
"""
FIND_JS = """<script>(function(){var i=document.getElementById('qfind');if(!i)return;var c=document.getElementById('qcount'),em=document.getElementById('qempty');
i.addEventListener('input',function(){var v=i.value.trim().toLowerCase(),n=0;
[].forEach.call(document.querySelectorAll('.k-topic'),function(sec){var m=0;[].forEach.call(sec.querySelectorAll('li'),function(li){var ok=!v||li.textContent.toLowerCase().indexOf(v)>-1;li.hidden=!ok;if(ok)m++});sec.hidden=!m;sec.classList.add('in');n+=m});
c.textContent=v?(n+(n===1?' question':' questions')):'';em.hidden=n>0;});})();</script>"""
page("answers/index.html", "Greek history and myth Q&A · KRIOS",
     f"Short answers to {len(qs)} questions about Greek history, faith, music and myth, from the newest KRIOS films to Achilles and Thermopylae.",
     "/answers/", "Q&amp;A", ans_body, FIND_JS)

# ---------- /tools/ ----------
quiz_vid = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6}
quizzes = []
for f in sorted(glob.glob("tools/quiz-ep*.html")):
    s = open(f, encoding="utf-8").read()
    n = int(re.search(r"ep(\d+)", f).group(1))
    t = first(r"<h1[^>]*>(.*?)</h1>", s)
    nq = s.count('"question"')
    quizzes.append(dict(href="/" + f, t=t, nq=nq, vid=S1[quiz_vid[n]]["id"] if n in quiz_vid else None))
new_quizzes = [dict(href=f"/tools/quiz-{t['quiz']['slug']}.html", t=t["quiz"]["title"], nq=len(t["quiz"]["questions"]), vid=t["episode"]["id"], label=t["episode"]["label"]) for t in _EXTRAS]
new_quiz_html = ('<section class="k-sec"><div class="k-sechead reveal"><h2>From the newest films</h2><p>Watch the film, then see how much stayed with you.</p></div>'
                 + grid(new_quizzes, lambda q, i: card(q['href'], thumb(q['vid']), f"{e(q['label'])} · {q['nq']} questions", q['t'], '', 'Take the quiz', False, (i % 3) * .08))
                 + '</section>') if new_quizzes else ""
rf = open("tools/real-or-fake.html", encoding="utf-8").read()
rf_n = len(re.findall(r'"statement"\s*:', rf)) or 15
tools_body = f"""<header class="k-hero reveal">
  <span class="k-kick">Quizzes</span>
  <h1>Test what you know</h1>
  <p class="k-lead">Short quizzes from the KRIOS films. A few minutes each, and every answer comes from the film.</p>
</header>
<a class="k-feature reveal" href="/tools/real-or-fake.html">
  <span class="k-kick">The game</span>
  <h2>Real myth, or modern invention?</h2>
  <p>{rf_n} statements about Greek mythology. Some come from the ancient sources, some were made up much later. Can you tell which is which?</p>
  <span class="k-cta">Play Real or Fake</span>
</a>
{new_quiz_html}
<section class="k-sec">
  <div class="k-sechead reveal"><h2>Where KRIOS began</h2><p>Quizzes from the first films, which told the ancient stories.</p></div>
  {grid(quizzes, lambda q, i: card(q['href'], thumb(q['vid']) if q['vid'] else '', f"{q['nq']} questions", q['t'], '', 'Take the quiz', False, (i % 3) * .08))}
</section>
<div class="k-note reveal">A new quiz is added as each new film is released. <a href="{YT}?sub_confirmation=1" rel="noopener">Subscribe on YouTube</a> to see them first.</div>
"""
page("tools/index.html", "Greek history quizzes · KRIOS",
     "Quick quizzes on Greek heroes, myths and history from the KRIOS films, plus Real or Fake: can you tell ancient myth from modern invention?",
     "/tools/", "Quizzes", tools_body)

# ---------- quiz pages: KRIOS look ----------
QMARK = "data-k=\"quiz-v1\""
QCSS = """<style>
body.k-quizpage{background:#faf6ec!important;color:#1d1a14!important}
.k-quiz{--bg:#faf6ec;--text:#1d1a14;--white:#14213a;--dim:#4a4336;--gold:#8a6a2c;--correct:#2f6b45;--wrong:#8c2a2a;
--muted:#4a4336;--card:#f5edd8;--border:#d9cdb0;--terracotta:#7e2418;--green:#2f6b45;--red:#8c2a2a}
body.k-quizpage{max-width:none!important;padding:0!important;margin:0!important;display:block!important;min-height:0!important}
.k-quiz{max-width:720px;margin:0 auto;padding:40px 24px 0;line-height:1.65}
.k-quiz h1{color:var(--white);font-weight:500;font-size:clamp(1.8rem,4vw,2.5rem);line-height:1.15;border:0;padding:0}
.k-quiz .nav{font-size:.9rem}
.k-quiz footer,.k-quiz .site-footer{display:none!important}
.k-quiz .site-header{display:none!important}
.k-quiz .page{padding:0!important;max-width:none!important}
.question-card,.score-card,.myth-card,.quiz-card{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:2px!important}
.explanation{background:#ebe1c7!important}
.k-quiz button,.k-quiz .share-btn,.k-quiz .btn{font-family:"EB Garamond",Georgia,serif!important;border-radius:2px!important;font-size:1.05rem}
.k-quiz #options button{display:block;width:100%;text-align:left;margin:.5rem 0;background:#fff;color:var(--text);border:1px solid var(--border)}
.k-quiz #options button:hover{border-color:var(--gold)}
.k-quiz #next-btn,.k-quiz .share-btn{background:#14213a!important;color:#f5edd8!important}
</style>"""


def quiz_restyle(f):
    s = open(f, encoding="utf-8").read()
    if QMARK in s:
        return False
    s = s.replace("https://youtube.com/@KriosMythology", YT).replace("youtube.com/@KriosMythology", "youtube.com/@KriosGreece")
    s = s.replace("@KriosMythology", "@KriosGreece").replace("Krios Mythology", "KRIOS")
    s = s.replace(" — ", " · ").replace(">Krios</a>", ">KRIOS</a>")
    s = re.sub(r"Perfect\. Stavros (is proud|approves)\.", "Perfect score.", s)             # retired persona
    s = re.sub(r"(?:The script|Stavros)(?: directly| explicitly)? (?:states|explains|notes|warns|says)\s*:", "The film says:", s)
    s = re.sub(r"\b([Tt])(?:he|his) script\b(?! type)", lambda m: m.group(1) + "he film", s)
    m = re.search(r"quiz-ep(\d+)", f)
    if m and int(m.group(1)) in quiz_vid:
        vid = S1[quiz_vid[int(m.group(1))]]["id"]
        s = re.sub(r'(<a href=")' + re.escape(YT) + r'(">Watch the full)', r"\g<1>" + watch(vid) + r"\2", s)
    s = s.replace("</head>", FONT + QCSS + "\n</head>", 1)
    s = re.sub(r"<body([^>]*)>", lambda mm: f'<body class="k-quizpage" {QMARK}{mm.group(1)}>' + top("Quizzes") + '\n<div class="k-quiz">', s, count=1)
    s = s.replace("</body>", "</div>\n" + FOOT + "\n</body>", 1)
    open(f, "w", encoding="utf-8").write(s)
    return True


done = [f for f in glob.glob("tools/quiz-ep*.html") + ["tools/real-or-fake.html", "tools/real-or-fake/index.html"] if quiz_restyle(f)]

HEADER_RX = re.compile(r'<header class="k-top">.*?</header>', re.S)
section = lambda f: "Articles" if f.startswith("blog/") else ("Q&amp;A" if f.startswith("answers/") else "Quizzes")
hdr_done = 0
for f in sorted(set(glob.glob("blog/**/*.html", recursive=True) + glob.glob("answers/**/*.html", recursive=True) + glob.glob("tools/**/*.html", recursive=True))):
    s0 = open(f, encoding="utf-8").read()
    if not HEADER_RX.search(s0):
        continue
    s1 = HEADER_RX.sub(lambda m: top(section(f)), s0, count=1)
    if "/assets/site-nav.js" not in s1:
        s1 = s1.replace("</body>", '<script src="/assets/site-nav.js" defer></script>\n</body>', 1)
    if '<script>document.documentElement.classList.add("js")' not in s1 and "d.className+=' js'" not in s1:
        s1 = s1.replace("</head>", '<script>document.documentElement.classList.add("js")</script>\n</head>', 1)
    if s1 != s0:
        open(f, "w", encoding="utf-8").write(s1); hdr_done += 1
print("headers updated", hdr_done)
print("hubs: articles", len(arts), "· questions", len(qs), "· quizzes", len(quizzes), "· quiz pages restyled", len(done))
