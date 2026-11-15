import sys,os,json,glob
from multiprocessing import Pool
import screen as S
def one(args):
    f,N=args
    lang=os.path.basename(f).rsplit('_',1)[1][:2]
    t=open(f,encoding='utf8',errors='ignore').read()
    o,e,pe,h,ph=S.score(t,lang,N,abs(hash(os.path.basename(f)))%10**9)
    return dict(file=f,lang=lang,words=len(S.toks(t,0)),letters=len(S.letters(t)),targets=e,p_targets=pe,hidden=h,p_hidden=ph,outputs=o)
if __name__=='__main__':
    N=int(sys.argv[1]); out=sys.argv[2]; files=sys.argv[3:]
    with Pool(4) as p:
        res=[]
        for r in p.imap_unordered(one,[(f,N) for f in files]):
            res.append(r); print(f"{os.path.basename(r['file']):55s} {r['lang']} w{r['words']:5d} tgt {r['targets']} p{r['p_targets']:.4f} tile '{r['hidden']}' p{r['p_hidden']:.4f}",flush=True)
    json.dump(res,open(out,'w'),ensure_ascii=False,indent=1)
