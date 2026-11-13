"""Chapitre 04, Première question en dix minutes : un PDF importé dans « File Collection », une question, la réponse
citée, la visionneuse PDF. Usage : lancer.sh outils/kotaemon/captures/c04_premiere_question.py [importer] [questionner]"""
import time
from ui import Scenario, etapes, RACINE

CH = "04-premiere-question"
DOC = RACINE / "corpus/documents/rapport-annuel-2025.pdf"
QUESTION = "Quel est le chiffre d'affaires 2025 de Vélanor ?"


def importer(s):
    p = s.page
    s.onglet("Files")
    s.cap("01-onglet-files", [(s.tab("Files"), "Files"), (s.tab("File Collection"), "File Collection"),
                              (s.tab("Upload Files"), "Upload Files"),
                              (s.zone_depot(), "zone de dépôt"),
                              (s.bouton("Upload and Index"), "Upload and Index")])
    s.deposer([DOC])
    s.cap_souple("02-fichier-choisi", [(p.locator("table").filter(has_text="KB").locator("visible=true").first, "fichier choisi"),
                                (s.texte("Advanced indexing options"), "Advanced indexing options"),
                                (s.bouton("Upload and Index"), "Upload and Index")])
    t0 = time.time()
    s.bouton("Upload and Index").click()
    p.wait_for_timeout(3000)
    s.attendre_fin()
    p.get_by_text("Upload Progress").locator("visible=true").first.wait_for()
    s.note(f"indexation de {DOC.name} : {time.time() - t0:.1f} s ; toasts {s.toasts()!r}")
    s.sans_toasts()
    s.cap_souple("03-progression", [(s.texte("Upload Progress"), "Upload Progress"),
                             (p.locator("textarea").locator("visible=true").first, "Upload result"),
                             (s.bouton("Clear Upload Info and Close"), "Clear Upload Info and Close")])
    s.bouton("Clear Upload Info and Close").click(); p.wait_for_timeout(1500)
    s.cap_souple("04-liste-fichiers", [(s.ligne("rapport-annuel-2025.pdf"), "rapport-annuel-2025.pdf"),
                                (s.texte("Filter by name:"), "Filter by name:")])


def questionner(s):
    p = s.page
    s.onglet("Chat")
    p.locator("#index-0").get_by_text("Search All", exact=True).click()
    langue = s.reglage_session("Language", "French")
    acc = p.locator("#chat-settings-expand")
    s.cap("05-langue-de-la-reponse", [(acc.get_by_text("Chat settings", exact=True), "Chat settings"),
                                      (acc.get_by_text("Language", exact=True), "Language"), (langue, "French")])
    zone = s.poser(QUESTION, envoyer=False)
    s.cap("06-poser-la-question", [(p.locator("#index-0"), "File Collection"),
                                   (p.locator("#index-0").get_by_text("Search All", exact=True), "Search All"),
                                   (zone, "zone de saisie"), (p.locator("#chat-input button").last, "bouton d'envoi")])
    t0 = time.time()
    zone.press("Enter")
    s.attendre_reponse()
    s.note(f"réponse en {time.time() - t0:.1f} s")
    rep = p.locator("#main-chat-bot .message").last
    s.cap("07-reponse-citee", [(rep, "réponse"), (p.locator("#html-info-panel"), "Information panel")])
    s.note("réponse : " + rep.inner_text()[:600].replace("\n", " "))
    lien = p.locator("#html-info-panel a.pdf-link").first
    if lien.count():
        p.locator("#html-info-panel details").first.evaluate("e => e.open = true")
        s.cap("08-extrait-et-score", [(p.locator("#html-info-panel details").first, "extrait cité"), (lien, "[Preview]")])
        lien.click(); p.wait_for_timeout(5000)
        s.cap("09-visionneuse-pdf", [(p.locator("#pdf-modal .modal-body"), "visionneuse")])
    else:
        s.note("aucun lien [Preview] dans le panneau d'information")


if __name__ == "__main__":
    s = Scenario(CH)
    try:
        etapes([importer, questionner], s)
    finally:
        s.fermer()
