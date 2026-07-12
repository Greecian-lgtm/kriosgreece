#!/bin/bash
# generate_aeo_pages.sh
# Generates AEO pages for all 10 Krios S1 episodes
# Run from: ~/krios-workspace/kriosmythology/
# Usage: bash generate_aeo_pages.sh

set -e

BASE_DIR="$(pwd)/answers"
echo "Generating AEO pages in: $BASE_DIR"

# ─── SHARED TEMPLATE FUNCTION ───────────────────────────────────────────────

generate_page() {
  local SLUG="$1"
  local TITLE="$2"
  local META_DESC="$3"
  local H1="$4"
  local BYLINE_SOURCES="$5"
  local DIRECT_ANSWER="$6"
  local INTRO="$7"
  local FAQ_SCHEMA="$8"
  local FAQ_HTML="$9"
  local EP_NUM="${10}"
  local EP_TITLE="${11}"
  local EP_DESC="${12}"
  local YT_URL="${13}"
  local RELATED="${14}"

  local DIR="$BASE_DIR/$SLUG"
  mkdir -p "$DIR"

  cat > "$DIR/index.html" << HTMLEOF
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${TITLE} | Krios Mythology</title>
  <meta name="description" content="${META_DESC}">
  <meta property="og:title" content="${TITLE}">
  <meta property="og:description" content="${META_DESC}">
  <meta property="og:url" content="https://kriosgreece.com/answers/${SLUG}/">
  <meta property="og:type" content="article">
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": ${FAQ_SCHEMA}
  }
  </script>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "${TITLE}",
    "author": {"@type": "Person", "name": "Stavros Krios", "url": "https://kriosgreece.com/about"},
    "publisher": {"@type": "Organization", "name": "Krios Mythology", "url": "https://kriosgreece.com"},
    "datePublished": "2026-04-03",
    "dateModified": "2026-04-03"
  }
  </script>
  <style>
    :root{--bg:#0f0d0a;--text:#e8dcc8;--gold:#c9972a;--terracotta:#b85c38;--muted:#8a7d6a;--card-bg:#1a1712;--border:#2a2318;}
    *{margin:0;padding:0;box-sizing:border-box;}
    body{background:var(--bg);color:var(--text);font-family:'Georgia',serif;line-height:1.75;font-size:1.05rem;}
    header{border-bottom:1px solid var(--border);padding:1.2rem 2rem;display:flex;align-items:center;gap:1rem;}
    header a{color:var(--gold);text-decoration:none;font-family:'Georgia',serif;font-size:1.1rem;letter-spacing:.05em;}
    header span{color:var(--muted);font-size:.9rem;}
    .container{max-width:760px;margin:0 auto;padding:3rem 2rem 5rem;}
    .breadcrumb{font-size:.85rem;color:var(--muted);margin-bottom:2rem;}
    .breadcrumb a{color:var(--gold);text-decoration:none;}
    h1{font-size:2rem;color:var(--text);font-weight:normal;line-height:1.3;margin-bottom:.5rem;}
    .byline{font-size:.85rem;color:var(--muted);margin-bottom:2.5rem;font-style:italic;}
    .answer-box{background:var(--card-bg);border-left:3px solid var(--gold);border-radius:4px;padding:1.5rem 1.75rem;margin-bottom:2.5rem;}
    .answer-box .label{font-size:.75rem;text-transform:uppercase;letter-spacing:.12em;color:var(--gold);margin-bottom:.6rem;}
    .answer-box p{font-size:1.05rem;color:var(--text);line-height:1.7;}
    h2{font-size:1.25rem;color:var(--gold);font-weight:normal;margin:2.5rem 0 1rem;border-bottom:1px solid var(--border);padding-bottom:.4rem;}
    p{margin-bottom:1.2rem;}
    .faq-item{border-bottom:1px solid var(--border);padding:1.25rem 0;}
    .faq-item h3{font-size:1rem;color:var(--text);font-weight:normal;margin-bottom:.5rem;}
    .faq-item p{color:var(--muted);font-size:.95rem;margin-bottom:0;}
    .episode-cta{background:var(--card-bg);border:1px solid var(--border);border-top:2px solid var(--terracotta);border-radius:4px;padding:1.75rem;margin-top:3rem;text-align:center;}
    .episode-cta .ep-label{font-size:.75rem;text-transform:uppercase;letter-spacing:.12em;color:var(--terracotta);margin-bottom:.5rem;}
    .episode-cta h3{font-size:1.2rem;color:var(--text);margin-bottom:.75rem;font-weight:normal;}
    .episode-cta p{font-size:.92rem;color:var(--muted);margin-bottom:1.25rem;}
    .btn{display:inline-block;background:var(--terracotta);color:#fff;text-decoration:none;padding:.65rem 1.5rem;border-radius:3px;font-size:.9rem;}
    .btn:hover{background:#a04d2e;}
    .related-links{margin-top:2.5rem;padding-top:1.5rem;border-top:1px solid var(--border);}
    .related-links ul{list-style:none;padding:0;}
    .related-links ul li{padding:.4rem 0;}
    .related-links ul li a{color:var(--gold);text-decoration:none;font-size:.95rem;}
    footer{border-top:1px solid var(--border);padding:1.5rem 2rem;text-align:center;font-size:.82rem;color:var(--muted);}
    footer a{color:var(--gold);text-decoration:none;}
    @media(max-width:600px){h1{font-size:1.5rem;}.container{padding:2rem 1.25rem 4rem;}}
  </style>
</head>
<body>
<header>
  <a href="https://kriosgreece.com">KRIOS</a>
  <span>/ Greek Mythology from Primary Sources</span>
</header>
<div class="container">
  <nav class="breadcrumb">
    <a href="https://kriosgreece.com">Home</a> ›
    <a href="https://kriosgreece.com/answers/">Answers</a> ›
    ${H1}
  </nav>
  <h1>${H1}</h1>
  <p class="byline">By Stavros Krios · Primary sources: ${BYLINE_SOURCES}</p>
  <div class="answer-box">
    <div class="label">Direct Answer</div>
    <p>${DIRECT_ANSWER}</p>
  </div>
  <p>${INTRO}</p>
  <h2>Frequently Asked Questions</h2>
  ${FAQ_HTML}
  <div class="episode-cta">
    <div class="ep-label">${EP_NUM} — Krios YouTube</div>
    <h3>${EP_TITLE}</h3>
    <p>${EP_DESC}</p>
    <a class="btn" href="${YT_URL}" target="_blank">Watch on YouTube →</a>
  </div>
  <div class="related-links">
    <h2>Related Questions</h2>
    <ul>${RELATED}<li><a href="https://kriosgreece.com/answers/">All mythology answers →</a></li></ul>
  </div>
</div>
<footer>
  <p><a href="https://kriosgreece.com">kriosgreece.com</a> · Greek mythology from primary sources · <a href="https://www.youtube.com/@KriosMythology">YouTube</a></p>
</footer>
</body>
</html>
HTMLEOF

  echo "✅ Generated: answers/$SLUG/index.html"
}

# ─── EP001: OLYMPIANS ────────────────────────────────────────────────────────
generate_page \
  "who-are-the-12-olympian-gods" \
  "Who Are the 12 Olympian Gods?" \
  "The 12 Olympian gods are Zeus, Hera, Poseidon, Demeter, Athena, Apollo, Artemis, Ares, Hephaestus, Aphrodite, Hermes, and Dionysus. Here is what the primary sources actually say about each one." \
  "Who Are the 12 Olympian Gods?" \
  "Hesiod Theogony, Homeric Hymns, Pindar" \
  "The 12 Olympian gods are <strong>Zeus, Hera, Poseidon, Demeter, Athena, Apollo, Artemis, Ares, Hephaestus, Aphrodite, Hermes, and Dionysus</strong>. They are called Olympians because they were believed to dwell on Mount Olympus in northern Greece. The list of twelve was not fixed in Homer — it solidified gradually in Greek religious tradition, and Hestia is sometimes listed in place of Dionysus." \
  "The concept of twelve Olympian gods — the Dodekatheon — became central to Greek religious life, but the ancient sources do not all agree on exactly who belongs in the twelve. Hesiod's Theogony describes the genealogy of the gods without fixing a number. The canonical list of twelve emerged through artistic tradition, particularly the twelve gods depicted on the east frieze of the Parthenon." \
  '[{"@type":"Question","name":"Who are the 12 Olympian gods?","acceptedAnswer":{"@type":"Answer","text":"The 12 Olympian gods are Zeus, Hera, Poseidon, Demeter, Athena, Apollo, Artemis, Ares, Hephaestus, Aphrodite, Hermes, and Dionysus. They dwell on Mount Olympus and govern different domains of the natural and human world."}},{"@type":"Question","name":"Why are they called Olympians?","acceptedAnswer":{"@type":"Answer","text":"They are called Olympians because Greek tradition placed their home on Mount Olympus, the highest mountain in Greece at 2,917 metres. Homer describes Olympus as a divine realm above the clouds, separate from the human world."}},{"@type":"Question","name":"Is Hades one of the 12 Olympians?","acceptedAnswer":{"@type":"Answer","text":"No. Hades rules the underworld and rarely leaves it. He is a brother of Zeus and Poseidon but is not counted among the twelve Olympians because he does not dwell on Mount Olympus."}}]' \
  '<div class="faq-item"><h3>Why are they called Olympians?</h3><p>They are called Olympians because Greek tradition placed their home on Mount Olympus — the highest mountain in Greece at 2,917 metres. Homer describes Olympus as a divine realm above the clouds, not simply the physical mountain.</p></div><div class="faq-item"><h3>Is Hades one of the 12 Olympians?</h3><p>No. Hades rules the underworld and rarely leaves it. He is a brother of Zeus and Poseidon but is not counted among the twelve because he does not dwell on Olympus. This is confirmed by Hesiod and the structure of the Homeric Hymns.</p></div><div class="faq-item"><h3>What primary sources describe the Olympians?</h3><p>Hesiod's Theogony is the earliest systematic account of the gods and their genealogy. The Homeric Hymns describe individual deities in detail. Pindar's Odes reference the Olympians extensively in the context of athletic and divine glory.</p></div>' \
  "EP001" \
  "The 12 Olympians: What the Primary Sources Actually Say" \
  "The full episode covers every Olympian god from primary sources — what Homer, Hesiod, and the Homeric Hymns actually say, not the popular retelling." \
  "https://www.youtube.com/@KriosMythology" \
  '<li><a href="https://kriosgreece.com/answers/what-is-the-real-story-of-odysseus/">What is the real story of Odysseus?</a></li><li><a href="https://kriosgreece.com/answers/who-is-zeus-in-greek-mythology/">Who is Zeus in Greek mythology?</a></li>'

# ─── EP002: ODYSSEUS ─────────────────────────────────────────────────────────
generate_page \
  "what-is-the-real-story-of-odysseus" \
  "What Is the Real Story of Odysseus?" \
  "Odysseus is the hero of Homer's Odyssey, a 24-book epic describing his 10-year journey home from Troy. Here is what Homer actually says — not the popular retelling." \
  "What Is the Real Story of Odysseus?" \
  "Homer Odyssey, Homer Iliad, Sophocles" \
  "Odysseus is the king of Ithaca and hero of Homer's <em>Odyssey</em> — a 24-book epic describing his <strong>10-year journey home from Troy</strong>. He is also a major figure in the <em>Iliad</em>, where his cunning is as important as his fighting ability. The <em>Odyssey</em> opens not at the beginning of his journey, but in year ten, when he is trapped on Calypso's island — a structural choice by Homer that places the backstory in flashback." \
  "The popular version of Odysseus as a simple adventure hero misses the complexity Homer built into the character. Odysseus lies, manipulates, and survives through intelligence rather than strength. The ancient Greeks debated whether he was admirable or morally questionable — Sophocles portrayed him as a cynical schemer, while Homer's Odyssey treats him with genuine sympathy." \
  '[{"@type":"Question","name":"What is the real story of Odysseus?","acceptedAnswer":{"@type":"Answer","text":"Odysseus is the king of Ithaca who fights in the Trojan War and then spends 10 years trying to return home. His journey is described in Homer'\''s Odyssey — a 24-book epic covering encounters with the Cyclops Polyphemus, the witch Circe, the Sirens, and the land of the dead, among others."}},{"@type":"Question","name":"How long did Odysseus journey take?","acceptedAnswer":{"@type":"Answer","text":"The Trojan War lasted 10 years, and Odysseus'\''s return journey also lasted 10 years — making 20 years total away from Ithaca. Homer'\''s Odyssey covers the final year of the return journey, with earlier events described in flashback."}},{"@type":"Question","name":"What primary source describes Odysseus?","acceptedAnswer":{"@type":"Answer","text":"Homer'\''s Odyssey is the primary source. It is one of the oldest works of Western literature, composed in the 8th century BC. The Iliad also features Odysseus as a secondary character. Sophocles'\'' Ajax portrays him more negatively as a cynical political operator."}}]' \
  '<div class="faq-item"><h3>How long did Odysseus journey take?</h3><p>The Trojan War lasted 10 years, and Odysseus took another 10 years to return home — 20 years total away from Ithaca. His wife Penelope waited the entire time, fending off suitors who assumed Odysseus was dead.</p></div><div class="faq-item"><h3>What primary source describes Odysseus?</h3><p>Homer'\''s Odyssey, composed in the 8th century BC, is the primary source. The Iliad also features Odysseus prominently. Sophocles'\'' Ajax presents a darker, more politically cynical version of the character.</p></div><div class="faq-item"><h3>Was Odysseus a hero or a villain in Greek mythology?</h3><p>He was a hero — but a morally complex one. The Greeks debated his character. Homer treats him sympathetically. Sophocles portrays him as a ruthless schemer. Virgil'\''s Aeneid, written from a Trojan perspective, portrays him as treacherous. His reputation depended entirely on whose side was telling the story.</p></div>' \
  "EP002" \
  "Odysseus: What Homer Actually Wrote" \
  "The full episode covers the real Odyssey from the primary source — what Homer wrote, what gets changed in modern retellings, and what the ancient Greeks thought of Odysseus." \
  "https://www.youtube.com/@KriosMythology" \
  '<li><a href="https://kriosgreece.com/answers/who-are-the-12-olympian-gods/">Who are the 12 Olympian gods?</a></li><li><a href="https://kriosgreece.com/answers/what-is-the-trojan-war-about/">What is the Trojan War about?</a></li>'

# ─── EP003: HERCULES ─────────────────────────────────────────────────────────
generate_page \
  "what-are-the-12-labours-of-hercules" \
  "What Are the 12 Labours of Hercules?" \
  "The 12 Labours of Hercules were tasks imposed by King Eurystheus as penance for killing his own family in a fit of madness sent by Hera. Here is what the primary sources actually say." \
  "What Are the 12 Labours of Hercules?" \
  "Apollodorus Library, Pindar, Diodorus Siculus" \
  "The 12 Labours of Hercules were tasks imposed by <strong>King Eurystheus of Tiryns</strong> as penance after Hercules killed his wife Megara and their children in a fit of madness sent by Hera. The Oracle at Delphi instructed him to serve Eurystheus for twelve years and complete whatever tasks were set. The labours were not originally twelve — the canonical list of twelve was standardized by later writers, particularly Apollodorus in his <em>Library</em>." \
  "The name Hercules is the Roman version of the Greek Heracles. In ancient sources he is always Heracles — the name meaning 'glory of Hera,' which is darkly ironic given that Hera is his greatest enemy throughout his life. His labours are covered most systematically by Apollodorus, writing in the 2nd century BC, who gives the full canonical list." \
  '[{"@type":"Question","name":"What are the 12 Labours of Hercules?","acceptedAnswer":{"@type":"Answer","text":"The 12 Labours are: (1) Nemean Lion, (2) Lernaean Hydra, (3) Ceryneian Hind, (4) Erymanthian Boar, (5) Augean Stables, (6) Stymphalian Birds, (7) Cretan Bull, (8) Mares of Diomedes, (9) Belt of Hippolyta, (10) Cattle of Geryon, (11) Apples of the Hesperides, (12) Cerberus from the Underworld."}},{"@type":"Question","name":"Why did Hercules have to do the 12 labours?","acceptedAnswer":{"@type":"Answer","text":"Hercules killed his wife and children in a fit of madness sent by the goddess Hera. The Oracle at Delphi told him to serve King Eurystheus for twelve years and complete whatever labours were assigned as penance. This is recorded in Apollodorus'\''s Library."}},{"@type":"Question","name":"What primary source lists the 12 Labours?","acceptedAnswer":{"@type":"Answer","text":"Apollodorus'\''s Library (2nd century BC) gives the most complete and systematic account. Pindar'\''s Nemean Odes and Diodorus Siculus also cover individual labours. The canonical list of twelve was not fixed until relatively late in Greek literary tradition."}}]' \
  '<div class="faq-item"><h3>Why did Hercules have to do the 12 labours?</h3><p>He killed his wife and children in a fit of divinely-sent madness. The Oracle at Delphi told him to serve King Eurystheus of Tiryns for twelve years as penance. This is the version in Apollodorus'\''s Library — the most complete ancient account of the labours.</p></div><div class="faq-item"><h3>What primary source lists all 12 Labours?</h3><p>Apollodorus'\''s Library, written in the 2nd century BC, gives the most complete canonical list. Individual labours appear in Pindar, Euripides, and Diodorus Siculus, but Apollodorus standardized the full sequence of twelve.</p></div><div class="faq-item"><h3>Is Hercules Greek or Roman?</h3><p>Hercules is the Roman name. The original Greek name is Heracles — meaning "glory of Hera," which is darkly ironic since Hera is his chief tormentor throughout his life. In all Greek primary sources he is always Heracles.</p></div>' \
  "EP003" \
  "Heracles: The Labours from Primary Sources" \
  "The full episode covers the real 12 Labours from Apollodorus, Pindar, and Euripides — including what the ancient sources say that modern retellings leave out." \
  "https://www.youtube.com/@KriosMythology" \
  '<li><a href="https://kriosgreece.com/answers/who-are-the-12-olympian-gods/">Who are the 12 Olympian gods?</a></li><li><a href="https://kriosgreece.com/answers/what-is-the-real-story-of-odysseus/">What is the real story of Odysseus?</a></li>'

# ─── EP004: ACHILLES ─────────────────────────────────────────────────────────
generate_page \
  "what-is-the-story-of-achilles-in-greek-mythology" \
  "What Is the Story of Achilles in Greek Mythology?" \
  "Achilles is the greatest warrior in Homer's Iliad. His rage, his friendship with Patroclus, and his death are the core of the Trojan War story. Here is what Homer actually wrote." \
  "What Is the Story of Achilles in Greek Mythology?" \
  "Homer Iliad, Pindar, Apollodorus" \
  "Achilles is the greatest Greek warrior in Homer's <em>Iliad</em> — a 24-book epic about the final weeks of the Trojan War. The <em>Iliad</em> opens with the word <em>menis</em> — rage — which is Achilles'\''s defining characteristic. <strong>His withdrawal from battle after a quarrel with Agamemnon</strong>, and his return after the death of his companion Patroclus, drive the entire narrative arc of the poem." \
  "The story of Achilles'\'' heel does not appear in Homer'\''s Iliad. It is a later tradition, recorded in Roman-era sources. Homer's Achilles dies from an arrow shot by Paris, guided by Apollo — but no heel vulnerability is mentioned. This is one of the most common misconceptions about what the primary source actually says." \
  '[{"@type":"Question","name":"What is the story of Achilles?","acceptedAnswer":{"@type":"Answer","text":"Achilles is the greatest Greek warrior at Troy. His rage after being dishonored by Agamemnon drives the Iliad. He withdraws from battle, his companion Patroclus is killed by Hector, and Achilles returns to kill Hector in revenge. He is later killed by an arrow from Paris guided by Apollo."}},{"@type":"Question","name":"Is the story of Achilles heel in Homer?","acceptedAnswer":{"@type":"Answer","text":"No. The Achilles heel vulnerability does not appear in Homer'\''s Iliad. It is a later Roman-era tradition. Homer describes Achilles dying from an arrow shot by Paris, guided by Apollo, but mentions no special vulnerability in his heel."}},{"@type":"Question","name":"What primary source tells the story of Achilles?","acceptedAnswer":{"@type":"Answer","text":"Homer'\''s Iliad is the primary source. It is one of the oldest works of Western literature, composed in the 8th century BC. The Iliad covers only the final weeks of the Trojan War, not the full war or Achilles'\'' early life."}}]' \
  '<div class="faq-item"><h3>Is the Achilles heel story in Homer?</h3><p>No. Homer'\''s Iliad does not mention a heel vulnerability. Achilles is killed by an arrow from Paris, guided by Apollo — but no special weakness is described. The heel tradition comes from later Roman-era sources, not from the original Greek primary source.</p></div><div class="faq-item"><h3>What is the relationship between Achilles and Patroclus?</h3><p>Patroclus is Achilles'\'' closest companion in the Iliad. When Achilles refuses to fight, Patroclus borrows his armor and enters battle, is killed by Hector, and his death brings Achilles back into the war in a rage. Homer uses the word hetairos — companion — for their relationship.</p></div><div class="faq-item"><h3>What primary source covers Achilles?</h3><p>Homer'\''s Iliad, 8th century BC, is the foundational text. Pindar'\''s Isthmian Odes and Nemean Odes reference Achilles. The later Achilleid by Statius (Roman era) covers his early life and introduces the heel tradition.</p></div>' \
  "EP004" \
  "Achilles: What Homer Actually Wrote" \
  "The full episode covers Achilles from the Iliad — the rage, Patroclus, Hector, and what the primary source says that modern versions change." \
  "https://www.youtube.com/@KriosMythology" \
  '<li><a href="https://kriosgreece.com/answers/what-is-the-trojan-war-about/">What is the Trojan War about?</a></li><li><a href="https://kriosgreece.com/answers/what-is-the-real-story-of-odysseus/">What is the real story of Odysseus?</a></li>'

# ─── EP005: MEDUSA ───────────────────────────────────────────────────────────
generate_page \
  "what-is-the-real-myth-of-medusa" \
  "What Is the Real Myth of Medusa?" \
  "Medusa was a mortal Gorgon whose gaze turned people to stone. Her story in the oldest sources is different from popular retellings. Here is what Hesiod and Pindar actually wrote." \
  "What Is the Real Myth of Medusa?" \
  "Hesiod Theogony, Pindar Pythian 12, Apollodorus" \
  "Medusa was one of three Gorgon sisters — the only mortal one. <strong>Her gaze turned anyone who looked at her directly to stone.</strong> The hero Perseus killed her by viewing her reflection in his shield, cutting off her head, and from her severed neck sprang the winged horse Pegasus and the giant Chrysaor. This core story is in Hesiod's <em>Theogony</em> and Pindar's <em>Pythian 12</em>." \
  "The popular version of Medusa as a victim of Athena'\''s punishment for being raped by Poseidon in her temple comes from Ovid'\''s <em>Metamorphoses</em> — a Roman text written in the 1st century AD, roughly 700 years after Hesiod. In the oldest Greek sources, Medusa is simply a monster, not a sympathetic victim. The transformation story is a Roman invention, not a Greek one." \
  '[{"@type":"Question","name":"What is the real myth of Medusa?","acceptedAnswer":{"@type":"Answer","text":"Medusa was a Gorgon — a monster whose gaze turned people to stone. She was the only mortal of the three Gorgon sisters. Perseus killed her by viewing her reflection in his shield and cutting off her head. From her severed neck sprang Pegasus and Chrysaor. This is recorded in Hesiod'\''s Theogony."}},{"@type":"Question","name":"Was Medusa originally human in Greek mythology?","acceptedAnswer":{"@type":"Answer","text":"In the oldest Greek sources — Hesiod and Pindar — Medusa is a monster from birth, not a transformed human. The story of Medusa being a beautiful woman punished by Athena comes from Ovid'\''s Metamorphoses, a Roman text from the 1st century AD, not from ancient Greek sources."}},{"@type":"Question","name":"What primary source tells the Medusa myth?","acceptedAnswer":{"@type":"Answer","text":"Hesiod'\''s Theogony (8th-7th century BC) is the oldest source, describing Medusa as a Gorgon and her death at Perseus'\''s hands. Pindar'\''s Pythian 12 (5th century BC) describes Perseus and the Gorgon. Apollodorus'\''s Library gives the most complete account of the Perseus myth."}}]' \
  '<div class="faq-item"><h3>Was Medusa a victim or a monster in the original myth?</h3><p>In the oldest Greek sources she is a monster — born that way. The sympathetic victim narrative comes from Ovid, writing in Rome in the 1st century AD, over 700 years after Hesiod'\''s Theogony. The two versions are from completely different cultures and time periods.</p></div><div class="faq-item"><h3>What came from Medusa'\''s blood in Greek mythology?</h3><p>From Medusa'\''s severed neck sprang two offspring: the winged horse Pegasus and the giant warrior Chrysaor. This is in Hesiod'\''s Theogony. Both were fathered by Poseidon before her death.</p></div><div class="faq-item"><h3>What primary source covers Medusa?</h3><p>Hesiod'\''s Theogony is the oldest Greek source. Pindar'\''s Pythian 12 covers the Perseus story. Apollodorus'\''s Library gives the fullest account. Ovid'\''s Metamorphoses (Roman, 1st century AD) is the source of the Athena punishment story — not a Greek primary source.</p></div>' \
  "EP005" \
  "Medusa: What the Greek Sources Actually Say" \
  "The full episode covers the real Medusa myth — what Hesiod and Pindar wrote versus what Ovid added 700 years later, and why the difference matters." \
  "https://www.youtube.com/@KriosMythology" \
  '<li><a href="https://kriosgreece.com/answers/who-are-the-12-olympian-gods/">Who are the 12 Olympian gods?</a></li><li><a href="https://kriosgreece.com/answers/what-is-the-story-of-achilles-in-greek-mythology/">What is the story of Achilles?</a></li>'

# ─── EP006: TROY ─────────────────────────────────────────────────────────────
generate_page \
  "what-is-the-trojan-war-about" \
  "What Is the Trojan War About?" \
  "The Trojan War was a 10-year Greek siege of the city of Troy, triggered by the abduction of Helen. Here is what Homer's Iliad and ancient sources actually say — including what archaeology has found." \
  "What Is the Trojan War About?" \
  "Homer Iliad, Thucydides, Herodotus, Virgil Aeneid" \
  "The Trojan War was a <strong>10-year Greek military campaign against the city of Troy</strong>, located in northwestern Anatolia (modern Turkey). According to Homer'\''s <em>Iliad</em>, it was triggered when Paris of Troy abducted Helen, wife of the Spartan king Menelaus. A coalition of Greek city-states under the leadership of Agamemnon sailed to Troy to retrieve her. The war ended with the Greeks'\'' Trojan Horse stratagem, first described not in the <em>Iliad</em> but in Homer'\''s <em>Odyssey</em>." \
  "The Trojan War is one of the most contested questions in ancient history — whether it happened at all, and if so, what it was really about. Thucydides treated it as a historical event. Modern archaeology at Hisarlik in Turkey has found evidence of multiple destroyed cities on the site identified as Troy, with Troy VIIa (destroyed around 1180 BC) the most likely candidate for the historical Trojan War." \
  '[{"@type":"Question","name":"What is the Trojan War about?","acceptedAnswer":{"@type":"Answer","text":"The Trojan War was a 10-year Greek siege of Troy, a city in northwestern Anatolia. It was caused by Paris of Troy abducting Helen, wife of Spartan king Menelaus. A Greek coalition under Agamemnon besieged Troy for 10 years before destroying it. The story is told in Homer'\''s Iliad and Odyssey."}},{"@type":"Question","name":"Did the Trojan War actually happen?","acceptedAnswer":{"@type":"Answer","text":"Archaeological evidence at Hisarlik, Turkey — identified as ancient Troy — shows a city destroyed around 1180 BC (Troy VIIa). This roughly matches the traditional dating of the Trojan War. Thucydides treated it as historical. Most modern scholars consider the war a historical event that became mythologized in Homer'\''s epics."}},{"@type":"Question","name":"What primary source tells the Trojan War story?","acceptedAnswer":{"@type":"Answer","text":"Homer'\''s Iliad covers the final weeks of the war. Homer'\''s Odyssey covers the aftermath. The Trojan Horse story first appears in the Odyssey, not the Iliad. Virgil'\''s Aeneid tells the Trojan story from the perspective of the losers."}}]' \
  '<div class="faq-item"><h3>Did the Trojan War actually happen?</h3><p>Archaeological evidence at Hisarlik, Turkey shows a city destroyed around 1180 BC. Thucydides treated the war as historical. Most modern scholars accept a historical kernel behind the myth. The details in Homer are mythologized — but the war itself likely occurred.</p></div><div class="faq-item"><h3>Where is the Trojan Horse in Homer?</h3><p>The Trojan Horse is not described in detail in the Iliad — it is mentioned briefly in the Odyssey and described fully in Virgil'\''s Aeneid, a Roman text. The Iliad ends before the fall of Troy. This surprises most people who assume the Horse is in Homer'\''s main Trojan War epic.</p></div><div class="faq-item"><h3>What primary sources cover the Trojan War?</h3><p>Homer'\''s Iliad (8th century BC) covers the final weeks. Homer'\''s Odyssey covers the aftermath. Virgil'\''s Aeneid (1st century BC) tells the Trojan side. Thucydides discusses its historicity in his History of the Peloponnesian War.</p></div>' \
  "EP006" \
  "Troy: What Homer and Archaeology Actually Say" \
  "The full episode covers the Trojan War from primary sources — what Homer wrote, what Thucydides thought, and what modern archaeology found at Hisarlik." \
  "https://youtu.be/2rg3tPOXz9Y" \
  '<li><a href="https://kriosgreece.com/answers/what-is-the-story-of-achilles-in-greek-mythology/">What is the story of Achilles?</a></li><li><a href="https://kriosgreece.com/answers/what-is-the-real-story-of-odysseus/">What is the real story of Odysseus?</a></li>'

# ─── EP007: THESEUS ──────────────────────────────────────────────────────────
generate_page \
  "what-is-the-real-myth-of-theseus-and-the-minotaur" \
  "What Is the Real Myth of Theseus and the Minotaur?" \
  "Theseus killed the Minotaur in the Labyrinth of Crete with help from Ariadne. Here is what Apollodorus, Plutarch, and the primary sources actually say — including what most retellings leave out." \
  "What Is the Real Myth of Theseus and the Minotaur?" \
  "Plutarch Life of Theseus, Apollodorus Library, Diodorus Siculus" \
  "Theseus was the legendary king of Athens who sailed to Crete and killed the <strong>Minotaur — a half-man, half-bull creature</strong> confined in a Labyrinth built by the craftsman Daedalus. He did this with the help of Ariadne, daughter of King Minos, who gave him a ball of thread to find his way out of the Labyrinth. The story is told most completely by Plutarch in his <em>Life of Theseus</em> and by Apollodorus in his <em>Library</em>." \
  "What most retellings omit: Theseus promised his father Aegeus he would change his ship'\''s sails from black to white if he survived — and forgot. Aegeus saw the black sails returning, believed his son was dead, and threw himself into the sea. The sea was named the Aegean after him. This detail — the forgotten sail — transforms Theseus from a pure hero into a more complicated figure whose victory comes at a cost." \
  '[{"@type":"Question","name":"What is the myth of Theseus and the Minotaur?","acceptedAnswer":{"@type":"Answer","text":"Theseus volunteered to be sent to Crete as tribute to King Minos, who demanded 14 Athenian youths every nine years to feed the Minotaur. Ariadne gave Theseus a thread to navigate the Labyrinth. He killed the Minotaur, escaped, and sailed home — but forgot to change his sails from black to white, causing his father Aegeus to kill himself."}},{"@type":"Question","name":"What is the Labyrinth in Greek mythology?","acceptedAnswer":{"@type":"Answer","text":"The Labyrinth was an elaborate maze built by the craftsman Daedalus on the orders of King Minos of Crete, to contain the Minotaur. It was designed so that anyone who entered could not find their way out — which is why Ariadne'\''s thread was essential to Theseus'\''s survival."}},{"@type":"Question","name":"What primary source tells the Theseus myth?","acceptedAnswer":{"@type":"Answer","text":"Plutarch'\''s Life of Theseus is the most complete ancient account. Apollodorus'\''s Library also covers the myth in detail. Diodorus Siculus provides additional material. The story appears in fragments in earlier sources including Bacchylides'\'' Dithyramb 17."}}]' \
  '<div class="faq-item"><h3>What detail do most retellings leave out?</h3><p>Theseus promised his father he would change his ship'\''s sails from black to white if he survived. He forgot. His father Aegeus saw the black sails, believed Theseus was dead, and jumped into the sea — which was named the Aegean after him. This is in Plutarch'\''s Life of Theseus.</p></div><div class="faq-item"><h3>Was the Minotaur'\''s Labyrinth real?</h3><p>Archaeologists at Knossos on Crete have found a massive Bronze Age palace with a complex floor plan that may have inspired the Labyrinth legend. Linear B tablets from the site mention a place called da-pu2-ri-to — possibly related to the word Labyrinth. The connection is debated but the palace is real.</p></div><div class="faq-item"><h3>What happened to Ariadne after Theseus?</h3><p>Theseus abandoned Ariadne on the island of Naxos — the reason is disputed in ancient sources. Some say he left her willingly, others say the god Dionysus appeared to him in a dream and claimed her. Dionysus then found Ariadne on Naxos and married her. This is in Apollodorus and Plutarch.</p></div>' \
  "EP007" \
  "Theseus: The Myth the Primary Sources Tell" \
  "The full episode covers Theseus and the Minotaur from Plutarch and Apollodorus — including the forgotten detail about the sails that changes everything about the story." \
  "https://youtu.be/AvdqOQHR2W4" \
  '<li><a href="https://kriosgreece.com/answers/which-god-is-associated-with-the-cyclades/">Which god is associated with the Cyclades?</a></li><li><a href="https://kriosgreece.com/answers/what-is-the-real-myth-of-medusa/">What is the real myth of Medusa?</a></li>'

# ─── EP008: CYCLADES ─────────────────────────────────────────────────────────
generate_page \
  "what-is-the-mythology-of-the-cyclades-islands" \
  "What Is the Mythology of the Cyclades Islands?" \
  "The Cyclades islands in the Aegean Sea are connected to Apollo, Dionysus, and Poseidon through ancient Greek mythology. Delos was Apollo's birthplace. Naxos is where Dionysus married Ariadne." \
  "What Is the Mythology of the Cyclades Islands?" \
  "Homeric Hymn to Apollo, Callimachus Hymn to Delos, Herodotus, Thucydides" \
  "The Cyclades are a group of islands in the Aegean Sea whose mythology is anchored to <strong>Delos — the birthplace of Apollo and Artemis</strong>. The <em>Homeric Hymn to Apollo</em> describes Leto searching all of Greece for a place willing to receive her before she gave birth. Delos agreed, and in return became the most sacred island in the Aegean — a pan-Hellenic sanctuary where no one could be born or die." \
  "Tourists visit the Cyclades every year for the whitewashed architecture and blue doors. Most walk past something older: the mythology embedded in the exact geography of the islands. The Portara on Naxos — a massive marble doorway still standing — is the entrance to an unfinished temple. Delos, a 20-minute ferry from Mykonos, was once the religious center of the Greek world. These are not background details. They are the mythology made physical." \
  '[{"@type":"Question","name":"What is the mythology of the Cyclades islands?","acceptedAnswer":{"@type":"Answer","text":"The Cyclades mythology centers on Delos, Apollo'\''s birthplace. The Homeric Hymn to Apollo describes Delos as the island that agreed to receive Leto before Apollo'\''s birth, making it sacred. Naxos is connected to Dionysus and Ariadne. Poseidon, as sea god, held authority across all the islands."}},{"@type":"Question","name":"Which Greek god was born on the island of Delos?","acceptedAnswer":{"@type":"Answer","text":"Apollo and his twin sister Artemis were born on Delos, according to the Homeric Hymn to Apollo. Delos is a small island in the center of the Cyclades that became one of the most important religious sanctuaries in ancient Greece because of this mythological connection."}},{"@type":"Question","name":"What is the Portara on Naxos?","acceptedAnswer":{"@type":"Answer","text":"The Portara is a massive marble doorway on Naxos, the entrance to an unfinished temple begun around 530 BC. It is traditionally attributed to Apollo, though Dionysus is also associated with Naxos through the myth of his marriage to Ariadne. The temple was never completed — the tyrant who commissioned it was overthrown mid-construction."}}]' \
  '<div class="faq-item"><h3>Which Greek god was born on Delos?</h3><p>Apollo and Artemis were both born on Delos, according to the Homeric Hymn to Apollo. Delos is at the geographic center of the Cyclades — which is part of why it became the religious center of the Aegean world. Thucydides records that Athens purified the island in 426 BC, removing all graves because the sanctity of Apollo'\''s birthplace forbade death there.</p></div><div class="faq-item"><h3>What is the Portara and why does it still stand?</h3><p>The Portara is the entrance gate of an unfinished temple on Naxos, begun around 530 BC. It was likely dedicated to Apollo. Construction stopped when the tyrant Lygdamis, who commissioned it, was overthrown. The marble blocks were too large to move — so the doorway was simply left standing, where it has remained for 2,500 years.</p></div><div class="faq-item"><h3>How are the Cyclades connected to Dionysus?</h3><p>Naxos is specifically connected to Dionysus through the myth of Ariadne. After Theseus abandoned her on Naxos, Dionysus arrived and married her. Naxos was also one of the first centers of Dionysiac worship in the Aegean — the island'\''s wine production is referenced in ancient sources as connected to his cult.</p></div>' \
  "EP008" \
  "The Cyclades: What Tourists Walk Past Without Seeing" \
  "The full episode covers the mythology of the Cyclades from primary sources — Delos, Naxos, the Portara, and the gods embedded in the exact geography of the islands." \
  "https://www.youtube.com/@KriosMythology" \
  '<li><a href="https://kriosgreece.com/answers/which-god-is-associated-with-the-cyclades/">Which god is associated with the Cyclades?</a></li><li><a href="https://kriosgreece.com/answers/what-is-the-real-myth-of-theseus-and-the-minotaur/">What is the myth of Theseus and the Minotaur?</a></li>'

# ─── EP009: PAROS ────────────────────────────────────────────────────────────
generate_page \
  "what-is-paros-famous-for-in-greek-mythology" \
  "What Is Paros Famous for in Greek Mythology?" \
  "Paros was famous in antiquity for its white marble and its connection to the hero Heracles and the poet Archilochus. Here is what ancient sources say about this Cycladic island." \
  "What Is Paros Famous for in Greek Mythology?" \
  "Archilochus Fragments, Apollodorus Library, Parian Marble Chronicle" \
  "Paros is a Cycladic island best known in antiquity for two things: its <strong>white marble — the finest in the ancient world</strong> — and as the birthplace of Archilochus, one of the earliest and most influential Greek lyric poets. In mythology, Paros was said to have been visited by Heracles, whose sons by the daughters of Minos settled the island. This is recorded in Apollodorus'\''s <em>Library</em>." \
  "The Parian Marble, an ancient Greek chronicle carved in stone around 264 BC and discovered on Paros, provides one of the earliest attempts at a chronological history of Greek civilization — including mythological events. It lists dates for events like the reign of Cecrops in Athens, the Trojan War, and the works of Homer, treating myth and history as a continuous timeline. The original is now in Oxford." \
  '[{"@type":"Question","name":"What is Paros famous for in Greek mythology?","acceptedAnswer":{"@type":"Answer","text":"Paros was said to have been settled by sons of Heracles in Greek mythology, according to Apollodorus. The island was famous in antiquity for its white marble and as the birthplace of the poet Archilochus. The Parian Marble — an ancient chronological chronicle found on Paros — is one of the most important documents for Greek historical and mythological chronology."}},{"@type":"Question","name":"What is the Parian Marble?","acceptedAnswer":{"@type":"Answer","text":"The Parian Marble is an ancient Greek chronicle inscribed on marble around 264 BC on the island of Paros. It lists key events in Greek history and mythology with dates, treating mythological events as part of a continuous historical timeline. It is now held in the Ashmolean Museum in Oxford."}},{"@type":"Question","name":"Who was Archilochus and why is he important?","acceptedAnswer":{"@type":"Answer","text":"Archilochus was a Greek lyric poet from Paros, active in the 7th century BC. He is considered one of the earliest Greek poets after Homer and Hesiod, and the first to write extensively in the first person. His fragments survive and include some of the earliest personal poetry in Western literature."}}]' \
  '<div class="faq-item"><h3>What is the Parian Marble?</h3><p>The Parian Marble is an inscribed stone chronicle from around 264 BC, found on Paros. It lists key events in Greek history with dates — including mythological events like the flood of Deucalion and the Trojan War — treating myth and history as a continuous record. Most of it is now in the Ashmolean Museum in Oxford.</p></div><div class="faq-item"><h3>Who was Archilochus?</h3><p>Archilochus was a 7th century BC lyric poet from Paros. He is one of the earliest Greek poets after Homer and Hesiod, and the first to write extensively in the first person voice. His surviving fragments include war poetry, erotic poetry, and personal reflection — making him one of the most distinctive voices in early Greek literature.</p></div><div class="faq-item"><h3>How is Heracles connected to Paros?</h3><p>According to Apollodorus'\''s Library, Heracles stopped at Paros during his expedition to retrieve the girdle of the Amazon queen Hippolyta. Two of his companions were killed by the sons of Minos on the island, so Heracles besieged Paros until the islanders surrendered and gave him two of Minos'\''s grandsons as replacements. His sons later settled the island.</p></div>' \
  "EP009" \
  "Paros: The Island the Ancient Sources Remember" \
  "The full episode covers the mythology and ancient history of Paros — the Parian Marble, Archilochus, and Heracles — from the primary sources." \
  "https://www.youtube.com/@KriosMythology" \
  '<li><a href="https://kriosgreece.com/answers/what-is-the-mythology-of-the-cyclades-islands/">What is the mythology of the Cyclades?</a></li><li><a href="https://kriosgreece.com/answers/which-god-is-associated-with-the-cyclades/">Which god is associated with the Cyclades?</a></li>'

# ─── EP010: ACROPOLIS ────────────────────────────────────────────────────────
generate_page \
  "what-is-the-myth-behind-the-acropolis-of-athens" \
  "What Is the Myth Behind the Acropolis of Athens?" \
  "The Acropolis of Athens was the site of the mythological contest between Athena and Poseidon for patronage of the city. Here is what Herodotus, Apollodorus, and the primary sources actually say." \
  "What Is the Myth Behind the Acropolis of Athens?" \
  "Herodotus Histories, Apollodorus Library, Pausanias Description of Greece" \
  "The Acropolis of Athens is the site of the mythological <strong>contest between Athena and Poseidon for patronage of the city</strong>. According to the myth, both gods struck the Acropolis rock — Poseidon produced a saltwater spring, Athena produced an olive tree. The gods of Olympus judged Athena'\''s gift more useful, and the city was named Athens in her honor. Apollodorus and Pausanias both record this myth, and the ancient Athenians pointed to physical evidence of both gifts on the Acropolis." \
  "When 5 million tourists visit the Acropolis each year, most see the Parthenon and little else. What they walk past: the Erechtheion, built directly over the site where the contest between Athena and Poseidon was said to have occurred. Inside the Erechtheion, ancient Athenians preserved what they believed were the marks of Poseidon'\''s trident in the rock, and the olive tree Athena was said to have planted. Pausanias, writing in the 2nd century AD, saw them both." \
  '[{"@type":"Question","name":"What is the myth behind the Acropolis of Athens?","acceptedAnswer":{"@type":"Answer","text":"The Acropolis was the site of a contest between Athena and Poseidon for patronage of the city. Poseidon struck the rock with his trident and produced a saltwater spring. Athena struck it and produced an olive tree. The gods judged Athena'\''s gift more useful and the city was named Athens. The Erechtheion temple was built over the exact site of this contest."}},{"@type":"Question","name":"Why is the Parthenon dedicated to Athena?","acceptedAnswer":{"@type":"Answer","text":"The Parthenon is dedicated to Athena because Athens was her city — she won the contest with Poseidon for patronage of the city. The Parthenon housed a massive gold and ivory statue of Athena made by the sculptor Pheidias, described by ancient sources as one of the wonders of the ancient world."}},{"@type":"Question","name":"What primary sources describe the Acropolis myths?","acceptedAnswer":{"@type":"Answer","text":"Apollodorus'\''s Library records the Athena-Poseidon contest. Pausanias'\''s Description of Greece (2nd century AD) describes visiting the Acropolis and seeing the marks of Poseidon'\''s trident and Athena'\''s olive tree in the Erechtheion. Herodotus mentions the sacred olive tree surviving the Persian burning of the Acropolis in 480 BC."}}]' \
  '<div class="faq-item"><h3>What is the Erechtheion and why is it important?</h3><p>The Erechtheion is the temple on the Acropolis built directly over the site where Athena and Poseidon'\''s contest was said to have occurred. Ancient Athenians preserved the marks of Poseidon'\''s trident in the rock inside it, and maintained an olive tree they believed was Athena'\''s original gift. Pausanias saw and described both in the 2nd century AD.</p></div><div class="faq-item"><h3>Did the sacred olive tree survive the Persian invasion?</h3><p>Yes — according to Herodotus. When the Persians burned the Acropolis in 480 BC, they destroyed the olive tree. But Herodotus records that the next day it had already sprouted a new shoot — which the Athenians took as a divine sign to rebuild and resist. The story is in his Histories, Book 8.</p></div><div class="faq-item"><h3>What primary sources cover the Acropolis myths?</h3><p>Apollodorus'\''s Library covers the Athena-Poseidon contest. Pausanias'\''s Description of Greece (2nd century AD) gives the most detailed ancient description of the Acropolis itself. Herodotus mentions the olive tree and the Persian destruction. Thucydides discusses the Acropolis'\''s ancient history in Book 1 of his History.</p></div>' \
  "EP010" \
  "The Acropolis: The Myth Beneath the Marble" \
  "The full episode covers the mythology of the Acropolis from primary sources — the contest of Athena and Poseidon, the Erechtheion, the olive tree, and what Pausanias saw when he visited." \
  "https://www.youtube.com/@KriosMythology" \
  '<li><a href="https://kriosgreece.com/answers/which-god-is-associated-with-the-cyclades/">Which god is associated with the Cyclades?</a></li><li><a href="https://kriosgreece.com/answers/what-is-the-trojan-war-about/">What is the Trojan War about?</a></li>'

# ─── UPDATE SITEMAP ──────────────────────────────────────────────────────────
echo ""
echo "Adding new pages to sitemap.xml..."

PAGES=(
  "who-are-the-12-olympian-gods"
  "what-is-the-real-story-of-odysseus"
  "what-are-the-12-labours-of-hercules"
  "what-is-the-story-of-achilles-in-greek-mythology"
  "what-is-the-real-myth-of-medusa"
  "what-is-the-trojan-war-about"
  "what-is-the-real-myth-of-theseus-and-the-minotaur"
  "what-is-the-mythology-of-the-cyclades-islands"
  "what-is-paros-famous-for-in-greek-mythology"
  "what-is-the-myth-behind-the-acropolis-of-athens"
)

SITEMAP_ENTRIES=""
for PAGE in "${PAGES[@]}"; do
  SITEMAP_ENTRIES="${SITEMAP_ENTRIES}  <url>\n    <loc>https://kriosgreece.com/answers/${PAGE}/</loc>\n    <lastmod>2026-04-03</lastmod>\n    <priority>0.8</priority>\n  </url>\n"
done

sed -i "s|</urlset>|${SITEMAP_ENTRIES}</urlset>|" sitemap.xml
echo "✅ Sitemap updated"

# ─── GIT PUSH ────────────────────────────────────────────────────────────────
echo ""
echo "Committing and pushing to GitHub..."
git add answers/ sitemap.xml
git commit -m "Add 10 episode AEO pages with FAQPage schema — S1 EP001-010"
git push origin main

echo ""
echo "═══════════════════════════════════════════════"
echo "✅ DONE — 10 AEO pages live on GitHub Pages"
echo "Next: Submit URLs to Bing Webmaster URL Inspection"
echo "═══════════════════════════════════════════════"
