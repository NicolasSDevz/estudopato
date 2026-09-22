# -*- coding: utf-8 -*-
"""Baixa as fotos/radiografias com licenca livre (Wikimedia Commons) usadas
no site, redimensiona/recomprime e grava credits.json com a atribuicao."""
import json
import os
import urllib.request

from PIL import Image

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, "site_src", "images")
os.makedirs(OUT_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "PatologiaPolpaStudyTool/1.0 (educational student project; contact: n/a) Python-urllib"
}

IMAGES = [
    dict(id="necrose_pulpar",
         url="https://upload.wikimedia.org/wikipedia/commons/4/4e/Chronic_apical_periodontitis.jpg",
         license="CC BY-SA 3.0", author="Michele Gardini (anotação: Lesion)",
         source="https://commons.wikimedia.org/wiki/File:Chronic_apical_periodontitis.jpg",
         caption="Radiografia periapical de pré-molar com perda óssea apical (seta) — consequência radiográfica da necrose pulpar."),
    dict(id="abscesso_periapical_agudo",
         url="https://upload.wikimedia.org/wikipedia/commons/2/2d/Abscessed_tooth_periapical_radiograph.jpg",
         license="CC BY-SA 3.0", author="Coronation Dental Specialty Group",
         source="https://commons.wikimedia.org/wiki/File:Abscessed_tooth_periapical_radiograph.jpg",
         caption="Radiografia periapical do dente 3.6 mostrando abscesso periapical envolvendo as duas raízes."),
    dict(id="granuloma_periapical",
         url="https://upload.wikimedia.org/wikipedia/commons/c/ca/Granuloma_sotto_dente_gi%C3%A0_devitalizzato_-_visione_di_lastra_su_schermo.jpg",
         license="CC BY-SA 4.0", author="Anna.Massini",
         source="https://commons.wikimedia.org/wiki/File:Granuloma_sotto_dente_gi%C3%A0_devitalizzato_-_visione_di_lastra_su_schermo.jpg",
         caption="Radiografia de dente tratado endodonticamente mostrando granuloma periapical."),
    dict(id="cisto_radicular",
         url="https://upload.wikimedia.org/wikipedia/commons/5/5d/Periapical_radiolucency.jpg",
         license="CC BY-SA 4.0", author="Shaimaa Abdellatif",
         source="https://commons.wikimedia.org/wiki/File:Periapical_radiolucency.jpg",
         caption="Radiografia periapical com radioluscência e perda óssea nas raízes de dois incisivos — representativo de cisto radicular."),
    dict(id="abscesso_periapical_cronico",
         url="https://upload.wikimedia.org/wikipedia/commons/4/48/Abces_parulique.jpg",
         license="CC BY-SA 3.0", author="Damdent",
         source="https://commons.wikimedia.org/wiki/File:Abces_parulique.jpg",
         caption="Fístula gengival ativa (parúlide) drenando abscesso periapical crônico."),
    dict(id="celulite_facial",
         url="https://upload.wikimedia.org/wikipedia/commons/4/43/Abces_dentaire.jpg",
         license="CC BY-SA 3.0", author="Égoïté",
         source="https://commons.wikimedia.org/wiki/File:Abces_dentaire.jpg",
         caption="Tumefação facial progressiva por celulite/abscesso odontogênico."),
    dict(id="angina_ludwig",
         url="https://upload.wikimedia.org/wikipedia/commons/5/5d/Ludwig_angina.jpg",
         license="CC BY 2.0", author="Kulkarni, Pai, Bhattarai, Rao, Ambareesha",
         source="https://commons.wikimedia.org/wiki/File:Ludwig_angina.jpg",
         caption="Tumefação submandibular bilateral em paciente com Angina de Ludwig."),
    dict(id="osteomielite_cronica",
         url="https://upload.wikimedia.org/wikipedia/commons/e/ee/Jaw_lesions_-_Chronic_osteomyelitis_-_Cone_beam_CT.jpg",
         license="CC BY 4.0", author="Silva, Bueno, Yamamoto-Silva, Gomez, Peters, Estrela",
         source="https://commons.wikimedia.org/wiki/File:Jaw_lesions_-_Chronic_osteomyelitis_-_Cone_beam_CT.jpg",
         caption="Tomografia cone-beam de osteomielite crônica: lesão esclerótica mista na região de molares inferiores."),
    dict(id="osteite_condensante",
         url="https://upload.wikimedia.org/wikipedia/commons/0/04/Jaw_lesions_-_Condensing_osteitis_-_Cone_beam_CT.jpg",
         license="CC BY 4.0", author="Silva, Bueno, Yamamoto-Silva, Gomez, Peters, Estrela",
         source="https://commons.wikimedia.org/wiki/File:Jaw_lesions_-_Condensing_osteitis_-_Cone_beam_CT.jpg",
         caption="Tomografia cone-beam mostrando osteíte condensante: lesão radiopaca difusa no ápice de molar inferior."),
    dict(id="osteomielite_garre",
         url="https://upload.wikimedia.org/wikipedia/commons/3/3c/Garre%27ssclerosingosteomyelitis.jpg",
         license="CC BY 3.0", author="Gumber, Sharma, Sharma, Gupta, Bhardwaj, Jakhar",
         source="https://commons.wikimedia.org/wiki/File:Garre%27ssclerosingosteomyelitis.jpg",
         caption="Radiografia pré-operatória de osteomielite esclerosante de Garré (periostite ossificante)."),
    dict(id="osteite_alveolar",
         url="https://upload.wikimedia.org/wikipedia/commons/1/19/Alveolar_osteitis_labeled_dry_socket.jpg",
         license="CC BY 3.0", author="Beatgoddess",
         source="https://commons.wikimedia.org/wiki/File:Alveolar_osteitis_labeled_dry_socket.jpg",
         caption="Fotografia clínica de alvéolo seco (osteíte alveolar) pós-exodontia."),
    dict(id="pulpite_reversivel",
         url="https://upload.wikimedia.org/wikipedia/commons/2/2f/Dental_Caries_Cavity_2.JPG",
         license="CC BY-SA 4.0", author="Suyash Dwivedi",
         source="https://commons.wikimedia.org/wiki/File:Dental_Caries_Cavity_2.JPG",
         caption="Cavidade de cárie profunda em molar — lesão típica que pode causar pulpite reversível."),
    dict(id="pulpite_irreversivel",
         url="https://upload.wikimedia.org/wikipedia/commons/9/98/Dental_Caries_.jpg",
         license="CC BY-SA 4.0", author="Ickyvickywiki",
         source="https://commons.wikimedia.org/wiki/File:Dental_Caries_.jpg",
         caption="Cárie extensa classe II em molar inferior — lesão compatível com pulpite irreversível."),
]


def download(url, dest):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp, open(dest, "wb") as f:
        f.write(resp.read())


def process():
    credits = {}
    for item in IMAGES:
        raw_path = os.path.join(OUT_DIR, f"_raw_{item['id']}.jpg")
        out_path = os.path.join(OUT_DIR, f"{item['id']}.jpg")
        try:
            download(item["url"], raw_path)
            im = Image.open(raw_path).convert("RGB")
            w, h = im.size
            max_w = 900
            if w > max_w:
                new_h = int(h * (max_w / w))
                im = im.resize((max_w, new_h), Image.LANCZOS)
            im.save(out_path, "JPEG", quality=82, optimize=True)
            os.remove(raw_path)
            size_kb = os.path.getsize(out_path) / 1024
            print(f"OK  {item['id']:28s} {im.size[0]}x{im.size[1]}  {size_kb:.0f}KB")
            credits[item["id"]] = {
                "file": f"images/{item['id']}.jpg",
                "license": item["license"],
                "author": item["author"],
                "source": item["source"],
                "caption": item["caption"],
            }
        except Exception as e:
            print(f"FAIL {item['id']:28s} {e}")
    with open(os.path.join(HERE, "site_src", "credits.json"), "w", encoding="utf-8") as f:
        json.dump(credits, f, ensure_ascii=False, indent=2)
    print("\nOK:", len(credits), "/", len(IMAGES))


if __name__ == "__main__":
    process()
