# chapter_stanza: GCTH chapter ↔ stanza desk map (17 Nov 2026)

**Question (Max):** Do the poem's 13 stanzas correspond to the bonus chapters (12 + GP, or 6 + 6), so that the GP is the stanza left over?

**Answer:** Partly. The chapters echo the poem many-to-many, so it is not a one-to-one map. The best-supported map puts 13 chapters on 10 stanzas: S1, 2, 3, 4, 5, 6, 7, 10, 11, 13. S3 (coast) takes three chapters and S6 takes two. Neither the 12 + 1 structure nor the 6 + 6 structure fits. What no chapter claims is **S8 (iron, cedar, northern call)** and **S9 (marker by shore and pine)**, plus the instruction stanzas **S12 and S13**. That non-place layer is the GP description.

## Files
- `map.md`: the full table, exact EN and FR quotes per chapter, the stanza 4 and stanza 7 discussion, the structure tests and the GP conclusion.
- `corpus/`: copies of the chapter texts that were read. Dawson EN and Nova Scotia EN come from the web posts. `manitoba_hist_fr.txt` is the second FR file.
- `scripts/hits.py`: a rough keyword tally per chapter per stanza. It is only an aid for finding passages and is not evidence; its regexes over-match.
- `scripts/order_tests.py`: Spearman and permutation tests (release order, longitude, stanza) and the 6 + 6 count, run on the map.

## Key results
- New verbatim FR echo: Manitoba FR "Flin Flon … une ceinture minérale qui **n'a jamais cessé** de livrer ses richesses" = poem FR L22 "la revendication de Flinty **n'a jamais cessé**".
- Dawson's closing line echoes S1 L2–3 (old, riches, vein, whisper), and chapter 1 came out right after GP clue #1, which expands L3's "mirror". Dawson also echoes S5 L19 ("siren call of Nome").
- S4: the Cobalt chapter says the Timmins brothers are those "whom the northern city was named after" (FR "la ville du nord"), and Bathurst lists "Sudbury, Timmins and Flin Flon" (the S5, S4 and S6 trio). So the best reading of S4 is Timmins/Porcupine (fire of 1911), reached through the Cobalt chapter. Confidence: moderate.
- S7: the best fit is Val-d'Or ("gives nothing away", "rumour", "Depression", "Valley"), at low-moderate confidence. Chibougamau is the only chapter that says "Canadian Shield", but it is already on S6.
- The Sudbury chapter never mentions the Big Nickel ("coinage" only).
- Cedar/cèdre: 0 hits in all chapters. borne: 0 hits.
- 6 + 6: 6 of 12 chapters align with the halves, which is chance (P = 0.51). Release order vs stanza: ρ = 0.51 (p = 0.08), not significant. Longitude vs stanza: ρ = 0.28 (p = 0.35).
- Vaccaro says "14 treasures" (13 bonus + GP), which breaks the 13 = 12 + 1 arithmetic.

Inbox copy on Max's Mac: `~/GCTH/inbox/GCTH_GP_chapter_stanza_map_DESK_17Nov2026.md`
