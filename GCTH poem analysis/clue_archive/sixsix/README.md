# GP "two numbers" — 6/6 chapter split · DESK · 17 Nov 2026

Max's question: could the 12 first bonus chapters (or the poem) split 6 and 6 into TWO codes, one per number
("two numbers mark the treasure's base", GP clue 5)?

**Answer: not as a coordinate, under any split, keep rule or reading in a declared 1,352-try family.
Nothing survives correction; nothing reaches p < 0.05 even uncorrected; the family as a whole lands on Canadian land
less often than random digits do.**

## Files
* `test_family.md`: the family, written before running (unchanged after).
* `numbers_table.csv`: every number each chapter carries (designed carriers + article structure counts), EN/FR, certainty.
* `run.py` (family + 3,000-replicate null), `analyze.py` (p, Holm, Bonferroni, omnibus, distances), `raw.json`, `results.json`.

## Numbers table, in short
* Designed digits exist only from chapter 6 on: Toronto 60-pair block (solved), NB `1`, Val-d'Or EN `810-419-227` / FR
  `1045-420-275`, SK `2638`, NS `9`, MB `42` (ALT42), Sudbury EN `62763732569420` / FR `32581671424253`.
  Chapters 1-5 (Dawson, Cobalt, GT, NL, S. BC) carry word leaves only. EN differs from FR only for Val-d'Or and Sudbury.
* Every chapter carries article word / paragraph / subhead / sentence counts (ledger, EN/FR; convention-dependent but
  validated against publisher PDFs).
* Release order: the record numbers Dawson 1 ... Sudbury 12 (Chibougamau 13). The brief listed Cobalt first and
  Klondike 8th; both orders were tested for the order-dependent splits.

## Run
* 26 configurations (6 splits × EN/FR × both orientations + EN-vs-FR × both orientations) × 13 source/keep combos ×
  4 reading families (decimal, DMS, UTM zone-from-digits, UTM zone 17/18) = **1,352 declared tries**.
* 580 void (the real digits cannot form that reading; mostly UTM needing 6-7-digit numbers, or a half with
  fewer than 2 designed digits, e.g. release half 1-6 has only Toronto). 12 repeats of CLOSED tests skipped (R-1325, R-1152).
  **m = 760 tested.**
* Null: 3,000 replicates; every chapter's code redrawn in the same shape (random digits; W/P uniform in the observed range).

## Results
| | real | null mean | P(null ≥ real) |
|---|---|---|---|
| tries landing on Canadian land | 16 | 41.1 | 0.97 |
| ...in the ON/QC southern box (44-47.5 N, 73.5-81.5 W) | 2 | 3.8 | 0.67 |

* Best single try: release halves (brief order), EN, designed codes, digit sum mod 10, decimal, second half first:
  49.962 N 91.000 W (NW Ontario, Cobb Bay), p = 0.060 uncorrected, Holm 1.0.
* All 16 land hits have uncorrected p 0.06-0.35; Holm and Bonferroni = 1.0 for all. **Survivors: none.**
* The two ON/QC-box hits are UTM readings of whole paragraph counts (odd/even and stanza splits):
  44.578 N 78.005 W (Kawarthas, 1.5 km from GeoNames "South Bay, ON"; 117 km from Frontenac PP, 199 km from Pink Lake) and
  44.571 N 81.360 W (Bruce Peninsula: inside the crude box but not Shield). p ≈ 0.33 each. Proximity is not evidence.
* Closest any hit comes to the shortlist: 117 km (Frontenac PP). Pink Lake ≥ 199 km, Tamara/Lac Pilon ≥ 350 km.
* The null for word/paragraph counts (uniform in range) is more coordinate-friendly than real counts (which cluster at
  1,000-2,000 words), so per-try p's for W/P are on the conservative side. No plausible null change brings any try near
  the Holm bar (~7×10⁻⁵ at m = 760), since every single try has a null hit rate of several percent.

## Untestable / not run
* Ontario lot/concession reading: report only. First-two-digit pairs from paragraph counts give e.g. Lot 30 Con 33,
  Lot 47 Con 22: concessions above ~16 are rare, and with no township named any lot/concession pair is unfalsifiable.
* "Township" readings: untestable without a township key in the clues.
* The poem as two codes: a 6/6 split of stanzas by count is a contiguous split of the poem count sequences,
  already CLOSED in R-1325 (17 sequences, every split). Not repeated.
* Readings outside this family (benchmark IDs, R-1215; word indices, R-1232; Alt codes, R-1227) are closed elsewhere.
