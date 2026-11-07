Paste everything below the line into a NEW chat **inside the claude.ai project "Treasure Hunt"**. That is the only place that can read the project files. The chat also needs the Mac connector (LMCP) switched on.

---

**Task: make the whole GCTH record searchable from any Claude session. Record-keeping only: no clue analysis, and no tests.**

Background: the master record (`claude/GCTH_findings.csv`, `claude/GCTH_STATE_OF_PLAY.md` and every dated PREREG / RESULT / DESK / correction file) lives in this project's knowledge. Claude Code cloud sessions and Cowork cannot read project knowledge. They only see copies moved to the Mac and Drive, and those copies are mostly PREREGs, not RESULTs. So other sessions keep missing results, and facts that were only ever said in chat (for example, the public name we found for "Lovers Rock" at Whitewater Lake Park, Azilda) are invisible to them.

Do this, in order, and stop to ask me if anything doesn't match:

1. **Mirror every project file to the Mac, byte-exact.**
   - Target: `~/GCTH/project_mirror/`, keeping the project path with `/` → `__` (the convention of the 13 Oct move).
   - Write `~/GCTH/project_mirror/_MANIFEST.tsv` (path, bytes, NFC sha256).
   - Two independent reads must agree before a file counts as copied (the 12 Sep rescue rule). Delete nothing from the project.
2. **Copy the same folder to Google Drive** › Treasure Hunt › `project_mirror/`, then check the file count and sizes.
3. **Write `~/GCTH/project_mirror/_FACTS_FROM_CHATS.md`.** It holds every fact that lives only in chat and not in a file. Start with:
   - (a) the public name of "Lovers Rock" at Whitewater Lake Park, Azilda, its coordinates, and the source we found it in;
   - (b) any other local or informal place names I have given you;
   - (c) field visits and what was searched vs only photographed (for example: Jane Goodall trail, 10 Sep, signs photographed, not searched).

   Mark each line with its source chat date. If you can't find the source, say "from Max, unsourced".
4. **Rebuild the search index on the Mac:** `python3 ~/GCTH/search/build_index.py`. It indexes all .md/.txt/.csv/.json under ~/GCTH, now including `project_mirror/`. Test it:
   - `python3 ~/GCTH/search/gcth_search.py '"lovers rock"'` must return `_FACTS_FROM_CHATS.md`;
   - `python3 ~/GCTH/search/gcth_search.py 'D66'` must return the 7 Nov D65/D66 RESULT.
5. **Bring back the 7 Nov Claude Code work.** It is already on the Mac at `~/GCTH/TreasureHunt/_recap_concept_D65_D66_07Nov2026/` (PREREG + RESULT with Amendments 1–2, sha256 of the RESULT `8f4a6c87…`). Upload it to the project and add findings rows:
   - D65: the recap adds one concrete detail per live region.
   - D66: the Sudbury concept key re-opened on the recap's "environmental restoration" line. It selects the Jane Goodall Reclamation Trail, which then fails the traffic screen (verified on Reddit, 3+ hunters since 25 Aug).
   - The Windmill Point lead is recorded, not ranked.
6. **Add a house rule** to `~/GCTH/00_READ_ME_FIRST.md` and to STATE_OF_PLAY §9: "Every new project file is also written to `~/GCTH/project_mirror/` the same day, and `build_index.py` is re-run. Any chat-only fact goes into `_FACTS_FROM_CHATS.md`."
7. Report back: the file count mirrored, any mismatches, and the top 5 search hits for "Lovers Rock".

After this, any new session (Claude Code, Cowork, or here) can be told: *"Search first with `python3 ~/GCTH/search/gcth_search.py '<terms>'`; the full record is mirrored in `~/GCTH/project_mirror/`."*
