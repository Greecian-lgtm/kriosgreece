# Builds index.html for kriosgreece.com from the episode data below.
# Run: python3 build_home.py  (writes index.html in this folder)
import html, json

EP = [  # newest first; titles as published on YouTube
 dict(n=21, id="vpQUH4lBkiU", date="2026-10-18", mins=9, label="Living Roots",
      title="The Greeks Who Left, and the Greece They Carried",
      tease="A suitcase can carry clothes and photographs. How do you pack a language, a song, or a church bell?"),
 dict(n=20, id="8cu1S1DVFDI", date="2026-10-11", mins=11, label="Living Roots",
      title="The Greek Dance That Wasn't Real… Until It Was",
      tease="Sirtaki was created for a film. So what makes a tradition real, and who keeps it alive?"),
 dict(n=19, id="5YvEvk2wy7Q", date="2026-07-29", mins=10, label="Music & memory",
      title="The Man Who Smuggled a Puppet Out of a Dictatorship",
      tease="You've heard the song. You've never heard the man."),
 dict(n=18, id="uzqERcTIqS0", date="2026-07-22", mins=13, label="Diaspora",
      title="Why a Greek Sponge Diver Built a Town in Florida",
      tease="How divers from the Aegean turned Tarpon Springs into a Greek town."),
 dict(n=17, id="EeUEsp4CVj4", date="2026-07-15", mins=10, label="Family table",
      title="I Ate This My Whole Childhood and Never Knew the Real Reason",
      tease="The spoon sweet, served to every guest at a Greek door, was never just dessert."),
 dict(n=16, id="WL4yl8BZEI8", date="2026-07-09", mins=9, label="Occupation",
      title="The Neutral Country That Broke a Blockade to Save Greece",
      tease="The famine under Axis occupation, and the neutral country whose ships broke the blockade."),
 dict(n=15, id="YPfrT9-Eblg", date="2026-07-03", mins=10, label="Heroines",
      title="Why Did Greece Forget the Greek Woman Who Bought Their Freedom?",
      tease="Manto Mavrogenous spent her fortune on the Revolution and was never repaid."),
 dict(n=14, id="WSqxEWNQW24", date="2026-06-18", mins=12, label="Music",
      title="The Music Your Greek Family Played at Every Party Was Illegal",
      tease="Rebetiko: the music the state tried to silence, and the families who kept playing it."),
 dict(n=13, id="8_RRyIg5Fko", date="2026-06-04", mins=12, label="Heroines",
      title="The Greek Captain Who Built Her Own Warship to Fight the Empire That Took Everything",
      tease="Laskarina Bouboulina, who paid for her own warships in the Revolution of 1821."),
 dict(n=12, id="s8dG4GvwRDs", date="2026-05-28", mins=13, label="Faith",
      title="The Greek Christians Who Hid Their Faith Inside the Ottoman Empire for 400 Years",
      tease="Families who kept their Orthodox faith hidden for generations under Ottoman rule."),
 dict(n=11, id="GeJD0oIcMEk", date="2026-05-01", mins=9, label="Heroes",
      title="The Greek Soldier Who Chose to Die at Thermopylae Rather Than Surrender to Persia",
      tease="Thermopylae, 1821: the second monument at the pass, and the soldier it remembers."),
]
S1 = [  # where KRIOS began (Season 1)
 ("Achilles", "rsNL4YMtjxY"), ("Odysseus", "R7WPPD-F9ts"), ("Thermopylae", "J6J9-ylN0rI"),
 ("Heracles", "cWglqxd8yTQ"), ("Perseus", "ErdjhcEI9P0"), ("Troy", "2rg3tPOXz9Y"),
 ("Theseus", "I8Yc6TAlIag"), ("The Cyclades", "f1Jh8yihNBQ"), ("Parian marble", "HwOjU-CLHag"),
 ("The Acropolis", "jmwkiQRkoxU"),
]
YT = "https://www.youtube.com/@KriosGreece"
SUB = "https://www.youtube.com/@KriosGreece?sub_confirmation=1"
MONTHS = "January February March April May June July August September October November December".split()

def watch(i): return f"https://www.youtube.com/watch?v={i}"
def thumb(i, q="maxresdefault"): return f"https://i.ytimg.com/vi/{i}/{q}.jpg"
def nice(d):
    y, m, dd = d.split("-"); return f"{MONTHS[int(m)-1][:3]} {int(dd)}, {y}"
e = html.escape

latest, rest = EP[0], EP[1:]

def card_list(xs): return "\n".join(f"""
      <li class="ep">
        <a class="ep-link" href="{watch(x['id'])}" rel="noopener">
          <span class="ep-img"><img src="{thumb(x['id'],'hqdefault')}" alt="" loading="lazy" width="480" height="360"></span>
          <span class="ep-meta"><span class="ep-num">S{3 if x['n']>=20 else 2} · EP{x['n']:03d}</span><span>{e(x['label'])}</span><span>{x['mins']} min</span></span>
          <span class="ep-title">{e(x['title'])}</span>
          <span class="ep-tease">{e(x['tease'])}</span>
        </a>
      </li>""" for x in xs)
s3 = card_list([x for x in EP if x['n'] >= 20])
s2 = card_list([x for x in rest if x['n'] < 20])

s1 = "\n".join(f'<li><a href="{watch(i)}" rel="noopener">{e(t)}</a></li>' for t, i in S1)

ld = {
  "@context": "https://schema.org",
  "@graph": [
    {"@type": "Organization", "name": "KRIOS", "url": "https://kriosgreece.com",
     "sameAs": [YT], "description": "KRIOS: the living story of Greek civilization. Documentaries on Greek history, faith, tradition and family memory."},
    {"@type": "ItemList", "name": "KRIOS documentaries", "itemListElement": [
      {"@type": "ListItem", "position": k+1, "item": {
        "@type": "VideoObject", "name": x["title"], "description": x["tease"],
        "thumbnailUrl": thumb(x["id"]), "uploadDate": x["date"], "url": watch(x["id"]),
        "embedUrl": f"https://www.youtube.com/embed/{x['id']}"}} for k, x in enumerate(EP)]},
  ]}

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="google-site-verification" content="pPkMXZrBWp8jReHeeuMGoONMkFykv5Va8zj8RIYuHsk">
<title>KRIOS · The Living Story of Greek Civilization</title>
<meta name="description" content="Documentaries on Greek history, faith, tradition and family memory, for Greeks in Greece and around the world. Real archives, sourced claims, and the stories families carried with them.">
<link rel="canonical" href="https://kriosgreece.com/">
<meta property="og:type" content="website">
<meta property="og:title" content="KRIOS · The Living Story of Greek Civilization">
<meta property="og:description" content="Documentaries on Greek history, faith, tradition and family memory. Newest: {e(latest['title'])}.">
<meta property="og:url" content="https://kriosgreece.com/">
<meta property="og:image" content="{thumb(latest['id'])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#14213a">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>
:root {{
  --blue-900:#101a2e; --blue-800:#14213a; --blue-700:#1c2d4d; --blue-500:#3a5a8c;
  --ivory:#f5edd8; --ivory-2:#ebe1c7; --paper:#faf6ec;
  --gold:#c9a35e; --gold-ink:#8a6a2c; --red:#7e2418;
  --ink:#1d1a14; --ink-2:#4a4336; --line:#d9cdb0;
  --serif:"EB Garamond", Georgia, "Times New Roman", serif;
  --w:1160px;
}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
@media (prefers-reduced-motion: reduce){{html{{scroll-behavior:auto}} *{{transition:none!important}}}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--serif);font-size:19px;line-height:1.55;-webkit-font-smoothing:antialiased}}
img{{max-width:100%;display:block}}
a{{color:inherit}}
:focus-visible{{outline:2px solid var(--gold);outline-offset:3px}}
.wrap{{max-width:var(--w);margin:0 auto;padding:0 24px}}
.label{{font-size:.78rem;letter-spacing:.18em;text-transform:uppercase;font-weight:500}}
.skip{{position:absolute;left:-9999px}} .skip:focus{{left:16px;top:16px;background:var(--ivory);padding:8px 12px;z-index:10}}

/* header */
.top{{background:var(--blue-900);color:var(--ivory);border-bottom:1px solid #2a3a5c}}
.top .wrap{{display:flex;align-items:center;justify-content:space-between;gap:24px;min-height:68px}}
.brand{{text-decoration:none;display:flex;align-items:baseline;gap:12px}}
.brand b{{font-weight:600;letter-spacing:.22em;font-size:1.25rem}}
.brand span{{color:var(--gold);font-style:italic;font-size:.95rem}}
.nav{{display:flex;gap:22px;align-items:center;flex-wrap:wrap}}
.nav a{{text-decoration:none;font-size:.95rem;opacity:.88}} .nav a:hover{{opacity:1;color:var(--gold)}}
.btn{{display:inline-flex;align-items:center;gap:.5em;min-height:46px;padding:10px 20px;border-radius:2px;text-decoration:none;font-size:1rem;font-weight:500;transition:background .2s,color .2s}}
.btn-gold{{background:var(--gold);color:var(--blue-900)}} .btn-gold:hover{{background:#d9b674}}
.btn-line{{border:1px solid rgba(245,237,216,.5);color:var(--ivory)}} .btn-line:hover{{border-color:var(--gold);color:var(--gold)}}
.nav .btn{{min-height:40px;padding:6px 14px;opacity:1}}

/* hero */
.hero{{background:linear-gradient(180deg,var(--blue-900),var(--blue-800));color:var(--ivory);padding:72px 0 88px;border-bottom:3px solid var(--red)}}
.hero .wrap{{display:grid;grid-template-columns:1.05fr 1fr;gap:56px;align-items:center}}
.hero .label{{color:var(--gold)}}
.hero h1{{font-weight:500;font-size:clamp(2.6rem,5.2vw,4.4rem);line-height:1.03;margin:.35em 0 .4em;letter-spacing:-.01em}}
.hero h1 em{{color:var(--gold);font-style:italic}}
.hero p.lead{{font-size:1.2rem;max-width:34em;color:#e9dfc6;margin:0 0 28px}}
.actions{{display:flex;gap:14px;flex-wrap:wrap}}
.latest{{text-decoration:none;display:block;background:var(--blue-700);border:1px solid #33476e;transition:border-color .2s}}
.latest:hover{{border-color:var(--gold)}}
.latest .frame{{display:block;position:relative;aspect-ratio:16/9;background:#0b1322;overflow:hidden}}
.latest .frame img{{width:100%;height:100%;object-fit:cover}}
.latest .new{{position:absolute;left:14px;top:14px;background:var(--red);color:var(--ivory);padding:4px 10px}}
.latest .play{{position:absolute;right:14px;bottom:14px;background:rgba(16,26,46,.86);color:var(--ivory);padding:6px 12px;font-size:.95rem}}
.latest .body{{display:block;padding:20px 22px 22px}}
.latest .meta{{color:var(--gold);display:flex;gap:14px;flex-wrap:wrap}}
.latest h2{{font-weight:500;font-size:1.65rem;line-height:1.15;margin:.35em 0 .3em}}
.latest p{{margin:0;color:#d9cfb6}}

/* creed */
.creed{{background:var(--ivory);border-bottom:1px solid var(--line)}}
.creed ol{{list-style:none;margin:0 auto;padding:22px 24px;max-width:var(--w);display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}}
.creed li{{font-size:1.15rem;letter-spacing:.06em;color:var(--blue-800)}}
.creed li::before{{content:"";display:inline-block;width:7px;height:7px;background:var(--gold);transform:rotate(45deg);margin-right:12px;vertical-align:middle}}

/* sections */
section.band{{padding:84px 0}}
.head{{display:flex;justify-content:space-between;align-items:end;gap:24px;margin-bottom:36px;flex-wrap:wrap}}
.head h2{{font-weight:500;font-size:clamp(2rem,3.4vw,2.8rem);line-height:1.08;margin:.2em 0 0;max-width:18em}}
.head .label{{color:var(--gold-ink)}}
.head p{{max-width:30em;margin:0;color:var(--ink-2)}}
.more{{text-decoration:none;border-bottom:1px solid var(--gold);padding-bottom:2px;white-space:nowrap}}

/* why */
.why .wrap{{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:start}}
.why blockquote{{margin:0;font-size:clamp(1.6rem,2.6vw,2.15rem);line-height:1.25;color:var(--blue-800)}}
.why blockquote em{{color:var(--red);font-style:italic}}
.why .text p{{margin:0 0 1em}}
.why .ladder{{list-style:none;padding:0;margin:24px 0 0;border-left:2px solid var(--gold)}}
.why .ladder li{{padding:6px 0 6px 18px;color:var(--ink-2)}}
.why .ladder li:last-child{{color:var(--ink);font-weight:500}}

/* episodes */
.eps{{background:var(--ivory)}}
.grid{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:34px 28px}}
.ep-link{{text-decoration:none;display:flex;flex-direction:column;gap:10px;height:100%}}
.ep-img{{aspect-ratio:16/9;overflow:hidden;background:var(--blue-800);display:block}}
.ep-img img{{width:100%;height:100%;object-fit:cover;transition:transform .3s}}
.ep-link:hover .ep-img img{{transform:scale(1.03)}}
.ep-link:hover .ep-title{{color:var(--red)}}
.ep-meta{{display:flex;gap:12px;font-size:.8rem;letter-spacing:.12em;text-transform:uppercase;color:var(--gold-ink)}}
.ep-num{{color:var(--blue-800);font-weight:600}}
.ep-title{{font-size:1.3rem;line-height:1.2;font-weight:500;transition:color .2s}}
.ep-tease{{color:var(--ink-2);font-size:1rem}}
.season{{font-weight:500;font-size:1.45rem;margin:8px 0 18px;padding-top:22px;border-top:1px solid var(--line);color:var(--blue-800)}}
.season span{{font-size:.8rem;letter-spacing:.14em;text-transform:uppercase;color:var(--gold-ink);margin-left:12px}}
.season-note{{margin:-8px 0 22px;color:var(--ink-2);max-width:40em}}
.grid + .season{{margin-top:48px}}
.began{{margin-top:56px;padding-top:28px;border-top:1px solid var(--line);display:grid;grid-template-columns:260px 1fr;gap:28px}}
.began h3{{font-weight:500;font-size:1.35rem;margin:.2em 0 .3em}}
.began p{{margin:0;color:var(--ink-2);font-size:1rem}}
.began ul{{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:10px}}
.began li a{{display:inline-block;padding:8px 14px;border:1px solid var(--line);text-decoration:none;font-size:1rem;min-height:44px;line-height:26px}}
.began li a:hover{{border-color:var(--gold);color:var(--red)}}

/* series */
.series .cols{{display:grid;grid-template-columns:repeat(3,1fr);gap:0;border-top:1px solid var(--line)}}
.series article{{padding:30px 28px 8px 0;border-right:1px solid var(--line);margin-right:28px}}
.series article:last-child{{border-right:0;margin-right:0}}
.series h3{{font-weight:500;font-size:1.55rem;margin:.3em 0 .4em;line-height:1.15}}
.series .gr{{color:var(--red);font-style:italic;font-size:1.05rem}}
.series p{{color:var(--ink-2);margin:0 0 1em}}

/* method */
.method{{background:var(--blue-800);color:var(--ivory)}}
.method .head .label{{color:var(--gold)}} .method .head p{{color:#d9cfb6}}
.rules{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:0}}
.rules li{{padding:26px 26px 26px 0;border-top:1px solid #33476e}}
.rules b{{display:block;font-weight:500;font-size:1.2rem;color:var(--gold);margin-bottom:6px}}
.rules span{{color:#e3d9bf;font-size:1rem}}

/* explore */
.explore .links{{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}}
.explore a.tile{{display:block;padding:24px;border:1px solid var(--line);text-decoration:none;background:#fffdf7;min-height:150px}}
.explore a.tile:hover{{border-color:var(--gold)}}
.explore a.tile b{{display:block;font-weight:500;font-size:1.25rem;margin-bottom:6px}}
.explore a.tile span{{color:var(--ink-2);font-size:1rem}}

/* ask */
.ask{{background:var(--ivory-2);text-align:center;padding:96px 0}}
.ask h2{{font-weight:500;font-style:italic;font-size:clamp(2.2rem,4.4vw,3.6rem);margin:0 0 .3em;color:var(--blue-800)}}
.ask p{{max-width:34em;margin:0 auto 28px;color:var(--ink-2);font-size:1.15rem}}
.ask .btn-gold{{background:var(--blue-800);color:var(--ivory)}} .ask .btn-gold:hover{{background:var(--red)}}

/* footer */
footer{{background:var(--blue-900);color:#cfc5ab;padding:56px 0 40px;font-size:.98rem}}
footer .wrap{{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:40px}}
footer b{{color:var(--ivory);letter-spacing:.2em;font-weight:600}}
footer ul{{list-style:none;padding:0;margin:0;display:grid;gap:8px}}
footer a{{text-decoration:none}} footer a:hover{{color:var(--gold)}}
.dedic{{grid-column:1/-1;border-top:1px solid #2a3a5c;padding-top:24px;display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap}}
.dedic i{{color:var(--ivory)}}

@media (max-width:980px){{
  .hero .wrap,.why .wrap{{grid-template-columns:1fr;gap:40px}}
  .grid{{grid-template-columns:repeat(2,1fr)}}
  .series .cols,.rules{{grid-template-columns:1fr}}
  .series article{{border-right:0;margin-right:0;border-bottom:1px solid var(--line);padding-right:0}}
  .explore .links{{grid-template-columns:repeat(2,1fr)}}
  .began{{grid-template-columns:1fr}}
  footer .wrap{{grid-template-columns:1fr 1fr}}
}}
@media (max-width:640px){{
  body{{font-size:18px}}
  .wrap{{padding:0 16px}}
  .nav a:not(.btn){{display:none}}
  .hero{{padding:48px 0 60px}}
  section.band{{padding:60px 0}}
  .grid,.explore .links{{grid-template-columns:1fr}}
  .creed ol{{justify-content:flex-start;padding:18px 16px;gap:8px 18px}}
  .creed li{{font-size:1rem}}
  footer .wrap{{grid-template-columns:1fr}}
}}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap">
    <a class="brand" href="/"><b>KRIOS</b><span>Greek cultural preservation</span></a>
    <nav class="nav" aria-label="Main">
      <a href="#episodes">Episodes</a>
      <a href="#series">Series</a>
      <a href="#how">How we work</a>
      <a href="#explore">Explore</a>
      <a class="btn btn-gold" href="{SUB}" rel="noopener">Subscribe</a>
    </nav>
  </div>
</header>

<main id="main">
<section class="hero">
  <div class="wrap">
    <div>
      <span class="label">Greek history, faith and family memory</span>
      <h1>The living story of <em>Greek civilization</em></h1>
      <p class="lead">Documentaries for Greeks everywhere: the heroes, the customs, the music and the families who carried Greece with them. Real archives, sourced history, and the questions worth asking the people who raised you.</p>
      <div class="actions">
        <a class="btn btn-gold" href="{watch(latest['id'])}" rel="noopener">Watch the newest episode</a>
        <a class="btn btn-line" href="#episodes">All episodes</a>
      </div>
    </div>
    <a class="latest" href="{watch(latest['id'])}" rel="noopener">
      <span class="frame">
        <img src="{thumb(latest['id'])}" onerror="this.onerror=null;this.src='{thumb(latest['id'],'hqdefault')}'" alt="{e(latest['title'])}" width="1280" height="720">
        <span class="new label">New</span>
        <span class="play">▶ Watch · {latest['mins']} min</span>
      </span>
      <span class="body">
        <span class="meta label"><span>Season 3 · EP{latest['n']:03d}</span><span>{e(latest['label'])}</span><span>{nice(latest['date'])}</span></span>
        <h2>{e(latest['title'])}</h2>
        <p>{e(latest['tease'])}</p>
      </span>
    </a>
  </div>
</section>

<div class="creed" aria-label="The KRIOS creed">
  <ol><li>Preserve</li><li>Teach</li><li>Understand</li><li>Connect</li><li>Pass forward</li></ol>
</div>

<section class="band why" id="why">
  <div class="wrap">
    <blockquote>History tells us what happened. KRIOS shows <em>why it still lives in us.</em></blockquote>
    <div class="text">
      <p>Greek civilization didn't end in antiquity. It changed, survived occupation, crossed oceans in suitcases and lived on in kitchens, churches and name days.</p>
      <p>Each film follows one real story, from the past to a living family today, and lets the evidence show what was kept, what changed and what was lost.</p>
      <ul class="ladder">
        <li>"I never knew that."</li>
        <li>"That's why my family does this."</li>
        <li>"I want to ask my grandparents about this."</li>
        <li>"I want my children to know this."</li>
      </ul>
    </div>
  </div>
</section>

<section class="band eps" id="episodes">
  <div class="wrap">
    <div class="head">
      <div><span class="label">The documentaries</span><h2>Every episode, newest first</h2></div>
      <a class="more" href="{YT}/videos" rel="noopener">Watch on YouTube ↗</a>
    </div>
    <h3 class="season">Season 3 · The living story <span>EP020 onward</span></h3>
    <p class="season-note">From EP020 the films follow Greek life as it is lived now: what families carried when they left, and how it survives.</p>
    <ul class="grid">{s3}
    </ul>
    <h3 class="season">Season 2 · Heroes, heroines and forgotten history <span>EP011 to EP019</span></h3>
    <ul class="grid">{s2}
    </ul>
    <div class="began">
      <div>
        <span class="label" style="color:var(--gold-ink)">Season 1 · EP001 to EP010</span>
        <h3>Where KRIOS began</h3>
        <p>The first season told the ancient stories. Everything since has followed those stories into the lives of the people who inherited them.</p>
      </div>
      <ul>{s1}</ul>
    </div>
  </div>
</section>

<section class="band series" id="series">
  <div class="wrap">
    <div class="head">
      <div><span class="label">Series</span><h2>Three ways into the story</h2></div>
    </div>
    <div class="cols">
      <article>
        <span class="gr">Ρίζες</span>
        <h3>Living Roots</h3>
        <p>Where Greek families came from, what they carried when they left, and how it survives abroad. It begins with the dance the world thinks is Greek and the Greeks who left home.</p>
        <a class="more" href="{watch(latest['id'])}" rel="noopener">Watch EP021</a>
      </article>
      <article>
        <span class="gr">Γιορτές</span>
        <h3>Sacred Days · Living Traditions</h3>
        <p>Feast days, name days and national days, released on the day itself. What families celebrate, why their grandparents celebrated it, and how it differs from village to village and city to city.</p>
        <a class="more" href="{SUB}" rel="noopener">Subscribe for the next one</a>
      </article>
      <article>
        <span class="gr">Θυμάμαι</span>
        <h3>Growing Up Greek</h3>
        <p>The things many of us remember: Sunday in church, the icon on the wall, Greek school after school, the team you were born into. Stories that start with "I remember that" and lead somewhere deeper.</p>
        <a class="more" href="{SUB}" rel="noopener">Coming to the channel</a>
      </article>
    </div>
  </div>
</section>

<section class="band method" id="how">
  <div class="wrap">
    <div class="head">
      <div><span class="label">How we work</span><h2>Built on evidence, told by people</h2></div>
      <p>If a claim can't be traced to a source, it doesn't go in the film. When the evidence runs out, we say so.</p>
    </div>
    <ul class="rules">
      <li><b>The oldest source, not the most famous</b><span>Primary sources and named scholarship for every historical claim, checked before recording and again on the finished film.</span></li>
      <li><b>Real archives first</b><span>Historical photographs, documents, icons and maps, credited with their licence. Low-resolution archives are shown as framed prints, never stretched or AI-enhanced.</span></li>
      <li><b>Illustration is labelled</b><span>Where no photograph exists, some everyday scenes are illustrated. They are marked on screen and never stand in for sacred or historical evidence.</span></li>
      <li><b>History, tradition and belief kept apart</b><span>We say which is which: what is documented, what the Church teaches, what families practice, and where communities differ.</span></li>
      <li><b>A human voice</b><span>Today every documentary is narrated by a real person, not a synthetic voice.</span></li>
      <li><b>English and Greek</b><span>New films get English and Greek captions reviewed by people, so the story reaches every generation of the family.</span></li>
    </ul>
  </div>
</section>

<section class="band explore" id="explore">
  <div class="wrap">
    <div class="head">
      <div><span class="label">Explore</span><h2>Keep reading</h2></div>
    </div>
    <div class="links">
      <a class="tile" href="/answers/"><b>Greek history Q&amp;A</b><span>Short, sourced answers to the questions people actually ask.</span></a>
      <a class="tile" href="/blog/"><b>Episode articles</b><span>The written companions to the films, with sources.</span></a>
      <a class="tile" href="/tools/"><b>Quizzes and tools</b><span>Test what you know, including Real or Fake.</span></a>
      <a class="tile" href="/links.html"><b>All KRIOS links</b><span>YouTube, social channels and everything else in one place.</span></a>
    </div>
  </div>
</section>

<section class="ask">
  <div class="wrap">
    <h2>Who taught you yours?</h2>
    <p>Behind every Greek custom, recipe and dance is a place, a family and somebody who decided it was worth remembering. Ask them while you can.</p>
    <a class="btn btn-gold" href="{SUB}" rel="noopener">Subscribe on YouTube</a>
  </div>
</section>
</main>

<footer>
  <div class="wrap">
    <div>
      <b>KRIOS</b>
      <p>The living story of Greek civilization.<br>Preserve. Teach. Understand. Connect. Pass forward.</p>
    </div>
    <ul>
      <li><a href="#episodes">Episodes</a></li>
      <li><a href="#series">Series</a></li>
      <li><a href="#how">How we work</a></li>
      <li><a href="/answers/">Q&amp;A</a></li>
    </ul>
    <ul>
      <li><a href="{YT}" rel="noopener">YouTube ↗</a></li>
      <li><a href="/blog/">Articles</a></li>
      <li><a href="/tools/">Quizzes</a></li>
      <li><a href="/legal/">Legal</a></li>
    </ul>
    <div class="dedic">
      <span>© 2026 KRIOS · kriosgreece.com</span>
      <i>For my father, Peter (Πέτρος).</i>
    </div>
  </div>
</footer>
</body>
</html>
"""
open("index.html", "w", encoding="utf-8").write(page)
print("index.html", len(page), "bytes;", len(EP), "episodes")
