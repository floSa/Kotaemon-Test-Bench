#!/usr/bin/env bash
# Restauration de Kotaemon depuis une archive de sauvegarder.sh : arrêt, l'ancien dossier de données est gardé à côté
# (donnees/kotaemon.avant-restauration-<date>), extraction, redémarrage.
# Usage : outils/kotaemon/restaurer.sh <archive .tar.gz>
set -euo pipefail
cd "$(dirname "$0")/../.."
IMAGE="ghcr.io/cinnamon/kotaemon:main-full@sha256:cb4b71561e529398bacdf12f1289c32290f6c70f286b8efb7a1ed7e66d089b66"
archive="${1:?usage : restaurer.sh <archive .tar.gz>}"
[ -f "$archive" ] || { echo "archive introuvable : $archive"; exit 1; }
outils/kotaemon/arreter.sh
ancien="donnees/kotaemon.avant-restauration-$(date +%Y%m%d-%H%M%S)"
[ -d donnees/kotaemon ] && mv donnees/kotaemon "$ancien" && echo "ancien dossier gardé : $ancien"
mkdir -p donnees/kotaemon
docker run --rm --entrypoint tar -v "$PWD/donnees/kotaemon:/dst" -v "$(cd "$(dirname "$archive")" && pwd):/src:ro" "$IMAGE" \
  -xzf "/src/$(basename "$archive")" -C /dst
outils/kotaemon/demarrer.sh
echo "Restauré depuis $archive"
