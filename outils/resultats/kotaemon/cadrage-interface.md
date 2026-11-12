# Cadrage de l'interface Kotaemon v0.12.0 (lecture du code, non vérifié en exécution)

Source : `sources/kotaemon` au tag `v0.12.0` (`git describe --tags`). Lecture seule, rien n'a été lancé.
Conventions : `ktem/` = `libs/ktem/ktem/` ; `fs` = `flowsettings.py` (racine du dépôt) ; `kot/` = `libs/kotaemon/kotaemon/`.
Gradio 4.x (`libs/ktem/pyproject.toml:29`, `gradio>=4.31.0,<5`). Tout ce qui suit est **prévisionnel** : à confirmer par Playwright.
Les libellés entre guillemets sont recopiés du code (anglais).

## 1. Onglets principaux et conditions d'affichage

Construits dans `ktem/main.py:46-125`, ordre d'affichage :

| Onglet (libellé) | elem_id | Condition | Réf. |
|---|---|---|---|
| "Welcome" (connexion) | `login-tab` | seulement si `KH_FEATURE_USER_MANAGEMENT` (défaut **True**, `fs:74-76`) ; masqué après connexion | `main.py:47-53`, `main.py:158-161` |
| "Chat" | `chat-tab` | toujours ; invisible avant connexion si gestion des utilisateurs | `main.py:55-61` |
| Index : nom de l'index si 1 seul index, sinon "Files" avec un sous-onglet par index (`elem_id=f"{index.id}-tab"`) | `indices-tab` | masqué si `KH_DEMO_MODE` | `main.py:63-92` |
| "Resources" | `resources-tab` | masqué si `KH_DEMO_MODE` ou `KH_SSO_ENABLED` ; après connexion **visible seulement pour un admin** | `main.py:94-103`, `main.py:162-163` |
| "Settings" | `settings-tab` | masqué si `KH_DEMO_MODE` | `main.py:105-112` |
| "Help" | `help-tab` | toujours (après connexion) | `main.py:114-121` |
| Assistant de premier lancement (hors onglets, colonne) | aucun | `KH_ENABLE_FIRST_SETUP` (défaut True, `fs:29`) et données absentes au démarrage | `main.py:123-125`, `main.py:21-25` |

- Pas d'onglet "Admin" : l'administration passe par "Resources" > "Users" (admin seulement, `ktem/pages/resources/__init__.py:35-37`, `:61-68`).
- Index par défaut créés au premier démarrage (`fs:375-404`, `ktem/index/manager.py:186-188`) : "File Collection" + "GraphRAG Collection" (si `USE_MS_GRAPHRAG`, défaut True, `fs:359`) + "LightRAG Collection" (si `USE_LIGHTRAG`, défaut True, `fs:358` ; `ENV USE_LIGHTRAG=true` dans `Dockerfile:94`) + "NanoGraphRAG Collection" (si `USE_NANO_GRAPHRAG`, défaut False). Donc, par défaut, plus d'un index : l'onglet s'appelle **"Files"** avec sous-onglets "File Collection", "GraphRAG Collection", "LightRAG Collection". Les index sont mémorisés en base : un index déjà créé reste même si la variable change (`manager.py:186-191`).
- Flags `KH_*` lus par l'UI : `KH_DEMO_MODE`, `KH_SSO_ENABLED`, `KH_ENABLE_FIRST_SETUP`, `KH_FIRST_SETUP` (force l'assistant, `main.py:17-18`), `KH_FEATURE_USER_MANAGEMENT`, `KH_FEATURE_USER_MANAGEMENT_ADMIN`/`_PASSWORD` (défaut `admin`/`admin`, `fs:78-83`), `KH_FEATURE_CHAT_SUGGESTION` (défaut False, `fs:71-73`), `KH_USER_CAN_SEE_PUBLIC` (`fs:77`), `KH_WEB_SEARCH_BACKEND` (Tavily, `fs:87-90`), `USE_LOW_LLM_REQUESTS` (désactive mindmap / citation / score LLM par défaut).

## 2. Contenu des onglets

### 2.1 "Welcome" (connexion) — `ktem/pages/login.py`
- Titre "# Welcome to Kotaemon!" (`login.py:35`, nom = `KH_APP_NAME`, défaut "Kotaemon", `ktem/app.py:42`).
- "Username", "Password" (type password), bouton "Login" ; Entrée dans "Password" valide aussi (`login.py:36-43`). Champs **masqués au chargement** puis affichés si aucun identifiant mémorisé : un script JS relit `localStorage` et reconnecte automatiquement (`login.py:20-22`, `:61-73`).
- Erreur : toast "Invalid username or password" (`login.py:131`). Mot de passe haché SHA-256 (`login.py:118`).
- Compte admin créé au démarrage depuis `KH_FEATURE_USER_MANAGEMENT_ADMIN/PASSWORD` (`ktem/pages/resources/user.py:126-133`).
- Changement de mot de passe et déconnexion : "Settings" > "User settings" (voir 2.5).

### 2.2 "Chat" — `ktem/pages/chat/`
Trois colonnes (`chat/__init__.py:223-406`) : gauche `conv-settings-panel`, centre `chat-area`, droite `chat-info-panel`.

**Colonne de gauche — conversations** (`chat/control.py:52-200`)
- Titre "## Conversations" (`control.py:54-55`).
- 3 boutons-icônes sans texte : mode sombre `toggle-dark-button` (bascule la classe `dark` du body, `control.py:56-63`, `:82-89`), agrandir le chat `chat-expand-button` (`:64-71`), agrandir le panneau d'information `info-expand-button` (`:72-80`).
- Liste déroulante "Chat sessions" (label non affiché, `container=False`, filtrable), `conversation-dropdown` (`control.py:92-100`).
- Case "Suggest chat" `suggest-chat-checkbox` (transformée en interrupteur par JS, `assets/js/main.js:83-91`) : affiche/masque l'accordéon "Chat Suggestion" (`chat/__init__.py:828-846`).
- Case "Share this conversation" `is-public-checkbox` (masquée si SSO) ; **déplacée par JS dans l'accordéon "Feedback"** (`main.js:73-80`). Effet : conversation publique, toast "Conversation: <nom> is public." (`chat/__init__.py:1011-1031`).
- Boutons-icônes sans texte ni elem_id : renommer (`rename.svg`), supprimer (`delete.svg`), nouvelle conversation (`new.svg`, elem_id `new-conv-button`) (`control.py:120-145`). Sélection Playwright des deux premiers : par l'image `img[src*="rename.svg"]` / `img[src*="delete.svg"]` (à vérifier).
- Suppression : apparition de "Delete" (variant stop) et "Cancel" (`control.py:182-188`).
- Renommage : zone "(Enter) to save", placeholder "Conversation name" (`control.py:190-199`) ; toast "Conversation renamed." (`control.py:405`).
- Conversations visibles : les siennes + publiques (si `KH_USER_CAN_SEE_PUBLIC` non défini, tout utilisateur voit les publiques) (`control.py:206-244`).

**Colonne de gauche — sélection des documents** (un accordéon par index, `chat/__init__.py:233-274`)
- Accordéon au nom de l'index (ex. "File Collection"), `elem_id="index-0"`, `index-1`… ; seul le premier est ouvert (`:247-251`).
- Radio sans label : "Search All" (`all`) / "Search In File(s)" (`select`) (`ktem/index/file/ui.py:1759-1766`). **Valeur initiale `disabled`** (aucune option cochée) = aucune recherche documentaire (`ui.py:1752-1755`, `:1805-1806`).
- "Search In File(s)" fait apparaître la liste multiple "Files" (`ui.py:1767-1775`, `:1787-1791`). Les **groupes** y figurent sous la forme `group: '<nom>'` (`ui.py:1847-1855`). Il n'existe **pas** de libellé « Search in collection » dans le code.
- "Search All" = tous les fichiers de l'index (filtrés sur l'utilisateur si index privé, `ui.py:1810-1819`).

**Colonne de gauche — autres accordéons**
- "Chat Suggestion" (visible si `KH_FEATURE_CHAT_SUGGESTION`), tableau "Next Question", elem_id `chat-suggestion`, exemples "Summary this document", "Generate a FAQ for this document", "Identify the main highlights in bullet points" ; un clic copie la question dans la saisie (`chat/chat_suggestion.py:7-35`, `chat/__init__.py:852-861`).
- "Quick Upload" (`chat/__init__.py:278-306`) : zone de dépôt multi-fichiers `quick-file`, champ placeholder "Or paste URLs" `quick-url`. Indexe dans le **premier index** (`index/file/ui.py:699-760`), message "Please wait for the indexing process to complete before adding your question." puis "Indexing completed." ; bascule le sélecteur sur "Search In File(s)" avec les nouveaux fichiers.
- "Feedback" `report-accordion` (`chat/report.py:15-42`) : radio "Correctness:" ("The answer is correct" / "The answer is incorrect"), cases "Other issue:" ("The answer is offensive" / "The evidence is incorrect"), zone "More detail (e.g. how wrong is it, what is the correct answer, etc...)", bouton "Report" → toast "Thank you for your feedback".

**Colonne centrale** (`chat/chat_panel.py`)
- Chatbot `main-chat-bot`, bouton copier et like/dislike par message (`chat_panel.py:27-35`) ; texte vide : "This is the beginning of a new conversation. Start by uploading a file or a web URL. Visit Files tab for more options (e.g: GraphRAG)." (`:8-12`).
- Saisie multimodale `chat-input`, placeholder "Type a message, use @WebSearch, or tag a file with @filename", accepte plusieurs fichiers joints (`chat_panel.py:37-47`).
  - `@WebSearch` : recherche web au lieu des index (`chat/__init__.py:910-912`, `:1250-1256`) ; nécessite `TAVILY_API_KEY` (`kot/indices/retrievers/tavily_web_search.py:5`, `:19-21`).
  - `@<nom de fichier>` : restreint la recherche aux fichiers cités (`chat/__init__.py:908-925`).
  - URL dans le message : indexée à la volée dans le premier index (`:927-939`).
  - Message vide au début d'une conversation : question par défaut "What is the summary of this document?" (`:59-63`, `:943-949`).
- Accordéon "Chat settings" `chat-settings-expand`, fermé par défaut (`chat/__init__.py:322-393`) — en-têtes "Reasoning method", "Model", "Language" :
  - Méthode de raisonnement : liste sans label, valeurs = identifiants `simple`, `complex`, `ReAct`, `ReWOO` (`ktem/settings.py:72-77`, `fs:319-324`) ; toast "Reasoning type changed to `<id>`" (`chat/__init__.py:1150-1153`).
  - Modèle : "(default)" + noms des LLM déclarés (`reasoning/simple.py:401-405`) ; masqué si SSO.
  - Langue : liste des 31 langues (voir §3).
  - Style de citation `citation-dropdown` : "citation: highlight" / "citation: inline" / "no citation" (`reasoning/simple.py:420-433`).
  - Case "Mindmap (on)" / "Mindmap (off)" `use-mindmap-checkbox` (libellé change avec l'état, `chat/__init__.py:378-393`, `:821-826`). Mindmap et citation sont déplacés par JS dans l'en-tête de l'accordéon (`main.js:63-71`).
  - Ces choix ne valent que pour la session de chat ; ils surchargent les réglages ("Settings") (`chat/__init__.py:1218-1245`).

**Colonne de droite — panneau d'information**
- Accordéon "Information panel" `info-expand`, ouvert (`chat/__init__.py:398-403`) ; contenu HTML `html-info-panel`, graphique Plotly optionnel, conteneur `pdf-modal`.
- Par extrait : en-tête cliquable avec `[score: x]`, lien "[Preview]" (PDF seulement) ouvrant la visionneuse PDF.js en fenêtre modale, avec recherche/surlignage du passage (`ktem/utils/render.py:75-123`, `assets/js/pdf_viewer.js:3-24`, id `pdf-viewer`, boutons fermer `modal-close` / agrandir `modal-expand`).
- Bloc repliable "Relevance score" détaillant "Vectorstore score", "LLM relevant score", "Reranking score" (`render.py:192-209`).
- "No evidence found." si aucune preuve (`reasoning/simple.py:231-232`).
- Alerte "WARNING! Context relevance score is low. Double check the model answer for correctness." si le meilleur score LLM < `CONTEXT_RELEVANT_WARNING_SCORE` (défaut **0.3**, variable d'environnement) (`reasoning/simple.py:251-258`, `kot/indices/qa/citation_qa.py:36-37`).
- "Answer confidence: x" si score QA disponible (`simple.py:260-270`).
- Clic sur une citation dans la réponse → défilement vers l'extrait (`main.js:129-145`, à vérifier).

### 2.3 "Files" (gestion d'un index) — `ktem/index/file/ui.py:186-405`
Identique pour chaque sous-onglet (File / GraphRAG / LightRAG Collection : même classe `FileIndex`, `index/file/graph/graph_index.py:9`).
- Colonne gauche : sous-onglets "Upload Files" (dépôt multi-fichiers + rappel "- Supported file types: …", "- Maximum file size: … MB") et "Use Web Links" (zone "Input web URLs", "(separated by new line)") (`ui.py:353-373`).
- Accordéon "Advanced indexing options" : case "Force reindex file" (`ui.py:375-379`).
- Bouton "Upload and Index" (primary) (`ui.py:381-383`) ; toasts "Start indexing N files...", "Successfully index N files", "Have errors for N files" (`ui.py:1241`, `:1274-1277`).
- Panneau "## Upload Progress" : "Upload result", "Upload info", bouton "Clear Upload Info and Close" (`ui.py:386-399`).
- Sous-onglet "Files" : champ "Filter by name:" (info "(1) Case-insensitive. (2) Search with empty string to show all files.") ; tableau `file_list_view` colonnes id, name, size, tokens, loader, date_created (`ui.py:221-244`). Sélection d'une ligne → "Go to Chat", "Download", "Delete" (stop), "Close", texte "Selected file: <nom>", liste "Chunk type" (all/text/table/image/thumbnail) et aperçu des segments (`ui.py:246-282`). Toast "File <nom> has been deleted" (`ui.py:579`).
- Accordéon "Advance options" : "Download all files" (masqué si SSO), "Delete all files" → "Confirm delete" / "Cancel" (`ui.py:284-298`). Téléchargement refusé pour un index privé : "This feature is not available for private collection." (`ui.py:654-655`).
- Sous-onglet "Groups" : tableau id, name, files, date_created ; boutons "Add", "Go to Chat", "Delete", "Close" ; formulaire "Group name", "Attached files" (multiple), "Save" ; toasts "Group <nom> has been saved/deleted" (`ui.py:300-350`, `:1656`, `:1673`).
- "Directory upload" (chemin serveur) existe (`ui.py:159-183`) mais n'est pas rendu dans `FileIndexPage.on_building_ui` : **non visible a priori**.

### 2.4 "Resources" — `ktem/pages/resources/__init__.py:19-37`
Sous-onglets : "Index Collections", "LLMs", "Embeddings", "Rerankings", "MCP Servers", "Users" (admin + gestion utilisateurs). Pas d'onglet "Prompts" (les prompts sont dans Settings > Reasoning settings).
- **Index Collections** (`ktem/index/ui.py:44-108`) : "View" (tableau id, name, index type ; édition "Index name", "Index config" (YAML), "Save", "Delete" → "Confirm Delete"/"Cancel", "Close") ; "Add" ("Index name", "Index type", "Specification" (YAML), bouton "Add"). Toujours suivi de "Please restart the app!" (`index/ui.py:257`, `:331`, `:340`). Clés YAML disponibles : `embedding`, `supported_file_types`, `max_file_size`, `max_number_of_files`, `private` (Yes/No), `chunk_size`, `chunk_overlap` (`index/file/index.py:377-438`).
- **LLMs** (`ktem/llms/ui.py:31-123`) : "View" (tableau name, vendor, default ; "Set default", "Name", "Specification" (YAML), accordéon **"Test connection"** avec bouton "Test" et journal "Logs", "Save", "Delete" → "Confirm Delete"/"Cancel", "Close") ; "Add" ("LLM name", "LLM vendors", "Specification", "Set default", bouton "Add LLM"). Le test envoie "Hi" et affiche "Connection success…" / "Connection failed…" (`llms/ui.py:344-380`). Fournisseurs = noms de classes : `ChatOpenAI`, `AzureChatOpenAI`, `LCAnthropicChat`, `LCGeminiChat`, `LCCohereChat`, `LCOllamaChat`, `LlamaCppChat` (`llms/manager.py:67-75`).
- **Embeddings** (`ktem/embeddings/ui.py:32-124`) : même structure ; "Add" = "Name", "Vendors", "Specification", "Set default", bouton "Add". Fournisseurs : `AzureOpenAIEmbeddings`, `OpenAIEmbeddings`, `FastEmbedEmbeddings`, `LCCohereEmbeddings`, `LCHuggingFaceEmbeddings`, `LCGoogleEmbeddings`, `LCMistralEmbeddings`, `TeiEndpointEmbeddings`, `VoyageAIEmbeddings` (`embeddings/manager.py:68-78`).
- **Rerankings** (`ktem/rerankings/ui.py:34-126`) : même structure. Fournisseurs : `TeiFastReranking`, `CohereReranking`, `VoyageAIReranking` (`rerankings/manager.py:61`). `TeiFastReranking` envoie `{"query", "texts", "is_truncated"}` à `endpoint_url` (format TEI, pas OpenAI/Jina) (`kot/rerankings/tei_fast_rerank.py:45-52`) : compatibilité avec le `rerank` de LLM-Service **à vérifier**.
- **MCP Servers** (`ktem/mcp/ui.py:32-90`) : "View" (name, config ; "Configuration (JSON)") et "Add" (éditeur "Configuration (JSON)", bouton "Add MCP Servers"). Les serveurs ajoutés deviennent des outils des agents ReAct/ReWOO (`reasoning/react.py:317-320`).
- **Users** (`ktem/pages/resources/user.py:136-179`) : "User list" (tableau id, name, admin ; "Username", "Change password", "Confirm change password", case "Admin", "Save", "Delete" → confirmation, "Cancel", "Close") ; "Create user" ("Username", "Password", "Confirm password", règles affichées, bouton "Create user"). Règles : nom 3-32 caractères alphanumériques/_ ; mot de passe ≥ 8 avec majuscule, minuscule, chiffre, caractère spécial (`user.py:10-27`).

### 2.5 "Settings" — `ktem/pages/settings.py`
- Bouton "Save & Close" `save-setting-btn`, déplacé par JS dans la barre d'onglets (`settings.py:120-127`, `main.js:40-44`) ; toast "Setting saved" (`settings.py:430`) ou "Need to login before saving settings" (`:416`).
- "User settings" (si gestion utilisateurs) : "Current user: <nom>", bouton "Logout", "New password", "Confirm password", bouton "Change password" → "Password changed" (`settings.py:248-287`).
- "General" : rendu seulement si `SETTINGS_APP` non vide — vide par défaut (`fs:333`), donc **masqué** (`settings.py:91-92`, `:292`).
- "Retrieval settings" : un sous-onglet par index (`settings.py:309-320`). Pour "File Collection" : "File loader" ("Default (open-source)", "Adobe API (figure+table extraction)", "Azure AI Document Intelligence (figure+table extraction)", "Docling (figure+table extraction)", "PaddleOCR PPStructureV3 (table+figure extraction)", "PaddleOCR-VL (VLM document parsing)") (`index/file/pipelines.py:714-735`) ; "LLM for relevant scoring", "Number of document chunks to retrieve" (10), "Retrieval mode" (vector/text/hybrid, défaut hybrid), "Prioritize table", "Use MMR", "Use reranking" (True), "Use LLM relevant scoring" (True) (`pipelines.py:225-280`). LightRAG ajoute "Search type" (local/global/hybrid) et une taille de lot + prompts d'indexation (`index/file/graph/lightrag_pipelines.py:290-305`, `:421-426`).
- "Reasoning settings" : "Language" (défaut en), "Max context length (LLM)" (32000) (`fs:337-353`) ; "### Reasoning-specific settings" ; radio "Reasoning options" (simple/complex/ReAct/ReWOO) qui affiche le groupe correspondant (`settings.py:322-376`) :
  - simple — "Simple QA" : "Language model", "Citation style", "Create Mindmap", "Create Embeddings Visualization", "Use Multimodal Input", "System Prompt", "QA Prompt (contains {context}, {question}, {lang})", "Number of interactions to include" (5), "Maximum message length for context rewriting" (150) (`reasoning/simple.py:409-470`).
  - complex — "Complex QA" : idem + "Decompose Prompt" (`simple.py:579-605`).
  - ReAct — "ReAct Agent" : "Language model", "Tools for knowledge retrieval" (Wikipedia, Google, LLM, SearchDoc + serveurs MCP), "Maximum number of iterations the LLM can go through" (5), "QA Prompt" (`reasoning/react.py:317-361`).
  - ReWOO — "ReWOO Agent" : "Language model for Planner", "Language model for Solver", "Highlight Citation", "Tools for knowledge retrieval", "Planner Prompt", "Solver Prompt" (`reasoning/rewoo.py:454-517`).
- Thème : pas de réglage dans Settings ; seul le bouton mode sombre du Chat (2.2). Thème Gradio maison `Kotaemon(Soft)` (`assets/theme.py:146`).

### 2.6 "Help" — `ktem/pages/help.py`
Accordéons "About", "User Guide" (ouvert hors démo) et "Changelogs (v<version>)" téléchargés depuis GitHub (`help.py:61-64`, `:91-92`, `:118-119` ; source `raw.githubusercontent.com/Cinnamon/kotaemon`, `help.py:39`) — sans accès réseau, contenu possiblement vide (à vérifier). En démo : "Create Your Own Space" (`help.py:66-68`).

## 3. Langues
- **Interface : anglais uniquement.** Aucun mécanisme i18n dans `ktem` (recherche `i18n|locale` sans résultat Python ; seule occurrence `locale="en"` du lecteur PDF, `pdf_viewer.js:20`). Pas de français pour les libellés.
- **Langue des réponses** ("Language", chat et Reasoning settings) : 31 langues dont **French (`fr`)** (`ktem/utils/lang.py:1-33`) : English, Japanese, Vietnamese, Spanish, French, German, Chinese, Russian, Arabic, Portuguese, Hindi, Bengali, Punjabi, Korean, Italian, Dutch, Turkish, Polish, Ukrainian, Romanian, Greek, Hungarian, Swedish, Czech, Finnish, Danish, Norwegian, Hebrew, Thai, Indonesian, Malay. Transmise aux pipelines de réponse, réécriture, agents et suggestions (`reasoning/simple.py:379-393`, `react.py:300`, `rewoo.py:426`, `chat/__init__.py:1439`).

## 4. Repères pour Playwright (elem_id réels)
- Onglets : `#login-tab`, `#chat-tab`, `#indices-tab` (et `#<id>-tab` par index si plusieurs : ids 1, 2, 3 attendus, à vérifier), `#resources-tab`, `#settings-tab`, `#help-tab`. Les sous-onglets (Resources, Files, Settings, View/Add) n'ont pas d'elem_id : cibler par rôle `tab` + nom (`getByRole('tab', {name: 'LLMs'})`).
- Chat : `#conv-settings-panel`, `#conversation-dropdown` (input : `#conversation-dropdown input`), `#suggest-chat-checkbox`, `#is-public-checkbox`, `#new-conv-button`, `#toggle-dark-button`, `#chat-expand-button`, `#info-expand-button`, `#index-0`/`#index-1`…, `#quick-file`, `#quick-url`, `#chat-suggestion`, `#report-accordion`, `#chat-area`, `#main-chat-bot`, `#chat-input` (textarea : `#chat-input textarea`, utilisé par `main.js:279`), `#chat-settings-expand`, `#quick-setting-labels`, `#citation-dropdown`, `#use-mindmap-checkbox`, `#chat-info-panel`, `#info-expand`, `#html-info-panel`, `#pdf-modal`, `#pdf-viewer`, `#modal-close`, `#modal-expand`.
- Panneau d'info : liens `a.pdf-link` (attributs `data-src`, `data-page`, `data-search`), contenu `.evidence-content`, citations `mark[id=…]` (`render.py:118-121`, `main.js:130`).
- Files : `#file_list_view` (tableau des fichiers) ; boutons à cibler par texte ("Upload and Index", "Delete", "Confirm delete"…).
- Settings : `#save-setting-btn` ; groupes de raisonnement `#simple`, `#complex`, `#ReAct`, `#ReWOO` (`settings.py:342-346`).
- Classes utiles : `indices-tab`, `fill-main-area-height`, `scrollable`, `no-background`, `right-button`, `unset-overflow`.
- Attention : plusieurs boutons portent le même texte ("Delete", "Close", "Save", "Add", "Cancel") dans des onglets cachés : restreindre la recherche à l'onglet visible.

## 5. Premier lancement (assistant « first setup ») — `ktem/pages/setup.py`
- Déclenché si `KH_ENABLE_FIRST_SETUP` (défaut True) et pas en démo et le dossier `ktem_app_data` n'existait pas au démarrage (`fs:35-36`, `main.py:21-25`), ou si `KH_FIRST_SETUP=true` (`main.py:17-18`). Il masque les onglets et affiche l'assistant (`main.py:205-210`) ; il précède donc l'écran de connexion (à vérifier). Une seule fois par processus (`main.py:24`).
- Écran : "# Welcome to Kotaemon first setup!" ; radio "Select your model provider" (info "Note: You can change this later. …") (`setup.py:47-61`) :
  - "Cohere API (*free registration*) - recommended" (défaut) → champ "Cohere API Key" ;
  - "Google API (*free registration*)" → "Google API Key" ;
  - "OpenAI API (for GPT-based models)" → "OpenAI API Key" ; **URL figée** `https://api.openai.com/v1`, modèles `gpt-4o` / `text-embedding-3-large` (`setup.py:236-259`) ;
  - "Local LLM (for completely *private RAG*)" → "LLM model name" (défaut `qwen2.5:7b`), "Embedding model name" (`nomic-embed-text`) ; enregistre `ChatOpenAI`/`OpenAIEmbeddings` sur `KH_OLLAMA_URL` puis **télécharge les modèles via l'API Ollama `/api/pull`** (`setup.py:279-333`).
- Boutons "Proceed" (primary) et "I am an advance user. Skip this." (stop) (`setup.py:109-113`). "Proceed" teste LLM et embedding ("Sending a message `Hi`") puis "Setup models completed successfully!" (`setup.py:338-388`).
- **Pour un fournisseur OpenAI-compatible personnalisé (LLM-Service)** : aucune option de l'assistant ne permet de saisir une URL (OpenAI = URL figée ; Local = Ollama + `pull`). Chemin prévu : cliquer "I am an advance user. Skip this." (`setup.py:139-147`), puis "Resources" > "LLMs" > "Add" : vendor `ChatOpenAI`, YAML avec `base_url`, `api_key`, `model` ; idem "Embeddings" avec `OpenAIEmbeddings` ; "Set default" ; "Test connection" dans "View". Alternative par variables d'environnement : `OPENAI_API_BASE`, `OPENAI_API_KEY`, `OPENAI_CHAT_MODEL`, `OPENAI_EMBEDDINGS_MODEL` déclarent les modèles "openai" au démarrage (`fs:143-172`). Attention : `OPENAI_API_KEY` vaut par défaut `<YOUR_OPENAI_KEY>`, donc une entrée "openai" (non par défaut) existe toujours (`fs:143-148`, `:159`). D'autres entrées sont toujours créées : "claude", "google", "groq", "cohere", "mistral" (`fs:232-308`), et "cohere" pour le reranking (`fs:310`) — à supprimer ou ignorer.
- Après "Proceed", le réglage `index.options.1.reranking_llm` reçoit le nom du fournisseur choisi (`setup.py:394-400`).

## 6. Fonctions présentes (d'après le code)
- **Collections privées/publiques** : propriété `private` de chaque index (YAML "Make private", Yes/No), fixée à la création dans "Resources" > "Index Collections" ; les index par défaut sont `private: True` (`fs:384`, `fs:399`). Index privé : chaque utilisateur ne voit que ses fichiers et groupes (`index/file/ui.py:1813-1851`). Pas de partage fichier par fichier. Les **conversations** se partagent avec "Share this conversation".
- **Citations avec surlignage PDF et score** : oui ("Citation style" highlight/inline/off ; "[Preview]" ouvre PDF.js à la page avec recherche du passage ; scores détaillés) (2.2).
- **Alerte de faible pertinence** : oui, seuil 0.3 sur le score LLM (`CONTEXT_RELEVANT_WARNING_SCORE`), affichée seulement si "Use LLM relevant scoring" est actif (`simple.py:238`, `:251`).
- **Mindmap** : case du chat + "Create Mindmap" (`simple.py:434-438`, `reasoning/prompt_optimization/mindmap.py`). Rendu markmap dans le panneau d'info (`main.js:176`).
- **Visualisation des embeddings des citations** : "Create Embeddings Visualization" (graphique Plotly, `chat/__init__.py:402`, `simple.py:439-443`).
- **QA multimodale** : "Use Multimodal Input" ; envoie les images des preuves de type figure à `KH_VLM_ENDPOINT`, construit pour **Azure OpenAI** (`fs:325-330`, `kot/indices/qa/citation_qa.py:99-100`, `:242`). Utilisation avec LLM-Service incertaine.
- **Décomposition** : raisonnement `complex` ("Complex QA", `simple.py:487-605`).
- **ReAct / ReWOO** : agents avec outils Wikipedia, Google, LLM, SearchDoc, MCP (`react.py`, `rewoo.py`) ; Wikipedia/Google demandent un accès Internet.
- **GraphRAG** : oui, **index séparés** = sous-onglets de "Files" ("GraphRAG Collection" = Microsoft GraphRAG, "LightRAG Collection", "NanoGraphRAG Collection" optionnel), chacun avec son accordéon dans le Chat (`fs:356-404`). Configuration du LLM de GraphRAG (variables `GRAPHRAG_*`, `USE_CUSTOMIZED_GRAPHRAG_SETTING` dans `.env.example:35`) non étudiée ici.
- **Recherche web** : commande `@WebSearch` (Tavily par défaut, clé `TAVILY_API_KEY` ; Jina en option) — service en ligne, hors périmètre.
- **Mode démo** (`KH_DEMO_MODE`) : masque Files/Resources/Settings, "Paper Collection", connexion externe, 2 raisonnements max, limitation de débit (`chat/__init__.py:57`, `:244-245`, `control.py:157-180`).
- **Suggestions de questions** : `KH_FEATURE_CHAT_SUGGESTION` (défaut False) + case "Suggest chat" ; toast "Chat suggestions updated." (`control.py:440`).
- **Feedback / signalement** : enregistré en base locale (`report.py:84-86`).

## Points incertains à confirmer en exécution
- Ordre réel assistant / écran "Welcome" ; persistance de la connexion par `localStorage`.
- Ids exacts des index (`#1-tab`…) et noms des sous-onglets après création.
- Contenu de "Help" sans Internet ; rendu mindmap ; comportement du clic sur citation.
- Compatibilité de `TeiFastReranking` avec le `rerank` de LLM-Service ; prise en compte de `model` (champ `model_name` non envoyé dans la requête, `tei_fast_rerank.py:45-52`).
