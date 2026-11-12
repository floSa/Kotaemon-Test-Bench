#!/usr/bin/env bash
# Lance un exemple Python DANS le conteneur rag-kotaemon (environnement /app/.venv de Kotaemon, dossier /app).
# La clé du service central est passée par variable d'environnement (LLM_CENTRAL_KEY, lue dans .env), jamais affichée.
# Usage : exemples/kotaemon/lancer.sh exemples/kotaemon/02_lister_collections.py
set -euo pipefail
cd "$(dirname "$0")/../.."
set -a; . ./.env; set +a
docker exec -i -e LLM_CENTRAL_KEY="$LLM_CENTRAL_KEY" -w /app rag-kotaemon /app/.venv/bin/python - < "$1" 2>&1 \
  | grep -v "alts_credentials\|absl::InitializeLog\|nltk_data\|punkt_tab\|^\s*$"
