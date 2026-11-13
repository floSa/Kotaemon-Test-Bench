#!/usr/bin/env bash
# Revient au fonctionnement d'origine : Kotaemon sans le lecteur extérieur. Le serveur rag-docling-serve n'est arrêté
# et supprimé que s'il a été lancé par Kotaemon (projet rag-kotaemon) ; un serveur partagé reste en place.
set -euo pipefail
cd "$(dirname "$0")/.."
if [ "$(docker inspect -f '{{index .Config.Labels "com.docker.compose.project"}}' rag-docling-serve 2>/dev/null)" = rag-kotaemon ]; then
  ./compose.sh -f compose.docling-externe.yml rm -sf docling-serve
fi
./compose.sh up -d --force-recreate kotaemon
