#!/bin/bash
# Double-click this file once. It installs what indexkit needs, checks the
# tool (selftest) and shows the demo. Safe to double-click again.
cd "$(dirname "$0")" || exit 1
echo "=== indexkit setup ==="
echo ""
if ! python3 -c "import sys" >/dev/null 2>&1; then
  echo "Your Mac needs Apple's free 'command line developer tools' first."
  echo "A box should appear: click Install, wait until it finishes,"
  echo "then double-click setup.command again."
  read -r -p "Press Enter to close this window."
  exit 1
fi
echo "Step 1 of 3: installing numpy and pytest (only slow the first time)..."
if ! python3 -m pip install --user --quiet numpy pytest; then
  echo ""
  echo "The install failed. Copy the messages above and send them to Claude."
  read -r -p "Press Enter to close this window."
  exit 1
fi
echo ""
echo "Step 2 of 3: checking the instrument (about 20 seconds)..."
if ! python3 -m indexkit selftest; then
  echo ""
  echo "The self-test failed. Copy the messages above and send them to Claude."
  read -r -p "Press Enter to close this window."
  exit 1
fi
echo ""
echo "Step 3 of 3: demo (a made-up article: one real hit, one coincidence)..."
python3 -m indexkit demo
open -e demo_output/demo_report_real_hit.md demo_output/demo_report_coincidence.md 2>/dev/null
echo ""
echo "All set. The two demo reports are open in TextEdit."
echo "To test a real clue, double-click test_clue.command."
read -r -p "Press Enter to close this window."
