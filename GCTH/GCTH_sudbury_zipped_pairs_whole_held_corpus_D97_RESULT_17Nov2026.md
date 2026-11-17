# RESULT — D97: EN×FR zipped (item, letter) pairs over the whole held text corpus · 17 Nov 2026

**Pre-registration:** `GCTH_sudbury_zipped_pairs_whole_held_corpus_D97_PREREG_17Nov2026.md` (sha256 `352fbae5…`), pushed and copied to the Mac before the run.
**Run (Mac):** `~/GCTH/TreasureHunt/_zipped_whole_corpus_D97_17Nov2026/` — `d97.py`, `d97_out.txt`, `d97_result.json`. Run time 63 s.
**Verdict: CLOSED at chance on the primary statistic.** The secondary scorer failed its control and decides nothing (reported below).

## Corpus (by the pre-registered rule)
- **A** (wide-harvest JSON records ≥ 300 chars): 2,070.
- **B** (held `.txt` sources): 4,153.
- **After dedupe: 5,905 texts.** Each text was split three ways into items: paragraphs, sentences and lines.
- Reads: 70,860 attempted, **16,693 fully in range** (strict, no wrapping).

## Primary — S1 (a lexicon word of ≥ 7 letters in the read)
- **Real: 6 reads.**
- **Null:** 20 random key pairs, same widths, same texts and reads: hits `[2, 8, 7, 8, 10, 1, 5, 5, 7, 2, 9, 5, 0, 4, 6, 8, 7, 7, 7, 7]`, mean 5.7. **P = 0.62.**
- **The six, all isolated words inside junk:**
  - `riposte` (`mhriposteoaart`, Muenster–OGS field studies, D1 line)
  - `ascribe` (`prascribelrilp`, FR wiki *Jim Bradley*)
  - `ralenti` ×2 (`leamcralentimd`, the same 1932 museum text in two folders)
  - `thistle` (`thistlettthhae`, cited-check text)
  - `clement` (`neilleeclement`, LAC *nickel* FR page)

  None continues into words.
- **Controls passed on S1:** `WHITEWATER` planted via D1 was recovered as `whitewaterircm` → `whitewater`. `DESSOUSPONT` planted via D2 was recovered as `dessousponttei` → `dessous`.

## Secondary — S2 (word-tiling coverage): INSTRUMENT FAILED, as the PREREG requires us to say
- Neither control reached the real top 30 by S2. Their scores were 0.71 / 0.79, at the null's 95th / 98th percentile.
- Junk such as `raresailtaiare` scores 1.00, because short common words (3–4 letters, EN or FR) tile almost any letter run.
- S2 therefore decides nothing. Its top 30 was still read by eye: nothing reads as an instruction or a place. Examples: `whoaaretootooe`, `teensricteeeut` (the same template sentence across 10 FR *Gare de …* stubs), `perprotalesitc`.

## Register
- **Closed:** zipped EN×FR (item, letter) pairs over every text we hold. That covers paragraphs, sentences and lines; group pairs and digit pairs; both directions; strict range. It joins the 25 Sep combined sweep (which excluded pairs) and the 16 Nov THE-screen (which kept only "the…" reads).
- **What is left of "both numbers together":** a key we **don't hold as text**, i.e. a physical set of numbered, labelled items, as the 16 Nov solver hints describe ("a physical object in town … numbered, labelled items"). The bound still applies (item 76 ≥ 58 letters, or item 58 ≥ 76). The 16 Nov file's ten-second test applies to any object photographed: with digit pairs, item 6 letter 3 = T, item 2 letter 2 = H, item 7 letter 5 = E.
- **Method note for future runs:** a coverage scorer needs a short-word penalty, or a minimum word length of 4, to be usable. Fix that before reusing S2.
