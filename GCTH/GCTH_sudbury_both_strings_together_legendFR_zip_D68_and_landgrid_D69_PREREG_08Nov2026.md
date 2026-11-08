# PREREG — "Both numbers together": D68 (zipped EN×FR pairs on the FRENCH OF 4570 legend) + D69 (EN×FR as Ontario township / lot / concession) · 08 Nov 2026

**Ask:** Max, 8 Nov: "Can we work with the idea that you need both numbers together?", then "Do it all". Claude proposed exactly these two.
**Evidence label:** `pre_registration`. Filed before either run. Append-only. D68/D69 follow D67 (this session).
**Already closed, not re-run:**
- EN±FR combined on plaques (93,600) and wide (15.1 M reads).
- Zipped (item, letter) on OGS P.2603 (arity) and on the **English** OF 4570 legend (24 schemes, 19 Sep).
- (unit, item) into the article (672).
- Cross-swap (2,048).
- D33 weave.
- D28 EN6/FR9.
- FR legend as a **whole-text** key (25 Sep).
- Today's quick checks: coordinate combos, pairs drawn as points, per-group sums/differences as letters (all empty).

**Keys:** EN groups `6 2 76 37 3 25 69 4 20`; FR groups `3 2 58 16 7 14 24 25 3` (FR digit 13 = 5). Digit strings EN `62763732569420`, FR `32581671424253`.

## D68 — zipped pairs on the FRENCH legend (`~/GCTH/gcth_combined/GSC_OF4570_legend_FR_units_1-90.csv`)
**Why it's new:** the 19 Sep zipped run used the English legend only. The FR legend (units 1–90, transcribed 25 Sep from Max's photos) was only run as a whole text. A bilingual clue + a bilingual legend = "both numbers together" in its most literal form.
- **Pairs:**
  - A = EN→unit, FR→letter: (6,3) (2,2) (76,58) (37,16) (3,7) (25,14) (69,24) (4,25) (20,3).
  - B = FR→unit, EN→letter: the same pairs reversed.
- **Texts:** FR legend (primary); EN legend (repeated only as a cross-check for a mixed reading: unit from one language, text from the other).
- **Units of the letter index:**
  - L = letters only, accents folded;
  - C = characters including spaces and punctuation.
- **Out-of-range rules:** strict (dead on arity) and wrap (mod length). Both reported.
- **Readings:** measured; dot/dash-swapped strings (derived by the same rule as 19 Sep); reversed group order.
- **Search space:** 2 directions × 2 texts × 2 units × 2 rules × 3 readings = **48 schemes**.
- **Hit:** a 9-letter output that contains a dictionary or place word of ≥ 6 letters (EN or FR, accents folded) **and** beats a **shuffle null** (10,000 random key pairs with the same digit widths, same scheme). P < 0.01 family-wise. **Arity is reported first:** how many of 9 pairs are in range under strict.

## D69 — the two strings as Ontario land-survey coordinates
**Why:** the city's property layer stores every parcel as (TOWNSHIP code, LOT, CONCESSION) (seen 7 Nov: McMahon Point = 36 / 6 / 1). Two strings that differ by language could be two halves of one survey address.
- **Reference ranges:** from `City_Owned_Property_view` (and, if reachable, `Land_Use_and_Boundaries_view/FeatureServer/6` Parcels), read the distinct TOWNSHIP codes and, per township, the maximum LOT and CONCESSION. Pulled **before** any key is applied.
- **Readings:**
  - R1 group pairs (EN_i, FR_i) as (lot, con);
  - R2 (FR_i, EN_i) as (lot, con);
  - R3 the 14 digit pairs (EN_d, FR_d) as (lot, con);
  - R4 the same reversed;
  - R5 each string's groups as three triples, (t, l, c) in written order.
- **Statistic:** validity share, i.e. pairs/triples that are a possible (lot, con) or (twp, lot, con) in the city's own ranges.
- **Null:** 10,000 random key pairs with the same widths.
- **Hit:** every pair or triple valid **and** P < 0.01 → list the parcels, flag land status, promote nothing without Max. Otherwise **closed at chance or on arity.**

## What this cannot do
It cannot place a box. Any parcel list is description, not prediction.
