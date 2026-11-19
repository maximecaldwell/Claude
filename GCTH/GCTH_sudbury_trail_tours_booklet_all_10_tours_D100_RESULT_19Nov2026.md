# RESULT — D100: the leaf numbers read on all 10 tours of Rainbow Routes' "Trail Tours" booklet (EN + FR) · 19 Nov 2026

**Pre-registration:** `GCTH_sudbury_trail_tours_booklet_all_10_tours_D100_PREREG_19Nov2026.md` (sha256 `4617567e…`), commit e00453e. It was pushed before the run with:
- `D100_run/d100.py` `5949d137…`
- `D100_run/build_items.py` `ae2e9abf…`
- `D100_run/pdftext.swift` `0c3d1cd5…`

The item files `items100_EN.json` `8464a59a…` and `items100_FR.json` `0833b5b3…` were built and hashed before the PREREG. All hashes were re-checked on the Mac before running.
**Run (Mac):** `~/GCTH/TreasureHunt/_trail_tours_all_D100_19Nov2026/`. Files: `d100_out.txt`, `d100_result.json`, and the post-hoc `d100_diag_control.py` / `d100_diag_control_out.txt`.
**Verdict: CLOSED at chance for the whole booklet.**
- Zero lexicon words and zero "the / le / la / les" starts, in 95 reads.
- The null averages 0.62 THE starts and 0.022 S1 per key.
- One pre-registered control failed **by design error, not by the instrument** (see Controls). **Nothing is promoted.**

## Coverage
- **84 items per language**, found by the fixed builder rule. Every title was located in order.
- **Reads fully in range: 95 of 144.**
  - Per-tour D2 needs item 8, and per-tour D1 (or its 13-pair prefix) needs item 9. So tours with fewer items read nothing: Oak Forest (6 items), Lake Laurentian (7) and Selkirk (6) produced no reads in either language.
  - Blueberry Hill (8 items) has D2 reads only.
  - Tours 2, 6 and 7 (10 items) carry full D1 reads.
- **Global numbering (items 1–84):** this was the first time in the record that **Z1 and Z2 were in range**. Item 76 is "Lucky Duck" / « Mouillé comme un canard », and item 58 is "Moss Points North" / « La mousse vous fera perdre le nord »; both carry the needed letter counts in their bodies (B / TB).

  | Language | Items | Z1 | Z2 |
  |---|---|---|---|
  | EN | B | `uhrritdck` | `dhlaeelee` |
  | EN | TB | `dlhkaherp` | `wltmstecd` |
  | FR | B | `uercsrvls` | `nensgcivn` |
  | FR | TB | `ceecudres` | `eeleedeou` |

  All are junk.

## Result
- **S1** (lexicon word ≥ 7 letters): **0.** Null mean 0.022 (5,000 keys). P = 1.0.
- **THE start:** **0.** Null mean 0.619. P = 1.0.
- **Every read** is printed in `d100_out.txt`. Examples:
  - Kelly Lake EN D1 `gauebrolmolehe`
  - Capreol EN D1 `uitrveipklgohe`
  - A.Y. Jackson EN D1 `siknserhtodefd`
  - Rotary EN D2 `showsoiahlweut`
  - Kelly Lake FR D2 `inerccterdgeeb`

  None reads as words.
- **The solvers' ten-second test** (D1: item 6 letter 3 = T, item 2 letter 2 = H, item 7 letter 5 = E) **fails on every tour where it can run**: tours 1, 2, 5, 6, 7 and 8, in EN.

## Controls
- **`DESSOUSPONT` via D2, tour 2 FR TB:** `dessousponteeb` → `dessous`. **Recovered.**
- **`WHITEWATER` via Z1, global EN TB:** **not recovered.**
  - Z1 has only 9 pairs, so a 10-letter plant can only yield `whitewate`, which is not a lexicon word.
  - This is a design error in the PREREG, not an instrument fault.
  - **Post-hoc check (not pre-registered):** the 9-letter `VERMILION` planted via Z1 and via Z2 is read back exactly (`vermilion` → S1 `vermilion`) both times.
  - By the letter of the PREREG, the run reports one control failed. The cause is identified.

## Register
- **Closed:** the leaf numbers on Rainbow Routes' 2007 Trail Tours booklet. That covers:
  - all 10 trails, EN and FR, as titles, bodies and title+body;
  - per-tour marker numbering (D1, D2);
  - booklet-wide numbering 1–84 (Z1, Z2, D1, D2).

  It includes the first in-range test of the Z reads against a real 84-item numbered set.
- **Not closed:**
  - What the physical markers carry today.
  - Any numbered set outside this booklet.
- **Method note:** a planted control must be no longer than the read that carries it. Z1/Z2 carry 9 letters; D1/D2 carry 14.
- **Correction to my D99 report to Max:** D99 called the other nine tours "listed for Max to decide". Max asked for them on 19 Nov; this file closes them.
