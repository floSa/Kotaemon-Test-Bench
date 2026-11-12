"""Captures de repérage de la carte de l'interface (docs/kotaemon/img/carte/), une par page ou sous-onglet, compte
administrateur. Usage : lancer.sh outils/kotaemon/captures/carte.py [--sans-connexion]"""
import sys
from ui import Scenario

PAGES = [("chat", ["Chat"]),
         ("files-upload", ["Files", "File Collection", "Upload Files"]),
         ("files-liens", ["Files", "File Collection", "Use Web Links"]),
         ("files-groupes", ["Files", "File Collection", "Groups"]),
         ("files-graphrag", ["Files", "GraphRAG Collection"]),
         ("files-lightrag", ["Files", "LightRAG Collection"]),
         ("resources-collections", ["Resources", "Index Collections", "View"]),
         ("resources-collections-ajout", ["Resources", "Index Collections", "Add"]),
         ("resources-llms", ["Resources", "LLMs", "View"]),
         ("resources-llms-ajout", ["Resources", "LLMs", "Add"]),
         ("resources-embeddings", ["Resources", "Embeddings", "View"]),
         ("resources-embeddings-ajout", ["Resources", "Embeddings", "Add"]),
         ("resources-rerankings", ["Resources", "Rerankings", "View"]),
         ("resources-rerankings-ajout", ["Resources", "Rerankings", "Add"]),
         ("resources-mcp", ["Resources", "MCP Servers", "View"]),
         ("resources-mcp-ajout", ["Resources", "MCP Servers", "Add"]),
         ("resources-users", ["Resources", "Users", "User list"]),
         ("resources-users-creer", ["Resources", "Users", "Create user"]),
         ("settings-user", ["Settings", "User settings"]),
         ("settings-retrieval", ["Settings", "Retrieval settings", "File Collection"]),
         ("settings-retrieval-lightrag", ["Settings", "Retrieval settings", "LightRAG Collection"]),
         ("settings-reasoning", ["Settings", "Reasoning settings"]),
         ("help", ["Help"])]

if "--sans-connexion" in sys.argv:
    s = Scenario("carte", connecter=False)
    s.cap("welcome", [], note="repérage : connexion")
    s.fermer(); sys.exit()
s = Scenario("carte")
try:
    for nom, chemin in PAGES:
        for t in chemin:
            s.onglet(t)
        s.page.evaluate("window.scrollTo(0, 0)")
        s.page.wait_for_timeout(1000)
        s.cap(nom, [], note="repérage : " + " › ".join(chemin))
finally:
    s.fermer()
