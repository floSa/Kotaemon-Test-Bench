#!/usr/bin/env bash
# Série de bancs sur la même « File Collection » (même corpus, mêmes questions) : seuls les réglages changent.
# free -m et santé du service central relevés avant chaque banc (kit/PROMPT.md §2). Usage : serie_banc.sh <étiquette> [options banc.py]
set -uo pipefail
cd "$(dirname "$0")/../.."
etiq="$1"; shift
log="outils/resultats/kotaemon/banc-$(date +%F)-$etiq.log"
{ free -m | head -2; outils/communs/llm_central_sante.sh --essai 2>&1 | tail -12; } > "$log" 2>&1
python3 -u outils/kotaemon/banc.py --etiquette "$etiq" "$@" >> "$log" 2>&1
tail -2 "$log"
