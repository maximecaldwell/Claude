# "Every post" on three channels — TNM vs MINING.COM vs CEO.CA (desk, 17 Nov 2026)

Prompt: Boyd GP card, "SEEK THE DIGITS … FROM EVERY CHAPTER, EVERY POST … TWO NUMBERS". TNM's launch post: "Each following round of clues will appear monthly, through The Northern Miner, MINING.COM or CEO.CA." Earlier work: R-1169 (social sweep, CLOSED), R-1170 (Val-d'Or syndication diff). This pass re-reads the live copies on 17 Nov 2026 and extends the search to every chapter and the GP posts.

Null, stated first: syndicated copies are made by other desks at other times. Their differences are usually copy-desk changes (house style, extra tickers, "said"→"says", their own deks, tracking links). A difference counts as meaningful here only if digits or words change, or an item is present on one channel only. Nothing below is read as a location.

## 0. Headline
- **MINING.COM carries only 4 hunt articles** (launch, Cobalt, Val-d'Or, Nova Scotia) and **8 hunt video pages** (launch promo + 7 winner interviews). **No** MINING.COM copy of Dawson, Golden Triangle, Argentia, Southern BC, Toronto, Bathurst, Saskatchewan, Manitoba, Sudbury or Chibougamau articles, and **no** GP clue post of any kind.
- **CEO.CA: nothing found.** No article, channel post or profile post about the hunt was visible to an ordinary signed-out visitor (details §4). This is a gap, not a negative.
- Text diffs of the 4 syndicated articles (line-by-line hash comparison, then full text of every differing line):
  - **Cobalt: identical** (58/58 lines). **Nova Scotia: identical** (48/48 lines).
  - **Val-d'Or: 2 differences**, both already in R-1170 and still true today: TNM's `810-419-227` trailer is absent on MINING.COM; TNM's ":mining finance" stray colon is absent on MINING.COM.
  - **Launch article: rewritten by MINING.COM** (7 of 16 lines differ). Two items are TNM-only: the **Sean Boyd quote paragraph** and the phrase **"minted from Agnico Eagle Mines' (TSX, NYSE: AEM) Detour Lake mine"**.
- Images: the 4 featured images are the same files with the same captions on both channels; alt text empty on both; no inline body images on either.
- No digit appears on MINING.COM that is absent from TNM, except launch-copy prize values (C$1.3 million, US$1M) and its own deks/video blurbs (§3).

## 1. Coverage table (chapter × channel)

| Chapter / post | TNM (local + live REST, 17 Nov) | MINING.COM article | MINING.COM video page | CEO.CA |
|---|---|---|---|---|
| Launch (Aug 2025) | 1003881490 (dated 27 Aug 2025) | **found** 1185715, 13 Aug 2025 | **found** launch promo (19 Sep 2025) | not found |
| GP clue posts (first clue 1003882129, update 1003882997, GP clue releases 1003891906, 1003893488, 1003895789) | found | not found | not found | not found |
| 1 Dawson / Klondike | 1003882693 | not found | winner video only (Gina Anderson, 24 Sep 2025) | not found |
| 2 Cobalt | 1003883880 | **found** 1191289 | winner video (23 Oct 2025) | not found |
| 3 Golden Triangle | 1003884857 | not found | winner video (19 May 2026) | not found |
| 4 Argentia | 1003885834 | not found | winner video (20 Jan 2026) | not found |
| 5 Southern BC (Britannia) | 1003887086 | not found | winner video (11 Feb 2026) | not found |
| 6 Toronto | 1003888214 | not found | not found | not found |
| 7 Bathurst | 1003889390 | not found | NB winner video (upload folder 2026/06) | not found |
| 8 Val-d'Or | 1003890554 | **found** 1205095 | not found | not found |
| 9 Saskatchewan | 1003891553 | not found | not found | not found |
| 10 Nova Scotia | 1003892433 | **found** 1209385 | NS winner video (upload folder 2026/06) | not found |
| 11 Manitoba | 1003893604 | not found | not found | not found |
| 12 Sudbury | 1003894370 | not found | not found | not found |
| 13 Chibougamau / Nelligan | 1003895353 | not found | not found | not found |

How "not found" was established on MINING.COM: WP REST `posts?search=` for 18 terms (treasure, bonus prize, every chapter place name, Boyd, grand prize, …, after 1 Jul 2025); REST `search?subtype=any` for 6 terms; tag 193567 ("Treasure Hunt") and tag 193569 (named "193567"); site search pages (`/?s=`) for 19 terms, 2–3 pages each. Every hunt title on TNM contains "Treasure Hunt", and the site search for "treasure" listed only the items above. Video pages are a separate post type not exposed in REST; they were found through site search only, so a video page with an unusual title could still be missed.

## 2. Meaningful differences (digits, words, items present on one channel only)

### 2.1 Val-d'Or (confirms R-1170; no new difference)
- TNM https://www.northernminer.com/treasure-hunt/…/1003890554/ last line: **`810-419-227`**. MINING.COM https://www.mining.com/treasure-hunt-val-dor-gold-grit-and-the-road-to-the-north/ ends at "Nearly a century later, that foundation still holds." — **no trailer**.
- TNM line 11: "…many backed by capital from Toronto, the growing nerve centre of **:mining** finance that helped turn discoveries into operating mines." MINING.COM: "…the growing nerve centre of **mining** finance…". All other 26 lines identical.
- Timing (WP `date_gmt` / `modified_gmt`): MINING.COM published **30 Apr 2026 15:01 UTC**, last modified 18:12 UTC. TNM published **20:00 UTC**, modified 20:53 UTC. So MINING.COM's copy was live about five hours before TNM's, and was last edited before TNM published. This fits MINING.COM working from an earlier text, but it cannot show when the trailer or the colon entered TNM's copy (no web revision history is public).
- MINING.COM-only dek (WP excerpt, shown on the search list): *"The hunt intensifies as all eyes turn to Val-d'Or, Quebec's gold sector, a symbol of discovery and untapped potential."* Not in the TNM post, the TNM page HTML, or anywhere in the local TNM web corpus. Reads as a MINING.COM-written blurb.

### 2.2 Launch article (new; not in R-1169/R-1170)
TNM 1003881490 "$1M gold up for grabs as Canada Treasure Hunt begins" vs MINING.COM 1185715 "**C$1.3M in gold** up for grabs as Canada Treasure Hunt begins" (https://www.mining.com/1m-gold-up-for-grabs-as-canada-treasure-hunt-begins/; slug still says "1m"; modified 20 Aug 2025).
- **TNM only — Boyd quote (TNM line 2):** "“This Treasure Hunt acknowledges the pivotal role mining has played in the history of Canada and how the mining industry is very well positioned to make major contributions to community building and nation building now and in the future,” Agnico Eagle chair Sean Boyd said." MINING.COM has no Boyd paragraph at all.
- **TNM only — coin source:** TNM line 1 "…Great Canadian Treasure Hunt for $1 million in gold coins **minted from Agnico Eagle Mines’ (TSX, NYSE: AEM) Detour Lake mine and an additional 12 monthly $25,000 rewards** starts Wednesday, Aug. 13." MINING.COM line 1 "Organized by **MINING.COM‘s sister publication** The Northern Miner, the coast-to-coast Great Canadian Treasure Hunt for $1 million in gold **and 12 monthly yellow metal prizes worth $25,000 each** starts Wednesday, Aug. 13."
- **Digits changed:** TNM line 0 "There’s more than **$1 million** in physical gold…"; MINING.COM "There’s more than **C$1.3 million (US$1M)** in physical gold…".
- Words: "Vaccaro … **said**" → "**says**" (2×, lines 2/4 and 12). Sponsor list (line 14): MINING.COM adds "(TSX, NYSE: AEM)" after Agnico Eagle Mines.
- Dates: MINING.COM 13 Aug 2025 12:00 UTC (launch day). TNM's post id 1003881490 is dated **27 Aug 2025 18:40 UTC**, two weeks later.
- Present on both (noted so nobody rediscovers it): an Outlook SafeLinks-wrapped link from a PR agency mailbox (Brookline PR) to treasure.northernminer.com.

### 2.3 Winner video pages (MINING.COM) vs TNM winner posts — small text items
- Golden Triangle: TNM 1003891359 "have found **six 6-oz. gold pieces**"; MINING.COM video page "**six ounces of gold !**" (space before "!"). Both channels refer to the same prize. TNM's "six 6-oz." is the odd one (36 oz.); TNM's own Saskatchewan/Manitoba/Sudbury copy says "six ounces of gold".
- Nova Scotia: TNM 1003892442 "Cape **D’Or**" (capital D, twice); MINING.COM video page "Cape **d’Or**".
- New Brunswick: both channels write "Baker and **Rupert**" in the last sentence, against "Bella **Ruppert**" earlier (same typo on both channels, so TNM-origin).
- Dawson video page: "More than **61,000** Canadians are on the hunt for **$1.3M**"; TNM's Dawson video post 1003882796 says 55,000 (an earlier date). Ordinary update.
- Launch promo video page (MINING.COM only, 19 Sep 2025, YouTube KHxUFwPbEec): "More than 55,000 Canadians…"; "We’ve hidden an incredible prize: over $1.3 million in pure gold."; "**From coast to coast, every riddle pulls you closer.**"; "Yeehaw!". Promotional text, not in the TNM web-post corpus. R-1169 already treats "coast to coast" as stock marketing language.
- Video hosting differs: TNM winner posts embed **Vimeo** (1121913214, 1156621649, 1164487970, 1194124607, 1201513992, 1204275074); MINING.COM video pages embed **YouTube** (XkumTS-wbfg Dawson, vpg6k4uNGKs Cobalt, uSiAE9Vqa18 Argentia, aioXHhKHNSg Southern BC, UjdFUb_yxuU GT, yI4G07H6wMg NB, DN-d6lSd6cM NS, KHxUFwPbEec launch). **The video files themselves were not compared** (gap; would need a frame/audio diff).

## 3. Layout / CMS noise (recorded so it is not rediscovered)
- **Cobalt links:** MINING.COM's "Watch the video [English] | [French]" and "Read the full article in French" links go through email-tracking redirects on www3.northernminer.com (`/e/398282/VlmEkfQ-lEk/…`, `/e/398282/B37UGUUDoUI/…`, `/e/398282/10-Treasure-Hunt-Cobalt-FR-pdf/…`). TNM links straight to youtu.be/VlmEkfQ_lEk, youtu.be/B37UGUUDoUI and Treasure-Hunt_Cobalt_FR.pdf. The underscore→hyphen in the video id and the "10-" prefix are the tracker's slug rules. Same targets.
- **Launch links:** TNM links `https://northernminer.com/category/treasure-hunt/`; MINING.COM has `https://treasure.northernminer.com/` in that slot. Otherwise the same hrefs.
- **Deks (WP excerpts):** MINING.COM writes its own. Cobalt dek = a TNM body sentence trimmed ("This community – where less than 1,000 people live – once hosted one of the three great silver rushes of the Americas."). NS dek = TNM's first body sentence cut down ("Long before prospectors flooded the Klondike, Nova Scotia was already mining." — drops "in search of gold, long before Sudbury became synonymous with nickel and long before Saskatchewan uncovered its vast potash deposits,"). Launch dek: "The coast-to-coast Great Canadian Treasure Hunt will also give away 12 monthly prizes worth $25,000 each." Val-d'Or dek: §2.1.
- **Markup:** MINING.COM headings carry `id="h-…"` anchors; Val-d'Or and launch headings are wrapped in `<strong>` on MINING.COM only. Paragraph-tag counts differ (NS 43 vs 41: TNM puts the "IMPORTANT … found prior to the release" notice in a `<div>`, MINING.COM in `<p>`; Cobalt 48 vs 49; Val-d'Or 24 vs 25 = the trailer). Text identical apart from §2.
- **Launch paragraph split:** TNM's "Taking inspiration…" paragraph is split into two on MINING.COM (text the same).
- **Byline/tags:** MINING.COM author "Northern Miner Staff" on all 4 articles; Cobalt and NS carry tag id 193569 whose *name* is "193567" (R-1169 noted this); launch carries tag 193567 "Treasure Hunt"; Val-d'Or has no tag. CMS artefacts.
- **Publication times (UTC):** Cobalt MC 22 Oct 2025 20:48 / TNM 21:50. NS TNM 24 Jun 2026 11:05 / MC 17:17. Val-d'Or §2.1. Launch §2.2.
- **Featured images (identical on both):** launch `GCTH-YT-Thumbnail-scaled-1.jpg` ("Credit: Joe Bond"); Cobalt `jpg-BX0001-FD0054-FL0028-PH_Bags-Of-Ore-Awaiting-Shipment-1-1-2-scaled-1.jpg` ("Bags of silver ore awaiting shipment at the Cobalt camp’s LaRose property, July 15, 1905. Credit: The Northern Miner"); Val-d'Or `Aerial-view-of-Malartic-town-and-Canadian-Malartic-mine.jpg` ("Agnico Eagle Mines’ Canadian Malartic mine in Val-d’Or, Que. Credit: Agnico Eagle Mines"); NS `5golwf8a.png` ("Mining gypsum at the Milford Quarry, N.S. Credit: Nova Scotia Information Service/Wikimedia Commons"). Alt text empty on all eight.
- Emoji lines in Cobalt ("🎥 Watch the video…") hash identically; the 1-character length difference is only JS counting the emoji as two UTF-16 units.

## 4. Gaps
1. **CEO.CA — not readable as a visitor.** Checked signed-out in the Mac browser: `#treasurehunt` channel (only 2016–2017 unrelated posts), `@northernminer` profile (account joined May 2020, 0 articles; its feed shows its own 2022 event posts and other users' mentions up to Jul 2026; none about the hunt), `/articles` and `/editors` (no "treasure", "clue" or "Northern Miner" text), `/search` (a chat channel, not a search). CEO.CA's full-text search needs an account; a probe of CEO.CA's internal JSON API from the container was **refused by this session's safety check** and not retried. Web search (`site:ceo.ca`) returned no CEO.CA page about the hunt. R-1169 had: "Search not usable unauthenticated; carries the Newsfile releases". The Newsfile press releases themselves (newsfilecorp.com, already in Max's record, e.g. R-0020) were not re-diffed here. **Cheapest close-out:** Max, signed in to CEO.CA, searches "treasure hunt" and "Northern Miner" and lists any hunt post that is not a Newsfile release.
2. **MINING.COM from the container is blocked** (CloudFront 403 for curl and WebFetch). All MINING.COM reads went through the LMCP web session on Max's Mac, as an ordinary visitor: the public WP REST API (`/wp-json/wp/v2/…`), public article pages and the site's own search. Full article text was compared by line hashes (same normaliser in JS and Python), and every differing line was then read in full.
3. **Videos not diffed.** MINING.COM's YouTube uploads vs TNM's Vimeo/YouTube cuts were not compared frame by frame or by duration.
4. **No public revision history** on either WordPress, so the order in which TNM's trailer/colon and MINING.COM's copy were made cannot be fixed beyond the timestamps in §2.1.
5. Reader comments on MINING.COM video pages were seen and ignored (one contains a private person's email address; not copied).
6. Canadian Mining Journal (third syndication site, named in contest terms, not in the launch post's channel list) was out of scope; web search shows CMJ copies of at least the launch, first clue, Newfoundland winner and Nova Scotia posts.

## 5. Register
- **FACT (re-confirmed 17 Nov 2026):** R-1170 still holds on the live pages: MINING.COM Val-d'Or lacks `810-419-227` and the ":mining" colon. Cobalt identical (58/58 lines).
- **FACT (new):** NS identical on MINING.COM (48/48 lines).
- **FACT (new):** MINING.COM's launch copy lacks the Boyd quote and the "minted from … Detour Lake mine" phrase, and gives "C$1.3 million (US$1M)" for TNM's "$1 million".
- **FACT (new):** MINING.COM has no copy of 10 of the 13 chapter articles and no GP clue post. "Every post" on MINING.COM adds no chapter text beyond TNM's.
- **GAP:** CEO.CA unreadable signed-out; videos not diffed.
- Meaning: low. The one digit item (`810-419-227`) is TNM-only, as already recorded; the launch-copy differences are ordinary rewriting by a sister site.
