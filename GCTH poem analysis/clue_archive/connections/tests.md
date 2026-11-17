# GP connection map: desk tests (17 Nov 2026)

Written by a Claude Code subagent for Max. Desk only. Each test's rule was written in this file BEFORE its data were fetched or counted (file timestamps in `work/`). Numbers: R-PENDING / D-PENDING-CONN (none taken).

## PRE-REGISTRATION (written before fetching / counting)

### T1. Do TNM's statements about bonus clues and the Grand Prize actually contradict each other? (scope + dating)
Question: the record treats the statements as a contradiction resolved by a later policy change (region note §2.1: "a later policy (Aug–Oct 2026)"). Alternative: they never contradicted, because each answers a different question.
Data: (a) exact wording of the five statements, read raw from the Mac captures/rows; (b) Wayback Machine snapshots of treasure.northernminer.com/start-here/ (earliest = 2025-08-22) and /faqs/ (earliest available), to date the "Hunt Marker" paragraph and the FAQ "separate" answer; (c) the full 10 Dec 2025 Golden Triangle post.
Rule (fixed now): classify every statement on two axes: DIRECTION (poem -> bonus prizes, or bonus material -> Grand Prize) and OBJECT (the poem; one specific riddle; all monthly/bonus clue content). A CONTRADICTION = two statements with the same direction and overlapping object that give opposite answers.
- H_scope (no real contradiction) is supported if 0 contradictions remain after classification.
- H_change (TNM changed its position) is supported if >= 1 contradiction remains AND the earlier statement disappears from the site before the later one appears.
- If the start-here "Hunt Marker" paragraph (monthly clues "help sharpen your search" for the treasure the poem guides to) is present in the 2025-08-22 snapshot, record: "bonus -> GP" was stated at launch, before any bonus chapter.
- If Wayback cannot be read, T1 reports the wording-only result and says the dating is open.

### T2. Is the GP verse set unusually full of survey vocabulary? (the assumed glue between the Boyd card, the marker stanzas, McEwen's paces and TNM's "Hunt Marker")
Why: the map's biggest *assumed* link is a "survey theme" joining clue #5 ("set your sights by true design", "two numbers mark the treasure's base"), poem st. 9/12/13 (marker, "paths align", "beyond the mark", "compass"), McEwen ("paces", "north to south") and the clue-set name "Hunt Marker". The region note calls it "a real theme (signal medium)" without a count. Mining articles talk about claims, stakes and surveys all the time, so the question is whether the GP verses are richer in it than the chapter articles are.
Caveat stated up front: I have already read the GP verses, so the lexicon is not blind. To limit this, the lexicon below is fixed now, split in two, and CORE is limited to technical surveying words (most of which are NOT in the GP verses).
- CORE (technical; lemmas, EN, lower-case, plural/-ed/-ing forms counted): survey, surveyor, surveying, benchmark, bench-mark, meridian, baseline, transit, theodolite, chain (as a unit or not: counted), azimuth, bearing, boundary, lot, concession, township, monument, marker, cairn, stake, picket, datum, elevation, station, traverse, compass, sight, plat, grid, corner, borne, cadastre, cadastral, range. ("line" is in BROAD only.)
- BROAD = CORE + line, mark, base, true, north, south, align, design, pace, stride, declare, level, point, map
Corpus GP = poem EN (52 lines) + mirror quatrain + shadows tercet + McEwen card + Boyd card (EN text as recorded in R-1144, R-0038, R-0037, the poem file).
Null pool = the 12 regional + Chibougamau EN articles available as text (Dawson EN and Nova Scotia EN fetched from the Mac if possible; otherwise 11 + Chibougamau), tokenised the same way. Null = 10,000 random contiguous windows of the same token count as GP drawn from the pooled articles (window within one article).
Statistic: lexicon tokens per GP corpus (CORE and BROAD separately). P = share of null windows with count >= GP count.
Decision rule: the survey theme counts as a measured SIGNAL only if CORE P <= 0.05. BROAD is secondary and can only describe (it contains everyday words that a poem uses more than an article does: north, true, line). A pass says nothing about MEANING (no place follows from it).
Secondary (descriptive only): same CORE count for the FR poem with a fixed FR list: arpentage, arpenteur, borne, repère, méridien, ligne de base, jalon, piquet, cadastre, canton, rang, lot, boussole, visée, viser, relevé, station, monument, coin. 

Deviation note (before counting): in the FR secondary list I first added "marque" and "ligne", then removed them again before the run so the list matches the one above. In the CORE list, "range" stays; a stray note about "line" was tidied before counting. A stemming bug ("rang" turning into "range") was found on the GP side in a dry run and fixed before the real run; the fix only removes false hits.

---

## RESULTS

### T1 result: the statements mostly answer different questions. The "bonus feeds the GP" line was on the site at launch.
Raw quotes and snapshot list: `work/t1_evidence.md`.

| # | Statement (verbatim) | First seen | Still live? | Direction | Object |
|---|---|---|---|---|---|
| S1 | Start-here: "In addition to the poem, we'll release new clues every month … to help sharpen your search. Together, we call these the Hunt Marker – the keys to the gold." | Wayback 22 Aug 2025 (launch week, before the first bonus chapter on 18 Sep 2025) | yes (Wayback 28 Sep 2026; Max's capture 4 Sep 2026) | monthly clues → GP search | all monthly clues |
| S2 | FAQ: "Does the Grand Prize poem contain information about the Bonus Prizes? The Grand Prize treasure poem and the Bonus Prize clues are separate. Each Bonus Prize has its own dedicated set of clues. Any further interpretation is part of the challenge…" | between 10 Sep and 15 Oct 2025 (absent / present in Wayback) | yes (28 Sep 2026) | **poem → bonus prizes** (that is the question asked) | the poem |
| S3 | GT post: "This clue applies to a set of six one-ounce gold coin prizes … The clue does not apply to the main treasure hunt prize." | 10 Dec 2025 | yes (live page re-read 17 Nov 2026) | bonus → GP | **one riddle** (the 4-line GT riddle released after the GT chapter) |
| S4 | Support emails: "Grand Prize clues may be found / embedded in any treasure hunt content" (R-0041) | 18/24 Aug 2026 | (email) | any content → GP | everything |
| S5 | "As with all bonus clues, the Chibougamau clues also double as clues for the $1.3 million Grand Prize." (R-0611) | 5 Oct 2026 | (email) | bonus → GP | all bonus clues |
| S6 | Boyd card: "SEEK THE DIGITS COAST TO COAST, / FROM EVERY CHAPTER, EVERY POST." (R-1144) | 15 Oct 2026 | yes | chapters → GP | the digits in every chapter |

Classification under the rule:
- S2 answers the opposite direction (does the *poem* describe the bonus prizes?). Under the rule it cannot contradict S1, S4, S5 or S6. Its wording ("are separate") sounds two-way, which is why it has been read as a contradiction; its own last sentence leaves the door open.
- S1, S4, S5 and S6 all say the same thing: monthly / bonus content helps with the GP. S1 says it in **launch week (22 Aug 2025)**, so this is not a late policy change.
- **One overlap remains:** S3 (this one GT riddle does *not* apply) vs S5 ("all bonus clues" *do*). Neither was withdrawn: S3 is still on the live page on 17 Nov 2026. So the H_change test fails (nothing was taken down before the later statement), and H_scope holds **with one explicit carve-out**: TNM has excluded exactly one item, the 10 Dec 2025 Golden Triangle riddle.
- **Verdict (rule as written):** 1 residual contradiction, so strict H_scope is not met; H_change is not met either. Plain reading: the statements were never a policy U-turn. From launch, TNM said the monthly clues help the GP search (S1). Its only explicit exclusion is one supplementary riddle (S3). The FAQ is about the poem not describing the bonus sites.
- **What this changes:** (a) the region note's "later policy (Aug–Oct 2026)" (§2.1) is wrong on dating: the bonus→GP link is in the launch-week page. (b) The GT riddle is the one piece of chapter content TNM has expressly ruled out for the GP. The record's GT↔stanza-12 "structural twin" reading (R-1694) and the GT narration's "north to south" (R-1209) should carry that caveat. (c) S1 names the monthly-clue channels as "The Northern Miner, MINING.COM, or CEO.CA". That bears on S6's "every post" (see connection U3 in map.md).
- **Signal vs meaning:** signal HIGH (verbatim, dated, two languages for S1/S2). Meaning: it tells you **that** chapter content counts and **which item is excluded**. It does not tell you **how** to use it; S6 is still the only statement that names a mechanism (digits).
- Caveats: Wayback dates are capture dates, not publication dates (S1 could be older, not newer). S2's first capture falls between 10 Sep and 15 Oct 2025; the region note's "25 Sep 2025" is consistent with that but not confirmed here.

### T2 result: the "survey theme" is NOT a measured signal (pre-registered rule: CORE P ≤ 0.05; observed P = 0.062)
Raw output: `work/t2_result.json`; script `work/t2_survey_lexicon.py` (Mac copy `work/t2_mac_ascii.py`, run read-only by piping to python3).

| | GP verse set (poem EN + quatrain + tercet + McEwen + Boyd) | Null: 10,000 random 457-token windows from the 12 regional EN articles |
|---|---|---|
| tokens | 457 | 457 each |
| CORE hits | **4** (marker, compass, sight, SIGHTS) | mean 0.96; 95th percentile 4; max 7 |
| P(null ≥ GP), CORE | **0.062** | |
| BROAD hits | 21 (adds base, design ×2, line ×2, mark ×4 forms, north, south, paces, strides, true, align, declared, point) | P = 0.000 (descriptive only, by the rule) |

- **Decision:** CORE P = 0.062 > 0.05, so the survey theme does **not** count as a measured signal. Two of the four CORE hits are "sight", and one of those ("No miner's truth is held in sight", L20) is not surveying at all. Without it the GP count would be 3, which is below the null's 95th percentile (4); its exact P was not computed.
- BROAD is far above the null (P < 0.0001), but by the pre-registered rule it can only describe. Poems use "north", "true", "line" and "mark" much more than news articles do, so BROAD measures register as much as theme.
- Descriptive side result: among the 12 chapter articles, **Sudbury is the most survey-dense** (CORE 6.15 per 1,000 tokens: survey, surveyor, surveying, compass, township, chain; "plating" is a false hit), then Dawson (5.33: staking vocabulary). This agrees with the region note's observation that only the Sudbury chapter tells a compass-deflection survey story. It was not a pre-registered test.
- FR poem: CORE hits « borne » and « boussole » only.
- Deviation from the pre-registration: the null pool was the 12 regional EN articles in `~/GCTH/clues/01–12/article_EN.md` (Dawson and Nova Scotia included). Chibougamau was left out because it has no article_EN.md on the Mac. Header metadata above each file's first `---` line was dropped.
- **What this changes:** the map's biggest assumed glue (Boyd's "sights / true design / mark / base" + the marker stanzas + McEwen's paces + "Hunt Marker" = one survey design) stays **assumed**. The words are there; the count is not unusual for this corpus once you leave out everyday words. Not killed: the test was not blind, n is small, and the lexicon could be argued either way. Treat it as "not shown", not "closed".
