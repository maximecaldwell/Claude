#!/bin/bash
# usage: tce_batch.sh slug...   (run from bi/A)
for s in "$@"; do
  scripts/fetch.sh https://thecanadianencyclopedia.ca/en/article/$s raw/tce_${s}_EN.html >/dev/null
  fr=$(grep -o 'hreflang="fr" href="[^"]*"' raw/tce_${s}_EN.html | head -1 | sed 's/.*href="//;s/"$//')
  echo "$s -> $fr"
  [ -n "$fr" ] && scripts/fetch.sh "$fr" raw/tce_${s}_FR.html
done
