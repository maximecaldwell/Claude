# BFS over sudburymuseums.ca virtual-museum "Greater Sudbury Histories" subtree (EN), list pages.
import re, subprocess, sys, json, time
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
V='https://sudburymuseums.ca/index.cfm?app=w_vmuseum&lang=en&currID=%s&parID=%s'
top={'1396','1397','1398','1399','1400','1401','1402'}
seen={}; q=[(c,'1390',1) for c in sorted(top)]
while q and len(seen)<150:
    c,p,d=q.pop(0)
    if c in seen: continue
    h=subprocess.run(['curl','-sL','-A',UA,'-m','40',V%(c,p)],capture_output=True).stdout.decode('utf-8','replace')
    m=re.search(r'<div class="title"[^>]*>(.*?)</div>',h,re.S)
    t=re.sub(r'<[^>]+>|\s+',' ',m.group(1)).strip() if m else ''
    seen[c]=(p,d,t)
    i=h.find('id="content"')
    for cc,pp in re.findall(r'currID=(\d+)&(?:amp;)?parID=(\d+)',h[i:]):
        if cc not in seen and pp!='0' and d<3: q.append((cc,pp,d+1))
for c,(p,d,t) in seen.items(): print(c,p,d,t,sep='\t')
