# PREREG — D98: OCR every hunt photo, then run the EN×FR zipped-pair test on every sign or display it reads · 17 Nov 2026

**Ask:** Max, 17 Nov: "Keep going." It follows D97 (closed: zipped pairs on every text we hold). The one branch left is a **physical** set of numbered or labelled items whose text we don't hold. The best untapped source of such text is Max's own photos.
**Evidence label:** `pre_registration`. Filed before any OCR is run. Append-only. D98 = D97 + 1.

## 1. Material
- Every still image (`.heic .jpg .jpeg .png`) in `/Volumes/MaxArchive/GCTH Hunt Photos from phone/` (Max's 603 hunt items, exported 6 Nov).
- Plus `~/GCTH/media/field photos/`.
- Videos (`.mov`) are skipped.

## 2. OCR (instrument)
- Apple Vision `VNRecognizeTextRequest`, accurate level, languages en-CA + fr-CA, language correction on. Implemented as a Swift script.
- Output per photo: recognised lines in reading order (top to bottom), with confidence.
- **Kept:** photos with ≥ 10 recognised lines, or ≥ 300 letters.
- **Instrument check before any key is applied:** the OCR of one photo whose text the record already holds verbatim must reproduce it to ≥ 90 % of characters. That photo is the 26 Sep NSHT Race Track panel (`nsht_en.txt`), if present in the set; otherwise the Salter plaque photo or any held sign.

## 3. Reads (the same as D97)
- **Items:**
  - (a) OCR lines;
  - (b) OCR text blocks (lines grouped by vertical gaps);
  - (c) **numbered items**: where a photo shows printed item numbers (a line starting with 1–3 digits), items are taken by their printed number.
- **Reads:** Z1, Z2 (group pairs, both directions), D1, D2 (digit pairs, 0 → 10). Strict range. Letters only, accents folded.
- **Ten-second test, logged separately:** reads beginning `the` (EN) or `le`/`la`/`les` (FR).

## 4. Scoring and bar (from D97, with S2 dropped because it failed its control there)
- **S1:** a lexicon word of ≥ 7 letters. Same lexicon as D97.
- **Null:** 20 random key pairs, same widths, same photos and reads. P = share of null keys with an S1 count ≥ real.
- **Controls:** `WHITEWATER` via D1 and `DESSOUSPONT` via D2, planted into copies of the two longest OCR texts. Both must be recovered, or the run reports **instrument failed**.
- **Hit:** S1 P < 0.01 and a read that a person reads as words, surviving a check against the photo itself. **Or** any read that is a sentence beginning "The", checked against the photo.
- **Otherwise:** closed at chance for the photographed objects. The output still gives the record the **text of every photographed sign**, kept in the run folder.

## 5. Limits stated now
- OCR misses small, angled or shadowed text. A miss is not a negative for that object.
- Photos of the same sign from several angles count once only if the OCR texts are identical. Otherwise all are run (correlated, so the null is conservative).
