# indexkit

indexkit tests claims like **"this digit string is an index into this text"**, for example "the digits
`810-419-227` pick words out of the clue article".

There are many ways to count: words or letters, starting at 0 or at 1, from the title or not, the digits
read one at a time or in groups. With that many choices, *some* way of counting almost always finds
something that looks meaningful. indexkit tries **every** way, says how many it tried, and then asks a
fair question: *do random digit strings do just as well?* If they do, what you found is a coincidence.

indexkit only measures whether there is a signal. It never tells you what a signal means.

---

## 0. The easiest way: double-click

1. Download and unzip the folder (step 1 below), and open the `indexkit` folder in Finder.
2. **Right-click `setup.command` → Open → Open.** (The right-click is needed only the first time,
   because macOS is careful with files downloaded from the internet.) A Terminal window installs what
   is needed, runs the self-test and shows the demo. Do this once.
3. Save your articles (and a place-name list) into the `indexkit` folder as plain text — see section 3.
4. **Double-click `test_clue.command`** (right-click → Open the first time). It asks for the digits and the
   file names, runs the test, and opens the report in TextEdit. Each clue gets its own report file
   (`report_810_419_227.md`), so nothing is overwritten.

Everything below explains the same thing with typed commands, plus the extra options.

---

## 1. One-time setup (Mac)

You need the Terminal app (press ⌘-Space, type `Terminal`, press Enter).
Each grey box below is **one line**. Type or paste it, then press Enter.

1. Get the `indexkit` folder onto your Mac (for example: on GitHub, use **Code → Download ZIP**, then
   double-click the ZIP to unzip it).
2. Go into the folder. Type `cd`, a space, then **drag the `indexkit` folder from Finder into the Terminal
   window** (this types its location for you), then press Enter. It looks something like:

   ```
   cd ~/Downloads/Claude-main/indexkit
   ```

3. Install the two helpers indexkit needs (numpy for the maths, pytest for the tests):

   ```
   python3 -m pip install --user numpy pytest
   ```

   If your Mac asks to install "command line developer tools", say yes, wait, then run the line again.

Every command below must be typed **from inside the `indexkit` folder** (step 2). If you open a new Terminal
window, do step 2 again. All commands are safe to run again: they never delete your files, and the only
files they overwrite are their own reports.

---

## 2. The commands

### `selftest` — check the instrument (always first)

```
python3 -m indexkit selftest
```

Takes about 20 seconds. It hides known messages in a made-up article and checks that indexkit finds
them with a small p-value. Then it feeds in hundreds of random digit strings and checks that they come
out **not** significant as often as they should (their p-values must be spread evenly between 0 and 1;
this is checked with a Kolmogorov–Smirnov test).

Until the self-test has passed, **every other command refuses to run**. If you update indexkit, Python or
numpy, it will ask you to run the self-test again.

### `demo` — see what a real hit and a coincidence look like

```
python3 -m indexkit demo
```

Writes a made-up English and French article (nothing is downloaded) into a folder called `demo_output`,
then runs two tests:

* **real hit**: digits `67-90-143`, which were planted so that they pick three place names out of the
  English article. Result: significant in English, not in French.
* **coincidence**: digits `130-315-814`, not planted. Some ways of counting still land on place names —
  15 of 280, when random strings manage about 10 on average — and the p-value is large.

Open `demo_output/demo_report_real_hit.md` and `demo_output/demo_report_coincidence.md` side by side.
Both show "hits". Only one is real. That is the whole point of the tool.

### `conventions` — list every way of counting that will be tried

```
python3 -m indexkit conventions --digits "810-419-227" --text en=article_en.txt --text fr=article_fr.txt
```

Prints each convention, one per line, and the total for each text (the "search space"). Nothing is tested.

### `run` — test your digits

```
python3 -m indexkit run --digits "810-419-227" --text en=article_en.txt --text fr=article_fr.txt --targets places.txt
```

* `--digits` — the digit string in quotes, exactly as in the clue. Spaces, dashes or other separators
  are kept as the "given" grouping: `"2638"`, `"810-419-227"`, `"6 2 76 37 3 25 69 4 20"`.
* `--text` — a text file. Put a short label and `=` in front (`en=`, `fr=`). Repeat for each language.
* `--targets` — a file with one word or name per line (e.g. place names). A convention "hits" when it
  picks out one of them. Accents, capitals, hyphens and apostrophes do not matter
  (`Val-d'Or` = `VAL D’OR` = `valdor`). Lines starting with `#` are ignored.

Without `--targets`, indexkit uses the **letters** score instead: does the extract spell words? It uses a
small built-in English or French word list (chosen from the label `en`/`fr`), or your own with
`--wordlist words.txt` (one word per line).

It takes from a few seconds to a few minutes. It prints a summary and writes the full report to
`indexkit_report.md` (choose another name with `--out myname.md`).

### `prereg` — decide everything before you look

A result is only trustworthy if you did not keep changing the question until something worked.
`prereg` writes down the question first:

```
python3 -m indexkit prereg --out clue7.prereg.json --digits "810-419-227" --text en=article_en.txt --text fr=article_fr.txt --targets places.txt
```

This creates `clue7.prereg.json` (the digits, the texts with their SHA-256 fingerprints, the targets,
every convention, the null hypothesis, number of draws, seed and pass threshold) and
`clue7.prereg.json.sha256`, and prints a hash. **Send that hash to a teammate** (or anywhere you cannot
edit later). Then:

```
python3 -m indexkit run --prereg clue7.prereg.json
```

`run --prereg` refuses to run if the file was edited, if a text or the target list changed, if you add
any option that the file already fixes (digits, texts, targets, draws, threshold...), or if this version
of indexkit would try a different list of conventions. `prereg` never overwrites a different
pre-registration; re-running the identical command just says "nothing changed".

### Running the tests

```
python3 -m pytest
```

Checks every tokenizer on tricky French and English text, the digit groupings, the scores, the shuffle
logic and the pre-registration refusals. Takes about 20 seconds.

---

## 3. Preparing your files

* **Texts**: plain text (`.txt`), saved as UTF-8 (TextEdit: *Format → Make Plain Text*, then save with
  encoding "Unicode (UTF-8)"). The **first non-empty line is the title**. Leave **one blank line between
  paragraphs**. If you copy the article with its original line breaks, indexkit can also count lines.
* **Targets**: one entry per line; multi-word names are fine (`Mont Sureau`).
* File names with spaces must be in quotes: `--text "en=my article.txt"`.

---

## 4. What gets counted (the conventions)

Every combination of these is tried:

| dimension | options |
|---|---|
| unit | word, letter, non-space character, line, sentence, paragraph |
| tokenizer (words only) | `ws` whitespace only (a lone `:` or `–` or `«` counts as a word) · `ws-drop` whitespace, lone punctuation dropped · `strip` punctuation stripped from both ends of each word · `split` also split at hyphens and apostrophes (`Val-d'Or` → Val, d, Or; `l'Or` → l, Or) |
| read | the whole word (for line/sentence/paragraph: its first word) · or only its first letter (classic book cipher) · letters/characters are taken as they are |
| start | from the title · from the first paragraph after the title · from a marker line (`--marker`) |
| counting | 0-based (first item is 0) or 1-based (first item is 1) |
| digit grouping | as given · single digits · pairs · cumulative (each number is a step from the previous position) · reversed (whole string read backwards) |

Notes:

* `--marker "Chapter 2|Chapitre 2"` adds a start point at the line containing that text. Use `|` to give
  the English and French wording; the first one found in each text is used.
* Conventions that give exactly the same result on your text (for example "line" and "paragraph" when the
  file has no line breaks, or `ws-drop` and `strip`, which only differ in how a word is displayed) are
  merged and shown as "identical readings", so the count is honest.
* An index that falls outside the text, or a 0 when counting from 1, gives a gap (`·`).
* French is handled properly: Unicode NFC, both `'` and `’`, `« guillemets »`, non-breaking spaces,
  `" : "` and `" – "` as standalone tokens, `Val-d'Or`, `l'Or`, `œ`.

You may restrict the search with `--units`, `--tokenizers`, `--bases`, `--starts`, `--groupings`
(comma lists, e.g. `--units word,letter`). A smaller search is more sensitive, **but only if you chose it
before seeing any result**, so do it in a `prereg`. indexkit prints a warning otherwise.

---

## 5. How the test works

**Scores.**

* *targets*: how many different target words the extract contains. A target can be one extracted word
  or several in a row that spell it (`Val` `d` `Or`). For letter extracts, it must appear as consecutive
  letters.
* *letters*: the best way to read the extract as dictionary words. Each word found scores its length
  squared (a 2-letter word = 4, a 4-letter word = 16), so long words count most but short words such as
  `is`, `or`, `a` still count.

**Null hypothesis.** The digits carry no information about the text. Two independent checks; both must
be passed:

* **Null A** — random digit strings with the same shape (same group lengths, every digit random).
* **Null B** — your real digits, on copies of the text whose paragraphs (except the title) are shuffled.

**Fair comparison across conventions.** One convention reads 28 letters, another reads 4, so their raw
scores are not comparable. indexkit first runs 10,000 *reference* draws to learn what is normal for each
convention, and turns every score into a "rarity" (how often random draws do that well with that one
convention). Your digits' most unusual convention is then compared with the most unusual convention of
each of 10,000 separate *test* draws, scored in exactly the same way. The p-value is the share of test
draws at least as unusual as yours. Because every draw also gets to pick its best convention, the p-value
already pays for the whole search. All draws are seeded, so the same command gives the same answer.

**Verdict.** p is the larger of the null-A and null-B p-values. The pass threshold (default 0.01) is split
between the texts (two texts → each needs p ≤ 0.005). English and French are always tested and reported
separately, never combined; the report says whether the same convention wins in both.

**"N of M conventions hit"** is shown next to how many random strings hit on average. If yours is in
the normal range, your hits are what chance produces.

---

## 6. Reading the report

The Markdown report lists, in this order: the null hypothesis (before any result), the inputs with the
SHA-256 of each file, the search-space size, then for each text: N of M conventions hit, the p-values and
the verdict, and the top 5 conventions with what they extract. The "uncorrected rarity" column ignores
the search and always looks impressive — quote the p-value, not that. It ends with the English/French
check and the line **"SIGNAL ONLY: this says nothing about what it means."**

---

## 7. Limits

* A significant result says "these digits are unlikely to be random with respect to this text". It does
  not say the convention found is the intended one, nor what the message means.
* The p-value covers the conventions inside indexkit. It does **not** cover choices made outside it: if
  you try ten digit strings, five articles, or rewrite the target list after looking, chance results
  will appear. Pre-register.
* Texts with fewer than two paragraphs after the title cannot be shuffled; null B then reports p = 1.
