# RESULT — D98: OCR of every hunt photo, then the EN×FR zipped-pair test on what it reads · 17 Nov 2026

**Pre-registration:** `GCTH_sudbury_zipped_pairs_on_every_hunt_photo_OCR_D98_PREREG_17Nov2026.md` (sha256 `86e34d87…`). Pushed before any OCR ran (commit 91b1941). Copied to the Mac folder during the OCR run, with a matching hash.
**Run (Mac):** `~/GCTH/TreasureHunt/_photo_ocr_D98_17Nov2026/`. Files:
- `list.txt`, `ocr_rapid.py`, `ocr.jsonl` (raw OCR);
- `d98.py`, `d98_out.txt`, `d98_result.json`;
- `photo_texts.md` (the text of every kept photo);
- `d98_diag.py`, `d98_diag_out.txt` (post-hoc diagnostics).

**Verdict by the pre-registered rules: INSTRUMENT FAILED.** The instrument check fell short of its bar, and one of the two planted controls was not recovered. The diagnostics below trace both failures to the test's set-up, not to the photos. On the primary statistic there were zero hits, against a null averaging 0.3. Nothing here points to a key. **Nothing is promoted.**

## Deviation from the PREREG (stated first)
- **OCR engine.** The PREREG named Apple Vision. The Vision script hung at 0 % CPU inside the LMCP sandbox and was killed before producing any output. All OCR was done with **RapidOCR 1.4.4** (onnxruntime, CPU) in a venv. HEIC files were converted with `sips -s format jpeg -Z 2200`. Lines are ordered by row, then by x. This change came before any result was seen.

## Material
- **Images:** 598 still images were OCR'd, with no errors.
- **Text found:** 500 had some text.
- **Kept** (≥ 10 lines or ≥ 300 letters): **358**.
- **After removing identical OCR texts: 348.**

## Pre-registered checks
- **Instrument check: FAILED as specified.**
  - The best single photo against `nsht_en.txt` was IMG_8453. It matched **27.4 %** of the reference letters; the bar was ≥ 90 %.
  - Cause (diagnostic 1): the panel was photographed in **pieces across six photos** (IMG_8449, 8453, 8454, 8456–8458). No single photo holds the whole text, so the check as written could not pass.
- **Controls: one of two recovered.**
  - `DESSOUSPONT` via D2 was recovered as `dessouspontpyy` → `dessous`.
  - `WHITEWATER` via D1 was **not recovered**: the read went out of range.

## Primary result (reported even though the instrument failed)
- **Reads fully in range: 483.** That is out of roughly 4,200 attempted (348 photos × 3 kinds of item × 4 reads).
  - Most photographed text is short lines.
  - Z1/Z2 need item 76 with ≥ 58 letters (R-0379). Almost no photo has that.
- **S1** (a lexicon word of ≥ 7 letters): **real 0.** Null `[1,1,0,0,2,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1]`. **P = 1.0.**
- **Reads beginning the / le / la / les: 12, all junk.**
  - `thecirxloolfia` (D2, IMG_8442).
  - The rest are `le…`/`la…`/`les…` strings such as `leitscnrverlea` and `lesycerorilban`.
  - None continues into a word.
- **Photos with ≥ 5 printed item numbers: 14.**
  - IMG_8433, IMG_8434, IMG_7393, IMG_7401, IMG_8093, IMG_8097, IMG_8139, IMG_8195, IMG_8196, IMG_8210, IMG_8602, IMG_8992, IMG_9007, image000000.
  - These were not vetted. The "highest number" values (up to 971) show that years and page numbers are being caught as item numbers.

## Post-hoc diagnostics (not pre-registered; labelled as such)
1. **The reader is accurate where the photo is clear.**
   - Share of each OCR line found word-for-word in the held race-track text:
     - IMG_8453: 0.98 (9 lines);
     - IMG_8454: 1.00 (5 lines);
     - IMG_8449: 0.51;
     - the angled shots (IMG_8456–8458): about 0.2.
   - The six photos together cover 58 % of the reference text.
2. **Line order is only partly kept.**
   - Adjacent OCR lines in the reference order: 5 of 7 (IMG_8453), 4 of 4 (IMG_8454), 10 of 17 (IMG_8449).
   - An OCR "line n" is therefore an unreliable stand-in for a sign's item n.
3. **The WHITEWATER failure was a bug in the planting code.**
   - The code padded only the 10 pairs it planted into. D1 has 14 pairs, and the last four, (9,4), (4,2), (2,5), (10,3), landed on short lines in IMG_8139, where items 4 and 5 are empty.
   - Padding all 14 pairs gives `whitewaterxxex`, which is recovered.
   - The D97 control passed only because its texts were longer.
4. **The solvers' ten-second test on every OCR'd photo.**
   - Test: digit pairs, item 6 letter 3 = T, item 2 letter 2 = H, item 7 letter 5 = E. Items: OCR lines, also with fragments under 3 letters dropped.
   - **Real: 2 photos.** Null (20 random first-three pairs): `[1,0,0,0,0,2,0,0,0,0,0,0,0,4,0,0,0,0,0,0]`. **P ≈ 0.14.** Both continue as junk:
     - **IMG_7788**, a Regreening Trail panel ("TRAJET DU REVERDISSEMENT DE SUDB…", "THE SO2 …"): D1 reads `the·ott?lnedhts`.
     - **IMG_7857**, a screenshot of a meteorite / gallery article: D1 reads `the·urrotrntift`.
   - IMG_7788 is worth a note only because D65 tied the recap's Sudbury detail to environmental restoration. Even so, its OCR lines are not the panel's own items, and the read does not continue.

## Register
- **Closed at the level this instrument can reach:** zipped EN×FR pairs over OCR lines, blocks and auto-detected numbered items of Max's 598 hunt photos. Zero lexicon hits; the ten-second test is at chance.
- **Not closed, and why:**
  - OCR lines are not the items of a physical numbered set.
  - Many signs were shot in pieces or at an angle.
  - Almost no photo carries text long enough for the Z reads (R-0379).
  - A real test of a photographed object needs its items transcribed by hand, from a straight-on photo, in the object's own numbering.
- **New for the record:** `photo_texts.md` holds the machine-read text of every photographed sign (348 unique). It is searchable, but **check against the photo before quoting.**
- **Method notes for future runs:**
  - Planted controls must pad every pair in the key, not only the planted ones.
  - An instrument check must compare like with like: a photo against the part of the reference it shows.
