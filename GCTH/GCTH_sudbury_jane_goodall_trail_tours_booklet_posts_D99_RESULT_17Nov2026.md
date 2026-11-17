# RESULT — D99: the leaf numbers read on the Jane Goodall trail's 9 numbered booklet items (EN + FR) · 17 Nov 2026

**Pre-registration:** `GCTH_sudbury_jane_goodall_trail_tours_booklet_posts_D99_PREREG_17Nov2026.md` (sha256 `59c46a42…`), commit fe95a9d. It was pushed with the run files before the run:
- `D99_run/items_EN.json` `6261ab3a…`
- `D99_run/items_FR.json` `be0eaad4…`
- `D99_run/d99.py` `01e5bfd5…`

All four hashes were re-checked on the Mac before running.
**Run (Mac):** `~/GCTH/TreasureHunt/_jane_goodall_posts_D99_17Nov2026/`. Files: `d99_out.txt`, `d99_result.json`, and both booklet PDFs.
**Verdict: CLOSED at chance.** The instrument is OK: both controls were recovered. No read contains a word, and none begins "the" / "le" / "la" / "les". **Nothing is promoted.**

## What was tested
- **Source:** Rainbow Routes' free bilingual "Trail Tours" booklet (2007), tour 5. Its 9 items correspond to the trail's 9 numbered posts.
- **Reads:** the leaf digits, read as D1 (EN digit = item, FR digit = letter) and D2 (the reverse), with 0 → 10.
- **Item sets:** titles, bodies, and title+body, each with and without the "I Will Survive" tip box. EN and FR booklets.

## Result
- **Reads in range: 18 of 20.**
  - EN titles were out of range for both D1 and D2: titles such as "Stumps" are too short for the letter numbers.
  - D1 always needs item 10, so it is reported as its 13-pair prefix, as pre-registered.
- **All 18 reads:**

| Booklet | Items | D1 (first 13 pairs) | D2 |
|---|---|---|---|
| EN | bodies | `ihocmuewkhtly` | `rhiuotnwkounor` |
| EN | title+body | `tciisamakitln` | `sctuobawkeudoy` |
| FR | titles | `peesdncdveoei` | `ueedutclbgeaes` |
| FR | bodies | `txzrvvoeaeaei` | `rxevuayebnemee` |
| FR | title+body | `peesdncdveoei` | `ueedutclbgeaes` |

  The tip variants are identical to the rows without the tip: none of the pairs reach the added text.
- **S1** (lexicon word ≥ 7 letters): **0.** Null mean 0.002 over 10,000 random keys. P = 1.0.
- **THE start:** **0.** Null mean 0.039. P = 1.0.
- **Controls:** `whitewaterudoy` → `whitewater` and `dessouspontaes` → `dessous`. Both recovered.

## About the letters seen before the PREREG
- The solvers' ten-second test needs D1 letters T, H, E from items 6, 2 and 7.
- The 3-letter starts actually produced are:
  - `tci` (EN title+body): item 6 gives "t", but item 2's 2nd letter is "c" ("Acid Needles").
  - `iho` (EN body).
  - `pee` / `txz` (FR).
- The "t" (item 6 title) and "h" (item 2 body) noticed earlier come from different item sets, so no single reading gives `the`. The test fails on this booklet.

## Register
- **Closed:** the leaf numbers on the Jane Goodall Reclamation Trail's numbered points, as written in the 2007 Trail Tours booklet (EN and FR, all item sets).
- **Not closed:**
  - What the posts themselves carry today, if it differs from the booklet.
  - The other nine tours in the same booklet. Each tour is a numbered set with the same EN/FR structure; listed for Max to decide, not run.
- **New for the record:** both booklet PDFs are saved, with hashes, in the run folder. The booklet is a free, bilingual, numbered set for 10 Sudbury trails, and it shapes the record's picture of what "numbered, labelled items" in town can look like.
