# Journal — Kotaemon

Mission : `kit/PROMPT.md` pour la fiche `kit/fiches/03-kotaemon.md`. Une entrée par étape (date, phase, fait, résultat, fichiers, prochaine étape).

## Décisions en attente

1. LLM-Service : modèle de réponse plus léger pour situer un plancher de qualité. Hors mission (modification de LLM-Service).

### 2026-11-12 19:30 — Phase A : diagnostic de la machine et santé du service central

- Fait : `outils/communs/llm_central_sante.sh --essai` en début de session : modèles listés (`chat`, `embed`, `rerank`, `transcribe` et alias), une requête réussie par usage (sortie : `outils/resultats/kotaemon/sante-2026-11-12-debut.txt`, code 0).
- AnythingLLM (banc précédent, `rag-anythingllm`) arrêté par son `arreter.sh` avant de commencer.
- `outils/communs/diagnostic.sh` : `outils/resultats/machine/diagnostic-2026-11-12.json` (machine du profil B, service central en profil `gpu`, `sante_essai` OK).
- Version : dernière release stable `v0.12.0` (31 mai 2026, `versions-2026-11-12.json`). Aucune image ghcr au tag 0.12.0 (étiquettes listées : 0.11.0-full est la dernière numérotée, `latest-full` pointe sur 0.11.0) ; `main` du dépôt = tag `v0.12.0` (commit 9ad3e4e, aucun commit après) : image `ghcr.io/cinnamon/kotaemon:main-full` figée par empreinte `sha256:cb4b71561e529398bacdf12f1289c32290f6c70f286b8efb7a1ed7e66d089b66`, comme le prévoit la fiche.
- Sources au tag dans `sources/kotaemon` (ignoré par git) ; cadrage confié à deux sous-agents (serveur, interface).
- Prochaine étape : cadrage, relecture, installation.
