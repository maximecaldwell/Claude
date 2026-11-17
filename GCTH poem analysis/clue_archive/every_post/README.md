# every_post — TNM vs MINING.COM vs CEO.CA (desk, 17 Nov 2026)

Question: for every bonus chapter and the GP posts, does MINING.COM or CEO.CA carry a version that differs from TNM's (digits, words, headings, captions, images, extra or missing paragraphs)?

## Files
- `diffs.md`: findings. §1 coverage table, §2 meaningful differences with quotes and URLs, §3 layout noise, §4 gaps, §5 register.
- `sources.csv`: every source read, with id, UTC dates, route and result. Commas inside titles are written as semicolons.
- `tnm_live/`: TNM WP REST JSON for all 47 hunt posts, fetched from the container on 17 Nov 2026 (`/wp-json/wp/v2/posts/<id>`), plus page HTML for the 4 syndicated posts (`page_<id>.html`).
- `raw/miningcom_line_hashes_17Nov2026.txt`, `raw/tnm_line_hashes_17Nov2026.txt`: per-line hashes for the 4 article pairs.
- `scripts/norm.py` (Python normaliser + FNV-1a hash), `scripts/norm.js` (the identical normaliser run in the browser on mining.com), `scripts/compare.py` (difflib over the hash lists; run `python3 -I scripts/compare.py`).

## Method
1. TNM: live REST copies (container). Checked no new hunt post since 5 Nov 2026.
2. MINING.COM: blocked from the container (CloudFront 403 for curl and WebFetch). Read through the LMCP web session on Max's Mac as an ordinary visitor: public WP REST API (`posts`, `search`, `tags`, `media`), article pages, and the site's own search (`/?s=`), which also lists the `/video/` pages that REST does not expose.
3. Text comparison: the HTML body is cut into lines at block-closing tags, tags stripped, entities decoded, NBSP→space, whitespace collapsed. Each line is hashed (FNV-1a 32 over UTF-16 units) identically on both sides. Hash lists were aligned with difflib; every non-matching line was then read in full on both channels and quoted in `diffs.md`.
4. Images: featured media (file, caption, alt) via REST on both sites; inline `<img>` checked in both bodies (none).
5. CEO.CA: signed-out browser reads of `#treasurehunt`, `@northernminer`, `/articles`, `/editors`, `/search`; web search. A probe of CEO.CA's internal API from the container was refused by the session's safety check and not retried.
6. Max's record read only (R-1169, R-1170, R-1874, the 23 Oct social/syndication RESULT). Nothing in `~/GCTH/record/` was edited; `merge_inbox.py` not run.

## Result in one line
MINING.COM has only 4 articles (launch, Cobalt, Val-d'Or, NS) and 8 video pages; Cobalt and NS are identical; Val-d'Or still lacks `810-419-227` and the ":mining" colon (R-1170, re-confirmed); MINING.COM's launch copy lacks the Boyd quote and the "Detour Lake mine" coin-source phrase. CEO.CA: nothing visible signed-out (gap).
