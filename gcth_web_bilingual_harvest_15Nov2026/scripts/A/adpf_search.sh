#!/bin/bash
# usage: adpf_search.sh TERM OUT.json   -- new Parks Canada DFHD (Arches) search API, with tiles
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
TF=$(python3 -I -c "import urllib.parse,json,sys;t=sys.argv[1];print(urllib.parse.quote(json.dumps([{'inverted':False,'type':'string','context':'','context_label':'','id':t,'text':t,'value':t}])))" "$1")
curl -s -A "$UA" "https://adpf-dfhd.pc.gc.ca/en/search/resources?term-filter=$TF&paging-filter=1&tiles=true" -o "$2" -w '%{http_code} %{size_download}\n'
