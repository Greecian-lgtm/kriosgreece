# /cyclades/ draft page: everyday Cycladic life and the things families keep. Region level only, no island names.
# Text only. No illustrations: image slots are listed in docs/CYCLADES_PAGE_DRAFT_2026-10-20.md for the director's workflow.
from site_lib import e

SRC_KOP = ("https://en.wikipedia.org/wiki/Kopanisti", "Kopanisti, protected designation of origin cheese of the Cyclades")
SRC_TAVLI = ("https://en.wikipedia.org/wiki/Tavli", "Tavli, the three games and how they are played")

WORDS = [
    ("κέφι", "kéfi", "high spirits", "The mood that makes a table, a song or an afternoon come alive."),
    ("φιλοξενία", "filoxenía", "hospitality", "Made from φιλία, friendship, and ξένος, stranger or guest."),
    ("παρέα", "paréa", "company", "The people you spend your time with, and the time itself."),
    ("κέρασμα", "kérasma", "a treat offered", "What a host puts in front of you before you have asked for anything."),
    ("καφενείο", "kafeneío", "the coffeehouse", "A place for coffee, talk, cards and tavli."),
    ("κομπολόι", "kompolói", "worry beads", "Strung beads kept moving through the fingers, for the hands more than for counting."),
    ("κανδήλι", "kandíli", "the small oil lamp", "Kept lit in front of the icons at home."),
    ("γιορτή", "giortí", "feast, celebration", "Also what many families call a name day."),
]

COFFEE = [
    ("σκέτος", "skétos", "no sugar"),
    ("μέτριος", "métrios", "medium sweet"),
    ("γλυκός", "glykós", "sweet"),
]

GAMES = [
    ("Πόρτες", "Pórtes", "The one closest to backgammon. You can hit a lone checker off the board."),
    ("Πλακωτό", "Plakotó", "No hitting. You pin an opposing checker by covering it with one of your own."),
    ("Έβγα", "Évga", "A running game. No hitting and no pinning, both sides move the same way round the board."),
]

ASK = [
    "Who made the coffee in our family, and how did they take it?",
    "Did anyone play tavli, and who did you have to beat first?",
    "Is there a lamp, an icon or a small shelf at home where someone used to stop and cross themselves?",
    "Which word did our family say that nobody else understood?",
    "What was on the table when the whole family came together?",
]


def body():
    cols = ["cobalt", "turq", "sun", "rose", "white", "cobalt", "turq", "sun"]
    tilt = [-2.5, 1.8, -1.2, 2.6, -2, 1.4, -2.2, 1.6]
    words = "".join(
        f'<li class="cy-word vv-c-{cols[i]}" data-tilt style="--r:{tilt[i]}deg;--d:{i*0.35}s"><span class="cy-gr" lang="el">{e(g)}</span><span class="cy-tr">{e(t)}</span><b>{e(m)}</b><span>{e(n)}</span></li>'
        for i, (g, t, m, n) in enumerate(WORDS))
    coffee = "".join(
        f'<li data-tilt style="--r:{r}deg"><span class="cy-gr" lang="el">{e(g)}</span><span class="cy-tr">{e(t)}</span><b>{e(m)}</b></li>'
        for (g, t, m), r in zip(COFFEE, (-2, 1.5, -1)))
    games = "".join(
        f'<li data-tilt style="--r:{r}deg"><span class="cy-gr" lang="el">{e(g)}</span><span class="cy-tr">{e(t)}</span><span>{e(n)}</span></li>'
        for (g, t, n), r in zip(GAMES, (-1.5, 1.2, -2)))
    ask = "".join(f"<li>{e(q)}</li>" for q in ASK)
    belt = "".join(f'<span lang="el">{e(g)}</span>' for g, *_ in WORDS) * 2
    hero_cards = "".join(
        f'<div class="vv-fl vv-c-{c}" style="--r:{r}deg;--d:{d}s"><span lang="el">{e(g)}</span><small>{e(t)}</small></div>'
        for (g, t, c, r, d) in [("κέφι", "kéfi", "sun", -6, 0), ("παρέα", "paréa", "rose", 5, .8), ("τάβλι", "távli", "turq", -3, 1.6), ("καφές", "kafés", "white", 7, 2.4)])
    petals = "".join(f'<i style="--x:{x}%;--s:{sz}px;--t:{t}s;--d:-{d}s"></i>' for x, sz, t, d in
                     [(6,10,19,0),(14,7,24,6),(23,12,21,3),(33,8,26,11),(41,10,18,2),(52,7,23,9),(61,12,20,5),(70,8,27,13),(79,10,22,7),(88,7,25,1),(94,12,19,10),(47,9,28,15)])
    return f'''<link rel="stylesheet" href="/assets/vivid.css">
<section class="vv-hero"><div class="vv-blob vv-b1"></div><div class="vv-blob vv-b2"></div><div class="vv-blob vv-b3"></div><div class="vv-petals" aria-hidden="true">{petals}</div>
  <div class="wrap vv-hero-in"><div class="vv-copy">
    <span class="vv-kick">Growing up Greek</span>
    <h1><span class="vv-big">The Cyclades,</span> <em class="vv-it">at the table and at home</em></h1>
    <p>Small things families keep without noticing: a word, a cup of coffee, a board game, a lamp before an icon.</p>
    <a class="vv-btn" href="#words">Start with the words</a></div>
    <div class="vv-stack" aria-hidden="true">{hero_cards}</div></div></section>
<div class="vv-belt" aria-hidden="true"><div class="vv-belt-in">{belt}</div></div>
<div class="cy-page vv-page">
  <section class="vv-band vv-w" id="words"><div class="wrap reveal"><h2><span class="vv-big">Words</span> <em class="vv-it">we keep</em></h2>
    <p>Everyday Greek words you may have heard at a family table. Spelling and accents are flagged for review by a Greek reader before release.</p>
    <ul class="cy-words">{words}</ul></div></section>

  <section class="vv-band vv-cobalt" id="table"><div class="wrap reveal"><h2><span class="vv-big">What was</span> <em class="vv-it">on the table</em></h2>
    <p>Cheese is part of the Cycladic table. One of them, kopanisti, has a protected designation of origin from the Cyclades. It is salty, peppery and creamy once it has ripened for a number of weeks, and it can be made from cow, sheep or goat milk, or a mix.</p>
    <p>Your family may have a different dish that says "home" more than any other. That one matters more to this page than any list.</p>
    <p class="m-note-sm">Source: <a href="{SRC_KOP[0]}" rel="noopener">{e(SRC_KOP[1])}</a></p></div></section>

  <section class="vv-band vv-sun" id="coffee"><div class="wrap reveal"><h2><span class="vv-big">Coffee,</span> <em class="vv-it">unhurried</em></h2>
    <div class="vv-steam" aria-hidden="true"><i></i><i></i><i></i></div>
    <p>Greek coffee is made in a small long-handled pot, a μπρίκι (bríki), and served in a small cup with a layer of foam on top. You order it by how much sugar you want, and then you stay a while.</p>
    <ul class="cy-orders">{coffee}</ul>
    <p class="m-note-sm">Method as described in common recipe and culture guides. A stronger ethnographic source is on the research list.</p></div></section>

  <section class="vv-band vv-turq" id="tavli"><div class="wrap reveal"><h2><span class="vv-big">Tavli</span></h2>
    <p>Tavli is a board game for two, played with dice. It is really three games played one after another until someone reaches the agreed score.</p>
    <ol class="cy-games">{games}</ol>
    <p class="m-note-sm">Source: <a href="{SRC_TAVLI[0]}" rel="noopener">{e(SRC_TAVLI[1])}</a></p></div></section>

  <section class="vv-band vv-rose" id="faith"><div class="wrap reveal"><h2><span class="vv-big">Faith</span> <em class="vv-it">at home</em></h2>
    <div class="vv-lamp" aria-hidden="true"></div>
    <p>In many Greek Orthodox homes there is a corner for the icons, an εικονοστάσι (eikonostási), often with a small κανδήλι lit before it. Name days, the feast of the saint you are named for, are marked with a call, a visit or a sweet.</p>
    <p class="m-note-sm">Customs differ from family to family, and none of them is more Greek than another. For feast days and name days, see <a href="/sacred-days/">Sacred Days</a>.</p></div></section>

  <section class="vv-band vv-w cy-ask" id="ask"><div class="wrap reveal"><h2><span class="vv-big">Ask someone</span> <em class="vv-it">in your family</em></h2>
    <p>Write the answers down while someone still remembers them. If nobody knows, leave the gap. Do not fill it in.</p>
    <ul class="m-askqs">{ask}</ul></div></section>
</div>'''
