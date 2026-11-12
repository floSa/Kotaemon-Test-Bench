"""Chapitre 12, Cas pratiques : (1) préparer la renégociation d'un fournisseur (groupe, décomposition) ;
(2) répondre au service client avec une question de suite ; (3) note RH partagée, consultée par un autre compte.
Usage : lancer.sh outils/kotaemon/captures/c12_cas_pratiques.py [fournisseur] [client] [equipe]"""
import time
from ui import Scenario, etapes, identifiants

CH = "12-cas-pratiques"


def nouvelle(s, methode=None):
    p = s.page
    p.locator("#new-conv-button").click(); p.wait_for_timeout(1500)
    s.reglage_session("Language", "French")
    if methode:
        s.reglage_session("Reasoning method", methode)


def fournisseur(s):
    p = s.page
    nouvelle(s, "complex")
    zone = p.locator("#index-0")
    zone.get_by_text("Search In File(s)", exact=True).click(); p.wait_for_timeout(1200)
    liste = zone.locator("input").locator("visible=true").last
    liste.click(); p.wait_for_timeout(600)
    p.get_by_role("option", name="group: 'Fournisseur Batterix'").locator("visible=true").first.click(); p.wait_for_timeout(600)
    p.keyboard.press("Escape")
    t0 = time.time()
    s.poser("Pour préparer la renégociation avec Batterix : quel prix unitaire et quel délai de livraison le contrat fixe-t-il, "
            "et quel score et quel délai moyen l'audit a-t-il constatés ?")
    s.note(f"fournisseur ({time.time() - t0:.0f} s) : " + p.locator("#main-chat-bot .message").last.inner_text()[:900].replace("\n", " "))
    s.cap_souple("01-fournisseur-reponse", [(zone, "groupe Fournisseur Batterix"), (p.locator("#main-chat-bot .message").last, "réponse"),
                                            (p.locator("#html-info-panel"), "sources : contrat et audit")])


def client(s):
    p = s.page
    nouvelle(s)
    p.locator("#index-0").get_by_text("Search All", exact=True).click()
    s.poser("Quelle est la durée de garantie du cadre ?")
    s.poser("Et quel numéro appeler pour le service après-vente ?")
    s.note("client : " + p.locator("#main-chat-bot").inner_text()[:1200].replace("\n", " "))
    s.cap_souple("02-client-suite", [(p.locator("#main-chat-bot .message").nth(1), "première réponse"),
                                     (p.locator("#main-chat-bot .message").last, "réponse à la question de suite"),
                                     (p.locator("#html-info-panel"), "source : faq-sav.html")])


def equipe(s):
    c = Scenario(CH, utilisateur="camille", mot_de_passe=identifiants()["kotaemon.camille.mot_de_passe"])
    try:
        p = c.page
        nouvelle(c)
        acc = p.get_by_text("Documents partagés", exact=True).locator("visible=true").first
        acc.click(); p.wait_for_timeout(1000)
        bloc = p.locator("[id^=index-]").filter(has_text="Documents partagés").first
        bloc.get_by_text("Search All", exact=True).click()
        c.poser("Quel est le montant de la prime d'intéressement 2025 ?")
        c.note("équipe (camille) : " + p.locator("#main-chat-bot .message").last.inner_text()[:600].replace("\n", " "))
        c.cap_souple("03-equipe-reponse", [(bloc, "Documents partagés (Search All)"), (p.locator("#main-chat-bot .message").last, "réponse"),
                                           (p.locator("#html-info-panel"), "source : cse-2025-10-14.md")])
    finally:
        c.fermer()


if __name__ == "__main__":
    s = Scenario(CH)
    try:
        etapes([fournisseur, client, equipe], s)
    finally:
        s.fermer()
