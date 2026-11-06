import re, json, collections, pronouncing, os
D=os.path.dirname(os.path.abspath(__file__))
L=[l for l in open(f"{D}/poem_en.txt",encoding="utf-8").read().split("\n") if l.strip()]
W=lambda l:[w.strip(",") for w in l.split()]
FUNC=set("a an the in of to by for with and but or nor yet where what when its it is be have may will won’t don’t not no through past beyond beneath behind once now still so as at on all one none".split())
def phon(w):
    w=re.sub(r"[^a-z']","",w.lower().replace("’","'"))
    sp={"chalco":"10","verdigris":"100","flinty's":"10","bathurst":"10","overgrown":"201","zinc-toned":"11","zinctoned":"11","wets":"1","birches":"10"}
    if w in sp: return sp[w]
    p=pronouncing.phones_for_word(w) or (pronouncing.phones_for_word(w[:-2]) if w.endswith("'s") else [])
    return pronouncing.stresses(p[0]) if p else None
out=[]
for g,l in enumerate(L,1):
    syl=[]
    for w in W(l):
        parts=[w] if phon(w) else w.split("-")
        for p in parts:
            s=phon(p) or "1"
            if len(s)==1:
                s = "0" if p.lower().replace("’","'").strip("'") in FUNC or p.lower() in FUNC else "1"
            else:
                s=s.replace("2","1")
            for i,c in enumerate(s): syl.append((p if i==0 else "·",c))
    pat="".join(c for _,c in syl)
    n=len(pat)
    ideal=("01"*4) if n==8 else ("1"+"01"*3 if n==7 else "01"*4+"0")
    mism=[i+1 for i,(a,b) in enumerate(zip(pat,ideal)) if a!=b]
    out.append({"g":g,"line":l,"pat":pat,"n":n,"mism":mism,"syl":[s for s,_ in syl]})
for o in out: print(o["g"],o["n"],o["pat"],o["mism"],o["line"])
json.dump(out,open(f"{D}/scan.json","w"),ensure_ascii=False)
