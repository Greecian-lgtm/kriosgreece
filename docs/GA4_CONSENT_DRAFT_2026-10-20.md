# GA4 for kriosgreece.com, consent first (draft, 2026-10-20)
Director chose option A on Oct 20, 2026. Branch `draft/ga4-consent-2026-10-20`. Not merged, not live.

Done in Google Analytics (director's account): the existing web stream was renamed "KRIOS Greece website" and its URL changed from kriosmythology.com to kriosgreece.com (Measurement ID G-CR9SJHDTPB, unchanged); the property was renamed "KRIOS Greece". A second stream was not created, because Google advises one stream per site.

Site changes: assets/analytics.js, loaded on every page through the site scripts and the SEO pass. Nothing from Google loads until the visitor chooses Allow analytics. No thanks, Global Privacy Control and Do Not Track all mean no. Ad personalization and Google signals are off in the tag. A footer link "Analytics choice" reopens the choice. The Legal page privacy text now matches, with an anchor at /legal/#privacy.

Tested: banner shows on first visit with 0 Google requests; No thanks stays off after reload; Allow starts GA; GPC shows no banner and no request; axe found no serious or critical issues with the banner on.

Open for the director: approve and merge after the Oct 24 to 27 freeze and the Oct 26 release; set GA data retention to 14 months and confirm Google signals stay off in the GA settings; the Legal page still says the site "complies with GDPR and CCPA" and mentions Kit email signups, which need review because no signup form was found on the pages checked.
