#!/usr/bin/env python3
"""Adaptateur du banc commun pour Kotaemon (pas d'API REST : bibliothèque Python dans le conteneur).

Le pilote outils/kotaemon/pilote_conteneur.py est copié dans le volume de données et lancé par
`docker exec -i rag-kotaemon /app/.venv/bin/python …` : il charge Kotaemon sans interface, lit les réglages enregistrés
dans l'interface par le compte admin (Settings) et répond aux commandes « indexer » et « demander ».
Indexation : chaque fichier du corpus dans « File Collection » (lecteur et découpage réglés dans l'interface, embedding
par défaut de Resources). Questions : tous les fichiers de la collection (« Search All »), une question sans historique,
langue et modèle des réglages de l'interface. Seuls les réglages passés en option changent d'un banc à l'autre.

Usage : outils/kotaemon/banc.py --etiquette defaut-sans-rerank --sans-rerank [--top-k 10] [--mode hybrid]
        [--score-llm] [--raisonnement simple] [--citation highlight] [--limite N] [--ids Q01,Q02] [--sans-juge]
"""
import argparse, json, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "communs/banc"))
import commun  # noqa: E402

APP = ["rag-kotaemon"]
MODELES = ["llm-central", "llm-swap", "llm-speaches"]
DANS = "/app/ktem_app_data/banc"


class Adaptateur:
    nom = "Kotaemon"

    def __init__(self, a):
        self.a = a
        r = {"index.options.1.use_reranking": not a.sans_rerank, "index.options.1.use_llm_reranking": a.score_llm,
             "reasoning.use": a.raisonnement}
        if a.top_k:
            r["index.options.1.num_retrieval"] = a.top_k
        if a.mode:
            r["index.options.1.retrieval_mode"] = a.mode
        if a.citation:
            r[f"reasoning.options.{a.raisonnement}.highlight_citation"] = a.citation
        self.reglages = r
        subprocess.run(["docker", "exec", "rag-kotaemon", "mkdir", "-p", DANS + "/corpus"], check=True)
        subprocess.run(["docker", "cp", f"{commun.DOCUMENTS}/.", f"rag-kotaemon:{DANS}/corpus/"], check=True)
        subprocess.run(["docker", "cp", str(Path(__file__).with_name("pilote_conteneur.py")), f"rag-kotaemon:{DANS}/"], check=True)
        self.p = subprocess.Popen(["docker", "exec", "-i", "rag-kotaemon", "/app/.venv/bin/python", "-u", f"{DANS}/pilote_conteneur.py"],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        self.pret = self._lire()
        self.base = self._commande({"cmd": "reglages"})

    def _lire(self):
        for l in self.p.stdout:
            if l.startswith(">>> "):
                return json.loads(l[4:])
        raise RuntimeError("pilote arrêté")

    def _commande(self, c):
        self.p.stdin.write(json.dumps(c, ensure_ascii=False) + "\n"); self.p.stdin.flush()
        r = self._lire()
        if "erreur" in r and set(r) <= {"erreur", "trace"}:
            raise RuntimeError(r["erreur"] + "\n" + r.get("trace", ""))
        return r

    def indexer(self, fichiers):
        r = self._commande({"cmd": "indexer", "fichiers": [f"{DANS}/corpus/{f.name}" for f in fichiers]})
        for d in r["detail"]:
            print("  ", d, flush=True)
        return r

    def demander(self, question):
        r = self._commande({"cmd": "demander", "question": question, "reglages": self.reglages})
        return r

    def config(self):
        b = {k: v for k, v in self.base.items() if k.startswith(("index.options.1.", "reasoning.")) and "prompt" not in k
             and not k.startswith("reasoning.options.ReAct") and not k.startswith("reasoning.options.ReWOO")}
        return {"methode": "bibliothèque kotaemon dans le conteneur (pilote_conteneur.py), réglages de l'interface",
                "collection": "File Collection", "recherche": "Search All", "reglages_interface": b,
                "reglages_du_banc": self.reglages}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--etiquette", required=True)
    p.add_argument("--sans-rerank", action="store_true")
    p.add_argument("--score-llm", action="store_true")
    p.add_argument("--top-k", type=int)
    p.add_argument("--mode", choices=["vector", "text", "hybrid"])
    p.add_argument("--raisonnement", default="simple")
    p.add_argument("--citation", choices=["highlight", "inline", "off"])
    p.add_argument("--limite", type=int)
    p.add_argument("--ids")
    p.add_argument("--sans-juge", action="store_true")
    p.add_argument("--sans-index", action="store_true")
    a = p.parse_args()
    ad = Adaptateur(a)
    res = commun.lancer(ad, a.etiquette, APP, MODELES, indexer=not a.sans_index, juge=not a.sans_juge, limite=a.limite,
                        ids=a.ids.split(",") if a.ids else None)
    commun.ecrire(res, commun.RACINE / "outils/resultats/kotaemon")
    ad.p.stdin.close()


if __name__ == "__main__":
    main()
