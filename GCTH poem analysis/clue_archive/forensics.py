"""Forensic pass over every article PDF: text, metadata, hidden text, edit history."""
import json, os, re, sys, collections, hashlib
import pymupdf

SRC = sys.argv[1]           # folder of PDFs (untrusted input)
OUT = sys.argv[2]           # output folder
os.makedirs(OUT, exist_ok=True)
os.makedirs(os.path.join(OUT, "text"), exist_ok=True)
res = {}
for fn in sorted(os.listdir(SRC)):
    if not fn.endswith(".pdf"):
        continue
    p = os.path.join(SRC, fn)
    raw = open(p, "rb").read()
    r = {"bytes": len(raw), "md5": hashlib.md5(raw).hexdigest()}
    r["eof_markers"] = raw.count(b"%%EOF")          # >1 = incremental saves (edit history)
    r["startxref"] = raw.count(b"startxref")
    r["header"] = raw[:9].decode("latin1", "replace")
    try:
        doc = pymupdf.open(p)
    except Exception as e:
        r["error"] = str(e); res[fn] = r; continue
    r["encrypted"] = doc.is_encrypted
    if doc.needs_pass:
        ok = doc.authenticate("")
        r["auth_empty_pw"] = bool(ok)
    r["permissions"] = doc.permissions
    r["meta"] = {k: v for k, v in (doc.metadata or {}).items() if v}
    try:
        r["xmp"] = (doc.get_xml_metadata() or "")[:4000]
    except Exception:
        r["xmp"] = ""
    r["pages"] = doc.page_count
    r["embedded_files"] = doc.embfile_names() if hasattr(doc, "embfile_names") else []
    try:
        r["toc"] = doc.get_toc()
    except Exception:
        r["toc"] = []
    full = []
    hidden = []
    fonts = collections.Counter()
    sizes = collections.Counter()
    colors = collections.Counter()
    annots = []
    links = []
    for pno, page in enumerate(doc):
        rect = page.rect
        d = page.get_text("dict")
        for b in d["blocks"]:
            if b.get("type") != 0:
                continue
            for line in b["lines"]:
                for sp in line["spans"]:
                    t = sp["text"]
                    if not t.strip():
                        continue
                    fonts[sp["font"]] += len(t)
                    sizes[round(sp["size"], 1)] += len(t)
                    col = "#%06x" % sp["color"]
                    colors[col] += len(t)
                    x0, y0, x1, y1 = sp["bbox"]
                    off = x1 < rect.x0 or x0 > rect.x1 or y1 < rect.y0 or y0 > rect.y1
                    reasons = []
                    if off: reasons.append("off-page")
                    if sp["size"] < 4: reasons.append(f"tiny {sp['size']:.1f}pt")
                    if sp["color"] in (0xffffff, 0xfefefe, 0xfdfdfd): reasons.append("white text")
                    if sp.get("alpha", 255) < 40: reasons.append("transparent")
                    if reasons:
                        hidden.append({"page": pno + 1, "text": t, "why": reasons, "font": sp["font"], "size": sp["size"], "color": col})
        # invisible render mode (3) via raw trace
        try:
            for tr in page.get_texttrace():
                if tr.get("type") == 3 or tr.get("opacity", 1) == 0:
                    txt = "".join(chr(c[0]) for c in tr["chars"])
                    if txt.strip():
                        hidden.append({"page": pno + 1, "text": txt, "why": ["invisible render mode" if tr.get("type") == 3 else "opacity 0"], "font": tr.get("font"), "size": tr.get("size"), "color": ""})
        except Exception:
            pass
        for a in page.annots() or []:
            annots.append({"page": pno + 1, "type": a.type[1], "content": a.info.get("content", ""), "title": a.info.get("title", "")})
        for l in page.get_links():
            links.append({"page": pno + 1, "uri": l.get("uri", ""), "kind": l.get("kind")})
        full.append(page.get_text("text"))
    text = "\n\f\n".join(full)
    open(os.path.join(OUT, "text", fn[:-4] + ".txt"), "w").write(text)
    r["chars"] = len(text)
    r["words"] = len(re.findall(r"\w+", text))
    r["fonts"] = fonts.most_common(12)
    r["sizes"] = sizes.most_common(10)
    r["colors"] = colors.most_common(8)
    r["hidden"] = hidden[:80]
    r["annots"] = annots
    r["links"] = links
    r["images"] = sum(len(pg.get_images()) for pg in doc)
    res[fn] = r
json.dump(res, open(os.path.join(OUT, "forensics.json"), "w"), indent=1, ensure_ascii=False)
for fn, r in res.items():
    print(f"{fn[:62]:62} p={r.get('pages')} w={r.get('words')} eof={r['eof_markers']} enc={r.get('encrypted')} hid={len(r.get('hidden',[]))} ann={len(r.get('annots',[]))} lnk={len(r.get('links',[]))} emb={len(r.get('embedded_files',[]))} {r.get('meta',{}).get('producer','')[:30]}")
