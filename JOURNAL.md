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

### 2026-11-12 21:15 — Phase C et D : cadrage, installation, configuration par l'interface

- Cadrage par deux sous-agents (`cadrage-serveur.md`, `cadrage-interface.md`), relecture (`relecture.md`).
- Installation `outils/kotaemon/installer.sh` (33 s hors téléchargement, 0,6 à 0,9 Gio au repos, port `127.0.0.1:7860`, `ports-publies-2026-11-12.txt`). Version affichée « 0.0.1 » (numéro git absent de l'image) : révision de l'image 9ad3e4e = v0.12.0.
- Chapitre 03 par Playwright : mot de passe admin changé (identifiants dans `donnees/IDENTIFIANTS-LOCAUX.txt`), modèles `llm-service-chat` (ChatOpenAI), `llm-service-embed` (OpenAIEmbeddings, sans `context_length`), `llm-service-rerank` (CohereReranking, `base_url` sans `/v1`) : test de connexion réussi pour les trois. Langue French, contexte 8000.
- Incidents : notation par LLM (10 appels simultanés) refusée en 429 par llama-swap (4 requêtes à la fois), réponse bloquée sur « Thinking ... » (`incident-2026-11-12-429-score-llm.log`) : option décochée ; langue de la session de chat (English) prioritaire sur « Settings » ; visionneuse PDF vide (`cdn.skypack.dev/pdfjs-viewer-element` en erreur de construction, `incident-2026-11-12-visionneuse-pdf.txt`) ; DOCX et PPTX en échec « HTTP Error 403 » (données NLTK d'unstructured sur un S3 fermé) : `installer.sh` télécharge `punkt_tab` et `averaged_perceptron_tagger_eng` depuis le dépôt NLTK, `NLTK_DATA` dans le compose (`installation-2026-11-12-essai-nltk-403.log`) ; fichiers en échec inscrits sans passage (réindexés d'office par le pilote du banc) ; MP3 refusé (format non lu).
- Banc : adaptateur par la bibliothèque dans le conteneur (`pilote_conteneur.py`, `banc.py`), réglages de l'interface. Premier banc lancé (sans reranker).
- Prochaine étape : banc avec `rerank`, captures des chapitres 05 à 13, rédaction.
