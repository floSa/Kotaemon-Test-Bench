#!/usr/bin/env bash
# Installation rejouable et idempotente de Kotaemon v0.12.0 (image officielle « full »), branchée au service LLM central.
#  1. image officielle figée par empreinte ;
#  2. dossier de données donnees/kotaemon (ignoré par git) ;
#  3. démarrage du projet compose rag-kotaemon (outils/kotaemon/compose.yml) et attente de la page d'accueil ;
#  4. vérification des ports (127.0.0.1 seulement) ; durée, taille de l'image, RAM au repos, disque.
# Le mot de passe du compte admin, la langue des réponses et les modèles (chat, embed, rerank) se règlent ensuite dans
# l'interface (manuel, chapitre 03). Aucune clé n'est écrite par ce script.
# Usage : outils/kotaemon/installer.sh   (journal : outils/resultats/kotaemon/installation-<date>.log)
set -euo pipefail
RACINE="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$RACINE"
IMAGE="ghcr.io/cinnamon/kotaemon:main-full@sha256:cb4b71561e529398bacdf12f1289c32290f6c70f286b8efb7a1ed7e66d089b66"
JOURNAL="outils/resultats/kotaemon/installation-$(date +%F).log"
mkdir -p "$(dirname "$JOURNAL")"
exec > >(tee -a "$JOURNAL") 2>&1
echo "== installer.sh $(date -Iseconds)"
debut=$(date +%s)
outils/kotaemon/compose.sh version >/dev/null || { echo "docker compose indisponible"; exit 1; }
docker network inspect llm-net >/dev/null 2>&1 || { echo "réseau llm-net absent : démarrer LLM-Service (~/mes_projets/Projet-IA/LLM-Service/scripts/demarrer.sh)"; exit 1; }
docker network inspect rag-local >/dev/null 2>&1 || docker network create rag-local
free -m | awk '/Mem:/{print "RAM disponible avant installation : " $7 " Mo"}'
docker image inspect "$IMAGE" >/dev/null 2>&1 || docker pull "$IMAGE"
docker image inspect --format 'image : {{index .RepoDigests 0}} {{.Size}} octets, révision {{index .Config.Labels "org.opencontainers.image.revision"}}' "$IMAGE"
mkdir -p donnees/kotaemon/ktem_app_data
outils/kotaemon/demarrer.sh
docker ps --filter name=rag-kotaemon --format '{{.Names}} {{.Ports}}'
docker ps --format '{{.Names}} {{.Ports}}' | grep -oE '[0-9a-f.:\[\]]+->' | grep -v '^127\.0\.0\.1:' && { echo "port publié hors de 127.0.0.1"; exit 1; } || echo "ports publiés : tous liés à 127.0.0.1"
echo "durée : $(( $(date +%s) - debut )) s"
sleep 5
docker stats --no-stream --format 'RAM au repos : {{.Name}} {{.MemUsage}}' rag-kotaemon
du -sh donnees/kotaemon | sed 's/^/disque des données : /'
