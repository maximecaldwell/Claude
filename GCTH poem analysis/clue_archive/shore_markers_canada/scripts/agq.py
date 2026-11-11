import json,urllib.parse,time,subprocess
def getj(url,p=None,post=False,timeout=180):
    q=url+('?'+urllib.parse.urlencode(p) if p and not post else '')
    cmd=['curl','-sS','-m',str(timeout),q]
    if post: cmd+=['--data',urllib.parse.urlencode(p)]
    err=''
    for i in range(3):
        try:
            r=subprocess.run(cmd,capture_output=True,timeout=timeout+10)
            return json.loads(r.stdout)
        except Exception as e: err=str(e)+' '+r.stdout[:200].decode('latin1') if 'r' in dir() else str(e);time.sleep(3)
    return {'error':err}
def agq(url,where,fields='*',geom=True,page=1000,extra=None,byoid=False):
    out=[]
    if byoid:
        ids=sorted(getj(url+'/query',dict(where=where,returnIdsOnly='true',f='json'))['objectIds'] or [])
        for i in range(0,len(ids),page):
            ch=ids[i:i+page]
            p=dict(objectIds=','.join(map(str,ch)),outFields=fields,returnGeometry=str(geom).lower(),outSR=4326,f='json')
            d=getj(url+'/query',p,post=True)
            if 'error' in d: raise Exception(str(d['error'])[:300])
            out+=d.get('features',[])
        return out
    off=0
    while True:
        p=dict(where=where,outFields=fields,returnGeometry=str(geom).lower(),outSR=4326,f='json',resultOffset=off,resultRecordCount=page)
        if extra: p.update(extra)
        d=getj(url+'/query',p)
        if 'error' in d: raise Exception(str(d['error'])[:300])
        fs=d.get('features',[]);out+=fs
        if not d.get('exceededTransferLimit') and len(fs)<page: break
        if not fs: break
        off+=len(fs)
    return out
