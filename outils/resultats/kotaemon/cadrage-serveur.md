# Kotaemon v0.12.0 : cadrage serveur (lecture du code source)

Source : `sources/kotaemon` au tag `v0.12.0` (commit `9ad3e4e4`, daté 2026-05-30). Les chemins sont relatifs à ce dossier.
Marqueurs : [Code] = lu dans le code cité ; [À vérifier] = déduction ou connaissance externe, à confirmer par un essai.

## 1. Image Docker, lancement, variables

- Cibles : `lite` (python:3.11-slim, uv sync --frozen, pdfservices-sdk, `graphrag<=0.3.6` **sur amd64 seulement**) `Dockerfile:2-56` ; `full` = lite + tesseract (+jpn), libreoffice, ffmpeg, libmagic, torch CPU, `libs/kotaemon[adv]`, `unstructured[all-docs]`, données NLTK, `libs/kotaemon[docling]` (docling<=2.5.2), `ENV USE_LIGHTRAG=true` + `libs/kotaemon[lightrag]` (lightrag-hku<=1.3.0) `Dockerfile:59-99`. `paddle` (GPU) et `ollama` existent `Dockerfile:102-124`, mais la CI ne publie que lite, full, ollama `.github/workflows/build-push-docker.yaml:28-31`.
- Étiquette `main-full` = branche `main` (`type=ref,event=branch,suffix=-full`, workflow:77), donc mobile : figer par empreinte. Plateformes amd64 et arm64 (workflow:100).
- Commande officielle `README.md:104-110` :
  `docker run -e GRADIO_SERVER_NAME=0.0.0.0 -e GRADIO_SERVER_PORT=7860 -v ./ktem_app_data:/app/ktem_app_data -p 7860:7860 -it --rm ghcr.io/cinnamon/kotaemon:main-full`
  Pour ce banc, utiliser `-p 127.0.0.1:7860:7860`.
- Point d'entrée `sh /app/launch.sh` `Dockerfile:99`. GRADIO_SERVER_NAME vaut 0.0.0.0 et GRADIO_SERVER_PORT 7860 par défaut `launch.sh:3-8`. Trois modes : `KH_DEMO_MODE=true` lance uvicorn `sso_app_demo:app` sans gestion des utilisateurs ni LightRAG `launch.sh:11-14` ; `KH_SSO_ENABLED=true` lance uvicorn `sso_app:app` `launch.sh:16-18` ; sinon `ollama serve &` puis `.venv/bin/python app.py` `launch.sh:20-21`. Dans l'image full, ollama est absent, d'où un message « not found » sans conséquence [À vérifier].
- Utilisateur : aucune directive `USER`, donc root. Répertoire de travail `/app` `Dockerfile:30`. Python : `/app/.venv` (pas d'`ENV PATH`).
- Données : `KH_APP_DATA_DIR = <dossier de flowsettings.py>/ktem_app_data`, soit `/app/ktem_app_data` `flowsettings.py:35`.
- `.env` : l'image copie `.env.example` vers `/app/.env` `Dockerfile:44`. `flowsettings.py` lit avec `decouple.config` `flowsettings.py:6`. Une variable passée par `-e` l'emporte sur `/app/.env` ; une variable vide (`-e LOCAL_MODEL=`) écrase aussi la valeur du fichier (comportement de python-decouple) [À vérifier].
- Contenu de `.env.example` `:1-64` : OPENAI_API_BASE=https://api.openai.com/v1, OPENAI_API_KEY=`<YOUR_OPENAI_KEY>`, OPENAI_CHAT_MODEL=gpt-4o-mini, OPENAI_EMBEDDINGS_MODEL=text-embedding-3-large ; AZURE_OPENAI_* ; COHERE_API_KEY=`<COHERE_API_KEY>` ; VOYAGE_API_KEY=`<VOYAGE_API_KEY>` ; LOCAL_MODEL=qwen2.5:7b, LOCAL_MODEL_EMBEDDINGS=nomic-embed-text ; GRAPHRAG_API_KEY=`<YOUR_OPENAI_KEY>`, GRAPHRAG_LLM_MODEL, GRAPHRAG_EMBEDDING_MODEL ; USE_CUSTOMIZED_GRAPHRAG_SETTING=false ; AZURE_DI_* ; PDF_SERVICES_* ; PDFJS_VERSION_DIST ; PADDLE_DEVICE=gpu ; AUTHENTICATION_METHOD et KEYCLOAK_*.
- Variables lues (code) :
  - Application : KH_APP_VERSION `flowsettings.py:19`, KH_GRADIO_SHARE (défaut False) `:28`, KH_ENABLE_FIRST_SETUP (True) `:29`, KH_DEMO_MODE `:30`, KH_OLLAMA_URL (`http://localhost:11434/v1/`) `:31`, KH_SSO_ENABLED `:69`, KH_FEATURE_CHAT_SUGGESTION (False) `:71`, KH_FEATURE_USER_MANAGEMENT (True) `:74`, KH_FEATURE_USER_MANAGEMENT_ADMIN/PASSWORD (admin/admin) `:78-83`, KH_FIRST_SETUP (force l'assistant) `libs/ktem/ktem/main.py:17`, USE_LOW_LLM_REQUESTS `libs/ktem/ktem/reasoning/simple.py:424`, `index/file/pipelines.py:290`, GRADIO_TEMP_DIR (défaut `ktem_app_data/gradio_tmp`) `app.py:7-11`, GR_FILE_ROOT_PATH `libs/ktem/ktem/app.py:16`.
  - Modèles : OPENAI_API_KEY/OPENAI_API_BASE/OPENAI_CHAT_MODEL/OPENAI_EMBEDDINGS_MODEL `flowsettings.py:143-173`, AZURE_OPENAI_* et OPENAI_API_VERSION `:110-141`, VOYAGE_API_KEY/VOYAGE_EMBEDDINGS_MODEL `:175-192`, LOCAL_MODEL/LOCAL_MODEL_EMBEDDINGS `:194-229`, GOOGLE_API_KEY `:145`, COHERE_API_KEY `:261,280,314`, MISTRAL_API_KEY `:270,297`, USE_MULTIMODAL `:325`, OPENAI_VISION_DEPLOYMENT_NAME `:328`.
  - GraphRAG : USE_GLOBAL_GRAPHRAG (True), USE_NANO_GRAPHRAG (False), USE_LIGHTRAG (True), USE_MS_GRAPHRAG (True) `flowsettings.py:356-359` ; GRAPHRAG_API_KEY, GRAPHRAG_EMBEDDING_MODEL, USE_CUSTOMIZED_GRAPHRAG_SETTING `index/file/graph/pipelines.py:56,139,253-260`.
  - Lecteurs : PADDLE_DEVICE (gpu) `libs/kotaemon/kotaemon/indices/ingests/files.py:43`, AZURE_DI_*, PDF_SERVICES_*.
- **Le `.env` ne sert pas qu'au premier lancement.** `flowsettings.py` est relu à chaque démarrage, mais les tables de la base ne sont amorcées qu'une fois :
  - LLM : chaque nom absent de la table est ajouté ; un nom déjà présent n'est jamais mis à jour `libs/ktem/ktem/llms/manager.py:22-34`.
  - Embeddings : seulement si la table est vide `embeddings/manager.py:22-32`. Rerankers : seulement si la table est vide `rerankings/manager.py:23-31`.
  - Compte admin : créé s'il n'existe pas `pages/resources/user.py:125-133`. Collections : créées si absentes `index/manager.py:185-187`.
  - Les variables USE_*, KH_FEATURE_*, GRAPHRAG_* et COHERE_API_KEY s'appliquent à chaque démarrage.
- **Assistant de premier lancement** : affiché seulement si `ktem_app_data` n'existait pas à l'import `flowsettings.py:36` et `main.py:23`. Avec un volume monté, le dossier existe déjà, donc pas d'assistant sauf `KH_FIRST_SETUP=true` [À vérifier]. Choix proposés : Cohere, Google, OpenAI (base URL figée à api.openai.com), Ollama, ou le bouton « I am an advance user. Skip this. » `pages/setup.py:59-67,134-137,240`.

## 2. Déclarer `chat` et `embed` par `.env`

- `OPENAI_API_BASE=http://llm-central:8080/v1`, `OPENAI_API_KEY=<clé>`, `OPENAI_CHAT_MODEL=chat`, `OPENAI_EMBEDDINGS_MODEL=embed` créent :
  - `KH_LLMS["openai"]` en `kotaemon.llms.ChatOpenAI` (temperature 0, **timeout 20 s**, `default` = clé différente de `<YOUR_OPENAI_KEY>`) `flowsettings.py:148-160` ;
  - `KH_EMBEDDINGS["openai"]` en `kotaemon.embeddings.OpenAIEmbeddings` (timeout 10, **context_length 8191**) `:161-173`.
- Autres entrées créées sans condition : claude (`your-key`), google (défaut si OpenAI n'est pas le défaut), groq, cohere, mistral `:232-273` ; embeddings cohere, google, mistral `:276-300` ; reranker `cohere` (rerank-v4.0-fast, **défaut**) `:310-317`. Avec le `.env` d'origine s'ajoutent les entrées `voyageai` (clé factice non vide) `:175-192` et `ollama`, `ollama-long-context`, `fast_embed` (LOCAL_MODEL non vide) `:194-229`. Les neutraliser avec `-e VOYAGE_API_KEY= -e LOCAL_MODEL=`.
- Paramètres de ChatOpenAI : base_url, api_key, model, timeout, max_retries, temperature, max_tokens, n, stop, frequency/presence_penalty, tool_choice, tools, logprobs, logit_bias, top_logprobs, top_p `llms/chats/openai.py:36-127,278-329`.
- **Piège embeddings** : avec `context_length` défini, chaque texte est découpé avec tiktoken `cl100k_base` et envoyé comme **listes d'identifiants de jetons**, pas comme texte `embeddings/openai.py:20-34,96-99`. bge-m3 n'utilise pas ce vocabulaire : les vecteurs seraient faux, ou l'appel refusé. Retirer `context_length` (null) dans Resources > Embeddings ou dans un `flowsettings.py` monté. Le paramètre `dimensions` existe aussi (non envoyé s'il est vide) `:176-187`.

## 3. Rerankers

- Fournisseurs proposés dans l'interface : TeiFastReranking, CohereReranking, VoyageAIReranking `rerankings/manager.py:54-62`. Dans le pipeline : LLMReranking, LLMScoring, LLMTrulensScoring `libs/kotaemon/kotaemon/indices/rankings/__init__.py`.
- **CohereReranking** accepte `base_url` (ajouté en 0.11.x, commit ffe766f2) `rerankings/cohere.py:29-33`. Il appelle `cohere.Client(key, base_url=base_url or $CO_API_URL).rerank(model=…, query=…, documents=[textes])` `:49-60`, avec cohere 5.18.0 (`uv.lock:830`). Le SDK v1 ajoute `/v1/rerank`, donc `base_url=http://llm-central:8080` **sans `/v1`** ; corps envoyé `{"model","query","documents"}` ; réponse lue : `results[].index` et `results[].relevance_score` [À vérifier par essai]. Le reranker est ignoré sans message d'erreur si la clé est vide ou contient « COHERE_API_KEY » `:45-47` : c'est le cas du défaut avec `<COHERE_API_KEY>`.
- **TeiFastReranking** envoie `POST endpoint_url {"query","texts","is_truncated"}` et attend une **liste** `[{index, score}]` (format TEI natif `/rerank`) `tei_fast_rerank.py:40-53,79-83`. Ce format n'est pas compatible avec `/v1/rerank` de LiteLLM, qui renvoie `{"results":[…]}`. Autres défauts : troncature à 512 **caractères** et lots de 6 `:41-43,70`.
- Activation, dans Settings > Retrieval settings `index/file/pipelines.py:266-304` :
  - « Number of document chunks to retrieve » (10) ;
  - « Retrieval mode » vector/text/hybrid (hybrid) ;
  - « Prioritize table » ;
  - « Use MMR » ;
  - « Use reranking » (True) ;
  - « Use LLM relevant scoring » (True) ;
  - « LLM for relevant scoring ».
  Le reranker utilisé est celui **par défaut** dans Resources ; la clé `reranking` de la collection n'a pas de champ dans l'interface `:323-329`.
- Chaîne : premier tour avec top_k×10 (do_extend) `pipelines.py:153` et `indices/vectorindex.py:151-153`. En hybrid, les résultats vecteur et plein texte sont concaténés `vectorindex.py:186-238`. Le reranker s'applique à environ 100 passages, puis la liste est coupée à top_k `:239-247`. Le scoring LLM (LLMTrulensScoring, en parallèle) fait **un appel LLM par passage** `pipelines.py:315` et `rankings/llm_trulens.py:100-122`.

## 4. Paramètres LLM, réflexion, contexte

- Pas de champ `extra_body` ni `chat_template_kwargs` : seuls les paramètres listés au §2 sont envoyés `openai.py:307-329`. `enable_thinking=false` ne peut pas se régler depuis kotaemon ; c'est à faire côté serveur [À vérifier : alias LiteLLM, interdit si le nom `chat` doit rester fixe]. `max_tokens` et `temperature` se règlent dans la spécification du modèle (Resources > LLMs, YAML).
- Réflexion :
  - en streaming, seul `delta.content` est rendu ; `reasoning_content` est ignoré `openai.py:246-268` ;
  - en non-streaming, seul `message.content` est lu `:163-193` ;
  - des balises `<think>` présentes dans `content` sont converties en bloc repliable « Thought » `reasoning/simple.py:318-323` et `indices/qa/utils.py:85-91` ;
  - `strip_think_tag` ne sert que pour le nom de conversation `pages/chat/__init__.py:1418`.
- Citations « citation: highlight » (défaut) : un second appel LLM avec `tools` et `tool_choice:"required"` (CiteEvidence) `indices/qa/citation.py:31-45`. Cet appel tourne en parallèle de la réponse ; s'il n'a pas fini 5 s après elle, il est abandonné `citation_qa.py:35,218-280`. Choix possibles : « citation: inline » (sans appel de plus) ou « no citation » `simple.py:420-433`.
- Contexte :
  - « Max context length (LLM) » = 32000 par défaut, au niveau global des réglages de raisonnement `flowsettings.py:349-353`. Il tronque les preuves avec le tokenizer tiktoken gpt-3.5 `indices/qa/format_context.py:25,34-45,107-112` et `simple.py:348-358`. **Pour 16 384 jetons, le baisser** (environ 10 000).
  - Historique : « Number of interactions to include » (5) ; « Maximum message length for context rewriting » (150) `simple.py:457-471`.
  - Autres réglages : « Language » (fr disponible, `utils/lang.py:6`), « System Prompt », « QA Prompt » `simple.py:449-456`.

## 5. Lecteurs, formats, découpage

- « File loader » (Settings > Retrieval settings) `index/file/pipelines.py:713-733` : Default (open-source), Adobe API, Azure AI Document Intelligence, Docling, PaddleOCR PPStructureV3, PaddleOCR-VL. Les quatre derniers ne remplacent que `.pdf` ; les deux Paddle remplacent aussi les images `:676-707`.
- Lecteurs par défaut `indices/ingests/files.py:48-64` : `.pdf` PDFThumbnailReader ; `.xlsx` Pandas ; `.docx .pptx .xls .doc` et images via unstructured ; `.html` ; `.mhtml` ; `.txt/.md` TxtReader. Toute extension inconnue passe par unstructured `pipelines.py:779`. Les URL passent par web_reader `:772-773`.
- Formats acceptés par les collections : `.png .jpeg .jpg .tiff .tif .pdf .xls .xlsx .doc .docx .pptx .csv .html .mhtml .txt .md .zip` `flowsettings.py:380-383,396-398`. Taille maximale 1000 Mo par défaut `index/file/index.py:397-401`.
- Docling : installé dans l'image full. DocumentConverter est appelé sans options `loaders/docling_loader.py:47-51`. Les modèles sont téléchargés au premier usage dans le cache HF `/app/ktem_app_data/huggingface` (HF_HOME et HF_HUB_CACHE forcés, `flowsettings.py:62-63`) ; leur taille n'est pas fixée par le code [À mesurer].
- Légendes de figures par VLM : l'URL est construite au format Azure `flowsettings.py:326-330` et n'est jamais vide, donc les appels échouent et sont ignorés `loaders/utils/adobe.py:209-219`. La doc annonce `KH_VLM_ENDPOINT` dans `.env` `docs/integrations/docling.md:15-19`, mais flowsettings ne lit pas cette variable.
- PaddleOCR : absent de l'image full (`paddle` est une cible GPU non publiée).
- Découpage TokenSplitter : taille 1024 et chevauchement 256 par défaut `pipelines.py:787-791`. Ordre de priorité : configuration de la collection (« Size of chunk (number of tokens) », « Number of overlapping tokens between chunks », 0 = valeur développeur) `index/file/index.py:419-437,457-458`, puis `FILE_INDEX_PIPELINE_SPLITTER_CHUNK_SIZE/OVERLAP` de flowsettings `pipelines.py:58-76`.

## 6. Raisonnement

- `KH_REASONINGS` `flowsettings.py:319-324` :
  - Simple QA (`simple`) : réglages du §4, plus « Create Mindmap », « Create Embeddings Visualization », « Use Multimodal Input » `simple.py:398-472`.
  - Complex QA (`complex`, décomposition en sous-questions) : ajoute « Decompose Prompt » `simple.py:579-602`.
  - ReAct Agent (`ReAct`) : outils Wikipedia, Google, LLM, SearchDoc et outils MCP ; défaut [SearchDoc, LLM] ; 5 itérations au maximum `reasoning/react.py:317-356`.
  - ReWOO Agent (`ReWOO`) : LLM Planner et Solver, « Highlight Citation », outils, Planner/Solver Prompt `reasoning/rewoo.py:462-510`.
- Le choix se fait par « Reasoning options » (global) ou par session dans le chat `pages/chat/__init__.py:1218-1222`.

## 7. GraphRAG

- Collections créées au premier démarrage selon les variables : `GraphRAG Collection` (MS, USE_MS_GRAPHRAG=True par défaut), `NanoGraphRAG Collection`, `LightRAG Collection` (USE_LIGHTRAG=true dans l'image) ; toutes privées `flowsettings.py:361-389`.
- **LightRAG** (lightrag-hku<=1.3.0, installé) : utilise le LLM **par défaut** et l'embedding **par défaut** de Resources. La dimension est mesurée par un appel `["Hi"]`, avec max_token_size 8192 `lightrag_pipelines.py:120-133`. Réglages : « Index batch size » (4), prompts, « Search type » local/global/hybrid `:57,297-305,424-426`. Données dans `user_data/files/lightrag` `:54`.
- **NanoGraphRAG** : non installé, l'import échoue avec un message `nano_pipelines.py:30-46`. Installation : `pip install nano-graphrag`, version non figée, avec conflit hnswlib connu (`pip uninstall hnswlib chroma-hnswlib && pip install chroma-hnswlib`) `README.md:202-205`. Il utilise aussi le LLM et l'embedding par défaut `nano_pipelines.py:129`.
- **MS GraphRAG** (graphrag 0.3.6, amd64) : il exige GRAPHRAG_API_KEY non vide `pipelines.py:50-56,110-111`. L'indexation passe par un sous-processus `python -m graphrag.index --root … --init` `:118-149`. Or **`python` désigne le Python du système, pas `/app/.venv`** (aucun `ENV PATH`) [À vérifier : échec probable]. Avec USE_CUSTOMIZED_GRAPHRAG_SETTING=true, `/app/settings.yaml.example` est copié ; ses `api_base` pointent vers 127.0.0.1:11434 / localhost:11434 avec les modèles qwen2 et nomic-embed-text, à remplacer `settings.yaml.example:8-12,43-46` et `pipelines.py:139-146,260-270`. Le README précise : « Official MS GraphRAG indexing only works with OpenAI or Ollama API » `README.md:194-196`.

## 8. Multi-utilisateur

- Activé par défaut. Compte admin `admin`/`admin` créé au démarrage s'il est absent `flowsettings.py:74-83` et `user.py:125-133`. Mots de passe stockés en SHA-256 sans sel `user.py:106`.
- Pas d'inscription libre : seul le SSO crée des comptes automatiquement `pages/login.py:108-116`. L'admin crée et modifie les comptes (case « Admin ») dans Resources > User Management, visible des admins seulement `user.py:153,286-305,406-437` et `pages/resources/__init__.py:61-68`. Règles : identifiant de 3 à 32 caractères alphanumériques ou `_` ; mot de passe d'au moins 8 caractères avec majuscule, minuscule, chiffre et caractère spécial `user.py:20-60`.
- Changement de son propre mot de passe : Settings, « New password » `pages/settings.py:218-226,259`.
- Rôles : admin ou utilisateur (`User.admin`) `db/base_models.py:64`.
- Collections : `private` (True pour toutes par défaut) filtre les fichiers par utilisateur `index/file/ui.py:1497`. Une collection non privée est partagée entre tous. Option « Make private » à la création d'une collection `index.py:412-417`.
- Conversations : case « Share this conversation » `pages/chat/control.py:112-118`. Les conversations publiques sont visibles par tous, ou seulement par l'utilisateur nommé dans `KH_USER_CAN_SEE_PUBLIC` `control.py:205-217`.

## 9. API

- Aucun `api_name` n'est défini dans ktem (grep vide). Gradio 4.39.0 (`uv.lock:2262`) expose donc chaque événement sous le nom de sa fonction, par exemple `/chat_fn`, `/submit_msg`, `/index_fn` `pages/chat/__init__.py:435,460` et `index/file/ui.py:975` [À vérifier sur `http://127.0.0.1:7860/info`]. Ces fonctions dépendent toutefois de `gr.State` (user_id posé à la connexion, réglages) `app.py:76-78`, ce qui les rend inutilisables en pratique avec gradio_client.
- Voie recommandée : la bibliothèque, dans le conteneur (`docker exec … /app/.venv/bin/python`, cwd `/app`). Pistes à valider ; aucune exécution n'a été faite :

```python
import os, sys; os.chdir("/app"); sys.path.insert(0, "/app")
from pathlib import Path
from sqlmodel import Session, select
from ktem.app import BaseApp                      # pas d'interface ; managers + collections (app.py:39-78)
from ktem.db.models import User, Settings, engine
from ktem.index.file.pipelines import DocumentRetrievalPipeline
from ktem.reasoning.simple import FullQAPipeline
app = BaseApp()
with Session(engine) as s:
    uid = s.exec(select(User).where(User.username == "admin")).one().id
    row = s.exec(select(Settings).where(Settings.user == uid)).first()
settings = row.setting if row else app.default_settings.flatten()   # réglages saisis dans l'interface
idx = app.index_manager.indices[0]                                  # « File Collection »
ip = idx.get_indexing_pipeline(settings, uid)                       # index.py:440-459
g = ip.stream([Path("/data/doc.pdf")], reindex=False)               # pipelines.py:810
try:
    while True: next(g)
except StopIteration as e: file_ids, errors, docs = e.value         # ui.py:1257-1262
pref = f"index.options.{idx.id}."
us = {k[len(pref):]: v for k, v in settings.items() if k.startswith(pref)}
r = DocumentRetrievalPipeline.get_pipeline(us, idx.config, file_ids) # pipelines.py:307-348
r.Source, r.Index = idx._resources["Source"], idx._resources["Index"]
r.VS, r.DS, r.FSPath, r.user_id = idx._vs, idx._docstore, idx._fs_path, uid
qa = FullQAPipeline.get_pipeline(settings, {"app": {}}, [r])        # simple.py:341-391
out = qa.stream("question ?", conv_id="", history=[])               # simple.py:281
chat, info = "", []
try:
    for d in out:
        if d.channel == "chat": chat = "" if d.content is None else chat + d.content
        elif d.channel == "info" and d.content: info.append(d.content)  # HTML des sources
except StopIteration: pass
```

  Passages cités : `qa.retrieve(message, history)` renvoie les documents et leurs métadonnées (`file_name`, `page_label`, `reranking_score`) `simple.py:108`.

## 10. Télémétrie et appels sortants

- Gradio : `analytics_enabled=False` `libs/ktem/ktem/app.py:203`. Ajouter `GRADIO_ANALYTICS_ENABLED=False` par précaution [À vérifier].
- Chroma 0.5.16 : `PersistentClient(path)` avec les réglages par défaut `storages/vectorstores/chroma.py:43`, donc télémétrie anonyme posthog active. La couper avec `ANONYMIZED_TELEMETRY=False` [À vérifier].
- unstructured (scarf) : `DO_NOT_TRACK=true` et `SCARF_NO_ANALYTICS=true` [À vérifier].
- Help : about.md et usage.md sont lus en local (`/app/docs`). Le changelog est demandé à `api.github.com/repos/Cinnamon/kotaemon/releases/tags/v<version>`. Le test de cache utilise par erreur `version` (la fonction importée) au lieu de `self.app_version`, donc un appel part à chaque démarrage `pages/help.py:94-114`.
- Navigateur : CDN skypack, cdnjs, jsdelivr `app.py:186-197` ; polices Google `assets/theme.py:164,171`.
- Mode démo seulement : daily papers de Hugging Face et Semantic Scholar `utils/hf_papers.py:6-10` et `pages/chat/__init__.py:317`.
- tiktoken : `cl100k_base` est téléchargé au premier usage s'il n'est pas en cache [À vérifier dans l'image].
- Docling/HF : téléchargement des modèles au premier usage.
- Réseau : un seul port, 7860 (Gradio sur 0.0.0.0 dans le conteneur). `KH_GRADIO_SHARE=False` par défaut (pas de tunnel gradio.live) `flowsettings.py:28`.

## 11. Stockage (sous `/app/ktem_app_data`)

- `user_data/sql.db` (SQLite : utilisateurs, réglages, conversations, modèles, collections) `flowsettings.py:85`.
- `user_data/files` (fichiers et dossiers `lightrag/`, `nano_graphrag/`, `graphrag/`) `:86`.
- `user_data/docstore` (LanceDB, plein texte) `:92-97`.
- `user_data/vectorstore` (Chroma) `:98-104`.
- `markdown_cache_dir`, `chunks_cache_dir`, `zip_cache_dir(_in)` `:44-57`.
- `huggingface` `:62-63`, `gradio_tmp` `app.py:9-11`, `changelogs` `help.py:42`.

## 12. Version et changements 0.11 → 0.12

- Version affichée : « Version: {KH_APP_VERSION} » dans Help > About `help.py:62-63`, injectée aussi en JS `app.py:52`. Ordre de résolution : variable `KH_APP_VERSION`, sinon `importlib.metadata.version("kotaemon_app")`, sinon « local » `flowsettings.py:19-26`. Le numéro vient de setuptools-git-versioning `pyproject.toml:9-13`, or `.git` est exclu du contexte Docker (`.dockerignore`). La valeur affichée par l'image peut donc ne pas être 0.12.0 [À vérifier dans l'interface].
- Pas de CHANGELOG à jour dans le dépôt (`libs/ktem/ktem/assets/md/changelogs.md` s'arrête à v0.0.1). Historique Git :
  - v0.11.x (2025-03 à 07) : VoyageAI (embeddings et rerank), Mistral, structured output OpenAI, `base_url` pour CohereReranking, ordre LanceDB conservé, correctif de traversée de chemin.
  - v0.12.0 : uv et `uv.lock` (fe52d208) ; outils **MCP** et renommage des ressources (155e5907) ; rerank Cohere par défaut passé à `rerank-v4.0-fast` (4015bb0f) ; PaddleOCR (PP-StructureV3, PaddleOCR-VL), mentions @fichier et @websearch dans le chat, filtre et aperçu des passages, panneau « test connection » rétabli dans Resources, `PADDLE_DEVICE`, cible Docker paddle (9ad3e4e4).
- Ruptures probables : l'image est construite par `uv sync` et non plus par pip `Dockerfile:47-50` ; le modèle de rerank Cohere a changé (une base existante garde l'ancien) ; nouvelle table MCP. Aucune migration Alembic n'est active (`KH_ENABLE_ALEMBIC=False`, `flowsettings.py:84`).

## Pièges probables pour l'installation

1. Le `.env` d'origine est intégré à l'image. Sans surcharge, il ajoute des entrées Ollama (localhost:11434, absent), VoyageAI (clé factice), Google (défaut si la clé OpenAI garde sa valeur d'exemple). Passer `-e OPENAI_*`, `-e LOCAL_MODEL= -e VOYAGE_API_KEY=`, ou monter un `.env` propre sur `/app/.env`.
2. Les modèles ne sont amorcés qu'une fois : une base existante ignore les changements du `.env`. Repartir d'un `ktem_app_data` vide, ou corriger dans Resources.
3. Embedding `openai` avec `context_length: 8191` : il envoie des jetons cl100k au lieu du texte, incompatible avec bge-m3. Mettre ce champ à null avant toute indexation.
4. Le reranker par défaut (Cohere avec la clé `<COHERE_API_KEY>`) est ignoré sans message. Créer un CohereReranking avec `base_url=http://llm-central:8080` (sans /v1), `model_name=rerank` et une vraie clé, puis le rendre défaut. TeiFastReranking ne parle pas le format `/v1/rerank`.
5. Timeout LLM de 20 s avec un modèle qui réfléchit : risque de délai dépassé et de deux tentatives de plus. Augmenter `timeout` et fixer `max_tokens` dans la spécification. `enable_thinking` ne se règle pas côté kotaemon.
6. « Max context length (LLM) » vaut 32000 par défaut, au-dessus de 16 384 : le baisser (environ 10 000). « Use LLM relevant scoring » et « citation: highlight » ajoutent des appels LLM (un par passage, plus un appel avec tool_choice=required, abandonné après 5 s).
7. Le changement d'embedding par défaut après une indexation casse les collections (dimension 1024 attendue). Choisir `embed` avant le premier import, LightRAG compris.
8. Avec un volume monté, l'assistant de premier lancement n'apparaît pas ; ce n'est pas un problème ici.
9. MS GraphRAG : sous-processus `python` hors de la venv, configuration Ollama ou OpenAI seulement, amd64 seulement. NanoGraphRAG : non installé. LightRAG : installé et actif.
10. Conteneur en root ; fichiers du volume appartenant à root. Port à publier sur `127.0.0.1:7860` seulement.
11. Étiquette `main-full` mobile (branche main) : figer par empreinte et contrôler la version affichée, qui peut différer de 0.12.0.
12. Appels sortants au démarrage (api.github.com) et dans le navigateur (CDN, Google Fonts) ; télémétrie Chroma et unstructured à couper par variables.
13. Premier usage de Docling : téléchargement de modèles HF dans `ktem_app_data/huggingface`, sans légende VLM (l'endpoint Azure est vide).
14. Mot de passe admin/admin par défaut, haché en SHA-256 sans sel. Le changer, ou fixer `KH_FEATURE_USER_MANAGEMENT_PASSWORD` avant le premier démarrage.
