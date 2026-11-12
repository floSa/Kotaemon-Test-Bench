# Relecture avant lancement — Kotaemon v0.12.0

Relu le 12 novembre 2026, sources au tag `v0.12.0` (commit 9ad3e4e, `sources/kotaemon`, ignoré par git). Synthèses détaillées : `cadrage-serveur.md` et `cadrage-interface.md`.

| Élément relu | Points relevés | Suite donnée |
|---|---|---|
| `Dockerfile` (cibles lite, full, paddle, ollama) | image « full » : tesseract, LibreOffice, ffmpeg, torch CPU, unstructured, Docling (<= 2.5.2), LightRAG (lightrag-hku <= 1.3.0), graphrag <= 0.3.6 ; aucun `USER` (root) ; `.env.example` copié en `/app/.env` ; la cible `paddle` (PaddleOCR, GPU) n'est pas publiée | image `main-full` figée par empreinte ; PaddleOCR noté absent |
| `launch.sh` | `ollama serve &` lancé sans condition (absent de l'image full : message « ollama: not found » sans effet) ; Gradio sur 0.0.0.0:7860 dans le conteneur | port publié sur 127.0.0.1 seulement |
| `flowsettings.py` | admin/admin créé d'office ; entrées de modèles en ligne créées d'office (openai, claude, google, groq, cohere, mistral ; reranker cohere par défaut) ; Ollama et VoyageAI ajoutés si `LOCAL_MODEL` / `VOYAGE_API_KEY` non vides ; « Max context length (LLM) » 32000 par défaut | `LOCAL_MODEL`, `LOCAL_MODEL_EMBEDDINGS`, `VOYAGE_API_KEY` vidés dans le compose ; mot de passe changé au chapitre 03 ; contexte réglé sous 16 384 |
| `embeddings/openai.py` | avec `context_length`, les textes partent en identifiants de jetons tiktoken (incompatibles avec bge-m3) | embedding `embed` déclaré sans `context_length` |
| `rerankings/cohere.py`, `tei_fast_rerank.py` | Cohere accepte `base_url` (SDK : `/v1/rerank` ajouté) ; TEI attend une réponse en liste, différente de LiteLLM | essai de `CohereReranking` vers `http://llm-central:8080` |
| `llms/chats/openai.py` | pas d'`extra_body` : la réflexion de `chat` ne peut pas être coupée depuis Kotaemon ; délai d'attente 20 s par défaut | `timeout` et `max_tokens` réglés dans la spécification YAML |
| Télémétrie | Gradio (coupée dans le code), Chroma (posthog), unstructured (scarf) ; appel à api.github.com au démarrage (page Help) | `GRADIO_ANALYTICS_ENABLED=False`, `ANONYMIZED_TELEMETRY=False`, `DO_NOT_TRACK=true`, `SCARF_NO_ANALYTICS=true` |
| GraphRAG | LightRAG installé ; NanoGraphRAG absent (« Nano-GraphRAG dependencies not installed » au démarrage) ; MS GraphRAG lance un `python` hors de l'environnement de l'application et vise OpenAI ou Ollama | essais au chapitre GraphRAG |

Constat au démarrage : la version affichée par l'interface est « 0.0.1 » (numéro calculé par git, absent de l'image) ; la révision de l'image (`org.opencontainers.image.revision` = 9ad3e4e) prouve qu'il s'agit de v0.12.0.
