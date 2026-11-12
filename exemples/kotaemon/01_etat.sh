#!/usr/bin/env bash
# Vérifie que l'interface de Kotaemon répond sur le poste et lit la version de Gradio annoncée par la page.
set -euo pipefail
curl -s -o /dev/null -w 'interface : HTTP %{http_code} en %{time_total} s\n' http://127.0.0.1:7860/
curl -s http://127.0.0.1:7860/config | python3 -c "import json,sys; c=json.load(sys.stdin); print('Gradio', c.get('version'), '- titre :', c.get('title'))"
docker ps --filter name=rag-kotaemon --format 'conteneur : {{.Names}} {{.Status}} {{.Ports}}'
