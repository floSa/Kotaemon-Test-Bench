#!/usr/bin/env bash
# Démarre Kotaemon (données conservées) et attend la page d'accueil. LLM-Service n'est pas démarré ici : il est géré à part.
set -euo pipefail
cd "$(dirname "$0")/../.."
docker network inspect llm-net >/dev/null 2>&1 || { echo "réseau llm-net absent : démarrer LLM-Service (~/mes_projets/Projet-IA/LLM-Service/scripts/demarrer.sh)"; exit 1; }
docker network inspect rag-local >/dev/null 2>&1 || docker network create rag-local >/dev/null
mkdir -p donnees/kotaemon/ktem_app_data
outils/kotaemon/compose.sh up -d
for i in $(seq 1 150); do
  [ "$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:7860/)" = 200 ] && { echo "Kotaemon prêt : http://127.0.0.1:7860 ($((i*2)) s)"; exit 0; }
  sleep 2
done
echo "Kotaemon ne répond pas après 300 s : docker logs rag-kotaemon"; exit 1
