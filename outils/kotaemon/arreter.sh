#!/usr/bin/env bash
# Arrête Kotaemon (données conservées dans donnees/kotaemon). LLM-Service n'est jamais arrêté ici : il est partagé.
set -euo pipefail
cd "$(dirname "$0")/../.."
outils/kotaemon/compose.sh stop
echo "Kotaemon arrêté."
