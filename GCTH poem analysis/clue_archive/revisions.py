import sys, os, re, difflib, json, pymupdf
SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT+"/rev", exist_ok=True)
def txt(doc): return "\n".join(p.get_text("text") for p in doc)
def norm(t): return [l.strip() for l in re.sub(r"[ \t]+"," ",t).split("\n") if l.strip()]
res={}
for fn in sorted(os.listdir(SRC)):
    raw=open(os.path.join(SRC,fn),"rb").read()
    if raw.count(b"%%EOF")<2 or b"/Linearized" in raw[:2000]: continue
    cuts=[m.end() for m in re.finditer(rb"%%EOF\r?\n?",raw)]
    out=[]
    final=norm(txt(pymupdf.open(stream=raw,filetype="pdf")))
    for i,c in enumerate(cuts[:-1]):
        try:
            d=pymupdf.open(stream=raw[:c],filetype="pdf"); t=norm(txt(d))
            meta=d.metadata
        except Exception as e:
            out.append({"rev":i,"error":str(e)}); continue
        diff=[l for l in difflib.unified_diff(t,final,lineterm="",n=0) if not l.startswith(("---","+++","@@"))]
        out.append({"rev":i,"bytes":c,"pages":d.page_count,"meta":{k:v for k,v in meta.items() if v},"diff_lines":len(diff),"diff":diff[:60]})
    # what does the appended update contain?
    tail=raw[cuts[0]:]
    objs=re.findall(rb"(\d+) 0 obj",tail)
    keys=sorted(set(re.findall(rb"/(Type|Subtype|Producer|ModDate|Author|Creator|Annots|Encrypt|Metadata)\b",tail)))
    res[fn]={"revisions":out,"appended_bytes":len(tail),"appended_objs":len(objs),"appended_keys":[k.decode() for k in keys]}
    print("==",fn,"appended",len(tail),"bytes,",len(objs),"objs",[k.decode() for k in keys])
    for r in out: print("   rev",r.get("rev"),"diff_lines",r.get("diff_lines"),r.get("error",""),r.get("meta",{}).get("modDate",""), r.get("diff",[])[:6])
json.dump(res,open(OUT+"/revisions.json","w"),indent=1,ensure_ascii=False)
