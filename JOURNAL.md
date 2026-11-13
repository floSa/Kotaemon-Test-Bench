# Journal — Kotaemon

Mission : `kit/PROMPT.md` pour la fiche `kit/fiches/03-kotaemon.md`. Une entrée par étape (date, phase, fait, résultat, fichiers, prochaine étape).

## Décisions en attente

1. LLM-Service : modèle de réponse plus léger (ou alias sans réflexion de `chat`) pour situer un plancher de qualité. Hors mission (modification de LLM-Service).
2. Serveur PaddleOCR externe, et serveur Docling sur une autre machine : même méthode que l'essai du 13 novembre, non essayés.
3. Sauvegarde d'essai `donnees/sauvegardes/kotaemon-20261113-013435.tar.gz` (1 007 Mo) : garder ou supprimer.
4. Changer la clé du service LLM central (un préfixe de 6 caractères est resté dans l'historique git) : relève de l'utilisateur, LLM-Service n'étant pas modifiable par la mission.

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

### 2026-11-13 02:00 — Phases E à H : bancs, captures, manuels, annexes, rapport

- Bancs (free -m et santé en tête des `banc-*.log`) : sans tri 26/34 (25 après relecture, Q17 faux positif), `rerank` 26/34, Docling pour le scan 30/34, 3 passages 31/34 ; 4/4 refus partout ; médiane 22 à 26 s.
- Captures des chapitres 03 à 13 (92) et carte (24), par Playwright ; exemples 01 à 04 (code 0).
- Nouveaux constats : « Delete » sans confirmation ; groupe qui perd un fichier relu (« Force reindex ») ; création d'une collection = réglages non relus (KeyError index.options.4.reader_mode), réparés par un nouvel enregistrement ; notation par le modèle : AssertionError (note non reconnue), alerte jamais affichée ; question de suite envoyée trop tôt non affichée ; LightRAG sans pipmaster (`completer_lightrag.sh`), indexation 527 s, réponse juste ; nano-graphrag : hnswlib puis pydantic cassent Chroma et Gradio (corrigés dans `installer_nanographrag.sh`), puis EmptyNetworkError ; Microsoft GraphRAG : « No module named 'graphrag' » ; question de 82 542 caractères : LanceError.
- Sauvegarde (1 007 Mo) et restauration réussies (`exploitation-2026-11-12.log`).
- Jeu de démonstration (`captures/demo.py`) : 35 conversations d'essai retirées, trois conversations « Démo — … ».
- Question de l'utilisateur (Docling externe) : méthode documentée (A3 §5, chapitre 05), essai en attente d'accord (image docling-serve hors enveloppe).
- Manuels 01 à 14, annexes A1 à A6, carte, README, index de la série, outils/README, RAPPORT ; `verifier_docs.py` à 0 point.
- Prochaine étape : relecture par un lecteur novice, relecture adversariale des annexes, commit final.

### 2026-11-13 04:30 — Phase H : relectures et clôture

- Relecture par un lecteur novice (partie 1), dix-sept passages avec un sous-agent neuf à chaque fois : 34, 24, 15, 3, 6, 7, 2, 2, 3, 3, 4, 5, 1, 1, 4, 4 remarques, puis « Aucune remarque » au dix-septième. Corrections commitées après chaque passage (captures refaites : 04/09, 06/06, 06/07, 06/12, 07/03, 07/04, 07/07, 08/02, 10/04, 11/04, 11/07, 12/01, 12/02 ; règle de langue unifiée ; nombre de passages conseillé 3 ; consignes de réglage après création de collection ; ordre des scripts LightRAG et NanoGraphRAG).
- Relecture adversariale des annexes : 27 écarts corrigés (requalifications, chiffres rectifiés, relevé `fin-de-mission-2026-11-13.log`) ; un préfixe de 6 caractères de la clé trouvé dans `graphrag-2026-11-13.log`, masqué (commit 87ce88a, historique non réécrit) : changement de clé inscrit dans les décisions en attente.
- Incident de ménage : le premier filtre de `demo.py` a supprimé aussi les conversations de démonstration et la conversation partagée ; recréées par l'interface (filtre corrigé).
- Style « citation: inline » : 2 réponses sur 7 essais (`captures/06-questions/notes.log`) ; chapitre 06 réécrit tel quel.
- État : Kotaemon en marche sur http://127.0.0.1:7860, jeu de démonstration en place, `verifier_docs.py` à 0 point.

### 2026-11-13 08:10 — Complément : serveur Docling séparé

- Demande de l'utilisateur (un essai, pas de banc) : docling-serve v1.38.2 (CPU, `quay.io/docling-project/docling-serve-cpu` figée par empreinte, 5,06 Go) dans `rag-docling-serve`, réseau `llm-net`, sans port publié.
- Branchement : `outils/kotaemon/docling_externe/` (lecteur `LecteurDoclingServe`, copie de `flowsettings.py` avec `FILE_INDEX_PIPELINE_FILE_EXTRACTORS`, `brancher.sh`, `debrancher.sh`) et `compose.docling-externe.yml`.
- Résultat : contrat scanné relu en 10 à 14 s (contre 47 s avec le Docling intégré), colonne « loader » `LecteurDoclingServe`, texte des pages lu ; « File loader » inchangé (`docling-externe-2026-11-13.log`, scénario `captures/c05_docling_externe.py`, capture 18 du chapitre 05). Groupe « Fournisseur Batterix » réparé ; serveur débranché, Kotaemon revenu à sa configuration (HTTP 200).
- Documentation : chapitre 05 (explication Docling intégré ou séparé, étapes 17 et 18), annexe A3 §5, A6, README, RAPPORT.

### 2026-11-13 — Uniformisation de la série

- `docs/README.md` remplacé par l'index commun aux cinq dépôts (Open Notebook, RAGFlow, AnythingLLM, Kotaemon, Open WebUI) : modèles utilisés, services déportables (OCR, audio, reranker), comparatif à deux lignes par solution (défaut, meilleur réglage). Chiffres repris des résultats bruts du 12 et du 13 novembre, aucun nouveau banc.
- README : section « Résultats » au même format que les autres dépôts.
- `verifier_docs.py` : 0 point.

### 2026-11-13 — Banc avec Docling déporté

- Kotaemon démarré avec `compose.docling-externe.yml` (service kotaemon seul, `--no-deps` : le conteneur `rag-docling-serve` tournait déjà, partagé avec Open WebUI).
- `outils/kotaemon/banc.py` : options `--reindexer` (réindexation forcée) et `--docling-deporte` (vérifie le branchement, compte Docling avec l'application).
- Banc `docling-deporte-rerank-serre-top3` : 29/34 (31 avec le Docling intégré, qui ne relisait que le scan), 4/4, médiane 18,4 s, indexation 28 s. Q13 et Q24 (tableaux du rapport annuel) échouent : tous les PDF sont relus par Docling. Annexe A1 (section 2.1) et index de la série à jour. Kotaemon remis dans sa configuration d'origine, puis arrêté.

### 2026-11-13 — Docling déporté partagé

- `brancher.sh` réutilise un serveur `rag-docling-serve` déjà démarré (partagé avec Open WebUI) au lieu d'échouer sur le nom du conteneur ; `debrancher.sh` ne supprime le serveur que s'il a été lancé par Kotaemon. [Testée] dans les deux sens. Manuel 05, étape 17 : une phrase sur ce cas.
