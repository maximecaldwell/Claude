# Broad screen of EN/FR text pairs with the Sudbury leaf numbers.
# Read-outs identical to raw/sovereign_king_edward_texts_12Nov2026/run.py (20 per text).
# Measures: TARGET words (pre-registered list) in word read-outs; HIDDEN word (longest dictionary word >=5 letters in letter read-outs).
# Dictionaries: wordfreq top-50k EN / FR, accents folded (cloud; differs from the Mac's /usr/share/dict and clue-article FR list).
import re,unicodedata,random,glob,os,sys,json,wordfreq
EN=[6,2,76,37,3,25,69,4,20]; FR=[3,2,58,16,7,14,24,25,3]
PAT={'EN':[1,1,2,2,1,2,2,1,2],'FR':[1,1,2,2,1,2,2,2,1]}
def norm(s): return ''.join(c for c in unicodedata.normalize('NFD',s.lower()) if c.isalpha())
TARGETS={norm(x) for x in '''north south east west southwest northeast northwest southeast nord sud est ouest sud-ouest nord-est nord-ouest sud-est
under below beneath behind sous dessous derrière bench banc tree arbre rock roche stone pierre pierres trail sentier
lookout belvédère treasure trésor box boîte cache dig creuser bridge pont gold or'''.split()}
def _ws(lang):
    top=wordfreq.top_n_list(lang,30000); s=set()
    for r,w in enumerate(top):
        w=norm(w)
        if len(w)>=4 or (len(w)==3 and r<1500) or (len(w)==2 and r<150): s.add(w)
    return s
WS={'EN':_ws('en'),'FR':_ws('fr')}
def toks(t,split):
    t=re.sub(r'[—–‒]',' ',t)
    if split: t=t.replace('-',' ')
    w=[x.strip('.,;:!?«»“”"\'’()[]') for x in t.split()]
    return [x for x in w if x and any(c.isalnum() for c in x)]
def letters(t): return [c for c in t if c.isalpha()]
def cum(a):
    s=0;o=[]
    for x in a: s+=x;o.append(s)
    return o
def pick(seq,idx,j=' '): return j.join(seq[i-1] if 1<=i<=len(seq) else '_' for i in idx)
def outputs(t,key):
    L=letters(t); o={}; W={0:toks(t,0),1:toks(t,1)}
    for lab,k in (('as given',key),('reversed',key[::-1])):
        for s in (0,1):
            w=W[s]; sl='split' if s else 'whole'
            o[f'{lab} | word n ({sl})']=pick(w,k)
            o[f'{lab} | word running ({sl})']=pick(w,cum(k))
            o[f'{lab} | initials ({sl})']=pick([x[0] for x in w],k,'')
        o[f'{lab} | letter n']=pick(L,k,'')
        o[f'{lab} | letter running']=pick(L,cum(k),'')
    return o
def targ(o): return sum(norm(x) in TARGETS for k,v in o.items() if '| word' in k for x in v.split())
def tile(s,ws):
    # max letters of s covered by non-overlapping dictionary words; returns (covered, words)
    n=len(s); best=[(0,[])]*(n+1)
    for i in range(n):
        if best[i+1][0]<best[i][0]: best[i+1]=best[i]
        for j in range(i+2,min(n,i+12)+1):
            if s[i:j] in ws:
                c=best[i][0]+(j-i)
                if c>best[j][0]: best[j]=(c,best[i][1]+[s[i:j]])
    return best[n]
def hidden(o,lang):
    best=(0,[])
    for k,v in o.items():
        if 'word' in k: continue
        for part in [norm(p) for p in v.split('_')]:
            r=tile(part,WS[lang])
            if r[0]>best[0]: best=r
    return '+'.join(best[1]) if best[0] else ''
def rkey(lang,rng): return [rng.randint(0,10**d-1) for d in PAT[lang]]
def score(t,lang,N,seed):
    rng=random.Random(seed)
    key=EN if lang=='EN' else FR
    o=outputs(t,key); e=targ(o); h=hidden(o,lang)
    re_=[];rh=[]
    for _ in range(N):
        ro=outputs(t,rkey(lang,rng)); re_.append(targ(ro)); rh.append(len(hidden(ro,lang).replace('+','')))
    pe=(1+sum(x>=e for x in re_))/(N+1) if e>0 else 1.0
    ph=(1+sum(x>=len(h.replace('+','')) for x in rh))/(N+1) if h else 1.0
    return o,e,pe,h,ph
if __name__=='__main__':
    files=sys.argv[2:]; N=int(sys.argv[1]); res=[]
    for f in files:
        lang=f.rsplit('_',1)[1][:2]; t=open(f,encoding='utf8',errors='ignore').read()
        o,e,pe,h,ph=score(t,lang,N,hash(os.path.basename(f))%10**9)
        res.append(dict(file=f,lang=lang,words=len(toks(t,0)),letters=len(letters(t)),targets=e,p_targets=pe,hidden=h,p_hidden=ph,outputs=o))
        print(f'{os.path.basename(f):45s} {lang} words {len(toks(t,0)):5d} targets {e} p {pe:.4f}  hidden "{h}" p {ph:.4f}',flush=True)
    json.dump(res,open('results_N%d.json'%N,'w'),ensure_ascii=False,indent=1)
