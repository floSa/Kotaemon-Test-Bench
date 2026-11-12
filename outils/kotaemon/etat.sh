#!/usr/bin/env bash
# État de Kotaemon : conteneur, ports (liés à 127.0.0.1), réponse HTTP, mémoire, disque ; santé du service LLM central (lecture seule).
set -uo pipefail
cd "$(dirname "$0")/../.."
echo "== conteneur";  docker ps -a --filter name=rag-kotaemon --format '{{.Names}} {{.Status}} {{.Ports}}'
echo "== http";       curl -s -o /dev/null -m 5 -w 'HTTP %{http_code}\n' http://127.0.0.1:7860/
echo "== mémoire";    docker stats --no-stream --format '{{.Name}} {{.MemUsage}} {{.CPUPerc}}' rag-kotaemon 2>/dev/null
echo "== disque";     du -sh donnees/kotaemon 2>/dev/null
echo "== service LLM central"; outils/communs/llm_central_sante.sh 2>&1 | head -6
