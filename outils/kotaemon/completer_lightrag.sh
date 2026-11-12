#!/usr/bin/env bash
# LightRAG (collection « LightRAG Collection ») : l'image main-full (v0.12.0) installe lightrag-hku 1.3.0 sans sa
# dépendance pipmaster ; l'indexation s'arrête sur « Error: No module named 'pipmaster' ». Ce script l'ajoute dans
# l'environnement Python du conteneur (uv, version figée), sans redémarrage. À relancer si le conteneur est recréé.
# Usage : outils/kotaemon/completer_lightrag.sh  (journal : outils/resultats/kotaemon/lightrag-dependance-<date>.log)
set -euo pipefail
cd "$(dirname "$0")/../.."
exec > >(tee -a "outils/resultats/kotaemon/lightrag-dependance-$(date +%F).log") 2>&1
echo "== completer_lightrag.sh $(date -Iseconds)"
docker exec rag-kotaemon uv pip install --python /app/.venv "pipmaster==1.2.2"
docker exec rag-kotaemon /app/.venv/bin/python -c "import pipmaster, lightrag.llm.openai; print('pipmaster', pipmaster.__file__)"
