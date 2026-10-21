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
    words = "".join(
        f'<li class="cy-word"><span class="cy-gr" lang="el">{e(g)}</span><span class="cy-tr">{e(t)}</span><b>{e(m)}</b><span>{e(n)}</span></li>'
        for g, t, m, n in WORDS)
    coffee = "".join(
        f'<li><span class="cy-gr" lang="el">{e(g)}</span><span class="cy-tr">{e(t)}</span><b>{e(m)}</b></li>' for g, t, m in COFFEE)
    games = "".join(
        f'<li><span class="cy-gr" lang="el">{e(g)}</span><span class="cy-tr">{e(t)}</span><span>{e(n)}</span></li>' for g, t, n in GAMES)
    ask = "".join(f"<li>{e(q)}</li>" for q in ASK)
    return f'''<section class="m-sdhero"><div class="wrap">
  <span class="label m-kick m-gold">Growing up Greek</span>
  <h1>The Cyclades, at the table and at home</h1>
  <p>Small things families keep without noticing: a word, a cup of coffee, a board game, a lamp before an icon.</p>
</div></section>
<div class="wrap m-page cy-page">
  <section class="cy-sec reveal" id="words"><h2>Words we keep</h2>
    <p>These are everyday Greek words you may have heard at a family table. Spelling and accents are flagged for review by a Greek reader before release.</p>
    <ul class="cy-words">{words}</ul></section>

  <section class="cy-sec reveal" id="table"><h2>What was on the table</h2>
    <div class="cy-split"><div>
      <p>Cheese is part of the Cycladic table. One of them, kopanisti, has a protected designation of origin from the Cyclades. It is salty, peppery and creamy once it has ripened for a number of weeks, and it can be made from cow, sheep or goat milk, or a mix.</p>
      <p>Your family may have a different dish that says "home" more than any other. That one matters more to this page than any list.</p>
      <p class="m-note-sm">Source: <a href="{SRC_KOP[0]}" rel="noopener">{e(SRC_KOP[1])}</a></p>
    </div></div></section>

  <section class="cy-sec reveal" id="coffee"><h2>Coffee, unhurried</h2>
    <p>Greek coffee is made in a small long-handled pot, a μπρίκι (bríki), and served in a small cup with a layer of foam on top. You order it by how much sugar you want, and then you stay a while.</p>
    <ul class="cy-orders">{coffee}</ul>
    <p class="m-note-sm">Method as described in common recipe and culture guides. A stronger ethnographic source is on the research list.</p></section>

  <section class="cy-sec reveal" id="tavli"><h2>Tavli</h2>
    <p>Tavli is a board game for two, played with dice. It is really three games played one after another until someone reaches the agreed score.</p>
    <ol class="cy-games">{games}</ol>
    <p class="m-note-sm">Source: <a href="{SRC_TAVLI[0]}" rel="noopener">{e(SRC_TAVLI[1])}</a></p></section>

  <section class="cy-sec reveal" id="faith"><h2>Faith at home</h2>
    <p>In many Greek Orthodox homes there is a corner for the icons, an εικονοστάσι (eikonostási), often with a small κανδήλι lit before it. Name days, the feast of the saint you are named for, are marked with a call, a visit or a sweet.</p>
    <p class="m-note-sm">Customs differ from family to family, and none of them is more Greek than another. For feast days and name days, see <a href="/sacred-days/">Sacred Days</a>.</p></section>

  <section class="cy-sec cy-ask reveal" id="ask"><h2>Ask someone in your family</h2>
    <p>Write the answers down while someone still remembers them. If nobody knows, leave the gap. Do not fill it in.</p>
    <ul class="m-askqs">{ask}</ul></section>
</div>'''
