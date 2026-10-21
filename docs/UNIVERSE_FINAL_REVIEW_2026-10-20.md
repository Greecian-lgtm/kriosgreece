# KRIOS Universe homepage v2: final-pass verification and open items (2026-10-20)
Status: design branch only. Not merged, not deployed, not indexed. No release authorized. Respect the Oct 24 to 27 freeze and the Oct 26 release. Responds to ChatGPT's final editorial assessment (Oct 20, 10:56 PM). Direction is v2; no redesign.

## 1. Verification run on the built prototype
Own tests on `prototype/universe/index.html` (Playwright, local server):
- Widths 320, 390, 768, 1440: no horizontal scroll, no script errors, axe clean on serious and critical, labels at 16px or larger, touch targets 44px or larger, no third-party requests beyond the YouTube thumbnail host.
- Menu opens with the keyboard and closes with Escape. Memory Room cycles all 6 questions and wraps. Works with JavaScript off (all 6 visible, buttons hidden).
- Reduced motion: no animations running.
- Keyboard focus: solid 3px outline on the Memory Room button.
- Robots: `noindex, nofollow`. Prototype is outside the sitemap and llms.txt.
- Images: 4 `<img>` elements, all with width and height attributes (no layout shift). The hero has descriptive alt. The two decorative thumbnail copies have empty alt; the real ones have alt text naming the film. Fonts are self-hosted; no Google Fonts call.
- Saint Demetrios: the prototype exposes only the title ("Saint Demetrios: More Than a Name Day") and the premiere date. No image, no story, no credits.

NOT verified here: the YouTube thumbnails could not load in my test environment (outbound requests to i.ytimg.com are blocked), so I could not see them render. They are the same published thumbnails the live film pages already use. Check them in a normal browser before release. The private Claude preview embeds them, so it is the place to look.

## 2. Saint Demetrios on the live site (main, not this branch)
`films/saint-demetrios/` and `sacred-days/saint-demetrios-name-day/` are already on main, with `held_until_release: true` in the data. The film page says the story, sources and credits appear when the film is public. Both URLs are in the sitemap (lastmod Oct 19). The director said on Oct 20, 10:56 PM that the film is scheduled and may be used for Shorts. That does not release the held story or credits; the website lock stays until the Oct 26 premiere.
Open for the director: keep both pages in the sitemap until Oct 26 (they carry no held content) or remove them until the premiere.

## 3. The 42 site warnings, classified (baseline on main; this branch adds none)
| Category | Count | Where | Remediation before release? |
|---|---|---|---|
| Episode or season number shown publicly (rule: no public episode or season numbers) | 27 | `answers/` pages (older mythology-era Q&A: EP001 to EP009, "Season 2") | YES, but on a separate content branch. Needs a director decision: reword, or retire the old pages. Not touched by the Universe prototype |
| Episode number shown publicly | 14 | `blog/ep001` to `blog/ep014` (file names and text) | YES, same decision. File names include the number, so a redirect plan is needed |
| Privacy blocklist not configured (`KRIOS_PRIVATE_TERMS` secret) | 1 | CI / local check | YES. The private-terms check cannot run until the director sets the secret. I did not and will not see or store it |
Total 42. Nothing in the prototype's own files triggers any of them.

## 4. Sirtaki research ledger
| ID | Source | Use | Status |
|---|---|---|---|
| SIR-01 | Erato Basea, "Zorba the Greek, Sixties exotica and a new cinema in Hollywood and Greece," Studies in European Cinema 12(1), 2015, pp. 60 to 76, DOI 10.1080/17411548.2015.1015830 | Film's production context and how Greek culture was presented to outside audiences | Citation verified by DOI record. I could not read the text or abstract. Do NOT cite it for the dance's choreography or origin |
| SIR-02 | Society of Folk Dance Historians, reproduction of a 2012 account of the dance as a film-era creation built from existing Greek dances (found by ChatGPT, GEO Finland piece) | Secondary lead only | NOT opened by me; the page was not found in my search. ChatGPT, please send the exact URL. Underlying reporting unverified |
| SIR-03 | Wikipedia "Sirtaki" (current citation in the film data) | None | Remains the sole reference on the live film data; flagged as weak |
Recommendation: leave the director-approved film text unchanged. Propose a separate correction only if SIR-01 (after reading) or a better source contradicts it. Sirtaki's exact origin stays flagged UNVERIFIED.

## 5. Seven-slot asset inventory (existing approved material first; no new images)
Only one approved image file is in the repository today (the harbour illustration). The other candidates below live in the production workflow; I have NOT placed, copied or approved any of them. Each needs the director's approval and a file handed over through the proper channel. File names in production use shot IDs from the EP021 QC notes.
| Slot | First choice | Where it is | Rights state | Label | Status |
|---|---|---|---|---|---|
| Ρίζες | Departure imagery from The Greeks Who Left: harbour illustration (already in this branch) or the doorway-and-suitcase frame (EP021 S040, QC PASS) | Branch / production | Illustration made for KRIOS | "AI-generated illustration" | Harbour is in use as the hero; use S040 for the gateway to avoid repeating the hero. Needs director OK |
| Πίστη | Saint Demetrios thumbnail (approved AI redraw) | Production | Approved, held | "AI-generated illustration" | HOLD until the Oct 26 premiere; the website lock stays. Fallback: a cleared photograph of a candle stand |
| Οικογένεια | EP021 kitchen-table frame (S020, empty chair, coffee, bread; QC PASS) or a bread-passing frame from the G6_table group | Production | Illustration | Same | Need to confirm which G6_table frame was approved; I did not open it |
| Χωριά | Mainland village lane from the EP021 set (S030) | Production | Illustration | Same | I saw the plan, not S030's QC result. Confirm before use. Gateway is marked "coming soon" |
| Μουσική | The Greek Dance published thumbnail | Live YouTube thumbnail | Published | Thumbnail credit | Ready; already used in the storybook |
| Ιστορία | Genuine archive only | Rights outreach pending (UIC, NHM, NYPL, LOC downloads awaiting approval) | NOT cleared | Source credit, not an illustration label | No approved artwork yet. Leave empty or use a typographic card. I did not find the "existing history-documentary artwork" ChatGPT mentions |
| Memory Room | Quiet family-object frame: the S010 album or S020 empty chair | Production | Illustration | Same | If S020 is used here, do not reuse it for Οικογένεια |
Hotlinked thumbnails: all published film images load from i.ytimg.com (same as the live site). Self-hosting them removes a third-party request; that needs your approval because it copies YouTube's images.

## 6. Language tag on Πέτρος (decision pending)
ChatGPT recommends `lang="el"` around Πέτρος in the locked dedication. It changes no visible text. It changes the locked HTML string, which a blocking check enforces byte-for-byte. I have NOT changed it. Decision for the director. If approved: a separate commit that updates the locked string and its check together, with a test showing the visible text is identical.

## 7. What the director should see before final approval
Desktop and mobile preview: the private Claude preview of the prototype (link in the chat). Four things to judge by eye, as ChatGPT suggests: whether the hero overlays and chapter marks feel like a travel campaign; whether the storybook page-turn slows reading; whether Greek words appear only where they mean something; whether the Memory Room stays quiet.

## 8. Decisions for the director
1. Approve v2 for final visual review as the candidate, or request changes.
2. Approve or decline `lang="el"` on Πέτρος (locked string).
3. Sirtaki: keep film text; ChatGPT to send the SFDH URL; Claude reads the Basea paper if you can get access.
4. Approve the slot-by-slot picks above, one at a time, and who delivers the files.
5. Warnings: authorize a separate content branch to deal with the 41 episode-number pages, and set the `KRIOS_PRIVATE_TERMS` secret yourself.
6. Keep the two Saint Demetrios pages in the sitemap until Oct 26, or pull them.
7. Self-host the YouTube thumbnails, yes or no.
8. Release date after the Oct 27 freeze. No deployment is authorized.
