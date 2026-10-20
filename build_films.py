# Builds /films/, /sacred-days/ and /how-we-work/ from the data files. Run by build_home.py.
# No episode numbers, no season numbers. Film pages (/films/<slug>/) are not generated yet:
# they need director-approved content files (Gate C plan, Phase 5), so cards link to YouTube.
import json, os
from site_lib import (ROOT, EP, UP, S1, SUBJ, SD, e, watch, nice, short, weekday, card, s1card, upcoming_card,
                      featured, featured_film, calendar_entries, film_for_feast, sacred_films, ILLUSTRATION_NOTE, MONTHS)
from site_parts import head, header, footer, SCRIPTS, SUB, breadcrumbs

FILTER_JS = """<script>(function(){var c=[].slice.call(document.querySelectorAll('[data-f]'));if(!c.length)return;
var live=document.getElementById('f-status');
function go(f,announce){c.forEach(function(b){b.setAttribute('aria-pressed',b.dataset.f===f?'true':'false')});
var n=0;[].forEach.call(document.querySelectorAll('.m-films [data-tags]'),function(el){var ok=f==='all'||(' '+el.dataset.tags+' ').indexOf(' '+f+' ')>-1;el.hidden=!ok;if(ok){n++;el.classList.add('in')}});
[].forEach.call(document.querySelectorAll('.m-group'),function(g){g.hidden=!g.querySelector('[data-tags]:not([hidden])')});
[].forEach.call(document.querySelectorAll('[data-empty]'),function(x){x.hidden=x.dataset.empty!==f});
if(live&&announce)live.textContent=(f==='all'?'Showing all films':'Showing '+n+(n===1?' film':' films'));}
c.forEach(function(b){b.addEventListener('click',function(){go(b.dataset.f,true);history.replaceState(null,'','#'+b.dataset.f)})});
function fromHash(){var h=location.hash.slice(1);if(h&&c.some(function(b){return b.dataset.f===h}))go(h,false);}
fromHash();window.addEventListener('hashchange',fromHash);})();</script>"""


def write(path, html_text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(html_text)


def page(path, title, desc, canonical, active, body, extra_js="", image=None, ld=None):
    write(path, f"""{head(title, desc, canonical, image=image, ld=ld)}
<body>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
{SCRIPTS}
{extra_js}
</body>
</html>
""")


# ================= /films/ =================
FEAT = featured_film()
n_films = len(EP) + len(S1)
chips = '<button type="button" data-f="all" aria-pressed="true">All films</button>' + "".join(
    f'<button type="button" data-f="{k}" aria-pressed="false">{e(SUBJ["names"][k])}</button>' for k in SUBJ["order"])
groups = [("The living story", "Greek life as it is lived now, and how it survives.",
           [x for x in EP if x.get("season", 2) >= 3 and x["id"] != FEAT["id"]], [u for u in UP]),
          ("Heroes, heroines and forgotten history", "", [x for x in EP if x.get("season", 2) == 2 and x["id"] != FEAT["id"]], [])]
gh = ""
for title, sub, xs, ups in groups:
    if not xs and not ups:
        continue
    gh += (f'<section class="m-group"><h2 class="reveal">{title}</h2>{f"<p>{sub}</p>" if sub else ""}<div class="m-grid m-grid--3">'
           + "".join(upcoming_card(u) for u in ups) + "".join(card(x, (j % 3) * .06) for j, x in enumerate(xs)) + "</div></section>")
gh += ('<section class="m-group"><h2 class="reveal">Where KRIOS began</h2><p>The first films told the ancient stories.</p>'
       f'<div class="m-grid m-grid--5">{"".join(s1card(x) for x in S1)}</div></section>')
films_body = f'''<div class="wrap m-page">
  <header class="m-phead reveal"><span class="label m-kick">The documentaries</span><h1>Every KRIOS film</h1>
  <p>Greek history, faith, music and family memory. {n_films} films, newest first.</p></header>
  <div class="m-films">
  {featured(FEAT)}
  <nav class="m-chips m-chips--filter" aria-label="Filter films by subject">{chips}</nav>
  <p class="m-sr" id="f-status" aria-live="polite"></p>
  <div class="m-emptystate" data-empty="growing-up-greek" hidden><span class="m-gr" lang="el">Θυμάμαι</span><h2>Growing Up Greek</h2>
  <p>Childhood memories that connect generations. The things many of us remember: Sunday in church, the icon on the wall, Greek school after school. Stories that start with "I remember that" and lead to the history behind it.</p>
  <p class="m-status"><span class="m-dot m-dot--grey"></span>New series. No films yet. <a href="{SUB}" rel="noopener">Subscribe on YouTube</a> to see the first one.</p></div>
  {gh}
  </div>
</div>'''
page("films/index.html", "Films · KRIOS", f"Every KRIOS documentary: Greek history, faith, music and family memory. {n_films} films, newest first.",
     "/films/", "Films", films_body, FILTER_JS, ld=[breadcrumbs(("Films", "/films/"))])

# ================= /sacred-days/ =================
rows = ""
for f in calendar_entries():
    d = f["date"]
    tile = f'<div class="m-cal m-cal--sm" aria-hidden="true"><span>{MONTHS[int(d[5:7]) - 1][:3]}</span><b>{int(d[8:10])}</b></div>'
    when = (f"Feast day · {weekday(d)}, {nice(d)}" + (" · moveable feast" if f.get("moveable") else ""))
    st, film = film_for_feast(f)
    if st == "scheduled":
        status = f'<span class="m-status"><span class="m-dot"></span>KRIOS film premieres {short(film["date"])}</span>'
    elif st == "published":
        status = f'<a class="m-status" href="{watch(film["id"])}" rel="noopener"><span class="m-dot"></span>Watch the KRIOS film</a>'
    else:
        status = '<span class="m-status m-status--muted"><span class="m-dot m-dot--grey"></span>No KRIOS film scheduled</span>'
    rows += (f'<li class="reveal"><div class="m-feast">{tile}<span class="m-feast-body"><b>{e(f["en"])}</b> '
             f'<span lang="el">{e(f["el"])}</span><small>{when}</small></span>{status}</div></li>')

st, sd = None, None
up = next((u for u in UP if u.get("label") == "Sacred Days"), None)
if up:
    note = f'<p class="m-imgnote">{ILLUSTRATION_NOTE}</p>' if up.get("image_is_illustration") else ""
    feat_html = f'''<section class="m-sdfeat reveal"><div><span class="m-sd-img"><img src="{up["image"]}" alt="{e(up["title"])}" width="960" height="540"></span>{note}</div>
    <div><span class="label m-kick m-red">Next Sacred Days film</span><h2>{e(up["title"])}</h2><p>{e(up["text"])}</p>
    <p class="m-status"><span class="m-dot"></span>Premieres {weekday(up["date"])}, {nice(up["date"])} on YouTube</p>
    <a class="btn btn-navy" href="{SUB}" rel="noopener">Subscribe on YouTube to see it first</a></div></section>'''
elif sacred_films():
    x = sacred_films()[0]
    feat_html = f'<section class="m-sdfeat-wrap">{featured(x)}</section>'
else:
    feat_html = ""
published = sacred_films()
films_html = ('<div class="m-grid m-grid--3">' + "".join(card(x, (j % 3) * .06) for j, x in enumerate(published)) + "</div>" if published else
              '<div class="m-emptystate m-emptystate--inline reveal"><p>Saint Demetrios will be the first. Each new Sacred Days film appears here on its feast day.</p></div>')
faith = next((x for x in EP if x.get("label") == "Faith"), None)
related = (card(faith) if faith else "") + (
    '<a class="m-card m-card--text reveal" href="/blog/ep012-cryptochristians.html"><span class="m-cbody"><span class="label m-kick">Article</span>'
    "<span class=\"m-ctitle\">They Didn't Lose Their Faith. They Hid It Inside the Empire Trying to Erase It.</span>"
    '<span class="m-cta">Read the article →</span></span></a>')
GUIDES = json.load(open(os.path.join(ROOT, "data", "guides.json"), encoding="utf-8"))["guides"]
guide_cards = "".join(
    f'<a class="m-card m-card--text reveal" href="/{g["slug"]}/"><span class="m-cbody"><span class="label m-kick">{e(g["kicker"])}</span>'
    f'<span class="m-ctitle">{e(g["title"])}</span><span class="m-cta">Read →</span></span></a>' for g in GUIDES)
sacred_body = f'''<section class="m-sdhero"><div class="wrap">
  <span class="label m-kick m-gold reveal">Sacred Days · Living traditions</span>
  <h1 class="reveal">The days we remember</h1>
  <p class="reveal">Faith, customs and the traditions we carry forward. Feast days and name days, released on the day itself: what families celebrate, why their grandparents celebrated it, and how it differs from village to village and city to city.</p>
</div></section>
<div class="wrap m-page">
  {feat_html}
  <section class="m-calendar"><div class="m-head reveal"><div><span class="label m-kick">The year ahead</span><h2>Sacred Days calendar</h2></div></div>
    <p class="m-note-sm reveal">A curated selection of feast days. Each feast date is listed separately from any KRIOS film release.</p>
    <ol class="m-feasts">{rows}</ol>
    <p class="m-note-sm reveal">{e(SD["calendar_note"])}</p></section>
  <section class="m-group"><h2 class="reveal">Sacred Days films</h2>{films_html}</section>
  <section class="m-group"><h2 class="reveal">Name days and national days</h2><div class="m-grid m-grid--3">{guide_cards}</div></section>
  <section class="m-group"><h2 class="reveal">Related films and reading</h2><div class="m-grid m-grid--3">{related}</div></section>
</div>'''
page("sacred-days/index.html", "Sacred Days · KRIOS",
     "Sacred Days: Greek Orthodox feast days and name days, with KRIOS documentaries released on the day itself.",
     "/sacred-days/", "Sacred Days", sacred_body, ld=[breadcrumbs(("Sacred Days", "/sacred-days/"))])

# ================= /how-we-work/ =================
how_body = '''<section class="band method m-method-page" id="how">
  <div class="wrap">
    <div class="head reveal">
      <div><span class="label">How we work</span><h1 class="m-h1">Built on evidence, told by people</h1></div>
      <p>If a claim can't be traced to a source, it doesn't go in the film. When the evidence runs out, we say so.</p>
    </div>
    <ul class="rules reveal">
      <li><b>The oldest source, not the most famous</b><span>Primary sources and named scholarship for every historical claim, checked before recording and again on the finished film.</span></li>
      <li><b>Real archives first</b><span>Historical photographs, documents, icons and maps, credited with their licence. Low-resolution archives are shown as framed prints, never stretched or AI-enhanced.</span></li>
      <li><b>Illustration is labelled</b><span>Where no photograph exists, some everyday scenes are illustrated. They are marked on screen and never stand in for sacred or historical evidence.</span></li>
      <li><b>History, tradition and belief kept apart</b><span>We say which is which: what is documented, what the Church teaches, what families practice, and where communities differ.</span></li>
      <li><b>A human voice</b><span>Every documentary today is narrated in a human voice.</span></li>
      <li><b>English and Greek</b><span>New films get English and Greek captions reviewed by people, so the story reaches every generation of the family.</span></li>
    </ul>
  </div>
</section>'''
page("how-we-work/index.html", "How we work · KRIOS", "The KRIOS standards: sources, real archives, labelled illustration, and history, tradition and belief kept apart.",
     "/how-we-work/", "", how_body, ld=[breadcrumbs(("How we work", "/how-we-work/"))])
print("films, sacred-days, how-we-work built")

# ================= film pages (/films/<slug>/) =================
from site_lib import FILMS, EXTRAS, released, thumb, film_page_for, card as _card
_matches_ex = lambda t, x: x is not None and t['episode']['id'] == x['id']

LITE_JS = """<script>(function(){[].forEach.call(document.querySelectorAll('[data-yt]'),function(b){b.addEventListener('click',function(){
var f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+b.dataset.yt+'?autoplay=1&rel=0';f.title=b.dataset.title;
f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';f.allowFullscreen=true;f.className='m-video-frame';
b.replaceWith(f);f.focus();});});})();</script>"""


def related_html(rel, this_id):
    out = []
    for r in rel:
        if "id" in r:
            x = next((x for x in EP if x["id"] == r["id"]), None)
            if x and x["id"] != this_id:
                out.append(_card(x, len(out) * .06, True))
        elif "label" in r:
            x = next((x for x in EP if x.get("label") == r["label"] and x["id"] != this_id), None)
            if x:
                out.append(_card(x, len(out) * .06, True))
        elif "page" in r:
            out.append(f'<a class="m-card m-card--text reveal" href="{r["page"]}"><span class="m-cbody"><span class="label m-kick">{e(r["kick"])}</span>'
                       f'<span class="m-ctitle">{e(r["title"])}</span><span class="m-cta">{e(r["cta"])} →</span></span></a>')
    return "".join(out)


def sources_html(src, note=""):
    cols = []
    for key, head in (("established", "Established"), ("interpretation", "Interpretation"), ("open", "Still open")):
        items = src.get(key) or []
        if not items:
            continue
        lis = "".join(f'<li><p>{e(i["text"])}</p>' + (f'<small>{"<a href=" + chr(34) + i["url"] + chr(34) + " rel=" + chr(34) + "noopener" + chr(34) + ">" + e(i["cite"]) + "</a>" if i.get("url") else e(i.get("cite", ""))}</small>' if i.get("cite") else "") + "</li>" for i in items)
        cols.append(f'<div><h3>{head}</h3><ul>{lis}</ul></div>')
    return f'<div class="m-src">{"".join(cols)}</div>' + (f'<p class="m-note-sm">{e(note)}</p>' if note else "")


for f in FILMS:
    x = released(f["match"])
    up = None if x else next((u for u in UP if f["match"].get("title", "\0").lower() in u["title"].lower()), None)
    if not x and not up:
        continue
    base = x or up
    title = base["title"]
    held = bool(f.get("held_until_release") and not x)
    if x:
        meta = f'{nice(x["date"])} · {x["mins"]} min'
        intro = x.get("tease", "")
        cta = f'<a class="btn btn-gold" href="{watch(x["id"])}" rel="noopener">Watch on YouTube</a>'
        video = (f'<button class="m-video" type="button" data-yt="{x["id"]}" data-title="{e(title)}" aria-label="Play {e(title)}">'
                 f'<img src="{thumb(x["id"], "maxresdefault")}" onerror="this.onerror=null;this.src=\'{thumb(x["id"])}\'" alt="" width="960" height="540">'
                 '<span class="m-bigplay" aria-hidden="true">▶</span></button><p class="m-vnote">The video loads from YouTube only when you press play.</p>')
    else:
        meta = f'Premieres {weekday(up["date"])}, {nice(up["date"])} on YouTube'
        intro = up.get("text", "")
        cta = f'<a class="btn btn-gold" href="{SUB}" rel="noopener">Subscribe on YouTube to see it first</a>'
        note = f'<p class="m-vnote">{ILLUSTRATION_NOTE}</p>' if up.get("image_is_illustration") else ""
        video = f'<div class="m-video m-video--soon"><img src="{up["image"]}" alt="" width="960" height="540"><span class="m-soon">Premieres {short(up["date"])}</span></div>{note}'
    hero_img = f.get("hero_image")
    right = (f'<figure class="m-herofig"><img src="{hero_img["src"]}" alt="{e(hero_img["alt"])}" width="1280" height="720"><figcaption>{e(hero_img["caption"])}</figcaption></figure>'
             if hero_img else video)
    secs = []
    if held:
        secs.append(("story", "The story", '<div class="m-held"><b>Opens with the film on its premiere day.</b> The story, sources and credits are published when the film is public, so nothing appears before it.</div>'))
    else:
        if f.get("opening"):
            secs.append(("opening", "", '<div class="m-opening">' + "".join(f"<p>{e(t)}</p>" for t in f["opening"]["text"]) + "</div>"))
        if hero_img and x:
            secs.append(("watch", "Watch the film", video))
        if f.get("story"):
            secs.append(("story", "The story", "".join(f"<p>{e(t)}</p>" for t in f["story"]) + f'<p class="m-note-sm">{e(f.get("story_from", ""))}</p>'))
    if not held and f.get("read"):
        words = sum(len(p_.split()) for s_ in f["read"] for p_ in s_["p"])
        inner = "".join(f'<h3>{e(s_["h"])}</h3>' + "".join(f"<p>{e(p_)}</p>" for p_ in s_["p"]) for s_ in f["read"])
        secs.append(("read", "Read the film", f'<p>The full narration, for anyone who would rather read, or wants to find a line again. '
                     f'About {words:,} words, {max(1, round(words / 230))} minutes to read.</p>'
                     f'<details class="m-read"><summary>Read the full narration</summary><div class="m-read-body">{inner}'
                     f'<p class="m-note-sm">{e(f.get("read_from", ""))}</p></div></details>'))
    if f.get("family_questions"):
        secs.append(("family", "Ask someone in your family", '<p>Questions to start a conversation at your own table.</p><ul class="m-askqs">'
                     + "".join(f"<li>{e(q)}</li>" for q in f["family_questions"]) + "</ul>"))
    if not held and f.get("sources"):
        secs.append(("sources", "What the sources tell us", sources_html(f["sources"], f.get("sources_note", ""))))
    if not held and (f.get("credits") or f.get("credits_link")):
        link = f'<p><a class="btn btn-navy" href="{f["credits_link"]}">Full image credits</a></p>' if f.get("credits_link") else ""
        secs.append(("credits", "Historical images and credits", "".join(f"<p>{e(t)}</p>" for t in f.get("credits", [])) + link))
    if held:
        secs.append(("credits", "Historical images and credits", '<div class="m-held"><b>Full per-image credits publish with the film.</b></div>'))
    ex = next((t for t in EXTRAS if _matches_ex(t, x)), None) if x else None
    if ex:
        more = f'<p><a class="m-more" href="/tools/quiz-{ex["quiz"]["slug"]}.html">Take the quiz on this film →</a></p>'
        secs.append(("quiz", "Test what you remember", more))
    toc = "".join(f'<a href="#{k}">{h}</a>' for k, h, _ in secs if h)
    body = f'''<section class="m-filmhero"><div class="wrap m-filmhero-in">
  <div class="reveal"><span class="label m-kick m-gold">{e(f["kicker"])}</span><h1>{e(title)}</h1>
    <p class="m-filmmeta">{meta}</p><p class="m-filmintro">{e(intro)}</p>{cta}</div>
  <div class="reveal" style="--d:.1s">{right}</div>
</div></section>
<div class="wrap m-page m-film">
  <nav class="m-toc reveal" aria-label="On this page">{toc}</nav>
  {"".join(f'<section class="m-fsec reveal" id="{k}">' + (f"<h2>{h}</h2>" if h else "") + f"{c}</section>" for k, h, c in secs)}
  <section class="m-fsec reveal" id="more"><h2>Continue exploring</h2><div class="m-grid m-grid--3">{related_html(f.get("related", []), (x or {}).get("id"))}</div></section>
</div>'''
    film_ld = [breadcrumbs(("Films", "/films/"), (title, f"/films/{f['slug']}/"))]
    if x:
        film_ld.append({"@context": "https://schema.org", "@type": "VideoObject", "name": title,
                        "description": intro or title, "thumbnailUrl": [thumb(x["id"], "maxresdefault"), thumb(x["id"])],
                        "uploadDate": x["date"], "embedUrl": f"https://www.youtube.com/embed/{x['id']}",
                        "url": watch(x["id"]), "inLanguage": "en",
                        "publisher": {"@type": "Organization", "name": "KRIOS", "url": "https://kriosgreece.com/"}})
    share_img = (hero_img["src"] if hero_img else (thumb(x["id"], "maxresdefault") if x else up["image"]))
    page(f"films/{f['slug']}/index.html", f"{title} · KRIOS", intro or title, f"/films/{f['slug']}/", "Films", body, LITE_JS,
         image=share_img, ld=film_ld)
print("film pages:", [f["slug"] for f in FILMS])

# ================= quizzes and Q&A for the newer films =================
QUIZ_JS = """<script>(function(){
var Q=JSON.parse(document.getElementById('quiz-data').textContent),box=document.getElementById('quiz'),res=document.getElementById('quiz-result'),i=0,score=0;
function esc(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML;}
function show(){if(i>=Q.length){box.hidden=true;res.hidden=false;document.getElementById('quiz-score').textContent=score+' out of '+Q.length;res.querySelector('h2').focus();return;}
var q=Q[i];box.innerHTML='<p class="m-qnum">Question '+(i+1)+' of '+Q.length+'</p><h2 tabindex="-1">'+esc(q.q)+'</h2><div class="m-opts">'+q.options.map(function(o,k){return '<button type="button" data-k="'+k+'">'+esc(o)+'</button>'}).join('')+'</div><p class="m-explain" aria-live="polite"></p><button type="button" class="btn btn-navy m-next" hidden>'+(i+1<Q.length?'Next question':'See your score')+'</button>';
box.querySelector('h2').focus();
[].forEach.call(box.querySelectorAll('.m-opts button'),function(b){b.addEventListener('click',function(){var k=+b.dataset.k,ok=k===q.correct;if(ok)score++;
[].forEach.call(box.querySelectorAll('.m-opts button'),function(x){x.disabled=true;var kk=+x.dataset.k;if(kk===q.correct){x.classList.add('ok');x.insertAdjacentHTML('beforeend',' <span class="m-tag">Correct answer</span>')}else if(kk===k){x.classList.add('no');x.insertAdjacentHTML('beforeend',' <span class="m-tag">Your answer</span>')}});
box.querySelector('.m-explain').innerHTML='<b>'+(ok?'That\\'s right. ':'Not quite. ')+'</b>'+esc(q.explain);var n=box.querySelector('.m-next');n.hidden=false;n.focus();
n.addEventListener('click',function(){i++;show();});});});}
document.getElementById('quiz-again').addEventListener('click',function(){i=0;score=0;res.hidden=true;box.hidden=false;show();});
show();})();</script>"""

import json as _json
for t in EXTRAS:
    x = t["episode"]
    fp = film_page_for(x)
    q = t["quiz"]
    data = [{"q": a["q"], "options": a["options"], "correct": a["correct"], "explain": a["explain"]} for a in q["questions"]]
    body = f'''<div class="wrap m-page m-narrow">
  <nav class="m-crumbs" aria-label="Breadcrumb"><a href="/tools/">Quizzes</a> › {e(x["title"])}</nav>
  <header class="m-phead reveal"><span class="label m-kick">Quiz · {e(x["label"])}</span><h1>{e(q["title"])}</h1><p>{e(q["intro"])}</p></header>
  <div id="quiz" class="m-quiz"><noscript><p>This quiz needs JavaScript. You can <a href="{fp or watch(x["id"])}">read about the film</a> instead.</p></noscript></div>
  <div id="quiz-result" class="m-quiz-result" hidden><h2 tabindex="-1">Your score: <span id="quiz-score"></span></h2>
    <p>Every answer comes from the film. Watch it again, then ask someone in your family what they remember.</p>
    <p class="m-links"><a class="btn btn-gold" href="{watch(x["id"])}" rel="noopener">Watch the film</a>{f'<a class="m-more" href="{fp}">About the film →</a>' if fp else ""}<button type="button" class="btn btn-navy" id="quiz-again">Try again</button></p></div>
  <script type="application/json" id="quiz-data">{_json.dumps(data, ensure_ascii=False).replace("</", "<\\/")}</script>
</div>'''
    page(f"tools/quiz-{q['slug']}.html", f"Quiz: {x['title']} · KRIOS", q["intro"], f"/tools/quiz-{q['slug']}.html", "Quizzes", body, QUIZ_JS,
         image=thumb(x["id"], "maxresdefault"), ld=[breadcrumbs(("Quizzes", "/tools/"), (q["title"], f"/tools/quiz-{q['slug']}.html"))])
    for a in t.get("qa", []):
        src = "".join(f'<li><a href="{s["url"]}" rel="noopener">{e(s["cite"])}</a></li>' for s in a.get("sources", []))
        body = f'''<div class="wrap m-page m-narrow">
  <nav class="m-crumbs" aria-label="Breadcrumb"><a href="/answers/">Q&amp;A</a> › {e(x["title"])}</nav>
  <article class="reveal"><span class="label m-kick">Q&amp;A · {e(x["label"])}</span><h1 class="m-qa-h1">{e(a["title"])}</h1>
  {"".join(f"<p>{e(t2)}</p>" for t2 in a["answer"])}
  {f'<h2 class="m-qa-h2">Sources</h2><ul class="m-srclist">{src}</ul>' if src else '<p class="m-note-sm">Drawn from the KRIOS film and its research notes.</p>'}
  <div class="k-note m-qa-film"><b>From the film</b> <a href="{fp or watch(x["id"])}">{e(x["title"])}</a>{f' · <a href="/tools/quiz-{q["slug"]}.html">Take the quiz</a>'}</div>
  </article>
</div>'''
        qa_ld = [breadcrumbs(("Q&A", "/answers/"), (a["title"], f"/answers/{a['slug']}/")),
                 {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": a["title"],
                  "acceptedAnswer": {"@type": "Answer", "text": " ".join(a["answer"])}}]}]
        page(f"answers/{a['slug']}/index.html", f"{a['title']} · KRIOS", a["answer"][0][:155], f"/answers/{a['slug']}/", "Q&amp;A", body,
             image=thumb(x["id"], "maxresdefault"), ld=qa_ld)
print("quizzes and Q&A for newer films:", [t["quiz"]["slug"] for t in EXTRAS])


# ================= guides: name days and national days (data/guides.json) =================
for g in GUIDES:
    feast = next((f for f in SD["feasts"] if f["key"] == g.get("feast_key")), None)
    x = released({"title": g["film_match"]}) if g.get("film_match") else None
    up = None if x or not g.get("film_match") else next((u for u in UP if g["film_match"].lower() in u["title"].lower()), None)
    when = f'<p class="m-filmmeta">This year: {weekday(feast["date"])}, {nice(feast["date"])}</p>' if feast else ""
    secs = "".join(f'<section class="m-fsec reveal"><h2>{e(s["h"])}</h2>' + "".join(f"<p>{e(p_)}</p>" for p_ in s["p"]) + "</section>" for s in g["sections"])
    film = ""
    if x:
        film = (f'<section class="m-fsec reveal"><h2>The KRIOS film</h2><p><b>{e(x["title"])}</b>. {e(x.get("tease", ""))}</p>'
                f'<p class="m-links"><a class="btn btn-gold" href="{watch(x["id"])}" rel="noopener">Watch on YouTube</a>'
                + (f' <a class="m-more" href="/films/{g["film_slug"]}/">About the film →</a>' if g.get("film_slug") else "") + "</p></section>")
    elif up:
        film = (f'<section class="m-fsec reveal"><h2>The KRIOS film</h2><p><b>{e(up["title"])}</b> premieres on YouTube on '
                f'{weekday(up["date"])}, {nice(up["date"])}, the feast day.</p><p class="m-links"><a class="btn btn-gold" href="{SUB}" rel="noopener">Subscribe to see it first</a>'
                + (f' <a class="m-more" href="/films/{g["film_slug"]}/">About the film →</a>' if g.get("film_slug") else "") + "</p></section>")
    else:
        film = (f'<section class="m-fsec reveal"><h2>Watch KRIOS</h2><p>Documentaries on Greek history, faith and family memory.</p>'
                f'<p class="m-links"><a class="btn btn-gold" href="/films/">Browse the films</a> <a class="m-more" href="{SUB}" rel="noopener">Subscribe on YouTube →</a></p></section>')
    ask = '<section class="m-fsec reveal"><h2>Ask someone in your family</h2><ul class="m-askqs">' + "".join(f"<li>{e(q)}</li>" for q in g["ask"]) + "</ul></section>"
    src = '<section class="m-fsec reveal"><h2>Sources</h2><ul class="m-srclist">' + "".join(
        f'<li><a href="{s["url"]}" rel="noopener">{e(s["cite"])}</a></li>' for s in g["sources"]) + "</ul></section>"
    crumb_name, crumb_url = ("Sacred Days", "/sacred-days/")
    body = f'''<div class="wrap m-page m-narrow">
  <nav class="m-crumbs" aria-label="Breadcrumb"><a href="{crumb_url}">{crumb_name}</a> › {e(g["title"])}</nav>
  <header class="m-phead reveal"><span class="label m-kick">{e(g["kicker"])}</span><h1>{e(g["title"])}</h1>{when}<p class="m-filmintro">{e(g["lead"])}</p></header>
  {secs}{film}{ask}{src}
</div>'''
    ld = [breadcrumbs((crumb_name, crumb_url), (g["title"], f"/{g['slug']}/")),
          {"@context": "https://schema.org", "@type": "Article", "headline": g["seo_title"], "description": g["desc"],
           "mainEntityOfPage": f"https://kriosgreece.com/{g['slug']}/", "publisher": {"@type": "Organization", "name": "KRIOS", "url": "https://kriosgreece.com/"}}]
    page(f"{g['slug']}/index.html", f"{g['seo_title']} · KRIOS", g["desc"], f"/{g['slug']}/", "Sacred Days", body, ld=ld)
print("guides:", [g["slug"] for g in GUIDES])
