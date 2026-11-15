#!/bin/bash
# usage: fetch.sh URL OUTFILE
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
curl -s -L --compressed --max-time 60 -A "$UA" -H "Accept-Language: en-CA,en;q=0.9,fr-CA;q=0.8" -o "$2" -w '%{http_code} %{size_download} %{url_effective}\n' "$1"
