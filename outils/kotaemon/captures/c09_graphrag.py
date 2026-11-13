"""Chapitre 09, Graphes de connaissances : indexation d'un document dans « LightRAG Collection », question posée à cette
collection ; « NanoGraphRAG Collection » (après outils/kotaemon/installer_nanographrag.sh) ; « GraphRAG Collection »
(Microsoft GraphRAG) : essai et erreur obtenue.
Usage : lancer.sh outils/kotaemon/captures/c09_graphrag.py [lightrag] [question_lightrag] [nano] [question_nano] [msgraphrag]"""
import time
from ui import Scenario, etapes, RACINE

CH = "09-graphrag"
DOC = RACINE / "corpus/documents/rapport-annuel-2025.pdf"
PETIT = RACINE / "corpus/documents/procedure-batteries.docx"


def indexer(s, collection, fichier, prefixe, delai=3600, forcer=False):
    p = s.page
    s.onglet("Files"); s.onglet(collection); s.onglet("Upload Files")
    s.deposer([fichier])
    if forcer:
        if not p.get_by_label("Force reindex file").locator("visible=true").count():
            s.texte("Advanced indexing options", exact=True).click(); p.wait_for_timeout(800)
        p.get_by_label("Force reindex file").locator("visible=true").first.check()
    t0 = time.time()
    s.bouton("Upload and Index").click(); p.wait_for_timeout(5000)
    s.attendre_fin(delai=delai * 1000)
    p.get_by_text("Upload Progress").locator("visible=true").first.wait_for()
    duree = time.time() - t0
    s.note(f"{collection} : indexation de {fichier.name} en {duree:.0f} s ; toasts {s.toasts()!r}")
    infos = p.locator("textarea").locator("visible=true")
    s.note(f"{collection} upload info : " + " | ".join(t.input_value()[:1500] for t in infos.all()).replace("\n", " / "))
    s.sans_toasts()
    s.cap_souple(prefixe, [(s.tab(collection), collection), (infos.first, "Upload result"), (infos.nth(1), "Upload info")])
    return duree


def lightrag(s):
    indexer(s, "LightRAG Collection", DOC, "03-lightrag-indexation", forcer=True)


def question(s, rang, nom, cap, q):
    p = s.page
    s.onglet("Chat")
    p.locator("#new-conv-button").click(); p.wait_for_timeout(1500)
    s.reglage_session("Language", "French")
    acc = p.locator(f"#index-{rang}")
    acc.get_by_text(nom, exact=True).first.click(); p.wait_for_timeout(1000)
    acc.get_by_text("Search All", exact=True).click()
    t0 = time.time()
    s.poser(q)
    s.note(f"{nom} : réponse en {time.time() - t0:.0f} s : " + p.locator("#main-chat-bot .message").last.inner_text()[:600].replace("\n", " "))
    s.note(f"{nom} panneau : " + p.locator("#html-info-panel").inner_text()[:1500].replace("\n", " | "))
    s.cap_souple(cap, [(acc, nom + " (Search All)"), (p.locator("#main-chat-bot .message").last, "réponse"),
                       (p.locator("#html-info-panel"), "entités, relations et passages")])


def question_lightrag(s):
    question(s, 2, "LightRAG Collection", "04-lightrag-question",
             "Quels sont les sites de Vélanor et combien de salariés compte chacun ?")


def nano(s):
    indexer(s, "NanoGraphRAG Collection", PETIT, "05-nanographrag-indexation")


def question_nano(s):
    question(s, 4, "NanoGraphRAG Collection", "06-nanographrag-question",
             "À quelle température les batteries doivent-elles être stockées ?")


def msgraphrag(s):
    indexer(s, "GraphRAG Collection", PETIT, "07-msgraphrag-erreur", delai=600)


if __name__ == "__main__":
    s = Scenario(CH)
    try:
        etapes([lightrag, question_lightrag, nano, question_nano, msgraphrag], s)
    finally:
        s.fermer()
