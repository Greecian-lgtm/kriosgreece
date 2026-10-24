# Fix 4: homepage hero shortlist (prep only)

Prepared Oct 23 to 24, 2026, for the director's pick. Nothing on the site changes in this pull request. The hero today is `/images/films/the-greeks-who-left-harbour.jpg`, labelled "AI-generated illustration" (set in `data/films/the-greeks-who-left.json`, `hero_image`). Fix 4 replaces it with a real archival photograph of Greek emigrants.

Source of candidates: the rights-checked KRIOS visual resource catalog (`stavros-skills/resource-library/KRIOS_visual_resource_catalog_v1.csv`, rows ARC-001 to ARC-003 and BOOK-001), plus Library of Congress 2003680488. Each Library of Congress record below was re-opened on Oct 24, 2026 through its JSON record (`?fo=json`), and the rights line is quoted from it word for word. Every preview image was downloaded and looked at.

## Recommendation

**Candidate 1 (Patras, 1910)** is the best match for "The Greeks Who Left": it shows the departure from Greece itself, not New York, and its record title says "for America". Candidates 2 and 3 are strong pictures but tell a different story (Greeks leaving New York in 1912 to fight in the First Balkan War).

## Candidate 1: Greek emigrants embarking at Patras, 1910

- **Record:** https://www.loc.gov/item/2003680488/
- **Title (from the item):** "Greek immigrants embarking in small boat for steamer for America, Patras, Greece"
- **Made by:** Keystone View Company, publisher, 1910 (stereograph No. 17100; "Copyright 1910 by Keystone View Company")
- **Rights line (Library of Congress):** "No known restrictions on publication." Collection rights page: https://www.loc.gov/rr/print/res/493_ster.html
- **Why it is free:** published in the United States in 1910, so its copyright has expired (published before 1931). Catalog rating: FREE.
- **Reproduction number:** LC-DIG-stereo-1s26156. Files: TIFF master (about 54 MB) and JPEGs at 640 and 1024 px wide. The card is a stereo pair, so the hero would use one half, cropped to the scene.
- **Credit caption (proposed):** Greek emigrants board small boats for the steamer to America, Patras, 1910. Keystone View Company. Library of Congress, Prints and Photographs Division, LC-DIG-stereo-1s26156. No known restrictions.
- **Why it fits:** it shows the moment the film is about, Greeks leaving Greece for America from a Peloponnese harbour. It replaces the AI harbour scene with a real harbour. Men on the quay and rowing boats in the foreground give a clear focal point for the hero.
- **Watch for:** one half of the stereo pair is roughly square, so a wide 16:9 hero crop loses sky or water. Check the crop at 320 and 1440 px. The 1024 px JPEG is 338 KB, so the web copy must be re-encoded (the pack's limit for the largest image is 250 KB). Use the TIFF master for the best quality.

## Candidate 2: Greeks boarding the MADONNA, New York, October 1912

- **Record:** https://www.loc.gov/item/2014690707/ (catalog ARC-001)
- **Made by:** Bain News Service, publisher. Glass negative.
- **Rights line (Library of Congress):** "No known restrictions on publication. For more information, see George Grantham Bain Collection - Rights and Restrictions Information https://www.loc.gov/rr/print/res/274_bain.html"
- **Reproduction number:** LC-DIG-ggbain-10724. Files: TIFF (about 24 MB) and JPEGs at 640 and 1024 px. Catalog rating: FREE.
- **Library summary:** "Photo taken when Greek immigrants left New York City to return to their country and fight in the first Balkan War, which began in October 1912." (source given by the Library: Flickr Commons project, 2008). The Bain title is marked "unverified".
- **Credit caption (proposed):** Greeks boarding the steamer Madonna in New York to return home for the First Balkan War, October 1912. Bain News Service. Library of Congress, Prints and Photographs Division, LC-DIG-ggbain-10724. No known restrictions.
- **Why it fits:** a dense, sharp crowd with suitcases on a pier, which reads clearly at phone width, and the 4:3 frame crops well to 16:9.
- **Watch for:** it shows Greeks going back, not leaving Greece, so the caption must say so. Ship rigging lines cross the right side of the frame.

## Candidate 3: Greeks in New York going back to fight, October 1912

- **Record:** https://www.loc.gov/item/2014691138/ (catalog ARC-003)
- **Made by:** Bain News Service, publisher. Glass negative.
- **Rights line (Library of Congress):** "No known restrictions on publication. For more information, see George Grantham Bain Collection - Rights and Restrictions Information https://www.loc.gov/rr/print/res/274_bain.html"
- **Reproduction number:** LC-DIG-ggbain-11696. Files: TIFF (about 24 MB) and JPEGs at 640 and 1024 px. Catalog rating: FREE.
- **Library summary:** same First Balkan War departure series as candidate 2. The Bain title is marked "unverified".
- **Credit caption (proposed):** Greek men in New York gather to go back and fight in the First Balkan War, October 1912. Bain News Service. Library of Congress, Prints and Photographs Division, LC-DIG-ggbain-11696. No known restrictions.
- **Why it fits:** faces turned to the camera and a hand-painted Greek sign give a strong human connection. Good 16:9 crop.
- **Watch for:** the sign reads "ΖΗΤΩ Ο ΠΟΛΕΜΟΣ" ("long live the war"), which is a war-recruitment message rather than an emigration one. That suits a Balkan Wars film better than the homepage hero.

## Considered, not shortlisted

- **ARC-002, "N.Y. Greeks going home"** (https://www.loc.gov/item/2014690809/, LC-DIG-ggbain-10827): same rights as 2 and 3, but the glass negative has a strong double exposure and large signs ("WE ARE OFF FOR THE WAR"). It does not read well at hero size.
- **BOOK-001, Fairchild, *Greek Immigration to the United States* (Yale University Press, 1911)**, https://archive.org/details/greekimmigration00fairuoft: Internet Archive says "NOT_IN_COPYRIGHT" (US, 1911). Its list of illustrations includes "Immigrants Embarking for the United States at Patras" (opposite p. 210) and "Immigrants on Board". These are good subjects, but they are halftone book plates from a scan, so the quality is lower than the Library of Congress negatives, and the plate photographers are not named. Keep as a fallback; the catalog notes the book treats emigrants through a 1911 restrictionist lens, so take only the image, not its captions.

## What the director decides

1. Pick one of the three (or none).
2. Confirm the caption wording. The proposed captions use only what each Library of Congress record says, and add no new claim.

## After the pick (the fix itself, for a later pull request)

- Download the TIFF master, crop it, and save a web JPEG under `images/films/` at 250 KB or less, with width and height set.
- Update `hero_image` (`src`, `alt`, and caption) in `data/films/the-greeks-who-left.json`, and remove the "AI-generated illustration" chip for the hero in `build_universe.py`.
- Add a rights ledger row (krios-rights-check rating FREE, record URL, reproduction number, date checked).
- Re-run the builders and checks, then take site test screenshots at 320, 390, 768 and 1440 px.
