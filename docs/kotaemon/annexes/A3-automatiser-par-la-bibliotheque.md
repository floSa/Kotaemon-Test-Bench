# A3. Automatiser par la bibliothèque Python

> **Objet** : piloter Kotaemon sans l'interface (lister les collections, indexer, poser une question), construire un pipeline personnalisé avec la bibliothèque `kotaemon`, et brancher un lecteur de fichiers extérieur (serveur Docling ou PaddleOCR).
> **Prérequis** : installation du [chapitre 02](../manuel/02-installer-kotaemon.md), modèles déclarés au [chapitre 03](../manuel/03-premiers-pas.md) ; terminal Ubuntu à la racine du dépôt.
> **Version décrite** : Kotaemon 0.12.0 (bibliothèques `kotaemon` et `ktem` de l'image `main-full`, Python 3.10, Gradio 4.39.0), essais du 12 et 13 novembre 2026.
> **Statut des informations** : [Vérifié] exécuté, sortie dans `exemples/kotaemon/sorties_verifiees.txt` ; [Source] lu dans le code ; [Estimation] calcul expliqué ; [À tester] non essayé.
> **Précautions** : les exemples lisent et écrivent dans la base de l'instance ; la clé du service de modèles leur est passée par variable d'environnement depuis `.env`, jamais écrite dans les fichiers.

## Sommaire

1. [Pas d'API REST](#1-pas-dapi-rest)
2. [Lancer un exemple](#2-lancer-un-exemple)
3. [Exemples](#3-exemples)
4. [Pilote du banc](#4-pilote-du-banc)
5. [Brancher un lecteur extérieur (Docling, PaddleOCR)](#5-brancher-un-lecteur-extérieur-docling-paddleocr)
6. [Dépannage](#dépannage)
7. [Sources](#sources)

## 1. Pas d'API REST

- [Source] Kotaemon ne définit aucune route d'API (aucun `api_name` dans `ktem`) ; Gradio expose ses fonctions internes, mais elles dépendent de l'état de la session du navigateur (compte connecté, réglages) et ne sont pas utilisables comme API (`cadrage-serveur.md`, section 9).
- [Vérifié] La page de configuration de Gradio répond (`/config`, exemple 01).
- [Vérifié] La voie retenue : exécuter du Python **dans** le conteneur, avec l'environnement de Kotaemon (`/app/.venv`), en chargeant l'application sans interface (`ktem.app.BaseApp`). Les réglages enregistrés dans l'interface s'appliquent.

## 2. Lancer un exemple

```bash
exemples/kotaemon/lancer.sh exemples/kotaemon/02_lister_collections.py
```

[Vérifié] `lancer.sh` lit `.env`, passe `LLM_CENTRAL_KEY` au conteneur et envoie le script à `docker exec -i rag-kotaemon /app/.venv/bin/python -`. Les messages techniques de démarrage (NLTK, journaux de gRPC) sont filtrés.

## 3. Exemples

| Exemple | Ce qu'il fait | Statut |
|---|---|---|
| `01_etat.sh` | réponse HTTP de l'interface, version de Gradio, état du conteneur | [Vérifié] |
| `02_lister_collections.py` | collections, type, caractère privé, fichiers et nombre d'éléments indexés | [Vérifié] |
| `03_poser_une_question.py` | question à « File Collection » avec les réglages de l'interface, réponse et pages citées | [Vérifié] (code 0) |
| `04_pipeline_personnalise.py` | pipeline construit avec les briques `kotaemon` : magasins en mémoire, `embed`, `rerank`, `chat` | [Vérifié] (code 0) |

Extrait de l'exemple 04 (le pipeline complet tient en 30 lignes) :

```python
emb = OpenAIEmbeddings(base_url="http://llm-central:8080/v1", api_key=CLE, model="embed")
vs, ds = InMemoryVectorStore(), InMemoryDocumentStore()
VectorIndexing(vector_store=vs, doc_store=ds, embedding=emb).run([Document(text="…"), …])
passages = VectorRetrieval(vector_store=vs, doc_store=ds, embedding=emb, top_k=2).run(question)
passages = CohereReranking(model_name="rerank", cohere_api_key=CLE, base_url="http://llm-central:8080").run(passages, question)
reponse = ChatOpenAI(base_url="http://llm-central:8080/v1", api_key=CLE, model="chat").invoke(…)
```

Les sorties réelles sont dans `exemples/kotaemon/sorties_verifiees.txt`.

## 4. Pilote du banc

`outils/kotaemon/pilote_conteneur.py` [Vérifié] reprend la méthode de l'exemple 03 et sert des commandes JSON ligne par ligne (`indexer`, `demander`, `reglages`) ; `outils/kotaemon/banc.py` le lance par `docker exec -i` et en tire les mesures de l'annexe A1. Un fichier présent sans aucun passage (lecture en échec) est réindexé d'office ; l'option `"forcer": true` réindexe comme « Force reindex file ».

## 5. Brancher un lecteur extérieur (Docling, PaddleOCR)

**Constat.** Dans l'image « full », Docling est une bibliothèque appelée dans le processus de Kotaemon (`loaders/docling_loader.py:47-51`) ; le réglage « File loader » ne propose aucune adresse de serveur. [Source] [Vérifié] (choix visibles dans l'interface, chapitre 05)

**Point d'extension.** Le fichier de configuration `flowsettings.py` peut définir `FILE_INDEX_PIPELINE_FILE_EXTRACTORS`, un dictionnaire extension → classe de lecteur (chemin Python). Kotaemon instancie ces classes et les applique **après** le choix de « File loader », pour toutes les collections de type fichier (`ktem/index/file/pipelines.py:58-66` et `708`). [Source]

**Essai avec un serveur Docling séparé** (docling-serve v1.38.2, version CPU) : [Vérifié] (`outils/resultats/kotaemon/docling-externe-2026-11-13.log`, capture `05-documents/18-scan-lu-par-docling-externe.png`)

1. le serveur tourne dans son propre conteneur `rag-docling-serve`, sur le réseau Docker `llm-net`, sans port publié (`outils/kotaemon/compose.docling-externe.yml`) ;
2. la classe `LecteurDoclingServe` (`outils/kotaemon/docling_externe/lecteur_docling_serve.py`) hérite de `kotaemon.loaders.base.BaseReader` ; `load_data(file_path, extra_info=None)` envoie le fichier à `POST /v1/convert/file` (`to_formats=json`, `do_ocr=true`), lit le document Docling renvoyé (`document.json_content`) et rend un `Document` par page (`metadata["page_label"]`, `metadata["file_name"]`) et un par tableau (Markdown), comme le lecteur Docling intégré ; les figures ne sont pas extraites ;
3. le module est monté en `/app/lecteur_docling_serve.py`, et une copie de `flowsettings.py` de l'image, complétée par la ligne suivante, est montée en `/app/flowsettings.py` :

   ```python
   FILE_INDEX_PIPELINE_FILE_EXTRACTORS = {".pdf": "lecteur_docling_serve.LecteurDoclingServe"}
   ```

4. `outils/kotaemon/docling_externe/brancher.sh` démarre les deux conteneurs (Kotaemon prêt en 28 s) ; `debrancher.sh` revient à la configuration d'origine.

Résultat : le contrat scanné (2 pages) est lu en 10 à 14 secondes (trois relectures), contre 47 secondes avec le Docling intégré (chapitre 05, étape 13) ; le journal du conteneur indique « Using reader LecteurDoclingServe() » ; les deux passages contiennent le texte des pages scannées. « File loader » reste sur « Default (open-source) » : le réglage l'emporte sur ce choix. [Vérifié] Le serveur sur une autre machine (seule l'adresse `DOCLING_SERVE_URL` change) et un serveur PaddleOCR (même méthode, module à adapter à son API) n'ont pas été essayés. [À tester]

Pour PaddleOCR-VL, le lecteur intégré a un paramètre `vl_rec_server_url` qui déporte seulement le modèle de vision ; il demande quand même la bibliothèque `paddleocr` dans le conteneur, absente de l'image « full », et l'interface ne permet pas de le régler. [Source] (`paddleocr_vl_loader.py:40,81`, `indices/ingests/files.py:44-45`)

**Image plus légère.** L'image « lite » ne contient ni Docling, ni unstructured, ni LibreOffice [Source] (`Dockerfile`) ; elle n'a pas été essayée : la lecture des DOCX et PPTX y est probablement perdue. [À tester]

## Dépannage

| Symptôme | Cause probable | Action |
|---|---|---|
| `ModuleNotFoundError: ktem` | script lancé hors du conteneur | passer par `exemples/kotaemon/lancer.sh` |
| `KeyError: 'LLM_CENTRAL_KEY'` | `.env` absent ou sans clé | copier `.env.example` en `.env` et y mettre la clé (chapitre 02) |
| `Nano-GraphRAG dependencies not installed` en tête de sortie | message de démarrage de Kotaemon | sans effet ; filtré ou ignoré |

## Sources

- Exemples : `exemples/kotaemon/*.py`, `*.sh`, `sorties_verifiees.txt`.
- Pilote : `outils/kotaemon/pilote_conteneur.py`.
- Code source de Kotaemon v0.12.0 : https://github.com/Cinnamon/kotaemon/tree/v0.12.0 ; relevé `outils/resultats/kotaemon/cadrage-serveur.md`.
