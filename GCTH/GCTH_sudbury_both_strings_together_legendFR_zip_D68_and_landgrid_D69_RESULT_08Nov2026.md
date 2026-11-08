# RESULT — D68 (zipped EN×FR pairs on the French OF 4570 legend) + D69 (EN×FR as township / lot / concession) · 08 Nov 2026

**Pre-registration:** `GCTH_sudbury_both_strings_together_legendFR_zip_D68_and_landgrid_D69_PREREG_08Nov2026.md` (sha256 `eb8c3629…`), pushed before either run.
**Run folder (Mac):** `~/GCTH/TreasureHunt/_both_together_D68_D69_08Nov2026/` — `d68.py`, `d68_out.txt`, `d68_result.json`, `d69_pull.py`, `cityowned_twp_lot_con.json`, `d69.py`, `d69_out.txt`.

## D68 — CLOSED at chance
- **48 schemes:** 2 directions × FR and EN legend text × letters / characters × strict / wrap × measured / dot-dash-swapped / reversed.
- **Arity:** no scheme puts all 9 pairs in range. The best is 8 of 9. On the measured reading, EN→unit fails on unit 4, *Formation de fer* / *Iron-formation* (14 letters), which needs letter 25.
- **Word screen** (any ≥ 6-letter word from the EN or FR top 50k, accents folded, plus 39 local place names): **0 of 48** schemes. Null of 10,000 random key pairs with the same digit widths: mean 0.04. **P = 1.00.**
  - Detector control: `creighton`, `lookout` and `tresor` are found when planted.
- Measured outputs, for the record: EN→unit on FR letters `aonrtci_r`, FR→unit on FR letters `sos_cetma`, EN→unit on EN letters `tamrtol_o`. Junk.
- **Consequence:** the 19 Sep bound (a list whose entry 76 carries ≥ 58 letters) is met by the OF 4570 legend in both languages, and the legend still says nothing in either. The legend is now closed for zipped reads in both languages.

## D69 — CLOSED (arity and chance)
- **Reference:** the City of Greater Sudbury `City_Owned_Property_view` has 10,981 rows and 29 township codes, with lots up to 12 and concessions up to 6.
  - The `Parcels` layer carries no lot or concession fields, so it was not usable.
- **Results by reading** (share of the pairs or triples that are possible survey addresses):

| reading | valid share | P (null ≥ real) |
|---|---|---|
| R1 group pairs (EN, FR) as (lot, con) | 0.22 (2 / 9) | 0.74 |
| R2 (FR, EN) | 0.33 | 0.31 |
| R3 digit pairs (EN, FR) | 0.79 (11 / 14) | 0.16 |
| R4 (FR, EN) | 0.71 | 0.34 |
| R5 EN triples (twp, lot, con) | 0 / 3 | 1.00 |
| R5 FR triples | 0 / 3 | 1.00 |

- **No reading is all-valid, and none beats chance.** Only (6, 3) and (2, 2) are possible lots and concessions. Every two-digit group exceeds the grid (lots ≤ 12, concessions ≤ 6). Closed.

## Register
- **"Both numbers together": status after 8 Nov.** Every concrete pairing proposed so far is closed:
  - combined sums (plaques, wide sweep);
  - zipped (item, letter) on P.2603 and on both OF 4570 legends;
  - (unit, item) into the article;
  - cross-swap;
  - weave (D33);
  - same-message EN/FR (175 pairs; D28);
  - coordinates; pairs drawn as points; per-group sums and differences as letters;
  - land-survey grid (D69).
- **What the idea still allows**, untested: a **physical** two-part lookup, where one string selects an object (a panel, plaque or post) and the other selects a position on it. That needs the object first. The measured bound stands: entry 76 carries ≥ 58 letters (or entry 58 ≥ 76 and entry 24 ≥ 69).
