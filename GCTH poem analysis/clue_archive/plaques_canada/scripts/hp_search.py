import re,subprocess,urllib.parse,json,sys,os
OUT=sys.argv[1]; kw=sys.argv[2]
UA='gcth-desk-research/1.0'
url='https://www.historicplaces.ca/en/results-resultats.aspx?m=2&Keyword='+urllib.parse.quote(kw)
ck='/tmp/hpck.txt'
h=subprocess.run(['curl','-sS','-m','90','-A',UA,'-c',ck,'-b',ck,url],capture_output=True).stdout.decode('utf8','ignore')
f={}
for m in re.finditer(r'<input[^>]*type="hidden"[^>]*>',h):
    n=re.search(r'name="([^"]+)"',m.group(0));v=re.search(r'value="([^"]*)"',m.group(0))
    if n: f[n.group(1)]=(v.group(1) if v else '').replace('&#43;','+').replace('&amp;','&')
dd=re.search(r"name=\"([^\"]*ddlResultsPerPage)\"",h)
if not dd: print(kw,"no results");json.dump([],open(OUT,"w"));sys.exit()
dd=dd.group(1)
f[dd]='65535';f['__EVENTTARGET']=dd;f['__EVENTARGUMENT']=''
tot=re.findall(r'Total Results:[^0-9]{0,200}([0-9,]+)',h)
open('/tmp/hppost.txt','w').write(urllib.parse.urlencode(f))
h2=subprocess.run(['curl','-sS','-m','300','-A',UA,'-c',ck,'-b',ck,'--data','@/tmp/hppost.txt',url],capture_output=True).stdout.decode('utf8','ignore')
m=re.search(r'var placeLayer = (\[.*?\]);',h2,re.S)
pl=json.loads(re.sub(r'\\(?!["\\/bfnrtu])','',m.group(1)),strict=False) if m else []
json.dump(pl,open(OUT,'w'))
print(kw,'total',tot[:1],'got',len(pl))
