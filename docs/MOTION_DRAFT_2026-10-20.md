# kriosgreece.com motion draft (2026-10-20)
Status: DRAFT on branch `draft/motion-four-styles-2026-10-20`. Not merged, not live. Needs director review (see "Decisions").

## What it adds
Four styles from Futurepedia's AI Style Atlas (the list in the `krios-motion-styles` skill), rebuilt as small CSS and SVG. No Futurepedia prompt or code is copied; only the movement ideas.
| Atlas style | Where | Effect |
|---|---|---|
| 70 Topographic Survey | Hero bands (home, film pages, Sacred Days) | Faint gold contour lines behind the hero, drifting very slowly |
| 10 Illuminated Manuscript | Section headings (h2); first letter of "The story" | Small gold flourish draws in under the heading; red drop cap |
| 57 Cross-Stitch Sampler | Family questions, the closing "Who taught you yours?" band, footer | A running stitch with small crosses sews itself across |
| 48 Transit Map | The Greeks Who Left, new section "Where they went" | Two route maps (1890 to 1914, 1950 to 1974) draw on from Greece to the destinations |

## Facts on screen
The route section uses only wording from the Migration Policy Institute source already cited on that film page. Data: `data/motion/the-greeks-who-left.route.json` (delete the file to remove the section). It is a simple schematic of destinations, not routes or journeys, and says so.

## Safeguards
- Decorative SVG is `aria-hidden`; the route maps carry a text label and the same facts are in plain text above each map.
- `prefers-reduced-motion: reduce`, or no JavaScript: everything shows in its final state, nothing animates.
- No sound, no autoplay, no new libraries, no third-party requests. About 4 KB of CSS and 4 KB of JavaScript.
- `scripts/check_site.py` and `tests/site.test.mjs` (axe, layout at four widths, menu) run on the branch.

## Files
New: `assets/motion.css`, `assets/motion.js`, `motion_parts.py`, `data/motion/the-greeks-who-left.route.json`.
Changed: `site_parts.py` (links the two assets on every generated page), `build_films.py` (adds the route section when a route file exists), and the regenerated pages from `python3 build_home.py`.

## Decisions for the director
1. Approve the route section wording on The Greeks Who Left (it is new content on an approved page).
2. Approve the four styles for the live site, and timing: after the Oct 24 to 27 branding freeze and the Oct 26 release.
3. Optional later: Style 49 place cards and 29 linocut headers for other pages.

## Rollback
Revert the merge commit, or delete the two `<link>`/`<script>` lines in `site_parts.py` and run `python3 build_home.py`.
