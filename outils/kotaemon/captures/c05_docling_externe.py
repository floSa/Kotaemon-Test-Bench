"""Chapitre 05, lecteur extérieur : PDF scanné lu par un serveur Docling séparé (rag-docling-serve).
Prérequis : outils/kotaemon/docling_externe/brancher.sh. « File loader » reste sur « Default (open-source) » :
le réglage de flowsettings.py remplace le lecteur des PDF. Le groupe « Fournisseur Batterix » est réparé à la fin.
Usage : lancer.sh outils/kotaemon/captures/c05_docling_externe.py"""
import time
from ui import Scenario, etapes, RACINE
from c05_documents import ouvrir_files, DOCS

CH = "05-documents"


def reglage(s):
    p = s.page
    s.onglet("Settings"); s.onglet("Retrieval settings")
    s.note("File loader affiché : " + repr(s.champ("File loader").input_value()))


def externe(s):
    p = s.page
    ouvrir_files(s); s.onglet("Upload Files")
    s.deposer([DOCS / "contrat-batterix-scan.pdf"])
    if not p.locator("label").filter(has_text="Force reindex file").locator("visible=true").count():
        s.texte("Advanced indexing options", exact=True).click(); p.wait_for_timeout(800)
    p.get_by_label("Force reindex file").locator("visible=true").first.check()
    t0 = time.time()
    s.bouton("Upload and Index").click(); p.wait_for_timeout(5000)
    s.attendre_fin(delai=900000); p.get_by_text("Upload Progress").locator("visible=true").first.wait_for()
    s.note(f"réindexation du scan par le serveur Docling séparé : {time.time() - t0:.1f} s ; toasts {s.toasts()!r}")
    s.note("Upload info : " + " | ".join(t.input_value()[:400] for t in p.locator("textarea").locator("visible=true").all()))
    s.sans_toasts()
    s.bouton("Clear Upload Info and Close").click(); p.wait_for_timeout(1500)
    s.ligne("contrat-batterix-scan.pdf").click(); p.wait_for_timeout(3000)
    p.mouse.move(900, 500); p.mouse.wheel(0, 380); p.wait_for_timeout(1000)
    s.cap_souple("18-scan-lu-par-docling-externe", [(s.ligne("contrat-batterix-scan.pdf"), "LecteurDoclingServe"),
                                                    (p.get_by_text("212 euros").locator("visible=true").first, "texte lu par le serveur")])


def reparer(s):
    p = s.page
    ouvrir_files(s); s.onglet("Groups")
    s.ligne("Fournisseur Batterix").click(); p.wait_for_timeout(2000)
    p.locator("label").filter(has_text="Attached files").locator("input").locator("visible=true").first.click(); p.wait_for_timeout(800)
    opt = p.get_by_role("option", name="contrat-batterix-scan.pdf", exact=True).locator("visible=true")
    if opt.count():
        opt.first.click(); p.wait_for_timeout(800)
    p.locator("body").click(position={"x": 1300, "y": 850}); p.wait_for_timeout(600)
    s.bouton("Save").click(); p.wait_for_timeout(2500)
    s.note("groupe réparé : toasts " + repr(s.toasts()))


if __name__ == "__main__":
    s = Scenario(CH)
    try:
        etapes([reglage, externe, reparer], s)
    finally:
        s.fermer()
