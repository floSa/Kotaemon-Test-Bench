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

**Méthode** pour un serveur Docling séparé (docling-serve) ou un serveur PaddleOCR : [À tester]

1. faire tourner le serveur dans son propre conteneur, relié au réseau Docker `rag-local`, port publié sur `127.0.0.1` seulement s'il doit être joint depuis l'hôte ;
2. écrire une classe de lecteur héritant de `kotaemon.loaders.base.BaseReader`, dont la méthode `load_data(file_path, extra_info=None)` envoie le fichier au serveur et renvoie une liste de `Document` (un par page, avec `metadata["page_label"]` et `metadata["file_name"]`, pour garder les pages dans les citations) ;
3. monter ce module dans le conteneur (par exemple `/app/lecteurs_externes.py`) et une copie de `flowsettings.py` complétée par :

   ```python
   FILE_INDEX_PIPELINE_FILE_EXTRACTORS = {".pdf": "lecteurs_externes.LecteurDoclingServe"}
   ```

4. redémarrer, puis réindexer les PDF (« Force reindex file »).

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
