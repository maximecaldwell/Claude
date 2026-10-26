#!/bin/bash
# Double-click this file to test a clue. It asks you a few questions,
# runs indexkit, and opens the report. Safe to double-click again.
cd "$(dirname "$0")" || exit 1
echo "=== indexkit: test a clue ==="
echo ""
echo "Before you start, save these files in this folder:"
echo "  $(pwd)"
echo "  - the English article as plain text (title on the first line,"
echo "    one empty line between paragraphs), e.g. article_en.txt"
echo "  - the French article the same way, e.g. article_fr.txt (optional)"
echo "  - a list of place names, one per line, e.g. places.txt (optional)"
echo "Just press Enter to accept the name in [brackets]."
echo ""

read -r -p "Digits, exactly as in the clue (e.g. 810-419-227): " DIGITS
if [ -z "$DIGITS" ]; then
  echo "No digits given."; read -r -p "Press Enter to close."; exit 1
fi
read -r -p "English article file [article_en.txt]: " EN
EN=${EN:-article_en.txt}
read -r -p "French article file [article_fr.txt] (type - if none): " FR
FR=${FR:-article_fr.txt}
read -r -p "Place-name list [places.txt] (type - if none): " TG
TG=${TG:-places.txt}

ARGS=(--digits "$DIGITS")
if [ "$EN" != "-" ]; then ARGS+=(--text "en=$EN"); fi
if [ "$FR" != "-" ]; then ARGS+=(--text "fr=$FR"); fi
if [ "$TG" != "-" ]; then ARGS+=(--targets "$TG"); fi
if [ "$EN" = "-" ] && [ "$FR" = "-" ]; then
  echo "At least one article is needed."; read -r -p "Press Enter to close."; exit 1
fi

SAFE=$(printf '%s' "$DIGITS" | tr -c '0-9' '_' | sed 's/__*/_/g; s/^_//; s/_$//')
OUT="report_${SAFE}.md"
ARGS+=(--out "$OUT")

echo ""
python3 -m indexkit run "${ARGS[@]}"
STATUS=$?
echo ""
if [ $STATUS -eq 0 ]; then
  open -e "$OUT" 2>/dev/null
  echo "The full report ($OUT) is open in TextEdit."
else
  echo "Something went wrong. Copy the messages above and send them to Claude."
fi
read -r -p "Press Enter to close this window."
