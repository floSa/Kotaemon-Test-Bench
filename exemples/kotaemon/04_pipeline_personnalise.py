"""Pipeline personnalisé construit avec les briques de la bibliothèque kotaemon, sans la base de l'application :
un magasin de vecteurs en mémoire, l'embedding `embed`, le tri `rerank` et le modèle `chat` du service central.
Il indexe trois phrases, cherche les deux plus proches de la question, les trie, puis fait rédiger la réponse."""
import os
from kotaemon.base import Document
from kotaemon.embeddings import OpenAIEmbeddings
from kotaemon.llms import ChatOpenAI
from kotaemon.rerankings import CohereReranking
from kotaemon.storages import InMemoryDocumentStore, InMemoryVectorStore
from kotaemon.indices import VectorIndexing, VectorRetrieval

CLE = os.environ["LLM_CENTRAL_KEY"]
emb = OpenAIEmbeddings(base_url="http://llm-central:8080/v1", api_key=CLE, model="embed")
vs, ds = InMemoryVectorStore(), InMemoryDocumentStore()
VectorIndexing(vector_store=vs, doc_store=ds, embedding=emb).run([
    Document(text="Le local B2 est inspecté le premier lundi de chaque mois."),
    Document(text="Les batteries se stockent entre 10 et 25 °C, à l'abri de l'humidité."),
    Document(text="Le service après-vente répond au 02 40 00 12 34."),
])
question = "Quand le local B2 est-il inspecté ?"
passages = VectorRetrieval(vector_store=vs, doc_store=ds, embedding=emb, top_k=2).run(question)
tri = CohereReranking(model_name="rerank", cohere_api_key=CLE, base_url="http://llm-central:8080")
passages = tri.run(passages, question)
for p in passages:
    print(f"passage (score de tri {p.metadata.get('reranking_score', 0):.2f}) : {p.text}")
llm = ChatOpenAI(base_url="http://llm-central:8080/v1", api_key=CLE, model="chat", temperature=0, max_tokens=2048, timeout=300)
contexte = "\n".join(p.text for p in passages)
print("réponse :", llm(f"Réponds en une phrase, d'après ce contexte seulement.\nContexte : {contexte}\nQuestion : {question}").text.strip())
