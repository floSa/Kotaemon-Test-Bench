#!/usr/bin/env bash
# Revient à la configuration d'origine : Kotaemon sans lecteur extérieur, serveur Docling séparé arrêté et supprimé.
set -euo pipefail
cd "$(dirname "$0")/.."
./compose.sh -f compose.docling-externe.yml rm -sf docling-serve
./compose.sh up -d --force-recreate kotaemon
