# GCTH: web harvest of EN/FR parallel texts, and the Sudbury leaf-number screen (15 Nov 2026)

Max asked: "dig super deep into the world of the Internet and find bilingual text about anything related to this hunt".

## What is here
- `texts/`: 335 EN/FR text pairs, each saved as `<slug>_EN.txt` / `<slug>_FR.txt` and extracted by script from raw downloads. Each subfolder has a `manifest.tsv` with the source URLs. Raw HTML and PDFs were not kept here.
  - `A_federal/` (37 used): Parks Canada / HSMBC, FHBRO buildings, Science North 1990s pages (LAC web archive), Bank of Canada Museum, Royal Canadian Mint, NRCan, Canadian Encyclopedia.
  - `B_ontario_sudbury/` (203): Ontario Heritage Trust plaques in Greater Sudbury (from the Trust's map feed), OGS GeoTours, City of Greater Sudbury, Greater Sudbury Museums, sudburymuseums.ca "Greater Sudbury Histories" (145), Science North, Place des Arts captions, Conservation Sudbury, Laurentian, GSPL.
  - `C_mining_industry/` (94 used, 108 saved): Glencore Sudbury INO, Canadian Mining Hall of Fame (FR is machine-translated by Weglot), CIM Magazine, CEMI, treasure.northernminer.com site pages. The 13 TNM regional articles and the poem page are saved but were NOT scored, since they are already in the clue archive.
  - `X_hsmbc_face/`: the federal "Nickel Mining in Canada" plaque, face text from the 9 Sep 2026 record.
- `scripts/`: the harvesting agents' extraction scripts.
- `engine/`: `screen.py` and `runset.py`, the file lists, and the planted control.
- `results/`: stage-1 (1,000 random strings) and stage-2 (20,000) JSON and logs, with all 20 read-outs per text.

## Result: null
- 670 texts were scored. The EN string was run on EN text and the FR string on FR text.
- **Stage 1:** 4 texts at p ≤ 0.005 (3.4 expected by chance) and 54 at p ≤ 0.05 (34 expected).
- **Stage 2** (20,000 random strings), against a bar of p < 0.05/670 ≈ 7.5e-5:
  - Knuckey FR "ciel+le+sac": 0.0023
  - Laurentian OHT FR "ne+dures+un": 0.0039
  - virtual museum EN "hide+he+pro": 0.0024

  None clears the bar, and all three read as word salad.
- **Both faces of one pair ≤ 0.05 on the same measure:** 0 pairs, against about 0.84 expected per measure.
- **Instrument limit:** the planted 9-letter FR message ("TRESORICI" → "tresor+ici") scores p 0.0016 at 20,000, which would NOT clear a 670-text bar. So this run cannot rule out a short French letter message hidden in one face. It does rule out anything that reads strongly in both faces, or that reads as words by eye.

The pre-registration is in Max's `~/GCTH/inbox/` on the Mac (written before any text was seen). The result file and table rows were filed there too.
