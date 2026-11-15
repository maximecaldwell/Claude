#!/usr/bin/env python3
"""Build EN/FR HTML from a new-DFHD (Arches) search JSON hit (all bilingual string tiles, in order).
usage: adpf_to_html.py SEARCH.json RESOURCE_ID_PREFIX OUT_PREFIX"""
import json, sys, html
d = json.load(open(sys.argv[1]))
hit = [r for r in d['results']['hits']['hits'] if r['_id'].startswith(sys.argv[2])][0]
for L in ('en', 'fr'):
    out = ['<html><body>']
    first = True
    for t in hit['_source']['tiles']:
        for k, v in t['data'].items():
            if isinstance(v, dict) and L in v:
                x = v[L]
                x = x.get('value', '') if isinstance(x, dict) else x
                if not x or not x.strip():
                    continue
                if first:
                    out.append('<h1>%s</h1>' % html.escape(x)); first = False
                elif '<' in x:
                    out.append('<div>%s</div>' % x)
                else:
                    out.append('<p>%s</p>' % html.escape(x))
    out.append('</body></html>')
    open('%s_%s.html' % (sys.argv[3], L.upper()), 'w').write('\n'.join(out))
print(hit['_id'], hit['_source']['displayname'])
