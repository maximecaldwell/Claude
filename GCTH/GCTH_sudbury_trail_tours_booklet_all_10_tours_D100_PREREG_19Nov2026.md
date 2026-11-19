# PREREG — D100: the leaf numbers read on all 10 tours of Rainbow Routes' "Trail Tours" booklet (EN + FR) · 19 Nov 2026

**Ask:** Max, 19 Nov: "Test everything" … "go ahead". Checked first: no earlier test of this booklet exists in the record (the repo). The 17 Nov sweep of every held text (D97) did not include the booklet, which was first fetched for D99.
**Evidence label:** `pre_registration`. Filed before any key is applied to these items. Append-only. D100 = D99 + 1.

## 1. Material
- **The booklet:** "Trail Tours / Les visites de sentiers" (Rainbow Routes, 2007). It is the same pair of PDFs as D99:
  - EN `85b0c083…`, FR `a3b03b99…`;
  - in `~/GCTH/TreasureHunt/_jane_goodall_posts_D99_17Nov2026/`.
- **Text:** extracted with Apple PDFKit (`pdftext.swift` `0c3d1cd5…`) into `en.txt` `dcda66e6…` and `fr.txt` `b7044c79…`.
- **Items:** built by `build_items.py` (`ae2e9abf…`) into `items100_EN.json` `8464a59a…` and `items100_FR.json` `0833b5b3…`.
- **Run folder:** `~/GCTH/TreasureHunt/_trail_tours_all_D100_19Nov2026/`.
- **84 items per language**, numbered by the booklet's own rule (marker number = order of the descriptions in each tour):

  | Tour | Trail | Items |
  |---|---|---|
  | 1 | Hillfield | 9 |
  | 2 | Kelly Lake | 10 |
  | 3 | Oak Forest | 6 |
  | 4 | Blueberry Hill | 8 |
  | 5 | Jane Goodall | 9 |
  | 6 | Capreol | 10 |
  | 7 | A.Y. Jackson Lookout | 10 |
  | 8 | Rotary Park | 9 |
  | 9 | Lake Laurentian | 7 |
  | 10 | Selkirk | 6 |

- **Item text** (fixed rule, in the builder):
  - **T** = the canonical title.
  - **B** = everything after the title up to the next title. That includes direction lines, "I Will Survive" tips and stray map labels. In tour 1 (EN), the first two items' text layer is partly scrambled in the PDF and is used as is.
  - **TB** = T then B.
- **Disclosure:**
  - Before this PREREG, the builder printed only titles, line numbers and body lengths. No body letters were viewed for tours 1–4 or 6–10.
  - Tour 5 was read in full for D99.

## 2. Reads
- **Strings:** EN `62763732569420`, FR `32581671424253`.
- **Per-tour numbering** (items 1..n within each tour):
  - D1 (EN digit = item, FR digit = letter) and D2 (the reverse), with 0 → 10.
  - D1 is strict. If it goes out of range, its 13-pair prefix is read instead (as in D99).
  - D2 is strict.
  - Grid: 10 tours × 2 languages × 3 sets × 2 reads = **120 reads**.
- **Global numbering** (items 1..84 in booklet order):
  - Z1 (EN group = item, FR group = letter), Z2 (the reverse), D1 and D2, all strict.
  - Grid: 2 languages × 3 sets × 4 reads = **24 reads**.
  - Global numbering is the only scheme in the record so far with an item 76, so it is the first real test of the R-0379 bound for Z1/Z2.

## 3. Scoring and bar (as in D99)
- **S1:** a lexicon word of ≥ 7 letters in a read.
- **THE:** the read begins `the` (EN) or `le` / `la` / `les` (FR).
- **Null:** 5,000 random string pairs (14 uniform digits each, same group widths), on the same 144 reads with the same prefix rule. P = share of null keys scoring ≥ the real key's count, for S1 and for THE separately.
- **Hit:**
  - (a) a read a person reads as words, with P < 0.01 on S1 or THE; or
  - (b) a read that begins "the"/"le…" and continues as words.

  A hit is a lead for Max, not a location.
- **Otherwise:** closed at chance for the whole booklet.

## 4. Controls
- `WHITEWATER` is planted via Z1 into a copy of the global EN TB items.
- `DESSOUSPONT` is planted via D2 into a copy of tour 2's FR TB items.
- Every pair is padded first. Both must be recovered by S1, or the run reports **instrument failed**.

## 5. Limits stated now
- This tests the 2007 booklet text, not what is on the physical markers today.
- Item boundaries come from a text layer with layout artefacts (merged title lines, map labels). The builder's rule is fixed above and applied blind.
- **Run files committed with this PREREG** (in `GCTH/D100_run/`): `build_items.py`, `pdftext.swift`, `d100.py`.
