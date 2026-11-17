# GP "two numbers" as a 6/6 chapter split · DESK + RESULT (CLOSED) · 17 Nov 2026 · D-PENDING-SIXSIX

**Ask (Max, via cloud session):** could the 12 first bonus chapters (or the poem) split 6 and 6 into TWO codes, one per number of GP clue #5 ("two numbers mark the treasure's base")?
**Evidence label:** `desk_test`. Family declared in writing before running (cloud scratch `sixsix/test_family.md`). Append-only. Nothing in `record/` was edited.

## Repeats checked first (CLOSED, cited, not re-run)
R-1325 (Rules B/C, every contiguous split, release + clock order; article codes; leaf digits; stanza-ordered digits; T9/A1Z26; poem counts), R-1152 (leaf digits, release order), R-1179 (clock-order assembly), R-1181 (ALT weave Sudbury EN/FR), R-1190, R-1227 (Alt codes), R-1232 (cross-chapter word indices), R-1215 (benchmark ID). 12 tries in this family that would repeat R-1325 / R-1152 (release halves 1-6/7-12, word-count last digit, paragraph counts whole, leaf digits; decimal/DMS, first half first) were skipped.

## Numbers each chapter carries (record order; Chibougamau = 13, excluded)
| # | Chapter | Designed digits EN / FR | Words EN/FR | Paras EN/FR | Certainty |
|---|---|---|---|---|---|
| 1 | Dawson | none (BRIDGE) | 1664/1889 | 30/26 | certain (no digit carrier) |
| 2 | Cobalt | none (STEPS) | 1991/2328 | 47/47 | certain |
| 3 | Golden Triangle | none (KLEANZA) | 1541/2038 | 48/49 | certain |
| 4 | Newfoundland | none (WALNUT) | 759/877 | 14/14 | certain |
| 5 | Southern BC | none (BOOM) | 1527/2031 | 33/35 | certain |
| 6 | Toronto | 60-pair block (= FR) | 1958/2442 | 34/31 | printed, solved |
| 7 | New Brunswick | 1 / 1 | 1103/1320 | 33/35 | measured, post hoc class |
| 8 | Val-d'Or | 810-419-227 / 1045-420-275 | 957/1127 | 22/22 | printed |
| 9 | Saskatchewan | 2638 / 2638 | 1272/1608 | 49/51 | high |
| 10 | Nova Scotia | 9 / 9 | 1125/1453 | 37/40 | measured, post hoc class |
| 11 | Manitoba | 42 / 42 (ALT42) | 1195/1476 | 36/35 | high |
| 12 | Sudbury | 62763732569420 / 32581671424253 | 2077/2499 | 71/72 | digits measured, parse open |
Counts are the Clue Number Ledger's (validated convention). EN differs from FR in designed digits only for Val-d'Or and Sudbury.
**Order note:** the session brief listed Cobalt as release 1 and Klondike as 8; the record numbers Dawson 1. Both orders were tested where order matters.

## Family (declared before running)
* Splits: (a) release halves, record order and brief order; (b) odd/even, both orders; (c) west/east by region longitude (W = Dawson, GT, S.BC, SK, MB, Sudbury); (d) stanzas 2-7 (GT, NS, Cobalt, Sudbury, MB, Val-d'Or; project map, interpretive) vs the rest; (e) EN number / FR number of all 12. (a)-(d) in EN and FR; all in both orientations: 26 configurations.
* Sources x keep rules: designed digits (first, last, sum mod 10, whole, leaf-only), word counts and paragraph counts (first, last, sum mod 10, whole): 13.
* Readings: decimal, DMS, UTM with zone from the digits, UTM zone 17/18 (NAD83): 4. Lot/concession and township: report only / untestable.
* **1,352 declared tries; 580 void (digits cannot form that reading), 12 repeats skipped; m = 760 tested.**
* Hit = Canadian land, 41.67-66.56 N, 52.6-141 W (the R-1325 checker). Null: 3,000 replicates, every chapter code redrawn in the same shape. Holm and Bonferroni over m.

## Result: CLOSED, at or below chance
* Land hits: **16 of 760 vs null mean 41.1** (P(null >= 16) = 0.97, so fewer than random digits give).
* ON/QC southern box (44-47.5 N, 73.5-81.5 W): **2 vs null 3.8** (P = 0.67). Both are UTM readings of whole paragraph counts: 44.578 N 78.005 W (Kawarthas, near "South Bay") and 44.571 N 81.360 W (Bruce Peninsula area, not Shield); p ~ 0.33 each.
* Best single try p = 0.060 uncorrected (brief-order release halves, EN, designed digits, digit sum mod 10, decimal: 49.962 N 91.000 W, NW Ontario). **Holm = Bonferroni = 1.0 for every try. Survivors: none. No try reaches p < 0.05 even uncorrected.**
* Shortlist proximity (reported, not evidence): closest hit is 117 km from Frontenac PP; Pink Lake >= 199 km; Tamara/Lac Pilon >= 350 km.
* The word/paragraph null (uniform in range) is a little more coordinate-friendly than the real counts, so those p's lean conservative; with every try's null hit rate in the percent range, no null choice gets near the Holm bar (~7e-5).

## Still untestable / open
* Ontario lot/concession: any pair names a lot somewhere; first-two-digit pairs give concessions 22-49 (rare in ON). Township reading needs a township key the clues don't give.
* Poem 6/6: a stanza split by counts is a contiguous split of the poem count sequences, already closed (R-1325).
* Chapters 1-5 carry no designed digits, so any 6/6 split built on designed carriers is lopsided by construction (release half 1-6 has only Toronto). This repeats the coverage gap noted 24-30 Oct.

**Files (cloud scratch, disposable):** `sixsix/test_family.md`, `numbers_table.csv`, `run.py`, `analyze.py`, `results.json`, `README.md`.

**Suggested row (for Max to file; not written as a ROWS_PENDING csv):** Grand Prize, CLOSED: "6/6 chapter split of the 12 bonus chapters into two numbers (release halves both orders, odd/even, west/east, poem stanzas 2-7, EN vs FR; designed digits, word and paragraph counts; first/last/sum-mod-10/whole/leaf; decimal, DMS, UTM): 760 tested tries, 16 land hits vs null 41, 2 ON/QC vs 3.8; best p 0.06 uncorrected, Holm 1.0. Closed."
