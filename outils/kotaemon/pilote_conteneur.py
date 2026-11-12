"""Pilote du banc exécuté DANS le conteneur rag-kotaemon (/app/.venv/bin/python, dossier /app).

Il charge l'application Kotaemon sans interface (ktem.app.BaseApp), lit les réglages enregistrés par l'utilisateur dans
l'interface (table Settings, compte « admin »), puis sert des commandes JSON, une par ligne sur l'entrée standard :
  {"cmd": "indexer", "fichiers": ["/app/ktem_app_data/banc/corpus/x.pdf", ...], "collection": 1}
  {"cmd": "demander", "question": "...", "reglages": {"index.options.1.use_reranking": false, ...}, "collection": 1}
  {"cmd": "reglages"}
Chaque réponse est une ligne JSON préfixée par « >>> » sur la sortie standard (le reste de la sortie est le journal de
Kotaemon). Les réglages passés dans « reglages » remplacent ceux de l'interface pour une question seulement.
Recherche : tous les fichiers de la collection appartenant à l'utilisateur (équivalent de « Search All »).
"""
import json, os, re, sys, time, traceback
os.chdir("/app"); sys.path.insert(0, "/app")
from pathlib import Path
from sqlmodel import Session, select

from ktem.app import BaseApp
from ktem.db.models import User, Settings, engine
from ktem.components import reasonings

UTILISATEUR = os.environ.get("KH_BANC_UTILISATEUR", "admin")
app = BaseApp()
with Session(engine) as s:
    UID = s.exec(select(User).where(User.username == UTILISATEUR)).one().id
    ligne = s.exec(select(Settings).where(Settings.user == UID)).first()
BASE_REGLAGES = app.default_settings.flatten()
if ligne:
    BASE_REGLAGES.update(ligne.setting)


def sortie(obj):
    print(">>> " + json.dumps(obj, ensure_ascii=False), flush=True)


def index(n):
    return next(i for i in app.index_manager.indices if i.id == n)


def fichiers_utilisateur(idx):
    Source = idx._resources["Source"]
    with Session(engine) as s:
        q = select(Source.id, Source.name)
        if idx.config.get("private", False):
            q = q.where(Source.user == UID)
        return s.execute(q).all()


def nb_passages(idx, source_id):
    Index = idx._resources["Index"]
    with Session(engine) as s:
        return len(s.execute(select(Index.id).where(Index.source_id == source_id)).all())


def indexer(fichiers, collection=1, reglages=None, forcer=False):
    """forcer : réindexe même un fichier déjà présent (« Force reindex file »). Un fichier présent sans aucun passage
    (échec d'une lecture précédente : Kotaemon l'inscrit quand même) est réindexé d'office."""
    idx = index(collection)
    reg = {**BASE_REGLAGES, **(reglages or {})}
    deja = {n: i for i, n in fichiers_utilisateur(idx)}
    detail = []
    for f in fichiers:
        nom = Path(f).name
        vide = nom in deja and nb_passages(idx, deja[nom]) == 0
        if nom in deja and not forcer and not vide:
            detail.append({"fichier": nom, "statut": "déjà indexé"}); continue
        t0 = time.time()
        pipe = idx.get_indexing_pipeline(reg, UID)
        g = pipe.stream([Path(f)], reindex=forcer or vide)
        msgs = []
        try:
            while True:
                d = next(g)
                if getattr(d, "text", None):
                    msgs.append(str(d.text)[:200])
        except StopIteration as e:
            ids, erreurs, _ = e.value
        detail.append({"fichier": nom, "duree_s": round(time.time() - t0, 1), "ids": [i for i in ids if i],
                       "erreurs": [str(x)[:300] for x in erreurs if x], "journal": msgs[-3:]})
        print("indexé", detail[-1], flush=True)
    return {"collection": idx.name, "detail": detail}


ENTETE = re.compile(r"(?:\[Page (\d+)\]\s*)?([\w.\-]+\.(?:pdf|docx|pptx|xlsx|html|md|txt|csv|png|jpg))", re.I)


def demander(question, collection=1, reglages=None):
    idx = index(collection)
    reg = {**BASE_REGLAGES, **(reglages or {})}
    prefixe = f"index.options.{idx.id}."
    us = {k[len(prefixe):]: v for k, v in reg.items() if k.startswith(prefixe)}
    ids = [i for i, _ in fichiers_utilisateur(idx)]
    retrievers = []
    for cls in idx._retriever_pipeline_cls:
        r = cls.get_pipeline(us, idx.config, ids)
        if r is None:
            continue
        r.Source, r.Index = idx._resources["Source"], idx._resources["Index"]
        r.VS, r.DS, r.FSPath, r.user_id = idx._vs, idx._docstore, idx._fs_path, UID
        retrievers.append(r)
    mode = reg.get("reasoning.use", "simple")
    cls_r = reasonings[mode]
    qa = cls_r.get_pipeline(reg, {"app": {"regen": False}, "pipeline": {}}, retrievers)
    chat, infos = "", []
    t0 = time.time()
    for d in qa.stream(question, conv_id="", history=[]):
        if d.channel == "chat":
            chat = "" if d.content is None else chat + d.content
        elif d.channel == "info" and d.content:
            infos.append(str(d.content))
    html = "\n".join(infos)
    texte_info = re.sub(r"<[^>]+>", " ", html)
    cits = []
    for m in re.finditer(r"<summary[^>]*>(.*?)</summary>", html, re.S):
        t = re.sub(r"<[^>]+>", " ", m.group(1))
        e = ENTETE.search(t)
        if e:
            score = re.search(r"score:\s*([\d.]+)", t)
            cits.append({"document": e.group(2), "page": int(e.group(1)) if e.group(1) else None,
                         "extrait": "", "score": float(score.group(1)) if score else None})
    return {"reponse": chat, "citations": cits, "duree_s": round(time.time() - t0, 2),
            "alerte_pertinence": "Context relevance score is low" in texte_info,
            "infos_debut": texte_info[:400]}


sortie({"pret": True, "utilisateur": UTILISATEUR, "collections": [(i.id, i.name) for i in app.index_manager.indices]})
for l in sys.stdin:
    try:
        c = json.loads(l)
        if c["cmd"] == "indexer":
            sortie(indexer(c["fichiers"], c.get("collection", 1), c.get("reglages"), c.get("forcer", False)))
        elif c["cmd"] == "demander":
            sortie(demander(c["question"], c.get("collection", 1), c.get("reglages")))
        elif c["cmd"] == "reglages":
            sortie({k: v for k, v in BASE_REGLAGES.items() if not k.endswith("prompt")})
    except Exception as e:
        sortie({"erreur": repr(e)[:800], "trace": traceback.format_exc()[-1500:]})
