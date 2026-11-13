"""Lecteur de PDF pour Kotaemon qui confie la lecture à un serveur Docling séparé (docling-serve).

Monté dans le conteneur en /app/lecteur_docling_serve.py et déclaré dans flowsettings.py :
    FILE_INDEX_PIPELINE_FILE_EXTRACTORS = {".pdf": "lecteur_docling_serve.LecteurDoclingServe"}
Adresse du serveur : variable DOCLING_SERVE_URL (défaut http://rag-docling-serve:5001).
Le résultat suit la forme du lecteur Docling intégré (kotaemon/loaders/docling_loader.py) : un Document par page
(metadata page_label, file_name), plus un Document par tableau (Markdown) ; les figures ne sont pas extraites.
"""

import os
from collections import defaultdict
from pathlib import Path

import requests
from kotaemon.base import Document
from kotaemon.loaders.base import BaseReader
from kotaemon.loaders.utils.adobe import make_markdown_table


class LecteurDoclingServe(BaseReader):
    def run(self, file_path, extra_info=None, **kwargs):
        return self.load_data(file_path, extra_info, **kwargs)

    def load_data(self, file_path, extra_info=None, **kwargs):
        url = os.environ.get("DOCLING_SERVE_URL", "http://rag-docling-serve:5001").rstrip("/")
        file_path = Path(file_path)
        metadata = extra_info or {}
        with open(file_path, "rb") as f:
            rep = requests.post(
                f"{url}/v1/convert/file",
                files={"files": (file_path.name, f, "application/pdf")},
                data={"to_formats": "json", "do_ocr": "true", "image_export_mode": "placeholder"},
                timeout=600,
            )
        rep.raise_for_status()
        doc = rep.json()["document"]["json_content"]

        base = {"file_name": file_path.name, "file_path": str(file_path)}
        pages = defaultdict(list)
        for t in doc.get("texts", []):
            page = t["prov"][0].get("page_no", 1) if t.get("prov") else 1
            pages[page].append(t["text"])
        textes = [
            Document(text="\n".join(txts), metadata={"page_label": p, **base, **metadata})
            for p, txts in sorted(pages.items())
        ]
        tableaux = []
        for tab in doc.get("tables", []):
            grille = [[c["text"] for c in ligne] for ligne in tab["data"]["grid"]]
            md = make_markdown_table(grille)
            page = tab["prov"][0].get("page_no", 1) if tab.get("prov") else 1
            tableaux.append(
                Document(
                    text=md,
                    metadata={"type": "table", "page_label": page, "table_origin": md, **base, **metadata},
                )
            )
        return textes + tableaux
