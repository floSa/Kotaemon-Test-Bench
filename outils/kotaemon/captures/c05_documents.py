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
    champ = p.locator("label").filter(has_text="Attached files").locator("input").locator("visible=true").first
    champ.click(); p.wait_for_timeout(800)
    for f in ("contrat-batterix-scan.pdf", "supplier-audit-batterix-en.pdf"):
        o = p.get_by_role("option", name=f, exact=True).locator("visible=true")
        if not o.count():
            champ.click(); p.wait_for_timeout(800)
        o.first.click(); p.wait_for_timeout(800)
    p.locator("body").click(position={"x": 1300, "y": 850}); p.wait_for_timeout(600)
    s.cap_souple("06-groupe-creer", [(s.tab("Groups"), "Groups"), (s.champ("Group name"), "Group name"),
                                     (p.locator("label").filter(has_text="Attached files").locator("visible=true").first, "Attached files"), (s.bouton("Save"), "Save")])
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


def reparer_groupe(s):
    """Après « Force reindex file », le fichier relu reçoit un nouvel identifiant : le groupe garde l'ancien et perd le
    fichier. On rouvre le groupe, on remet le fichier et on enregistre."""
    p = s.page
    ouvrir_files(s); s.onglet("Groups")
    s.ligne("Fournisseur Batterix").click(); p.wait_for_timeout(2000)
    champ = p.locator("label").filter(has_text="Attached files").locator("input").locator("visible=true").first
    s.cap_souple("16-groupe-incomplet", [(s.ligne("Fournisseur Batterix"), "Fournisseur Batterix"),
                                         (p.locator("label").filter(has_text="Attached files").locator("visible=true").first, "Attached files")])
    champ.click(); p.wait_for_timeout(800)
    p.get_by_role("option", name="contrat-batterix-scan.pdf", exact=True).locator("visible=true").first.click(); p.wait_for_timeout(800)
    p.locator("body").click(position={"x": 1300, "y": 850}); p.wait_for_timeout(600)
    s.cap_souple("17-groupe-repare", [(p.locator("label").filter(has_text="Attached files").locator("visible=true").first, "Attached files"),
                                      (s.bouton("Save"), "Save")])
    s.bouton("Save").click(); p.wait_for_timeout(2500)
    s.note("réparation du groupe : toasts " + repr(s.toasts()))


def supprimer(s):
    """Supprime la note du CSE (aucune confirmation n'est demandée), puis la remet par « Upload and Index »."""
    p = s.page
    ouvrir_files(s)
    if not s.ligne("cse-2025-10-14.md").count():
        s.onglet("Upload Files"); s.deposer([DOCS / "cse-2025-10-14.md"])
        s.bouton("Upload and Index").click(); p.wait_for_timeout(3000); s.attendre_fin(); s.sans_toasts()
        s.bouton("Clear Upload Info and Close").click(); p.wait_for_timeout(1500)
    s.onglet("Files")
    s.ligne("cse-2025-10-14.md").click(); p.wait_for_timeout(2500)
    s.cap_souple("14-supprimer-fichier", [(s.texte("Selected file: cse-2025-10-14.md"), "Selected file"),
                                          (s.bouton("Delete"), "Delete")])
    s.bouton("Delete").click(); p.wait_for_timeout(2500)
    s.note("suppression sans confirmation : toasts " + repr(s.toasts())); s.sans_toasts()
    s.cap_souple("15-fichier-supprime", [(p.locator(".toast-body").first, "message"), (p.locator("table.table").locator("visible=true").first, "liste des fichiers")])
    s.onglet("Upload Files"); s.deposer([DOCS / "cse-2025-10-14.md"])
    s.bouton("Upload and Index").click(); p.wait_for_timeout(3000); s.attendre_fin()
    s.note("remise : toasts " + repr(s.toasts()))


def lecteur(s):
    """Lecteur Docling pour le PDF scanné : réglage, réindexation forcée du scan, retour au lecteur par défaut."""
    p = s.page
    s.onglet("Settings"); s.onglet("Retrieval settings")
    s.choisir("File loader", "Docling (figure+table extraction)")
    s.cap("12-lecteur-docling", [(s.tab("Retrieval settings"), "Retrieval settings"), (s.champ("File loader"), "File loader"),
                                 (p.locator("#save-setting-btn"), "Save & Close")])
    p.locator("#save-setting-btn").click(); p.wait_for_timeout(2500); s.sans_toasts()
    ouvrir_files(s); s.onglet("Upload Files")
    s.deposer([DOCS / "contrat-batterix-scan.pdf"])
    acc = s.texte("Advanced indexing options", exact=True)
    if not p.locator("label").filter(has_text="Force reindex file").locator("visible=true").count():
        acc.click(); p.wait_for_timeout(800)
    p.get_by_label("Force reindex file").locator("visible=true").first.check()
    t0 = time.time()
    s.bouton("Upload and Index").click(); p.wait_for_timeout(5000)
    s.attendre_fin(delai=900000); p.get_by_text("Upload Progress").locator("visible=true").first.wait_for()
    s.note(f"réindexation Docling du scan : {time.time() - t0:.1f} s ; toasts {s.toasts()!r}")
    s.sans_toasts()
    s.bouton("Clear Upload Info and Close").click(); p.wait_for_timeout(1500)
    s.ligne("contrat-batterix-scan.pdf").click(); p.wait_for_timeout(3000)
    s.cap_souple("13-scan-lu-par-docling", [(s.ligne("contrat-batterix-scan.pdf"), "contrat-batterix-scan.pdf (lecteur)"),
                                            (p.get_by_text("212 euros").locator("visible=true").first, "texte lu dans le scan")])
    s.onglet("Settings"); s.onglet("Retrieval settings")
    s.choisir("File loader", "Default (open-source)")
    p.locator("#save-setting-btn").click(); p.wait_for_timeout(2500)


if __name__ == "__main__":
    s = Scenario(CH)
    try:
        etapes([avance, plusieurs, liens, fiche, groupes, rapide, supprimer, lecteur, reparer_groupe], s)
    finally:
        s.fermer()
