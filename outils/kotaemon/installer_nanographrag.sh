#!/usr/bin/env bash
# Option NanoGraphRAG (chapitre 09) : active la collection « NanoGraphRAG Collection » et installe le paquet nano-graphrag
# dans l'environnement Python du conteneur, comme l'indique le README de Kotaemon (« pip install nano-graphrag », puis
# remplacement de hnswlib par chroma-hnswlib en cas de conflit).
#  1. USE_NANO_GRAPHRAG=true dans donnees/kotaemon/options.env, conteneur recréé (la collection est créée au démarrage) ;
#  2. installation du paquet à version figée (uv, dans /app/.venv), relevé des paquets modifiés ;
#  3. redémarrage du conteneur (docker restart : le paquet installé est conservé tant que le conteneur n'est pas recréé).
# Le paquet disparaît si le conteneur est recréé (installer.sh, changement du compose) : relancer alors ce script.
# Usage : outils/kotaemon/installer_nanographrag.sh  (journal : outils/resultats/kotaemon/nanographrag-<date>.log)
set -euo pipefail
cd "$(dirname "$0")/../.."
VERSION="0.0.8.2"
JOURNAL="outils/resultats/kotaemon/nanographrag-$(date +%F).log"
exec > >(tee -a "$JOURNAL") 2>&1
echo "== installer_nanographrag.sh $(date -Iseconds)"
mkdir -p donnees/kotaemon
touch donnees/kotaemon/options.env
grep -q '^USE_NANO_GRAPHRAG=' donnees/kotaemon/options.env || echo 'USE_NANO_GRAPHRAG=true' >> donnees/kotaemon/options.env
outils/kotaemon/demarrer.sh
docker exec rag-kotaemon sh -c '/app/.venv/bin/python -c "import importlib.metadata as m; print(\"\n\".join(sorted(f\"{d.metadata[\"Name\"]}=={d.version}\" for d in m.distributions())))" > /tmp/avant.txt'
debut=$(date +%s)
docker exec rag-kotaemon uv pip install --python /app/.venv "nano-graphrag==$VERSION"
echo "durée d'installation : $(( $(date +%s) - debut )) s"
docker exec rag-kotaemon sh -c '/app/.venv/bin/python -c "import importlib.metadata as m; print(\"\n\".join(sorted(f\"{d.metadata[\"Name\"]}=={d.version}\" for d in m.distributions())))" > /tmp/apres.txt; diff /tmp/avant.txt /tmp/apres.txt || true'
docker restart rag-kotaemon >/dev/null
for i in $(seq 1 150); do [ "$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:7860/)" = 200 ] && break; sleep 2; done
docker logs --since 5m rag-kotaemon 2>&1 | grep -i "graphrag\|error" | grep -v alts | tail -5 || true
echo "Kotaemon redémarré avec NanoGraphRAG : http://127.0.0.1:7860"
