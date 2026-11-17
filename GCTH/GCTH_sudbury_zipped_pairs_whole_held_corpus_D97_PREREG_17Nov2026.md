# PREREG — D97: EN×FR zipped (item, letter) pairs over the WHOLE held text corpus, full word screen · 17 Nov 2026

**Ask:** Max, 17 Nov: "Don't we have a lot of long descriptive texts?", then "Yes, do everything the best way you can."
**Evidence label:** `pre_registration`. Filed before the corpus is counted or any read is made. Append-only. D97: the highest D in `~/GCTH/record` filenames is D96 (checked 17 Nov).
**Why this is not a re-run:**
- The 25 Sep wide sweep (1,954 texts) states: "Not covered: … (item, letter) pairs (underpowered, as in batch 3)".
- The 16 Nov THE-screen ran (item, letter) on 1,759 files but **kept only outputs beginning "the"** (an exploratory screen, not pre-registered). Any other message was discarded unread.
- The 26 Sep (unit, item) test covered the Sudbury article only.
- R-0379's bound (entry 76 ≥ 58 letters) says the key must be long descriptive text, which this corpus is.

## 1. Corpus (fixed by rule now; counts reported, not chosen)
- **A. Wide harvest:** every record with a `text` field in `~/GCTH/gcth_combined/gcth_wide_*.json`. That covers Wikipedia EN/FR, Canadian Encyclopedia, historicplaces, HMdb, ontarioplaques, Copper Cliff Notes, Northern Ontario Travel EN/FR, Science North/Dynamic Earth, museums, Vale, greatersudbury.ca / grandsudbury.ca, Discover Sudbury, Internet Archive books and book pages.
- **B. Held source texts on disk:** every `.txt` file of 300 B – 2 MB under `~/GCTH/TreasureHunt`, `~/GCTH/raw`, `~/GCTH/gcth_combined` and `~/GCTH/Downloads_hunt`.
  - Excluded: anything under `record/`, `archive/`, `_gcth_temp/`, `search/`, `venv`, `site-packages`, or any folder named `results*`.
  - **`.md` files are excluded** (they are project notes, not sources).
- **Dedupe:** exact duplicates after whitespace/case normalisation are counted once.

## 2. Units and reads (the Toronto shape: one number picks the item, the other picks the letter in it)
- **Items:** paragraphs (blank-line split), sentences (`. ! ?` split), lines. Letters only, accents folded to ASCII.
- **Reads:**
  - **Z1** group pairs (EN_i item, FR_i letter), 9 letters.
  - **Z2** (FR_i item, EN_i letter).
  - **D1** digit pairs (EN digit item, FR digit letter), 0 read as 10, 14 letters.
  - **D2** reversed.
- **Strict:** a read counts only if all positions are in range (no wrapping). 1-based.
- **Space:** texts × 3 item types × 4 reads. Arity deaths are counted and reported.

## 3. Scoring (fixed now)
- **Lexicon:**
  - EN and FR wordfreq top 50,000, accents folded, letters only;
  - plus the place list of D68 and the Whitewater / McMahon / Rouleau names;
  - plus direction and instruction words: north, south, east, west, nord, sud, est, ouest, under, behind, beneath, dessous, derriere, sous, rock, rocher, bridge, pont, bench, banc, tree, arbre, lookout, belvedere, treasure, tresor, cache.
- **Primary statistic S1:** reads containing a lexicon word of **≥ 7 letters** (any position).
- **Secondary S2:** best "coverage" per read, i.e. the share of letters covered by a non-overlapping tiling of lexicon words of ≥ 3 letters (Zipf ≥ 3.5 for 3–4-letter words). Report the top 30 reads by S2 for eye reading.
- **Null:** 20 random key pairs (seed 20261117), the same digit widths (EN 1,1,2,2,1,2,2,1,2; FR 1,1,2,2,1,2,2,2,1; two-digit groups have a non-zero lead), run through **exactly the same texts and reads**.
  - P(S1) = share of null keys whose S1 count ≥ the real one.
  - Top-S2 percentile against the pooled null S2 distribution.
- **Control (planted, copies only):** `WHITEWATER`, a 10-letter run inside a 14-letter D1 read, planted into a copy of one long EN text; and `DESSOUSPONT`, the same via D2 into a copy of one FR text. Each must be recovered in S1 and land in the top 30 of S2, or the run reports **instrument failed**.

## 4. Bar
- **Hit:** S1 P < 0.01 **and** at least one read that a person reads as words (≥ 2 words, or one ≥ 8-letter word in a 9/14-letter read), which survives a raw re-read of the source text at the stated positions.
- **Otherwise:** closed at chance for the held corpus. The key would then have to be an object we don't hold (physical labels or panels), as the 16 Nov solver hints already suggest.

## 5. Limits stated now
- Scrape text can differ from printed or posted text (line breaks, captions). Line-based reads are only as good as the capture.
- Large corpora produce chance short words. The bar is set on the null, not on any single output.
