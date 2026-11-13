"""Chapitre 06, Poser des questions et lire les sources : conversations (nouvelle, renommer, parcourir, supprimer),
recherche dans certains fichiers ou un groupe, mention @fichier, styles de citation, carte mentale, détail des scores,
avis sur une réponse, partage, boutons d'affichage.
Usage : lancer.sh outils/kotaemon/captures/c06_questions.py [fichiers] [mention] [citations] [carte] [conversations] [avis] [affichage]"""
import re, time
from ui import Scenario, etapes

CH = "06-questions"


def nouvelle(s):
    s.nouvelle_conversation()


def fichiers(s):
    """Recherche limitée à un fichier puis à un groupe."""
    p = s.page
    nouvelle(s)
    s.reglage_session("Language", "French")
    zone = p.locator("#index-0")
    zone.get_by_text("Search In File(s)", exact=True).click(); p.wait_for_timeout(1500)
    liste = zone.locator("input").locator("visible=true").last
    liste.click(); p.wait_for_timeout(800)
    s.cap_souple("01-choisir-fichiers", [(zone.get_by_text("Search In File(s)", exact=True), "Search In File(s)"),
                                          (liste, "Files"),
                                          (p.get_by_role("option", name="group: 'Fournisseur Batterix'").locator("visible=true").first, "group: 'Fournisseur Batterix'"),
                                          (p.get_by_role("option", name="contrat-batterix-scan.pdf", exact=True).locator("visible=true").first, "contrat-batterix-scan.pdf")])
    p.get_by_role("option", name="group: 'Fournisseur Batterix'").locator("visible=true").first.click(); p.wait_for_timeout(800)
    p.keyboard.press("Escape")
    s.poser("Quel score Batterix a-t-il obtenu à l'audit, et quel prix unitaire le contrat fixe-t-il ?")
    s.cap_souple("02-reponse-groupe", [(zone, "File Collection (groupe choisi)"), (p.locator("#main-chat-bot .message").last, "réponse"),
                                       (p.locator("#html-info-panel"), "Information panel")])
    s.note("réponse groupe : " + p.locator("#main-chat-bot .message").last.inner_text()[:500].replace("\n", " "))


def mention(s):
    p = s.page
    nouvelle(s)
    s.reglage_session("Language", "French")
    p.locator("#index-0").get_by_text("Search All", exact=True).click()
    zone = p.locator("#chat-input textarea")
    zone.fill("Quel est le prix du Vilaine Compact ? @strat")
    p.wait_for_timeout(2000)
    s.cap_souple("03-mention-fichier", [(zone, "zone de saisie avec @"),
                                        (p.get_by_text("strategie-2026.pptx").locator("visible=true").first, "suggestion strategie-2026.pptx")])
    sug = p.get_by_text("strategie-2026.pptx").locator("visible=true")
    if sug.count():
        sug.first.click(); p.wait_for_timeout(800)
    s.note("saisie après mention : " + zone.input_value())
    zone.press("Enter"); s.attendre_reponse()
    s.note("réponse mention : " + p.locator("#main-chat-bot .message").last.inner_text()[:400].replace("\n", " "))


def citations(s):
    p = s.page
    nouvelle(s)
    s.reglage_session("Language", "French")
    p.locator("#index-0").get_by_text("Search All", exact=True).click()
    cit = p.locator("#citation-dropdown input").first
    cit.click(); p.wait_for_timeout(600)
    s.cap_souple("04-styles-citation", [(cit, "style de citation"),
                                        (p.get_by_role("option", name="citation: inline").locator("visible=true").first, "citation: inline"),
                                        (p.locator("#use-mindmap-checkbox"), "Mindmap")])
    p.get_by_role("option", name="citation: inline").locator("visible=true").first.click(); p.wait_for_timeout(800)
    p.locator("#use-mindmap-checkbox input").uncheck(); p.wait_for_timeout(500)
    s.poser("Quelle est la capacité prévue de l'usine de Saint-Nazaire ?")
    s.cap_souple("05-citation-en-ligne", [(p.locator("#main-chat-bot .message").last, "réponse avec citations en ligne"),
                                          (p.locator("#html-info-panel"), "Information panel")])
    s.note("réponse inline : " + p.locator("#main-chat-bot .message").last.inner_text()[:500].replace("\n", " "))
    # bloc « Relevance score » (détails imbriqués dans le bloc du passage) : on l'ouvre par son titre
    titre = p.locator("#html-info-panel details details summary").filter(has_text="Relevance score").locator("visible=true").first
    titre.click(); p.wait_for_timeout(1000)
    bloc = titre.locator("xpath=..")
    s.note("détail des scores : " + bloc.inner_text()[:300].replace("\n", " | "))
    s.cap_souple("06-detail-scores", [(bloc, "Relevance score et détail des notes")])


def carte(s):
    p = s.page
    nouvelle(s)
    s.reglage_session("Language", "French")
    p.locator("#index-0").get_by_text("Search All", exact=True).click()
    cit = p.locator("#citation-dropdown input").first
    cit.click(); p.wait_for_timeout(600)
    p.get_by_role("option", name="citation: highlight").locator("visible=true").first.click(); p.wait_for_timeout(800)
    cb = p.locator("#use-mindmap-checkbox input")
    if not cb.is_checked():
        cb.check()
    s.poser("Quelles sont les perspectives 2026 de Vélanor ?")
    p.wait_for_timeout(5000)
    s.sans_toasts()
    mm = p.locator("#html-info-panel svg, #html-info-panel .markmap").locator("visible=true").first
    s.cap_souple("07-carte-mentale", [(p.locator("#use-mindmap-checkbox"), "Mindmap (on)"), (mm, "carte mentale")])


def conversations(s):
    p = s.page
    dd = p.locator("#conversation-dropdown input")
    dd.click(); p.wait_for_timeout(800)
    s.cap_souple("08-parcourir", [(dd, "liste des conversations"), (p.get_by_role("option").locator("visible=true").first, "une conversation")])
    p.get_by_role("option").locator("visible=true").first.click(); p.wait_for_timeout(2500)
    ren = p.locator("#conv-settings-panel img[src*='rename']").locator("..").locator("visible=true").first
    sup = p.locator("#conv-settings-panel img[src*='delete']").locator("..").locator("visible=true").first
    s.cap_souple("09-boutons-conversation", [(ren, "renommer"), (sup, "supprimer"), (p.locator("#new-conv-button"), "nouvelle conversation"),
                                             (p.locator("#suggest-chat-checkbox"), "Suggest chat")])
    ren.click(); p.wait_for_timeout(800)
    nom = p.get_by_placeholder("Conversation name").locator("visible=true").first
    nom.fill("Audit et contrat Batterix")
    s.cap_souple("10-renommer", [(nom, "Conversation name")])
    nom.press("Enter"); p.wait_for_timeout(2000)
    s.note("renommer : toasts " + repr(s.toasts())); s.sans_toasts()
    sup.click(); p.wait_for_timeout(800)
    s.cap_souple("11-supprimer", [(s.bouton("Delete"), "Delete"), (s.bouton("Cancel"), "Cancel")])
    s.bouton("Cancel").click(); p.wait_for_timeout(800)


def avis(s):
    p = s.page
    acc = p.locator("#report-accordion")
    acc.get_by_text("Feedback").first.click(); p.wait_for_timeout(1000)
    acc.get_by_text("The answer is correct", exact=True).click()
    acc.locator("textarea").first.fill("Réponse juste, source vérifiée dans le panneau.")
    s.cap_souple("12-avis", [(acc.get_by_text("The answer is correct", exact=True), "The answer is correct"),
                             (acc.get_by_text("The evidence is incorrect", exact=True), "The evidence is incorrect"),
                             (acc.locator("textarea").first, "More detail"), (s.bouton("Report"), "Report"),
                             (p.locator("#is-public-checkbox"), "Share this conversation")])
    s.bouton("Report").click(); p.wait_for_timeout(2500)
    s.note("avis : toasts " + repr(s.toasts()))


def affichage(s):
    p = s.page
    p.locator("#toggle-dark-button").click(); p.wait_for_timeout(1200)
    s.cap_souple("13-mode-sombre", [(p.locator("#toggle-dark-button"), "mode sombre"), (p.locator("#chat-expand-button"), "agrandir la discussion"),
                                    (p.locator("#info-expand-button"), "agrandir le panneau d'information")])
    p.locator("#toggle-dark-button").click(); p.wait_for_timeout(800)


if __name__ == "__main__":
    s = Scenario(CH)
    try:
        etapes([fichiers, mention, citations, carte, conversations, avis, affichage], s)
    finally:
        s.fermer()
