# KRIOS Universe homepage prototype (PROPOSAL, 2026-10-20)
Status: design branch only. Not merged, not deployed, not indexed. Needs director approval before anything goes live. Respect the Oct 24 to 27 freeze and the Oct 26 release.
Branch: `design/universe-homepage-prototype-2026-10-20`. Prototype page: `/prototype/universe/` (noindex, outside sitemap and llms.txt). Production and `main` are untouched.

## 1. Audit (read-only)
- Static site on GitHub Pages (`main`, CNAME kriosgreece.com), built by Python: `build_home.py` runs `build_films.py`, `build_hubs.py`, `scripts/seo_pass.py`. Shared parts in `site_parts.py` and `site_lib.py`. Film data in `data/films/*.json`, subjects in `data/subjects.json`.
- Workflows: `sync-youtube.yml` (every 30 min on main), `site-checks.yml`, `indexnow.yml`. A push to a `design/` branch deploys nothing.
- Baseline `check_site.py`: 0 blocking, 42 warnings, 186 pages. Unchanged by this branch.
- Navigation today: Films, Sacred Days, Q&A and related hubs. No theme hubs for diaspora, music, villages or family.
- Legacy images in `images/*.jpg` and `frames/` (241 webp, 26 MB) are unreferenced with unverified rights. Not used.

## 2. What the prototype contains
1. Hero: "The stories we inherited. The questions we never asked." with the approved harbour illustration, labelled as an illustration.
2. The newest film, with source material and what comes next. Related Shorts appear only when a Short is public (none are, so the block is hidden).
3. Six gateways: Roots & Diaspora, Faith & Sacred Days, Family & Traditions, Villages & Places (coming soon), Music & Identity, History & Hidden Greece. Greek word as the anchor. Film counts are computed.
4. Memory Room (proposed): one question at a time, taken from published film pages. Nothing saved, sent or typed.
5. Questions the films answer (proposed): two entries built from approved film data by index, so text cannot drift from the film pages.
6. How we work, the locked dedication (byte-exact), close.
Order on phones: hero, newest film, themes, Memory Room, questions, how we work, close.

## 3. Design system (`assets/universe.css`, prefix `u-`)
Aegean 950/900/800/700/500, ivory, paper, stone, charcoal, gold #c0a05c, gold-ink #664c16 for text on light. EB Garamond (display, Greek-capable) and Inter (labels). Labels never under 16px. Motion is gentle and off under reduced motion. Focus rings per surface. 44px targets.

## 4. Architecture proposal for promotion
- Hubs `/explore/<slug>/` per gateway, `/memory-room/`, `/why/`. Data: `data/universe/gateways.json`, `why.json`, `featured.json`; optional `gateway` override per film.
- Wire into `build_home.py`; remove `PROTO`, banner and noindex.
- New checks: Why entries point at published approved films; gateway links resolve; illustration chip present when a hero is an illustration; no island names; no em dashes; no episode numbers.
- Release only after approval and outside the freeze.

## 5. Asset inventory
| Asset | Use | Rights state |
|---|---|---|
| images/films/the-greeks-who-left-harbour.jpg (sha256 3051c8be7c37794b567116040ac993be94098b08a3e996f2c8b75d77001fb7a6, 125,976 bytes, no EXIF) | Hero | KRIOS illustration from the film (EP021 S090). The film page credit says illustrations are made for KRIOS and labelled. Chip says "Illustration". Saying "AI-generated" is a director decision |
| Saint Demetrios thumbnail | Not used | Approved AI redraw, held |
| images/share-default.jpg | Not used | Typographic card |
| Legacy images/*.jpg, frames/ | Not used | Unreferenced, rights unverified |
| YouTube thumbnails | Not used | Hotlinked on live pages |
| EB Garamond, Inter | Fonts via Google Fonts | OFL. Self-hosting recommended |

Image slots still empty (fill only through ChatGPT's workflow or the rights-cleared archive): gateway images, featured poster, Memory Room backdrop, Villages & Places.

## 6. Review record
Critic plus five reviewers (truth and rights, cultural authenticity, privacy and safety, access and performance, simplicity and voice). Fixed: hero caption overlap on phones, chip wording, gateway lines, copy trimmed, Preserve/Teach strip removed, empty states removed, focus ring contrast, touch targets, Greek lang on the quote, both migration waves shown. Own tests pass: axe clean on serious and critical, no horizontal scroll 320 to 1440, works without JavaScript.
Not fixed on purpose: "Πέτρος" lang inside the locked dedication (see decision 7).

## 7. Decisions for the director
1. Approve the direction, the six gateways and their names, or change them.
2. Greek words (Ρίζες, Πίστη, Οικογένεια, Χωριά, Μουσική, Ιστορία) need a fluent reviewer.
3. Hero chip: "Illustration" or "AI-generated illustration".
4. Images for gateways, featured poster and Memory Room, and who supplies them.
5. The Sirtaki claim cites Wikipedia. Keep, or replace with an older source?
6. "Saint Demetrios: More Than a Name Day" is already on live pages. Confirm the title is final.
7. Allow a lang wrapper on "Πέτρος" in the locked dedication (changes the locked string)?
8. Nav names (Themes, Memory Room) and whether Q&A stays.
9. Self-host fonts.
10. Whether the Memory Room ever collects family stories (not in this prototype).
11. Release date after the Oct 27 freeze.

## 8. Update: v2 cinematic direction (director, Oct 20, 10:29 PM)
The prototype now uses a full-bleed hero with large serif type, warm terracotta accents, chapter marks (I to IV), translucent layered captions and scroll-driven depth (hero drift, page-turn entry on storybook pages). Motion is progressive enhancement and off under reduced motion. The storybook uses the film thumbnails. The previous version is in git history (commit 2d98509). Peer research: `KRIOS_website_peer_research_2026-10-20.md`.

## 9. ChatGPT creative review applied (Oct 20, 10:35 PM)
Applied: hero chip now "AI-generated illustration"; Memory Room copy "Some questions stay with us..." as proposed copy only; featured film shows the published thumbnail; fonts self-hosted (EB Garamond and Inter, Latin and Greek subsets, SIL OFL licences in `assets/fonts/universe/`), and the prototype no longer calls Google Fonts; the locked Saint Demetrios page no longer carries any image, only its title and date, both already on the live site. Gateway names unchanged.

### Approved versus placeholder assets
| Slot | Status |
|---|---|
| Hero (harbour illustration) | Approved, labelled AI-generated illustration |
| Storybook: The Greeks Who Left, The Greek Dance | Approved, published film thumbnails |
| Featured film thumbnail | Approved, published thumbnail |
| Storybook: Saint Demetrios | No image. Lock only. Title and date already public |
| Six gateway images | EMPTY. Mood-board briefs only (ChatGPT). Fill from approved assets or rights-cleared archive first |
| Memory Room image | EMPTY. Brief: ordinary family object, no staging |
| Fonts | Self-hosted, OFL |

### Decisions resolved or still open
- Saint Demetrios title: CONFIRMED against the director-approved release package (title and description approved Oct 19, 14:58).
- Sirtaki source: OPEN. I could not find an authoritative source yet. Pages found: a hobby music site (no named scholar) and a folk-dance blog without citations; Britannica's Zorba page does not mention the dance. One academic lead I could not open: Studies in European Cinema 12(1), 2015, "Zorba the Greek, Sixties exotica and a new cinema in Hollywood and Greece". The film data is director-approved, so it is not edited. Needs a source from the director or ChatGPT.
- lang tag on Πέτρος: OPEN. The dedication is locked byte-exact and a blocking check enforces it. Changing it needs the director's decision, not only a recommendation.
- Release after the Oct 24 to 27 freeze, no automatic deployment.
- Premature exposure of Saint Demetrios: the prototype exposes only the public title and date. The film page, credits and release files stay on `release/stdemetrios-credits`, not in this branch.
