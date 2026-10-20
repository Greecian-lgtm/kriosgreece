# Builds /films/, /sacred-days/ and /how-we-work/ from the data files. Run by build_home.py.
# No episode numbers, no season numbers. Film pages (/films/<slug>/) are not generated yet:
# they need director-approved content files (Gate C plan, Phase 5), so cards link to YouTube.
import os
from site_lib import (ROOT, EP, UP, S1, SUBJ, SD, e, watch, nice, short, weekday, card, s1card, upcoming_card,
                      featured, featured_film, calendar_entries, film_for_feast, sacred_films, ILLUSTRATION_NOTE, MONTHS)
from site_parts import head, header, footer, SCRIPTS, SUB

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


def page(path, title, desc, canonical, active, body, extra_js=""):
    write(path, f"""{head(title, desc, canonical)}
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
     "/films/", "Films", films_body, FILTER_JS)

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
  <section class="m-group"><h2 class="reveal">Related films and reading</h2><div class="m-grid m-grid--3">{related}</div></section>
</div>'''
page("sacred-days/index.html", "Sacred Days · KRIOS",
     "Sacred Days: Greek Orthodox feast days and name days, with KRIOS documentaries released on the day itself.",
     "/sacred-days/", "Sacred Days", sacred_body)

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
     "/how-we-work/", "", how_body)
print("films, sacred-days, how-we-work built")
