#!/usr/bin/env python3
"""Extract a Northern Miner post (title + content.rendered) from saved WP REST JSON.
usage: tnm_en.py link_substring out.txt json_files..."""
import sys, json, html, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract import extract

key, out = sys.argv[1], sys.argv[2]
for f in sys.argv[3:]:
    try:
        d = json.load(open(f))
    except Exception:
        continue
    for p in d if isinstance(d, list) else []:
        if key in p['link']:
            title = html.unescape(p['title']['rendered'])
            body = extract('<div id="c">' + p['content']['rendered'] + '</div>', '#c',
                           'figure,.wp-caption,.wp-block-embed,.wp-block-file,.wp-block-buttons')
            body = '\n\n'.join(b for b in body.split('\n\n') if not b.startswith(('\U0001f3a5', '\U0001f5de')))
            open(out, 'w', encoding='utf-8').write(title + '\n\n' + body + '\n')
            print(out, len((title + ' ' + body).split()), p['link'])
            sys.exit(0)
print('not found', key)
