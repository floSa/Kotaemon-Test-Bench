#!/usr/bin/env bash
# Lance le serveur Docling séparé et redémarre Kotaemon branché dessus (manuel, chapitre 05).
set -euo pipefail
cd "$(dirname "$0")/.."
./compose.sh -f compose.docling-externe.yml up -d
for i in $(seq 1 150); do
  [ "$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:7860/)" = 200 ] && { echo "Kotaemon prêt, PDF lus par rag-docling-serve ($((i*2)) s)"; exit 0; }
  sleep 2
done
echo "Kotaemon ne répond pas après 300 s : docker logs rag-kotaemon"; exit 1
