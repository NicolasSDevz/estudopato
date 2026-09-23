# -*- coding: utf-8 -*-
"""Seleciona as melhores imagens reais extraidas do PDF da aula (slides da
Profa. Angela Maragno) para cada doenca, recomprime e grava credits.json.
Substitui as fotos do Wikimedia por fotos/radiografias das proprias aulas."""
import json
import os

from PIL import Image

HERE = os.path.dirname(__file__)
SRC_DIR = os.path.join(HERE, "extracted_slides")
OUT_DIR = os.path.join(HERE, "site_src", "images")
os.makedirs(OUT_DIR, exist_ok=True)

SOURCE = "Slides da aula — Doenças da Polpa e Periápice (Profa. Ângela Catarina Maragno, Patologia Bucal, UNESC)"

PICKS = {
    "pulpite_reversivel": ("p08_0_758x495.jpeg",
        "Teste de sensibilidade ao frio realizado em incisivo (slide de aula)."),
    "pulpite_irreversivel": ("p11_0_654x365.jpeg",
        "Paciente com dor pulpar aguda e espontânea (slide de aula)."),
    "pulpite_hiperplasica": ("p10_3_602x527.jpeg",
        "Pólipo pulpar em molar decíduo e radiografia correspondente (slide de aula)."),
    "calcificacoes_pulpares": ("p06_1_860x614.jpeg",
        "Radiografia com denticulo/calculo pulpar indicado pela seta (slide de aula)."),
    "periodontite_apical_aguda": ("p14_1_468x360.jpeg",
        "Radiografia periapical com aumento do espaço do ligamento periodontal (seta, slide de aula)."),
    "granuloma_periapical": ("p16_3_207x300.jpeg",
        "Radiografia periapical com radioluscência bem definida no ápice (slide de aula)."),
    "cisto_radicular": ("p18_1_243x207.jpeg",
        "Peça cirúrgica: área de lesão após ostectomia (Figura 4, slide de aula)."),
    "cisto_radicular_lateral": ("p20_1_256x192.jpeg",
        "Radiografia periapical (slide de aula, seção Cisto Radicular Lateral)."),
    "cisto_residual": ("p20_2_419x521.jpeg",
        "Radiografia de área radiolúcida em rebordo (slide de aula, seção Cisto Residual)."),
    "abscesso_periapical_agudo": ("p23_2_480x360.jpeg",
        "Tumefação vestibular aguda associada a abscesso periapical (slide de aula)."),
    "abscesso_periapical_cronico": ("p25_3_380x326.jpeg",
        "Rastreamento de fístula intraoral com cone de guta-percha (Figura 10, slide de aula)."),
    "celulite_facial": ("p28_1_554x420.jpeg",
        "Evolução de celulite facial de origem odontogênica (slide de aula)."),
    "trombose_seio_cavernoso": ("p28_4_252x185.jpeg",
        "Edema periorbitário em paciente com trombose de seio cavernoso (slide de aula)."),
    "angina_ludwig": ("p30_0_270x187.jpeg",
        "Tumefação volumosa do pescoço em Angina de Ludwig (slide de aula)."),
    "osteomielite_aguda": ("p34_0_567x301.jpeg",
        "Radiografia panorâmica com área de osteomielite aguda destacada (slide de aula)."),
    "osteomielite_cronica": ("p36_5_1014x734.jpeg",
        "Caso clínico de osteomielite crônica: face, intraoral e radiografia (slide de aula)."),
    "osteite_condensante": ("p39_1_255x198.jpeg",
        "Radiografia com área radiopaca compatível com osteíte condensante (slide de aula)."),
    "osteomielite_garre": ("p41_2_980x756.jpeg",
        "Tomografia (corte axial) mostrando laminação óssea em “casca de cebola” (slide de aula)."),
    "osteite_alveolar": ("p44_1_793x595.jpeg",
        "Alvéolo seco (osteíte alveolar) após exodontia (slide de aula)."),
}


def process():
    credits = {}
    for disease_id, (fname, caption) in PICKS.items():
        src = os.path.join(SRC_DIR, fname)
        im = Image.open(src).convert("RGB")
        w, h = im.size
        max_w = 1000
        if w > max_w:
            im = im.resize((max_w, int(h * max_w / w)), Image.LANCZOS)
        out_path = os.path.join(OUT_DIR, f"{disease_id}.jpg")
        im.save(out_path, "JPEG", quality=85, optimize=True)
        credits[disease_id] = {
            "file": f"images/{disease_id}.jpg",
            "license": "Uso educacional (material de aula)",
            "author": "Profa. Ângela Catarina Maragno",
            "source": SOURCE,
            "caption": caption,
        }
        print(f"{disease_id:28s} <- {fname}  ({im.size[0]}x{im.size[1]})")

    with open(os.path.join(HERE, "site_src", "credits.json"), "w", encoding="utf-8") as f:
        json.dump(credits, f, ensure_ascii=False, indent=2)
    print("\ntotal:", len(credits), "doencas com foto real")


if __name__ == "__main__":
    process()
