# -*- coding: utf-8 -*-
"""Baixa as fotos/radiografias com licenca livre (Wikimedia Commons) usadas
no site, redimensiona/recomprime e grava credits.json com a atribuicao."""
import json
import os
import time
import urllib.request
import urllib.error

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
         url="https://upload.wikimedia.org/wikipedia/commons/4/4e/Chronic_apical_periodontitis.jpg",
         license="CC BY-SA 3.0", author="Michele Gardini",
         source="https://commons.wikimedia.org/wiki/File:Chronic_apical_periodontitis.jpg",
         caption="Radiografia periapical mostrando radioluscência periapical bem definida no ápice radicular, compatível com granuloma periapical em dente não vital."),
    dict(id="calcificacoes_pulpares",
         url="https://upload.wikimedia.org/wikipedia/commons/5/5b/X-ray_manual_-_U.S._Army_(1917)_(14734336166).jpg",
         license="Domínio público", author="U.S. Army / American Roentgen Ray Society (1917, digitalizado pelo Internet Archive)",
         source="https://commons.wikimedia.org/wiki/File:X-ray_manual_-_U.S._Army_(1917)_(14734336166).jpg",
         caption="Radiografia histórica (manual do Exército dos EUA, 1917) cuja legenda original identifica um cálculo pulpar (dentículo) radiopaco dentro da câmara pulpar. Imagem antiga, mas é o único registro real e identificado deste achado disponível com licença livre."),
    dict(id="cisto_residual",
         url="https://upload.wikimedia.org/wikipedia/commons/f/f8/Torbiel_korzeniowa_po_ekstrakcji_fragmentu_korzenia.jpg",
         license="CC BY-SA", author="Barte3k",
         source="https://commons.wikimedia.org/wiki/File:Torbiel_korzeniowa_po_ekstrakcji_fragmentu_korzenia.jpg",
         caption="Peça cirúrgica: cisto radicular removido junto com um fragmento de raiz dentária após exodontia com curetagem incompleta — o tecido cístico remanescente que caracteriza o cisto residual."),
    dict(id="trombose_seio_cavernoso",
         url="https://upload.wikimedia.org/wikipedia/commons/b/bf/Gray571.png",
         license="Domínio público", author="Henry Vandyke Carter (Gray's Anatomy, 1918)",
         source="https://commons.wikimedia.org/wiki/File:Gray571.png",
         caption="Ilustração anatômica clássica (Gray's Anatomy) em corte, mostrando o seio cavernoso e estruturas vizinhas. Usada como referência anatômica — não há fotografia clínica real com licença livre disponível para esta condição."),
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
         url="https://upload.wikimedia.org/wikipedia/commons/3/34/Tooth_decay_and_abscess_xray.png",
         license="CC BY-SA 3.0", author="Coronation Dental Specialty Group",
         source="https://commons.wikimedia.org/wiki/File:Tooth_decay_and_abscess_xray.png",
         caption="Radiografia periapical mostrando cárie profunda (seta verde) com radioluscência periapical associada (pontas de seta azuis) — compatível com pulpite irreversível evoluindo para necrose."),
]


def download(url, dest, retries=5):
    req = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp, open(dest, "wb") as f:
                f.write(resp.read())
            return
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                wait = 4 * (attempt + 1)
                print(f"  (429, aguardando {wait}s antes de tentar de novo...)")
                time.sleep(wait)
                continue
            raise


def process():
    credits = {}
    for item in IMAGES:
        raw_path = os.path.join(OUT_DIR, f"_raw_{item['id']}.jpg")
        out_path = os.path.join(OUT_DIR, f"{item['id']}.jpg")
        try:
            download(item["url"], raw_path)
            time.sleep(1.2)
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
