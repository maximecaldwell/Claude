"""Per-article content analysis for the GCTH regional clue articles (EN/FR pairs)."""
import json, os, re, sys, collections, unicodedata
import pymupdf

PDF, OUT, POEM = sys.argv[1], sys.argv[2], sys.argv[3]
ARTS = [  # (key, region, month, EN id, FR id)
    ("cobalt", "Cobalt, ON", "2025-10", "1003883782", "1003883783"),
    ("golden", "Golden Triangle, BC", "2025-11", "1003884744", "1003884870"),
    ("argentia", "Argentia, NL", "2025-12", "1003885767", "1003885833"),
    ("southbc", "Southern BC", "2026-01", "1003886917", "1003886916"),
    ("toronto", "Toronto, ON", "2026-02", "1003888069", "1003888212"),
    ("bathurst", "Bathurst, NB", "2026-03", "1003889269", "1003889385"),
    ("valdor", "Val-d'Or, QC", "2026-04", "1003890424", "1003890541"),
    ("klondike", "Klondike, YT", "2026-05", None, "1003891142"),
    ("sask", "Saskatchewan", "2026-05", "1003891454", "1003891545"),
    ("novascotia", "Nova Scotia", "2026-06", None, "1003892426"),
    ("manitoba", "Manitoba", "2026-07", "1003893528", "1003893609"),
    ("sudbury", "Sudbury, ON", "2026-08", "1003894294", "1003894368"),
    ("nelligan", "Chibougamau / Nelligan, QC", "2026-09", "1003895272", "1003895351"),
    ("oneyear", "One-year update", "2026-11", "1003897109", "1003897110"),
    ("blast1923", "Blast from the Past (Oct 2025 reprint)", "2025-10", "1003883495", None),
    ("blast1942", "Blast from the Past (Dec 2025 reprint)", "2025-12", "1003886083", None),
]
files = {f.split("__")[1]: f for f in os.listdir(PDF) if f.endswith(".pdf")}

def strip_acc(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")

def extract(pid):
    doc = pymupdf.open(os.path.join(PDF, files[pid]))
    paras, styled = [], []
    for page in doc:
        for b in page.get_text("dict")["blocks"]:
            if b.get("type") != 0:
                continue
            btxt = []
            for line in b["lines"]:
                for sp in line["spans"]:
                    t = sp["text"]
                    btxt.append(t)
                    f = sp["font"].lower()
                    bold = "bold" in f or "black" in f or (sp["flags"] & 16)
                    ital = "italic" in f or "oblique" in f or (sp["flags"] & 2)
                    if (bold or ital) and t.strip():
                        styled.append({"t": t.strip(), "b": bool(bold), "i": bool(ital), "size": round(sp["size"], 1), "page": page.number + 1})
                btxt.append(" ")
            p = re.sub(r"\s+", " ", "".join(btxt)).strip()
            p = p.replace("ﬁ", "fi").replace("ﬂ", "fl")
            if p:
                paras.append(p)
    text = "\n".join(paras)
    return text, paras, styled

def sentences(text):
    t = re.sub(r"\s+", " ", text)
    return [s.strip() for s in re.split(r"(?<=[.!?»”])\s+(?=[A-ZÀ-Ý«“\"])", t) if len(s.strip()) > 2]

def words(t):
    return re.findall(r"[A-Za-zÀ-ÿ’'\-]+", t)

poem = [l for l in open(POEM, encoding="utf-8").read().split("\n") if l.strip()]
STOP = set("""the a an and of in on to by for with but where what its it is be have may will not no nor once now still
yet through past beyond beneath behind all one none as at from that this was were are or so his her their our they he she
we you your who which when there here than then into over under out up down off been has had would could should can do did
also more most other some such only very about after before during while these those them him us me my i if""".split())
poem_words = collections.Counter()
for l in poem:
    for w in re.findall(r"[a-z’]+", l.lower()):
        w = w.replace("’s", "")
        if w not in STOP and len(w) > 2:
            poem_words[w] += 1
poem_bigrams = set()
for l in poem:
    ws = [w for w in re.findall(r"[a-z’\-]+", l.lower())]
    for i in range(len(ws) - 1):
        if not (ws[i] in STOP and ws[i + 1] in STOP):
            poem_bigrams.add(ws[i] + " " + ws[i + 1])
KEY = ["birch", "birches", "marker", "core", "compass", "shore", "pine", "shield", "sliver", "overgrown", "script", "brush",
       "trail", "path", "mark", "cedar", "cedars", "iron", "verdigris", "mirror", "phoenix", "siren", "chalco", "flinty", "glacier",
       "brine", "moss", "ember", "coin", "circles", "hoard", "suits", "zinc", "bell", "plaque", "cairn", "grass", "buried", "hush",
       "align", "design", "whisper", "veins", "seams", "faults", "breaks", "roots", "lore", "riches", "crowned"]
PRIZE = re.compile(r"grand prize|main prize|main treasure|grand treasure|grand trésor|trésor principal|prix principal|grand prix|"
                   r"poem|poème|riddle|énigme|clue|indice|hunters?|chasseurs?|keep your eyes|between the lines|entre les lignes|"
                   r"hidden|caché|bonus", re.I)
NUM = re.compile(r"\b\d[\d,\. ]*\d\b|\b\d\b")
CAPS = re.compile(r"\b[A-Z][a-zA-Z’'\-]+(?:\s+[A-Z][a-zA-Z’'\-]+)*")

def num_set(t):
    out = collections.Counter()
    for m in NUM.findall(t):
        k = re.sub(r"[ ,]", "", m).replace(".", "")
        if k:
            out[k] += 1
    return out

R = {}
for key, region, month, en, fr in ARTS:
    a = {"key": key, "region": region, "month": month, "en_id": en, "fr_id": fr}
    for lang, pid in (("en", en), ("fr", fr)):
        if not pid:
            continue
        text, paras, styled = extract(pid)
        open(os.path.join(OUT, "text", f"{key}_{lang}.txt"), "w").write(text)
        ss = sentences(text)
        ws = words(text)
        a[lang] = {"words": len(ws), "sentences": len(ss), "paragraphs": len(paras), "chars": len(text),
                   "letters": sum(c.isalpha() for c in text), "styled": styled[:200], "numbers": num_set(text)}
        if lang == "en":
            low = [w.lower().replace("’s", "") for w in ws]
            lc = collections.Counter(low)
            a["poem_word_hits"] = {w: lc[w] for w in poem_words if lc.get(w)}
            a["key_hits"] = {w: lc[w] for w in KEY if lc.get(w)}
            tl = " ".join(low)
            a["poem_bigrams"] = sorted({b for b in poem_bigrams if re.search(r"\b" + re.escape(b) + r"\b", tl)})
            a["key_sentences"] = [s for s in ss if any(re.search(r"\b" + k + r"\b", s.lower()) for k in KEY)][:60]
            a["prize_sentences"] = [s for s in ss if PRIZE.search(s)][:60]
            a["caps"] = collections.Counter(m for m in CAPS.findall(text) if len(m) > 2).most_common(80)
        else:
            a["prize_sentences_fr"] = [s for s in ss if PRIZE.search(s)][:60]
    if "en" in a and "fr" in a:
        ne, nf = a["en"]["numbers"], a["fr"]["numbers"]
        a["numbers_only_en"] = sorted(set(ne) - set(nf))
        a["numbers_only_fr"] = sorted(set(nf) - set(ne))
        a["number_count_mismatch"] = sorted(k for k in set(ne) & set(nf) if ne[k] != nf[k])
    for lang in ("en", "fr"):
        if lang in a:
            a[lang]["numbers"] = dict(a[lang]["numbers"])
    R[key] = a
json.dump(R, open(os.path.join(OUT, "articles.json"), "w"), indent=1, ensure_ascii=False)
for k, a in R.items():
    e, f = a.get("en", {}), a.get("fr", {})
    print(f"{k:11} EN w={e.get('words','-'):>5} s={e.get('sentences','-'):>4}  FR w={f.get('words','-'):>5} s={f.get('sentences','-'):>4}  "
          f"poemwords={len(a.get('poem_word_hits',{})):>3} bigrams={len(a.get('poem_bigrams',[])):>2} key={a.get('key_hits',{})}")
    if a.get("numbers_only_en") or a.get("numbers_only_fr"):
        print("    numbers only EN:", a.get("numbers_only_en"), " only FR:", a.get("numbers_only_fr"), " count≠:", a.get("number_count_mismatch"))
    print("    poem bigrams:", a.get("poem_bigrams"))
