"""Chapitre 10, Collections et modèles (onglet Resources) : liste et ajout de collections (collection partagée),
suppression d'un modèle en ligne inutilisé, vues Embeddings et Rerankings.
Usage : lancer.sh outils/kotaemon/captures/c10_ressources.py [collections] [ajouter] [supprimer] [vues]
Après « ajouter », redémarrer Kotaemon (outils/kotaemon/arreter.sh puis demarrer.sh), comme l'interface le demande."""
from ui import Scenario, etapes

CH = "10-ressources"
SPEC = """embedding: llm-service-embed
max_file_size: 1000
max_number_of_files: 0
private: false
supported_file_types: .png, .jpeg, .jpg, .tiff, .tif, .pdf, .xls, .xlsx, .doc, .docx, .pptx, .csv, .html, .mhtml, .txt, .md, .zip
"""


def collections(s):
    p = s.page
    s.onglet("Resources"); s.onglet("Index Collections"); s.onglet("View")
    s.ligne("File Collection").click(); p.wait_for_timeout(2000)
    s.cap_souple("01-collections", [(s.tab("Index Collections"), "Index Collections"), (s.ligne("File Collection"), "File Collection"),
                                    (s.champ("Index name"), "Index name"), (p.locator("textarea").locator("visible=true").nth(1), "Index config")])
    s.note("config File Collection : " + p.locator("textarea").locator("visible=true").nth(1).input_value()[:600].replace("\n", " | "))


def ajouter(s):
    p = s.page
    s.onglet("Resources"); s.onglet("Index Collections"); s.onglet("Add")
    s.champ("Index name").fill("Documents partagés")
    s.choisir("Index type", "FileIndex")
    p.wait_for_timeout(1500)
    zone = p.locator("textarea").locator("visible=true").last
    s.note("spécification proposée : " + zone.input_value()[:800].replace("\n", " | "))
    zone.fill(SPEC)
    s.cap_souple("02-collection-ajouter", [(s.tab("Add"), "Add"), (s.champ("Index name"), "Index name"), (s.champ("Index type"), "Index type"),
                                          (zone, "Specification"), (s.bouton("Add"), "Add")])
    s.bouton("Add").click(); p.wait_for_timeout(3000)
    s.note("ajout collection : toasts " + repr(s.toasts()))
    s.cap_souple("03-redemarrer", [(p.get_by_text("restart").locator("visible=true").first, "message de redémarrage")])


def supprimer(s):
    p = s.page
    s.onglet("Resources"); s.onglet("LLMs"); s.onglet("View")
    s.ligne("claude").click(); p.wait_for_timeout(2000)
    s.bouton("Delete").click(); p.wait_for_timeout(1000)
    s.cap_souple("04-supprimer-modele", [(s.bouton("Confirm Delete"), "Confirm Delete"), (s.bouton("Cancel"), "Cancel")])
    s.bouton("Confirm Delete").click(); p.wait_for_timeout(2500)
    s.note("suppression claude : toasts " + repr(s.toasts()))


def vues(s):
    p = s.page
    s.onglet("Resources"); s.onglet("Embeddings"); s.onglet("View")
    s.cap_souple("05-embeddings-liste", [(s.ligne("llm-service-embed"), "llm-service-embed"), (s.ligne("cohere"), "cohere")])
    s.onglet("Rerankings"); s.onglet("View")
    s.cap_souple("06-rerankings-liste", [(s.ligne("llm-service-rerank"), "llm-service-rerank"), (s.ligne("cohere"), "cohere")])


if __name__ == "__main__":
    s = Scenario(CH)
    try:
        etapes([collections, ajouter, supprimer, vues], s)
    finally:
        s.fermer()
