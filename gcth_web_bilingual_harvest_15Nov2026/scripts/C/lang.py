import sys,re
def frratio(t):
    w=re.findall(r"[a-zàâçéèêëîïôûùüÿœ']+",t.lower())
    if not w: return 0
    fr=sum(1 for x in w if x in {'le','la','les','des','et','du','une','est','pour','dans','qui','sur','au','aux','avec','nous','notre','nos','sont'})
    en=sum(1 for x in w if x in {'the','and','of','to','is','for','with','our','we','are','that','in','on'})
    return fr/(fr+en+1e-9)
if __name__=='__main__':
    for f in sys.argv[1:]:
        t=open(f).read(); print(f'{frratio(t):.2f} {len(t.split())} {f}')
