import sys,collections;sys.path.insert(0,'.')
from agq import agq
u,fld=sys.argv[1],sys.argv[2]
fs=agq(u,sys.argv[3] if len(sys.argv)>3 else '1=1',fld,geom=False,page=int(sys.argv[4]) if len(sys.argv)>4 else 1000)
c=collections.Counter(str(f['attributes'][fld]) for f in fs);print(len(fs));print(c.most_common(60))
