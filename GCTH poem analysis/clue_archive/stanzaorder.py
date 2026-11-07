import itertools,random,pickle,os,sys,math
sys.argv=["x"]
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"coords.py")).read().split("# ---------------- fragments")[0]
__file__=os.path.join(os.path.dirname(os.path.abspath(sys.argv[0] if False else "gp/coords.py")),"coords.py")
exec(src)
SUD={"EN":"62763732569420","FR":"32581671424253"}
def orders(frag):
    # slots by stanza: S1 ch1(none) S2 ch3(none) S3 ? S4 ? S5 ch12 S6 ch13+ch11 S7 ch8 S8 ? S9 ? S10 ch7 S11 ch6(none)
    amb=["S3","S4","S8","S9"]
    for a,b in itertools.permutations(amb,2):
        seq=[]
        for s in ["S1","S2","S3","S4","S5","S6","S7","S8","S9","S10","S11"]:
            if s==a: seq.append(frag["sask"])
            if s==b: seq.append(frag["ns"])
            if s=="S5": seq.append(frag["sud"])
            if s=="S6": seq+= [frag["chib"],frag["man"]]
            if s=="S7": seq.append(frag["vd"])
            if s=="S10": seq.append(frag["nb"])
        yield f"sask@{a} ns@{b}", "".join(seq)
def hits_for(frag):
    H=[]
    for lab,digs in orders(frag):
        for la,lo,l2 in candidates_from_split(digs):
            if ok(la,lo): H.append((lab,round(la,5),round(lo,5),l2))
    return H
R={}
for lang in ("EN","FR"):
    frag={"sask":"2638","ns":"9","sud":SUD[lang],"chib":"2","man":"42","vd":"810419227","nb":"1"}
    real=hits_for(frag)
    null=[]
    random.seed(7)
    for _ in range(200):
        rf={k:"".join(random.choice("0123456789") for _ in v) for k,v in frag.items()}
        null.append(len(hits_for(rf)))
    p=sum(1 for x in null if x>=len(real))/len(null)
    R[lang]=(len(real),sum(null)/len(null),p,real)
    print(lang,"hits",len(real),"null mean",round(sum(null)/len(null),2),"p",p)
    for h in real[:12]: print("   ",h, nearest(h[1],h[2]))
