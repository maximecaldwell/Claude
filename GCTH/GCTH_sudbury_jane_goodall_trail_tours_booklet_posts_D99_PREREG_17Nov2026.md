# PREREG — D99: the leaf numbers read on the Jane Goodall Reclamation Trail's 9 numbered posts (Rainbow Routes "Trail Tours" booklet, EN + FR) · 17 Nov 2026

**Ask:** Max, 17 Nov: "Yes, please." He was answering: "look up whether the Regreening trail, or another Sudbury site, has a numbered set of stations or plaques."
**Evidence label:** `pre_registration`. Filed before any key is applied. Append-only. D99 = D98 + 1.

## 1. What was found (desk lookup, before this PREREG)
- **Source.** The Ontario GeoTour booklet *Jane Goodall Reclamation Trail* (files.ontario.ca, 2021) says: "A trail guide … describes 9 points of interest that are marked with posts along the trail."
- **The guide itself.** That guide is Rainbow Routes' free bilingual booklet **"Trail Tours / Les visites de sentiers" (2007)**, retrieved from the Internet Archive capture of 29 Apr 2016:
  - EN: `trail_tours_guide_EN_2016.pdf`, sha256 `85b0c083…`.
  - FR: `trail_tours_guide_FR_2016.pdf`, sha256 `a3b03b99…`.
  - Saved in `~/GCTH/TreasureHunt/_jane_goodall_posts_D99_17Nov2026/`.
- **How the booklet describes itself:** "On the trails you will notice trail markers that will have a corresponding number to its description in the booklet." The FR edition: "des balises … sur lesquelles figurera un chiffre correspondant à sa description dans le livret."
- **The trail's section (tour 5) has 9 items, in this order:**

  | # | EN | FR |
  |---|---|---|
  | 1 | Two Million + Trees | Plus de deux millions d'arbres |
  | 2 | Acid Needles | Des aiguilles acides |
  | 3 | Stumps | Des souches ancrées dans le temps |
  | 4 | Black Locust | Le robinier faux-acacia |
  | 5 | Lookout #1 | Belvédère no 1 |
  | 6 | Little Birch | De petits bouleaux |
  | 7 | Glacial Meltwater Channel | Un chenal d'eau de fonte glaciaire |
  | 8 | Lookout #2 | Belvédère no 2 |
  | 9 | Two-Toned Rock | Un rocher à deux couleurs |

- **Cross-check:** the GeoTour's own marker numbers agree with this order. Marker 1 is the 2-millionth tree, marker 3 the stump, marker 5 the first lookout, marker 8 the second lookout.
- **Why it fits the 16 Nov solver hints:** a physical, free set of numbered, labelled items in town, in both EN and FR. The 7 Nov recap concept ("environmental restoration", D65) also points to this trail.
- **Against it:**
  - The trail was heavily searched (D65: three Reddit users).
  - The booklet is from 2007, and today's posts may differ.

## 2. Disclosure: what I saw before writing this
While reading the text I noticed, without trying to:
- **Item 6, title** ("Little Birch"), letter 3 = **t**.
- **Item 2, body** ("When you look down…"), letter 2 = **h**.

These are the solvers' first two ten-second letters under D1. Nothing else was checked: no full read and no other item.

## 3. Items (fixed now; transcribed from the PDFs' text layer into `items_EN.json` / `items_FR.json` before the run)
- **T:** the 9 titles.
- **B:** the 9 bodies (the description paragraph), in full.
- **TB:** title followed by body.
- **Variant +tip:** the "I Will Survive" / « Je survivrai » tip box printed after item 7 is attached to item 7's body. Primary excludes it.
- **Letters:** letters only, accents folded, digits and punctuation dropped (so "Lookout #1" = `lookout`).

## 4. Reads
- **Strings:** EN `62763732569420`, FR `32581671424253`.
- **D1:** item = EN digit, letter = FR digit. **D2:** item = FR digit, letter = EN digit. In both, 0 → 10.
- **Range:**
  - D1 needs item 10 (its last pair is (10,3)), which a 9-post trail lacks. D1 is reported strict (it will go out of range at its last pair) and also as its 13-pair prefix. That prefix rule is fixed now.
  - D2's items are all ≤ 8, so D2 is fully in range wherever the letters exist.
- **Z1/Z2 are not run:** they need items up to 76.
- **Grid:** 2 reads × 2 languages × 5 distinct item sets (T, B, TB, B+tip, TB+tip; T has no tip variant) = **20 reads**.
- **Run files, committed with this PREREG:** `items_EN.json`, `items_FR.json`, `d99.py` (in `GCTH/D99_run/`).

## 5. Scoring and bar
- **S1:** a lexicon word of ≥ 7 letters in the read (D97/D98 lexicon).
- **THE:** the read begins `the` (EN) or `le` / `la` / `les` (FR).
- **Null:** 10,000 random string pairs.
  - Each pair has 14 random digits per string, so the 0 → 10 rate matches.
  - Scored on the same 24 reads, with the same prefix rule.
  - P = share of null keys scoring ≥ the real key's count, separately for S1 and THE.
- **Hit:**
  - (a) any read that a person reads as words (two or more real words in a row, or one sentence fragment), with P < 0.01 on S1 or THE; or
  - (b) a read that begins "the" and continues as English words.
  - **A hit is still not a location.** It goes to Max as a lead.
- **Otherwise:** closed at chance for this booklet's text of this trail.

## 6. Controls
- `WHITEWATER` is planted via D2 into a copy of the EN TB items. Every pair is padded first (the D98 bug is fixed).
- `DESSOUSPONT` (11 letters) is planted via D2 into a copy of the FR TB items.
- Both must be recovered by S1, or the run reports **instrument failed**.

## 7. Limits stated now
- These are the 2007 booklet's descriptions. The physical posts may carry only a number, and their text, order or count may since have changed.
- With 24 reads, a real signal must be strong to show. A null result here does not close the posts as physical objects.
