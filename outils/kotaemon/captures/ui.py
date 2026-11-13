"""Socle des scénarios de captures de Kotaemon (exécutés dans le conteneur Playwright, outils/communs/captures/lancer.sh).

- navigateur 1440 × 900 ; interface Gradio en anglais seulement (aucune traduction dans Kotaemon 0.12.0) ;
- connexion avec les identifiants fictifs de donnees/IDENTIFIANTS-LOCAUX.txt (clé kotaemon.admin.*), sinon admin/admin
  (compte créé d'office au premier démarrage, à changer : chapitre 03) ;
- Scenario.cap(...) : capture annotée (annoter.capture) dans docs/kotaemon/img/<chapitre>/<nom>.png, texte de la page dans
  outils/resultats/kotaemon/captures/<chapitre>/<nom>.txt, libellés des pastilles dans .../<chapitre>/scenario.json ;
- les secrets (clé du service central, mots de passe) sont masqués avant capture.
"""
import json, os, re, sys, time
from pathlib import Path

from playwright.sync_api import sync_playwright, expect  # noqa: F401
import annoter

CLE = os.environ.get("LLM_CENTRAL_KEY", "")
CLE_RE = re.compile((re.escape(CLE) + "|" if len(CLE) > 6 else "") + r"sk-[A-Za-z0-9_-]{8,}")
RACINE = Path("/depot") if Path("/depot").exists() else Path(__file__).resolve().parents[3]
BASE = os.environ.get("KOTAEMON_URL", "http://rag-kotaemon:7860")
IMG = RACINE / "docs/kotaemon/img"
TXT = RACINE / "outils/resultats/kotaemon/captures"
IDENT = RACINE / "donnees/IDENTIFIANTS-LOCAUX.txt"
URL_CENTRAL = "http://llm-central:8080/v1"


def identifiants():
    d = {}
    if IDENT.exists():
        for l in IDENT.read_text().splitlines():
            if "=" in l and l.startswith("kotaemon."):
                k, v = l.split("=", 1); d[k.strip()] = v.strip()
    return d


class Scenario:
    def __init__(self, chapitre, connecter=True, utilisateur=None, mot_de_passe=None):
        self.chapitre = chapitre
        self.journal = []
        self._pw = sync_playwright().start()
        self.navigateur = self._pw.chromium.launch()
        self.contexte = self.navigateur.new_context(viewport={"width": 1440, "height": 900}, locale="fr-FR",
                                                    accept_downloads=True)
        self.page = self.contexte.new_page()
        self.page.set_default_timeout(30000)
        self.page.goto(BASE + "/", wait_until="domcontentloaded")
        self.page.locator(".gradio-container").first.wait_for(state="visible", timeout=60000)
        self.page.wait_for_timeout(3000)
        if connecter:
            self.connecter(utilisateur, mot_de_passe)

    # ---------- navigation ----------
    def connecter(self, utilisateur=None, mot_de_passe=None):
        d = identifiants()
        u = utilisateur or d.get("kotaemon.admin.utilisateur", "admin")
        m = mot_de_passe or d.get("kotaemon.admin.mot_de_passe", "admin")
        p = self.page
        champ = p.get_by_label("Username").first
        try:
            champ.wait_for(state="visible", timeout=8000)
        except Exception:
            return  # session déjà ouverte
        champ.fill(u)
        p.get_by_label("Password").first.fill(m)
        p.get_by_role("button", name="Login").click()
        p.locator("#main-chat-bot").wait_for(state="visible", timeout=30000)
        p.wait_for_timeout(1500)

    def onglet(self, nom, parent=None):
        """Clique un onglet (role tab) visible portant ce nom."""
        zone = parent if parent is not None else self.page
        t = zone.get_by_role("tab", name=nom, exact=True).locator("visible=true").first
        t.click(); self.page.wait_for_timeout(1200)
        return t

    def tab(self, nom, parent=None):
        zone = parent if parent is not None else self.page
        return zone.get_by_role("tab", name=nom, exact=True).locator("visible=true").first

    def bouton(self, nom, exact=True, parent=None):
        zone = parent if parent is not None else self.page
        return zone.get_by_role("button", name=nom, exact=exact).locator("visible=true").first

    def texte(self, t, exact=False, parent=None):
        zone = parent if parent is not None else self.page
        return zone.get_by_text(t, exact=exact).locator("visible=true").first

    def champ(self, libelle, parent=None):
        """Champ Gradio repéré par son libellé (span du label)."""
        zone = parent if parent is not None else self.page
        loc = zone.get_by_label(libelle, exact=True).locator("visible=true")
        if loc.count():
            return loc.first
        # libellé Gradio suivi d'un texte d'aide : le champ est dans le même bloc que le titre
        return zone.locator("div.block").filter(has=zone.locator(f'span[data-testid="block-info"]:text-is("{libelle}")')) \
            .locator("textarea, input").locator("visible=true").first

    def bloc(self, libelle, parent=None):
        """Bloc Gradio entier (label + champ) d'un libellé : pour encadrer le composant complet."""
        zone = parent if parent is not None else self.page
        return zone.locator("div.block").filter(has=zone.get_by_text(libelle, exact=True)).locator("visible=true").last

    def ligne(self, texte):
        """Cellule d'un tableau Gradio (Dataframe) : le composant dessine un tableau de mesure caché puis le vrai
        tableau (classe « table ») ; on vise la cellule du vrai tableau."""
        return self.page.locator("table.table td").filter(has_text=texte).locator("visible=true").first

    def attendre_fin(self, delai=600000):
        """Attend la fin d'un traitement Gradio (plus d'indicateur de progression ni d'élément « generating »)."""
        p = self.page
        p.wait_for_timeout(1500)
        p.wait_for_function("""() => !document.querySelector('.generating, .progress-text, .eta-bar, .meta-text-center')""",
                            timeout=delai, polling=1000)
        p.wait_for_timeout(1500)

    def attendre_reponse(self, delai=600, stable=4, apres=None, question=None):
        """Attend que la dernière réponse du chat soit écrite : texte différent de « Thinking ... » et inchangé pendant
        `stable` relevés de 2 s. Renvoie le texte (None si délai dépassé)."""
        p, avant, n = self.page, None, 0
        for _ in range(delai // 2):
            p.wait_for_timeout(2000)
            n_msg, t = p.evaluate("() => { const m = [...document.querySelectorAll('#main-chat-bot .message')]; return [m.length, (m.pop() || {innerText: ''}).innerText]; }")
            if (apres is not None and n_msg < apres + 1) or (question and t.strip().startswith(question.strip()[:40])):
                avant, n = t, 0
                continue
            if t and t.strip() not in ("Thinking ...", "") and t == avant:
                n += 1
                if n >= stable:
                    return t
            else:
                n = 0
            avant = t
        self.note(f"réponse non terminée après {delai} s : {str(avant)[:200]!r}")
        return None

    def nouvelle_conversation(self):
        """Bouton « nouvelle conversation » ; recliqué tant que la zone de discussion n'est pas vide (un clic pendant la
        fin d'une réponse est ignoré)."""
        p = self.page
        for _ in range(10):
            p.locator("#new-conv-button").click(); p.wait_for_timeout(2500)
            if p.locator("#main-chat-bot .message").count() == 0:
                return
        self.note("nouvelle conversation : la zone de discussion n'a pas été vidée")

    def reglage_session(self, quoi, valeur):
        """Chat settings (accordéon sous la zone de saisie) : quoi = « Reasoning method », « Model » ou « Language »."""
        p = self.page
        acc = p.locator("#chat-settings-expand")
        if not acc.get_by_text("Reasoning method", exact=True).is_visible():
            acc.get_by_text("Chat settings", exact=True).click(); p.wait_for_timeout(1000)
        listes = acc.locator("input[aria-label=Dropdown]").locator("visible=true")
        rang = {"Reasoning method": 1, "Model": 2, "Language": 3}[quoi]
        champ = listes.nth(rang)
        champ.click(); p.wait_for_timeout(500)
        p.get_by_role("option", name=valeur, exact=True).locator("visible=true").first.click()
        p.wait_for_timeout(1000)
        return champ

    def poser(self, question, envoyer=True, stable=4):
        """Écrit la question dans la zone de saisie du chat et l'envoie (Entrée)."""
        p = self.page
        zone = p.locator("#chat-input textarea")
        zone.fill(question)
        if envoyer:
            n0 = p.locator("#main-chat-bot .message").count()
            zone.press("Enter")
            self.attendre_reponse(stable=stable, apres=n0, question=question)
        return zone

    def zone_depot(self):
        """Zone de dépôt de fichiers Gradio visible (texte « Cliquer pour Télécharger » en locale française)."""
        return self.page.locator("button.center, div.wrap").filter(has_text="Cliquer pour Télécharger").locator("visible=true").last

    def deposer(self, fichiers):
        """Choisit des fichiers par la fenêtre de sélection ouverte en cliquant la zone de dépôt visible."""
        with self.page.expect_file_chooser() as fc:
            self.zone_depot().click()
        fc.value.set_files([str(f) for f in fichiers])
        self.page.wait_for_timeout(2500)

    def toasts(self):
        try:
            return [t.inner_text() for t in self.page.locator(".toast-body").all()]
        except Exception:
            return []

    def sans_toasts(self):
        self.page.evaluate("() => document.querySelectorAll('.toast-wrap .toast-body').forEach(t => t.remove())")

    # ---------- captures ----------
    def cap(self, nom, elements=(), masques=(), plein=False, clip=None, attendre=None, note="", auto=True):
        if attendre is not None:
            attendre.wait_for(state="visible")
        self.page.wait_for_timeout(500)
        img = IMG / self.chapitre / f"{nom}.png"
        txt = TXT / self.chapitre / f"{nom}.txt"
        masques = list(masques) + (self._secrets_visibles() if auto else [])
        n = self._voiler_cle()
        try:
            libs = annoter.capture(self.page, img, elements, masques=masques, plein=plein, clip=clip, texte=txt)
        finally:
            if n:
                self._devoiler_cle()
        txt.write_text(CLE_RE.sub("[clé masquée]", txt.read_text()))
        self.journal.append({"capture": f"{self.chapitre}/{nom}.png", "pastilles": libs, "note": note,
                             "heure": time.strftime("%H:%M:%S")})
        self._ecrire_journal()
        return libs

    def cap_souple(self, nom, elements=(), **kw):
        """Comme cap, mais ignore (et note) les éléments introuvables ou invisibles."""
        garde = []
        for loc, lib in elements:
            try:
                loc.wait_for(state="visible", timeout=5000); garde.append((loc, lib))
            except Exception:
                self.note(f"{nom} : élément absent « {lib} »")
        return self.cap(nom, garde, **kw)

    def _secrets_visibles(self):
        res = []
        for loc in self.page.locator("input[type=password]").all():
            try:
                if loc.is_visible() and loc.input_value():
                    res.append(loc)
            except Exception:
                pass
        if len(CLE) > 6:
            # clé dans un éditeur YAML (textarea ou code) : on masque la ligne qui la contient
            for loc in self.page.locator(f"textarea, .cm-line, td, span").filter(has_text=CLE).all():
                try:
                    if loc.is_visible():
                        res.append(loc)
                except Exception:
                    pass
        return res

    def _voiler_cle(self):
        """Remplace, dans l'affichage seulement, la clé du service central par des astérisques dans les zones de texte
        (spécifications YAML) : la valeur réelle reste dans l'état de Gradio et est remise juste après la capture."""
        if len(CLE) < 7:
            return 0
        return self.page.evaluate("""(cle) => { let n = 0;
          document.querySelectorAll('textarea, input[type=text]').forEach(t => { if (t.value.includes(cle)) {
            t.dataset.vraie = t.value; t.value = t.value.split(cle).join('********'); n++; } }); return n; }""", CLE)

    def _devoiler_cle(self):
        self.page.evaluate("""() => document.querySelectorAll('[data-vraie]').forEach(t => {
          t.value = t.dataset.vraie; delete t.dataset.vraie; })""")

    def choisir(self, libelle, valeur, parent=None):
        """Liste déroulante Gradio : ouvre la liste du bloc `libelle` et clique l'option `valeur`."""
        champ = self.champ(libelle, parent)
        champ.click(); self.page.wait_for_timeout(300)
        self.page.wait_for_timeout(500)
        opt = self.page.get_by_role("option", name=valeur, exact=True).locator("visible=true")
        if not opt.count():
            print("options visibles :", self.page.evaluate("() => [...document.querySelectorAll('[role=option]')].filter(e=>e.offsetParent).map(e=>JSON.stringify(e.innerText))"))
        opt.first.click()
        self.page.wait_for_timeout(800)
        return champ

    def _ecrire_journal(self):
        f = TXT / self.chapitre / "scenario.json"
        f.parent.mkdir(parents=True, exist_ok=True)
        anciens = json.loads(f.read_text()) if f.exists() else []
        noms = {j["capture"] for j in self.journal}
        anciens = [a for a in anciens if a["capture"] not in noms]
        f.write_text(json.dumps(anciens + self.journal, ensure_ascii=False, indent=1))

    def note(self, texte):
        texte = CLE_RE.sub("[clé masquée]", texte)
        print("NOTE", texte, flush=True)
        f = TXT / self.chapitre / "notes.log"
        f.parent.mkdir(parents=True, exist_ok=True)
        with f.open("a") as h:
            h.write(time.strftime("%Y-%m-%d %H:%M:%S ") + texte + "\n")

    def fermer(self):
        try:
            self.navigateur.close()
        finally:
            self._pw.stop()


def etapes(fonctions, scenario):
    noms = sys.argv[1:] or [f.__name__ for f in fonctions]
    for f in fonctions:
        if f.__name__ in noms:
            print("==", f.__name__, flush=True)
            f(scenario)
