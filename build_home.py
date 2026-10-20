# Builds index.html for kriosgreece.com from data/episodes.json and data/upcoming.json,
# then the Films, Sacred Days and How we work pages (build_films.py) and the hubs (build_hubs.py).
# Run: python3 build_home.py   (the YouTube sync runs this after adding a new video)
import json, os, re, runpy
from site_lib import (EP, UP, S1, SUBJ, e, watch, thumb, nice, short, weekday, card, sacred_next,
                      DEDICATION_HTML, ILLUSTRATION_NOTE, MONTHS)
from site_parts import head, header, footer, SCRIPTS, YT, SUB

ROOT = os.path.dirname(os.path.abspath(__file__))
latest = EP[0]
recent = EP[1:4]                                    # the hero already features the newest film
n_films = len(EP) + len(S1)
n_lr = sum(1 for x in EP if x.get("label") == "Living Roots")

ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "Organization", "name": "KRIOS", "url": "https://kriosgreece.com", "sameAs": [YT],
     "description": "KRIOS: the living story of Greek civilization. Documentaries on Greek history, faith, tradition and family memory."},
    {"@type": "ItemList", "name": "KRIOS documentaries", "itemListElement": [
        {"@type": "ListItem", "position": k + 1, "item": {
            "@type": "VideoObject", "name": x["title"], "description": x["tease"],
            "thumbnailUrl": thumb(x["id"], "maxresdefault"), "uploadDate": x["date"], "url": watch(x["id"]),
            "embedUrl": f"https://www.youtube.com/embed/{x['id']}"}} for k, x in enumerate(EP)]}]}

# ---------- Sacred Days module: next scheduled special, or one released in the last 30 days ----------
state, sd = sacred_next()
sacred_html = ""
if sd:
    d = sd["date"]
    cal = f'<div class="m-cal" aria-hidden="true"><span>{MONTHS[int(d[5:7]) - 1][:3]}</span><b>{int(d[8:10])}</b></div>'
    if state == "upcoming":
        img = sd["image"]
        status = f'<p class="m-status"><span class="m-dot"></span>Premieres {weekday(d)}, {nice(d)} on YouTube</p>'
        links = (f'<a class="btn btn-navy" href="/sacred-days/">Sacred Days calendar</a>'
                 f'<a class="m-more" href="{SUB}" rel="noopener">Subscribe on YouTube to see it first →</a>')
        text = sd["text"]
        img_link = "/sacred-days/"
        note = f'<p class="m-imgnote">{ILLUSTRATION_NOTE}</p>' if sd.get("image_is_illustration") else ""
    else:
        img = thumb(sd["id"], "maxresdefault")
        status = f'<p class="m-status"><span class="m-dot"></span>Now on YouTube · {sd["mins"]} min</p>'
        links = (f'<a class="btn btn-navy" href="{watch(sd["id"])}" rel="noopener">Watch the film</a>'
                 f'<a class="m-more" href="/sacred-days/">All Sacred Days →</a>')
        text = sd.get("tease", "")
        img_link = watch(sd["id"])
        note = ""
    sacred_html = f'''<section class="m-sd" aria-label="Sacred Days">
  <div class="wrap"><div class="m-sd-in reveal">
    {cal}
    <div class="m-sd-body">
      <span class="label m-kick m-red">Sacred Days · Living traditions</span>
      <h2>{e(sd["title"])}</h2>
      <p>{e(text)}</p>
      {status}
      <div class="m-links">{links}</div>
    </div>
    <div><a class="m-sd-img" href="{img_link}"{' rel="noopener"' if img_link.startswith("http") else ""}><img src="{img}" alt="{e(sd["title"])}" width="960" height="540" loading="lazy"></a>{note}</div>
  </div></div>
</section>'''

chips = "".join(f'<a href="/films/#{k}">{e(SUBJ["names"][k])}</a>' for k in SUBJ["order"])
sd_entry = ("First film October 26 →" if state == "upcoming" and sd and sd["date"].endswith("-10-26")
            else (f'Next: {short(sd["date"])} →' if state == "upcoming" else "Feast days and name days →"))

page = f"""{head("KRIOS · The Living Story of Greek Civilization",
               "Documentaries on Greek history, faith, tradition and family memory, for Greeks in Greece and around the world. Real archives, sourced claims, and the stories families carried with them.",
               "/",
               '<meta name="google-site-verification" content="pPkMXZrBWp8jReHeeuMGoONMkFykv5Va8zj8RIYuHsk">\n'
               f'<meta property="og:image" content="{thumb(latest["id"], "maxresdefault")}">\n<meta name="twitter:card" content="summary_large_image">\n'
               f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>')}
<body>
{header()}

<main id="main">
<section class="hero">
  <div class="wrap">
    <div>
      <span class="label reveal" style="--d:.05s">Greek history, faith and family memory</span>
      <h1 class="reveal" style="--d:.15s">The living story of <em>Greek civilization</em></h1>
      <p class="lead reveal" style="--d:.28s">Documentaries for Greeks everywhere: the heroes, the customs, the music and the families who carried Greece with them. Real archives, sourced history, and the questions worth asking the people who raised you.</p>
      <div class="actions reveal" style="--d:.4s">
        <a class="btn btn-gold" href="{watch(latest['id'])}" rel="noopener">Watch the newest film</a>
        <a class="btn btn-line" href="/films/">All films</a>
      </div>
    </div>
    <a class="latest reveal" style="--d:.3s" href="{watch(latest['id'])}" rel="noopener">
      <span class="frame">
        <img src="{thumb(latest['id'], 'maxresdefault')}" onerror="this.onerror=null;this.src='{thumb(latest['id'])}'" alt="{e(latest['title'])}" width="1280" height="720">
        <span class="new label">New</span>
        <span class="play">▶ Watch · {latest['mins']} min</span>
      </span>
      <span class="body">
        <span class="meta label"><span>{e(latest['label'])}</span><span>{nice(latest['date'])}</span></span>
        <h2>{e(latest['title'])}</h2>
        <p>{e(latest['tease'])}</p>
      </span>
    </a>
  </div>
</section>

<div class="creed" aria-label="The KRIOS creed">
  <ol><li class="reveal" style="--d:0s">Preserve</li><li class="reveal" style="--d:.08s">Teach</li><li class="reveal" style="--d:.16s">Understand</li><li class="reveal" style="--d:.24s">Connect</li><li class="reveal" style="--d:.32s">Pass forward</li></ol>
</div>

<section class="m-begin" aria-labelledby="begin-h">
  <div class="wrap">
    <h2 id="begin-h" class="reveal">Where would you like to begin?</h2>
    <div class="m-entries">
      <a class="m-entry reveal" href="/films/#living-roots"><span class="m-gr" lang="el">Ρίζες</span><b>Living Roots</b><span>Family, migration and belonging.</span><i>{n_lr} films →</i></a>
      <a class="m-entry reveal" style="--d:.08s" href="/sacred-days/"><span class="m-gr" lang="el">Γιορτές</span><b>Sacred Days</b><span>Faith, customs and the traditions we carry forward.</span><i>{sd_entry}</i></a>
      <a class="m-entry reveal" style="--d:.16s" href="/films/#growing-up-greek"><span class="m-gr" lang="el">Θυμάμαι</span><b>Growing Up Greek</b><span>Childhood memories that connect generations.</span><i>New series · coming soon →</i></a>
    </div>
  </div>
</section>

{sacred_html}

<section class="band m-lib" id="films">
  <div class="wrap">
    <div class="m-head reveal"><div><span class="label m-kick">The documentaries</span><h2>Explore the films</h2></div><a class="m-more" href="/films/">View all {n_films} films →</a></div>
    <nav class="m-chips reveal" aria-label="Browse films by subject">{chips}</nav>
    <div class="m-grid m-grid--3">{"".join(card(x, i * .08) for i, x in enumerate(recent))}</div>
    <p class="m-all reveal"><a class="btn btn-navy" href="/films/">View all {n_films} films</a></p>
  </div>
</section>

<section class="band m-why" id="why">
  <div class="wrap">
    <span class="label m-kick reveal">Why KRIOS exists</span>
    <blockquote class="reveal">History tells us what happened.<br>KRIOS shows <em>why it still lives in us.</em></blockquote>
    <p class="m-why-text reveal">Each film follows one real story, from the past to a living family today, and lets the evidence show what was kept, what changed and what was lost.</p>
    <ol class="m-ladder">
      <li class="reveal"><span>1</span>"I never knew that."</li>
      <li class="reveal" style="--d:.1s"><span>2</span>"That's why my family does this."</li>
      <li class="reveal" style="--d:.2s"><span>3</span>"I want to ask my grandparents about this."</li>
      <li class="reveal" style="--d:.3s"><span>4</span>"I want my children to know this."</li>
    </ol>
    {DEDICATION_HTML}
  </div>
</section>

<section class="band m-support" id="how">
  <div class="wrap m-support-in">
    <div class="reveal"><span class="label m-kick">How we work</span><h2>Built on evidence, told by people</h2>
      <ul class="m-rules"><li><b>The oldest source, not the most famous.</b> Every historical claim is traced to a primary source or named scholarship.</li>
      <li><b>Real archives first.</b> Photographs, documents, icons and maps, credited with their licence.</li>
      <li><b>Illustration is labelled.</b> It never stands in for sacred or historical evidence.</li></ul>
      <a class="m-more" href="/how-we-work/">Read all six standards →</a></div>
    <div class="reveal" style="--d:.1s"><span class="label m-kick">Keep reading</span><h2>More from KRIOS</h2>
      <ul class="m-linklist"><li><a href="/blog/">Articles<span>The written companions to the films</span></a></li>
      <li><a href="/answers/">Q&amp;A<span>Questions about ancient Greece, answered</span></a></li>
      <li><a href="/tools/">Quizzes<span>Test what you know, including Real or Fake</span></a></li>
      <li><a href="/links.html">All links<span>YouTube and every KRIOS page</span></a></li></ul></div>
  </div>
</section>

<section class="ask">
  <div class="wrap">
    <h2 class="reveal">Who taught you yours?</h2>
    <p>Behind every Greek custom, recipe and dance is a place, a family and somebody who decided it was worth remembering. Ask them while you can.</p>
    <a class="btn btn-gold" href="{SUB}" rel="noopener">Subscribe on YouTube</a>
  </div>
</section>
</main>

{footer()}
{SCRIPTS}
</body>
</html>
"""
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(page)
for lp in ("links.html", "links/index.html"):
    p = os.path.join(ROOT, lp)
    t = open(p, encoding="utf-8").read()
    t = re.sub(r'<li><a class="hi" href="[^"]*" rel="noopener"><b>Newest: [^<]*</b>',
               f'<li><a class="hi" href="{watch(latest["id"])}" rel="noopener"><b>Newest: {e(latest["title"])}</b>', t)
    open(p, "w", encoding="utf-8").write(t)
print("index.html", len(page), "bytes;", len(EP), "episodes")

# Films, Sacred Days and How we work pages, then the Articles, Q&A and Quizzes hubs
runpy.run_path(os.path.join(ROOT, "build_films.py"))
runpy.run_path(os.path.join(ROOT, "build_hubs.py"))
