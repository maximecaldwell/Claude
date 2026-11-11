import json,sys,time
sys.argv=['x'];sys.path.insert(0,'/tmp/claude-0/-home-user-Claude/e088f49c-24ac-59a0-bf76-b6e7517bba6d/scratchpad/plaques_canada/scripts')
src=open('/tmp/claude-0/-home-user-Claude/e088f49c-24ac-59a0-bf76-b6e7517bba6d/scratchpad/plaques_canada/scripts/hp_detail.py').read()
g={};exec(src.split("ids=list(")[0].replace('import geo','import geo'),g)
exec('def get'+src.split('def get')[1].split('with ThreadPoolExecutor')[0],g)
P=g['geo'].R+'hp_details.json';D=json.load(open(P))
for rnd in range(3):
    for i,o in enumerate(D['details']):
        if o['lat'] is None:
            D['details'][i]=g['get'](o['id']);time.sleep(0.5)
    print(rnd,sum(1 for o in D['details'] if o['lat'] is None),flush=True)
json.dump(D,open(P,'w'))
