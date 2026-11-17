# 6/6 split test family — DECLARED BEFORE RUNNING (17 Nov 2026)

Question (Max): could the 12 first bonus chapters split 6 and 6 into TWO codes, one per number
("two numbers mark the treasure's base", GP clue 5, Boyd video 15 Oct 2026)?

Written before any result was computed. Nothing below was changed after the run.

## 0. Chapter set and orders
The 12 = chapters 1-12 (Dawson ... Sudbury); Chibougamau (13) is excluded (it is the 13th release;
its clocks / CUFES2 are cited, not used).

* Order R (record, ledger and inventory numbering): 1 Dawson, 2 Cobalt, 3 Golden Triangle, 4 Newfoundland (Argentia/Dover),
  5 Southern BC (Britannia), 6 Toronto, 7 New Brunswick (Bathurst), 8 Val-d'Or, 9 Saskatchewan, 10 Nova Scotia,
  11 Manitoba, 12 Sudbury.
* Order C (as given in the brief): 1 Cobalt, 2 GT, 3 Argentia, 4 S. BC, 5 Toronto, 6 Bathurst, 7 Val-d'Or, 8 Klondike/Dawson,
  9 SK, 10 NS, 11 MB, 12 Sudbury. The record puts Dawson first (ledger, inventory, "Cobalt = Bonus Prize 2" video title),
  so C is tested only as a declared alternate for the order-dependent splits (a) and (b).

## 1. Number sources per chapter (each chapter's "code")
* **D = designed carrier** (leaf Morse, article trailer, article pair block), EN and FR:
  Dawson, Cobalt, GT, NL, S.BC: none (word leaves only). Toronto: the 60-pair block, digits concatenated (EN = FR).
  NB `1`. Val-d'Or EN `810419227` / FR `1045420275`. SK `2638`. NS `9`. MB `42` (from ALT42).
  Sudbury EN `62763732569420` / FR `32581671424253`.
* **W = article word count** (ledger "Compare the clues" table, EN / FR; validated against publisher PDFs).
* **P = article paragraph count** (same table, EN / FR).

## 2. Digit-keep rules (per chapter, then concatenated in the half's order)
first digit · last digit · digit sum mod 10 · whole code · leaf-digit only (D only: whole code of chapters whose
digit is a leaf — NB, SK, NS, MB, Sudbury; Toronto pairs and Val-d'Or trailer excluded).
A chapter with no digits in a source contributes nothing.
→ source×keep combos: D×5, W×4, P×4 = 13.

## 3. The 6/6 splits (half A / half B)
* (a_R) release halves, order R: {1-6} / {7-12}; within-half order R.
* (a_C) release halves, order C; within-half order C.
* (b_R) odd / even positions, order R. (b_C) odd / even, order C.
* (c) west / east by longitude of the chapter region: W = Dawson, GT, S.BC, SK, MB, Sudbury (-81.0);
  E = Cobalt (-79.7), Toronto, Val-d'Or, NB, NS, NL. Within-half order R.
* (d) chapters named in poem stanzas 2-7 vs the rest. Stanza map (project map, interpretive):
  S2 GT, S3 Nova Scotia, S4 Cobalt, S5 Sudbury, S6 Manitoba (Flinty; Chibougamau excluded), S7 Val-d'Or.
  Stanza half in stanza order; rest (Dawson, NL, S.BC, Toronto, NB, SK) in order R.
* (e) EN / FR: A = all 12 in order R from the EN source, B = the same from the FR source.
For (a)-(d) each is run once with EN sources and once with FR sources. Each split is run in both orientations
(A first / B first).  → 6 splits × 2 languages × 2 orientations + (e) × 2 orientations = **26 configurations**.

## 4. Readings of the pair (first number, second number)
* DEC: lat = first 2 digits + "." + rest; lon = first 2 or 3 digits + "." + rest (hit if either).
* DMS: DD MM [SS] lat; DD or DDD MM [SS] lon; MM, SS < 60.
* UTMz (zone from the digits, only if well-defined): zone = first 2 digits of the first number (must be 07-22),
  easting = next 6 digits (166000-834000), northing = first 7 digits of the second number (4,600,000-7,400,000); NAD83.
* UTM17/18: easting = first 6 digits of the first number, northing = first 7 of the second, zone 17 or 18 (hit if either).
* Ontario lot/concession and "lot/concession or township": REPORT ONLY / UNTESTABLE (no province-wide fabric map
  in hand; any small pair names a lot somewhere). Not counted as tries.
→ 4 testable reading families. **Declared tries = 26 × 13 × 4 = 1,352.**
A try whose real digits cannot form any reading of that family is VOID (the null has the same shape, so it cannot hit
either); voids are listed but not counted in m. Tries that repeat a CLOSED test (below) are skipped and cited.

## 5. Hit and null
* Hit = any reading of the try falls in lat 41.67-66.56 N, lon 52.6-141.0 W and on Canadian land
  (Natural Earth 1:50m, scratchpad/geo/canada.pkl — same checker as R-1325).
* Secondary flag: southern Shield ON/QC lake country box, lat 44.0-47.5 N, lon 73.5-81.5 W, on land.
* Null: 3,000 replicates. Per replicate, every chapter's code is redrawn with the same shape:
  D = uniform random digits of the same length (first digit 1-9); EN=FR codes stay identical within a replicate;
  W, P = uniform integers in the observed range of that source (W 759-2499, P 14-72), EN and FR drawn independently.
  All 1,352 tries are evaluated on each replicate (so the omnibus null keeps the correlation between tries).
* Per-try p = share of replicates where that try hits (if the real try hits; else p = 1).
* Correction: Holm and Bonferroni over m = non-void, non-repeat tries.
* Omnibus: total land hits and total ON/QC-box hits across the family vs their null distributions.
* Shortlist distances (report only, NOT evidence unless the try survives correction): Pink Lake 45.4668, -75.8082;
  Frontenac PP 44.52, -76.53; Tamara/Lac Pilon 46.0022, -74.0195.

## 6. Repeats of CLOSED tests (skipped, cited)
* (a_R) W-last and P-whole in DEC/DMS, orientation A-first: inside R-1325 Rules B/C (every contiguous split of the
  release-order strings).
* (a_R) D-leaf whole, A-first, DEC/DMS: inside R-1152 / R-1325 (leaf digits, release order, any split).
Everything else in this family is a non-contiguous or re-ordered split, or a keep rule / reading not used before.
