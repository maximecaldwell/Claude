#!/bin/bash
# usage: fetch_lac.sh URL OUT  (LAC web archive; sets disclaimer cookie)
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
curl -s -L --max-time 60 -A "$UA" -b "disclaimed=1" -o "$2" -w '%{http_code} %{size_download} %{url_effective}\n' "$1"
