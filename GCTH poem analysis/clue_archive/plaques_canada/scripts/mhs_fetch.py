import re,subprocess,json,html
from concurrent.futures import ThreadPoolExecutor
R='/tmp/claude-0/-home-user-Claude/e088f49c-24ac-59a0-bf76-b6e7517bba6d/scratchpad/plaques_canada/raw/'
h=open('/tmp/mb1870.html',encoding='latin1').read()
rows=re.findall(r"<a href='(http://www.mhs.mb.ca/docs/sites/[^']+)' target='_blank'>([^<]*)</a></td><td[^>]*>([^<]*)</td><td[^>]*>([^<]*)</td>",h)
print(len(rows),flush=True)
def get(r):
    u,n,m,a=r
    t=subprocess.run(['curl','-sS','-m','40','-A','gcth-desk-research/1.0',u],capture_output=True).stdout.decode('latin1')
    txt=html.unescape(re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',t)))
    c=re.search(r'Site Coordinates \(lat/long\):\s*N([0-9.]+),\s*W([0-9.]+)',txt)
    i=txt.find(n);body=''
    m2=re.search(re.escape(n)+r'(.*?)(Site Coordinates|Sources:)',txt)
    if m2: body=m2.group(1)[-1500:]
    return dict(url=u,name=html.unescape(n),muni=m,addr=a,lat=float(c.group(1)) if c else None,lon=-float(c.group(2)) if c else None,text=body.strip())
with ThreadPoolExecutor(4) as ex: out=list(ex.map(get,rows))
json.dump(out,open(R+'mhs_monuments.json','w'))
print('done',len(out),sum(1 for o in out if o['lat']))
