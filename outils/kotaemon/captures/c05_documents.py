"""Chapitre 05, Ajouter et organiser ses documents : ajout de plusieurs fichiers, liens web (onglet seulement : service
en ligne r.jina.ai), fiche d'un fichier et ses passages, groupes, options avancées, ajout rapide depuis le chat,
lecteur Docling. Usage : lancer.sh outils/kotaemon/captures/c05_documents.py [plusieurs] [liens] [fiche] [groupes]
[avance] [rapide] [lecteur]"""
import shutil, time
from pathlib import Path
from ui import Scenario, etapes, RACINE

CH = "05-documents"
DOCS = RACINE / "corpus/documents"
AUTRES = ["rapport-annuel-2025.pdf", "procedure-batteries.docx", "strategie-2026.pptx", "stocks-octobre-2025.xlsx", "faq-sav.html",
          "cse-2025-10-14.md", "contrat-batterix-scan.pdf", "supplier-audit-batterix-en.pdf"]


def ouvrir_files(s):
    s.onglet("Files"); s.onglet("File Collection")


def plusieurs(s):
    """Ajoute en une fois les huit documents du corpus lisibles par Kotaemon (le MP3 ne l'est pas)."""
    p = s.page
    ouvrir_files(s); s.onglet("Upload Files")
    s.deposer([DOCS / f for f in AUTRES])
    s.cap("01-plusieurs-fichiers", [(p.locator("table").filter(has_text="KB").locator("visible=true").first, "fichiers choisis"),
                                    (s.bouton("Upload and Index"), "Upload and Index")])
    t0 = time.time()
    s.bouton("Upload and Index").click(); p.wait_for_timeout(3000)
    s.attendre_fin(); p.get_by_text("Upload Progress").locator("visible=true").first.wait_for()
    s.note(f"ajout de {len(AUTRES)} fichiers : {time.time() - t0:.1f} s ; toasts {s.toasts()!r}")
    s.sans_toasts()
    s.cap("02-resultat-plusieurs", [(p.locator("textarea").locator("visible=true").first, "Upload result"),
                                    (p.locator("textarea").locator("visible=true").nth(1), "Upload info")])
    s.bouton("Clear Upload Info and Close").click(); p.wait_for_timeout(1500)


def liens(s):
    p = s.page
    ouvrir_files(s); s.onglet("Use Web Links")
    s.cap("03-liens-web", [(s.tab("Use Web Links"), "Use Web Links"), (p.locator("textarea").locator("visible=true").first, "Input web URLs"),
                           (s.bouton("Upload and Index"), "Upload and Index")])


def fiche(s):
    p = s.page
    ouvrir_files(s)
    s.cap("04-liste-complete", [(s.tab("Files", parent=p.locator("#indices-tab")) if False else s.ligne("contrat-batterix-scan.pdf"), "contrat-batterix-scan.pdf"),
                                (s.champ("Filter by name:"), "Filter by name:")])
    s.ligne("strategie-2026.pptx").click(); p.wait_for_timeout(3000)
    s.cap_souple("05-fiche-fichier", [(s.texte("Selected file:"), "Selected file"), (s.bouton("Go to Chat"), "Go to Chat"),
                                      (s.bouton("Download"), "Download"), (s.bouton("Delete"), "Delete"), (s.bouton("Close"), "Close"),
                                      (s.champ("Chunk type"), "Chunk type")])
    s.note("fiche : " + p.locator("body").inner_text()[:1500].replace("\n", " | "))


def groupes(s):
    p = s.page
    ouvrir_files(s); s.onglet("Groups")
    s.bouton("Add").click(); p.wait_for_timeout(1500)
    s.champ("Group name").fill("Fournisseur Batterix")
    liste = s.champ("Attached files")
    for f in ("contrat-batterix-scan.pdf", "supplier-audit-batterix-en.pdf"):
        liste.click(); p.wait_for_timeout(500)
        p.get_by_role("option", name=f, exact=True).locator("visible=true").first.click(); p.wait_for_timeout(500)
    p.keyboard.press("Escape")
    s.cap_souple("06-groupe-creer", [(s.tab("Groups"), "Groups"), (s.champ("Group name"), "Group name"),
                                     (s.bloc("Attached files"), "Attached files"), (s.bouton("Save"), "Save")])
    s.bouton("Save").click(); p.wait_for_timeout(2500)
    s.note("groupe : toasts " + repr(s.toasts())); s.sans_toasts()
    s.cap_souple("07-groupes-liste", [(s.ligne("Fournisseur Batterix"), "Fournisseur Batterix"), (s.bouton("Add"), "Add")])


def avance(s):
    p = s.page
    ouvrir_files(s)
    s.texte("Advance options", exact=True).click(); p.wait_for_timeout(1000)
    s.bouton("Delete all files").click(); p.wait_for_timeout(1000)
    s.cap_souple("08-options-avancees", [(s.texte("Advance options", exact=True), "Advance options"),
                                         (s.bouton("Download all files"), "Download all files"),
                                         (s.bouton("Confirm delete"), "Confirm delete"), (s.bouton("Cancel"), "Cancel")])
    # suppression réelle : la collection est ensuite remplie à nouveau par l'interface (étape « plusieurs »)
    s.bouton("Confirm delete").click(); p.wait_for_timeout(4000)
    s.note("tout supprimer : toasts " + repr(s.toasts())); s.sans_toasts()
    s.onglet("Upload Files")
    s.texte("Advanced indexing options", exact=True).click(); p.wait_for_timeout(800)
    s.cap_souple("09-forcer-reindexation", [(s.texte("Advanced indexing options", exact=True), "Advanced indexing options"),
                                            (p.locator("label").filter(has_text="Force reindex file").locator("visible=true").first, "Force reindex file")])


def rapide(s):
    """Ajout rapide depuis le chat : une copie renommée du message CSE (pour ne pas doublonner le corpus)."""
    p = s.page
    copie = RACINE / "donnees/essais/note-rapide-cse.md"
    copie.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(DOCS / "cse-2025-10-14.md", copie)
    s.onglet("Chat")
    with p.expect_file_chooser() as fc:
        p.locator("#quick-file").get_by_text("Cliquer pour Télécharger").click()
    fc.value.set_files(str(copie))
    p.wait_for_timeout(2000)
    s.cap_souple("10-ajout-rapide", [(p.locator("#quick-file"), "Quick Upload"), (p.locator("#chat-area"), "zone de discussion")])
    s.attendre_reponse(delai=180, stable=2)
    s.note("ajout rapide : " + p.locator("#main-chat-bot").inner_text()[:400].replace("\n", " | "))
    s.cap_souple("11-ajout-rapide-fini", [(p.locator("#main-chat-bot .message").last, "message de fin"),
                                          (p.locator("#index-0"), "File Collection")])


def lecteur(s):
    p = s.page
    s.onglet("Settings"); s.onglet("Retrieval settings")
    s.choisir("File loader", "Docling (figure+table extraction)")
    s.cap("12-lecteur-docling", [(s.tab("Retrieval settings"), "Retrieval settings"), (s.champ("File loader"), "File loader"),
                                 (p.locator("#save-setting-btn"), "Save & Close")])


if __name__ == "__main__":
    s = Scenario(CH)
    try:
        etapes([avance, plusieurs, liens, fiche, groupes, rapide, lecteur], s)
    finally:
        s.fermer()
