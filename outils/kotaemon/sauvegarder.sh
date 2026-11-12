#!/usr/bin/env bash
# Sauvegarde de Kotaemon : arrêt bref du conteneur (base SQLite, Chroma et LanceDB cohérentes), archive du dossier de
# données, redémarrage. Les fichiers appartiennent à root (conteneur sans USER) : l'archive est faite par un conteneur
# jetable de l'image de Kotaemon, déjà présente. L'archive contient la clé du service de modèles (spécifications des
# modèles dans la base) : à garder sur le poste.
# Usage : outils/kotaemon/sauvegarder.sh [dossier de destination, défaut donnees/sauvegardes]
set -euo pipefail
cd "$(dirname "$0")/../.."
IMAGE="ghcr.io/cinnamon/kotaemon:main-full@sha256:cb4b71561e529398bacdf12f1289c32290f6c70f286b8efb7a1ed7e66d089b66"
dest="${1:-donnees/sauvegardes}"; mkdir -p "$dest"
nom="kotaemon-$(date +%Y%m%d-%H%M%S).tar.gz"
outils/kotaemon/arreter.sh
docker run --rm --entrypoint tar -v "$PWD/donnees/kotaemon:/src:ro" -v "$(cd "$dest" && pwd):/dest" "$IMAGE" \
  -czf "/dest/$nom" --exclude=ktem_app_data/banc -C /src .
docker run --rm --entrypoint chown -v "$(cd "$dest" && pwd):/dest" "$IMAGE" "$(id -u):$(id -g)" "/dest/$nom"
chmod 600 "$dest/$nom"
outils/kotaemon/demarrer.sh
echo "Sauvegarde : $dest/$nom ($(du -h "$dest/$nom" | cut -f1))"
