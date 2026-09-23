# -*- coding: utf-8 -*-
"""Monta o site final (pasta estatica pronta para deploy na Vercel) a partir
de scripts/site_src/*, injetando os dados (JSON) + SVGs + fotos licenciadas."""
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))
import pathdata as pd
import accents

accents.patch_pathdata(pd)

HERE = os.path.dirname(__file__)
SRC_DIR = os.path.join(HERE, "site_src")
OUT_DIR = os.path.join(HERE, "..", "site")

CREDITS_PATH = os.path.join(SRC_DIR, "credits.json")
CREDITS = {}
if os.path.exists(CREDITS_PATH):
    with open(CREDITS_PATH, "r", encoding="utf-8") as f:
        CREDITS = json.load(f)


def disease_payload(d):
    shapes, vb = pd.build_diagram_shapes(d["diagram"])
    svg = pd.shapes_to_svg(shapes, vb, css_class="dg")
    out = {
        "id": d["id"],
        "nome": d["nome"],
        "categoria": d["categoria"],
        "resumo": d["resumo"],
        "svg": svg,
        "clinico": d["clinico"],
        "localizacao": d["localizacao"],
        "etiologia": d["etiologia"],
        "sintomas": d["sintomas"],
        "testes": d["testes"],
        "radiografico": d["radiografico"],
        "tratamento": d["tratamento"],
        "diferenciar": d["diferenciar"],
        "aparenciaCurta": d["aparencia_curta"],
        "causaCurta": d["causa_curta"],
        "tratamentoCurto": d["tratamento_curto"],
        "dor": d.get("dor", ""),
        "mobilidade": d.get("mobilidade", ""),
        "percussao": d.get("percussao", ""),
        "necrose": d.get("necrose", ""),
        "vitalidade": d.get("vitalidade", ""),
        "radiografiaCurta": d.get("radiografia_curta", ""),
    }
    if d["id"] in CREDITS:
        out["foto"] = CREDITS[d["id"]]
    return out


def quiz_payload(q):
    out = {
        "id": q["id"],
        "kind": q["kind"],
        "prompt": q["prompt"],
        "options": q["options"],
        "correct": q["correct_label"],
        "explain": q["explain"],
    }
    if q["kind"] == "image":
        d = pd.DISEASE_BY_ID[q["disease"]]
        shapes, vb = pd.build_diagram_shapes(d["diagram"])
        out["svg"] = pd.shapes_to_svg(shapes, vb, css_class="dg qimg")
        out["categoria"] = d["categoria"]
        if d["id"] in CREDITS:
            out["foto"] = CREDITS[d["id"]]
    elif "categoria" in q:
        out["categoria"] = q["categoria"]
    else:
        for d in pd.DISEASES:
            if d["nome"] == q["correct_label"]:
                out["categoria"] = d["categoria"]
                break
        else:
            out["categoria"] = "geral"
    return out


def build():
    payload = {
        "categories": [{"id": cid, "label": label} for cid, label in pd.CATEGORIES],
        "diseases": [disease_payload(d) for d in pd.DISEASES],
        "quiz": [quiz_payload(q) for q in pd.QUIZ],
    }
    data_js = "window.APP_DATA = " + json.dumps(payload, ensure_ascii=False) + ";\n"

    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR)

    for fname in ("index.html", "styles.css", "app.js"):
        shutil.copyfile(os.path.join(SRC_DIR, fname), os.path.join(OUT_DIR, fname))

    with open(os.path.join(OUT_DIR, "data.js"), "w", encoding="utf-8") as f:
        f.write(data_js)

    src_images = os.path.join(SRC_DIR, "images")
    if os.path.isdir(src_images):
        dst_images = os.path.join(OUT_DIR, "images")
        shutil.copytree(src_images, dst_images)
        n_img = len([f for f in os.listdir(dst_images) if not f.startswith("_raw_")])
    else:
        n_img = 0

    # arquivos de deploy / documentacao
    shutil.copyfile(os.path.join(HERE, "vercel.json"), os.path.join(OUT_DIR, "vercel.json"))
    shutil.copyfile(os.path.join(HERE, "SITE_README.md"), os.path.join(OUT_DIR, "README.md"))

    # PDFs para download direto pelo site (gerados por build_pdf.py / build_comparison_pdf.py)
    PROJECT_ROOT = os.path.join(HERE, "..")
    for pdf_name in ("Guia_Revisao_Doencas_Polpa_Periapice.pdf", "Planilha_Comparativa_Patologias.pdf"):
        src_pdf = os.path.join(PROJECT_ROOT, pdf_name)
        if os.path.exists(src_pdf):
            shutil.copyfile(src_pdf, os.path.join(OUT_DIR, pdf_name))
        else:
            print(f"AVISO: {pdf_name} nao encontrado - rode build_pdf.py / build_comparison_pdf.py antes.")

    total = sum(os.path.getsize(os.path.join(root, f))
                for root, _, files in os.walk(OUT_DIR) for f in files)
    print("Site gerado em:", os.path.abspath(OUT_DIR))
    print("Fotos reais incluidas:", n_img, "/", len(pd.DISEASES))
    print("Tamanho total:", round(total / 1024, 1), "KB")


if __name__ == "__main__":
    build()
