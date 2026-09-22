# -*- coding: utf-8 -*-
"""
Base de dados unica (Doencas da Polpa e Periapice - UNESC) + gerador de
icones vetoriais esquematicos ("raio-x anotado"), reutilizados tanto no
site (SVG) quanto no PDF de estudo (ReportLab Drawing).

Fonte: slides "Doencas da Polpa e Periapice" (Profa. Angela Maragno) +
Atividade Discente 1 / Gabarito (Patologia Bucal - UNESC).
"""

# ----------------------------------------------------------------------
# PALETA (compartilhada entre SVG e PDF)
# ----------------------------------------------------------------------
PAL = {
    "film": "#0b1220",        # fundo "pelicula radiografica"
    "bone": "#c9c2ab",        # osso / dentina
    "bone_dark": "#a89f84",
    "enamel": "#efe9d8",
    "pdl": "#5c6470",
    "pulp_normal": "#b9b3a2",
    "pulp_mild": "#e0935f",
    "pulp_severe": "#d94a2b",
    "pulp_necrotic": "#3a3a3a",
    "pulp_calc": "#f4efe0",
    "polyp": "#c65b6a",
    "lesion_dark": "#050a12",   # radiolucido
    "lesion_rim": "#8b94a3",
    "radiopaque": "#faf6e9",   # radiopaco (oposto do radiolucido)
    "caries": "#241a12",
    "accent_warn": "#c6462f",
    "accent_ok": "#3f8f6a",
}

CATEGORIES = [
    ("pulpar", "Alteracoes Pulpares"),
    ("periapical_aguda", "Alteracoes Periapicais Agudas"),
    ("periapical_cronica", "Alteracoes Periapicais Cronicas"),
    ("disseminacao", "Complicacoes por Disseminacao"),
    ("osteomielite", "Osteomielites e Condicoes Osseas Correlatas"),
]
CAT_LABEL = dict(CATEGORIES)

# ----------------------------------------------------------------------
# GEOMETRIA DOS ICONES (lista de "shapes" -> renderizada em SVG ou PDF)
# ----------------------------------------------------------------------
VB_TOOTH = (100, 130)
VB_FACE = (100, 100)


def _tooth_base(pulp="normal", caries=0):
    """Retorna shapes do dente base: coroa, raiz, camara/canal pulpar, LP."""
    s = []
    pulp_color = {
        "normal": PAL["pulp_normal"],
        "mild": PAL["pulp_mild"],
        "severe": PAL["pulp_severe"],
        "necrotic": PAL["pulp_necrotic"],
    }.get(pulp, PAL["pulp_normal"])

    # fundo pelicula
    s.append(dict(t="rect", x=0, y=0, w=100, h=130, fill=PAL["film"]))

    # ligamento periodontal (halo curvo ao redor da raiz)
    s.append(dict(t="path", stroke=PAL["pdl"], sw=2.4, fill="none", cmds=[
        ("M", 33, 33), ("C", 33, 55, 30, 78, 40, 95),
        ("C", 44, 101, 56, 101, 60, 95),
        ("C", 70, 78, 67, 55, 67, 33),
    ]))

    # raiz (dentina) - contorno afunilado com curvatura anatomica
    s.append(dict(t="path", fill=PAL["bone"], stroke=PAL["bone_dark"], sw=1, cmds=[
        ("M", 38, 36), ("L", 62, 36),
        ("C", 61, 58, 58, 78, 51, 97),
        ("C", 50.4, 98.6, 49.6, 98.6, 49, 97),
        ("C", 42, 78, 39, 58, 38, 36),
        ("Z",),
    ]))

    # coroa - topo oclusal com cuspides suaves
    s.append(dict(t="path", fill=PAL["enamel"], stroke=PAL["bone_dark"], sw=1, cmds=[
        ("M", 27, 21), ("C", 26, 15, 30, 10, 37, 9),
        ("C", 41, 8.3, 43, 11, 40.5, 15.5),
        ("C", 44, 10.5, 49, 8.3, 55, 9.3),
        ("C", 63, 10.6, 69, 15, 68, 21),
        ("L", 68, 36), ("L", 32, 36),
        ("Z",),
    ]))

    # carie (se houver) - entalhe escuro na coroa
    if caries >= 1:
        depth = {1: 6, 2: 12, 3: 20}[caries]
        s.append(dict(t="polygon",
                       pts=[(44, 12), (56, 12), (58, 12 + depth), (50, 16 + depth), (42, 12 + depth)],
                       fill=PAL["caries"]))

    # camara pulpar
    if pulp != "calcified":
        s.append(dict(t="polygon", pts=[(44, 16), (56, 16), (53, 34), (47, 34)],
                       fill=pulp_color))
        # canal
        s.append(dict(t="rect", x=47.5, y=34, w=5, h=52, fill=pulp_color))
    else:
        s.append(dict(t="polygon", pts=[(44, 16), (56, 16), (53, 34), (47, 34)],
                       fill=PAL["pulp_normal"]))
        s.append(dict(t="rect", x=47.5, y=34, w=5, h=52, fill=PAL["pulp_normal"]))
        s.append(dict(t="circle", cx=50, cy=22, r=2.4, fill=PAL["pulp_calc"]))
        s.append(dict(t="circle", cx=49, cy=55, r=1.6, fill=PAL["pulp_calc"]))

    if pulp == "polyp":
        s.append(dict(t="circle", cx=50, cy=8, r=9, fill=PAL["polyp"], stroke="#7c2f39", sw=1))

    return s


def tooth_diagram(pulp="normal", caries=0, apex=None, lateral=False,
                   edentulous=False, dry_socket=False):
    if edentulous:
        return _edentulous(apex)
    if dry_socket:
        return _dry_socket()

    s = _tooth_base(pulp=pulp, caries=caries)
    ax, ay = 50, 96

    if apex == "widened_pdl":
        s.append(dict(t="circle", cx=ax, cy=ay, r=5.5, fill="none", stroke=PAL["lesion_dark"], sw=3))

    elif apex == "granuloma":
        s.append(dict(t="circle", cx=ax, cy=ay + 3, r=9, fill=PAL["lesion_dark"], stroke=PAL["lesion_rim"], sw=1.4))

    elif apex == "cyst":
        s.append(dict(t="circle", cx=ax, cy=ay + 4, r=13, fill=PAL["lesion_dark"], stroke=PAL["lesion_rim"], sw=1.2))
        s.append(dict(t="circle", cx=ax, cy=ay + 4, r=13, fill="none", stroke=PAL["bone_dark"], sw=1))

    elif apex == "abscess_acute":
        pts = [(ax - 12, ay - 2), (ax - 4, ay - 9), (ax + 9, ay - 5), (ax + 13, ay + 6),
               (ax + 4, ay + 15), (ax - 9, ay + 12), (ax - 14, ay + 4)]
        s.append(dict(t="polygon", pts=pts, fill=PAL["lesion_dark"], stroke=PAL["accent_warn"], sw=1.4))
        for dx, dy in [(-16, -14), (16, -14), (-18, 6), (18, 6)]:
            s.append(dict(t="line", x1=ax + dx * 0.55, y1=ay + dy * 0.55, x2=ax + dx, y2=ay + dy,
                           stroke=PAL["accent_warn"], sw=1.6))

    elif apex == "abscess_chronic":
        pts = [(ax - 11, ay - 1), (ax - 3, ay - 8), (ax + 8, ay - 4), (ax + 12, ay + 5),
               (ax + 3, ay + 13), (ax - 8, ay + 10), (ax - 13, ay + 3)]
        s.append(dict(t="polygon", pts=pts, fill=PAL["lesion_dark"], stroke=PAL["lesion_rim"], sw=1.2))
        s.append(dict(t="polyline", pts=[(ax + 2, ay - 6), (ax + 10, ay - 30), (ax + 14, ay - 46)],
                       fill="none", stroke=PAL["accent_warn"], sw=1.6, dash=[3, 2]))
        s.append(dict(t="circle", cx=ax + 15, cy=ay - 48, r=2.4, fill=PAL["accent_warn"]))

    elif apex == "condensing":
        s.append(dict(t="circle", cx=ax + 10, cy=ay - 4, r=9, fill=PAL["radiopaque"]))
        s.append(dict(t="circle", cx=ax, cy=ay + 2, r=4.5, fill=PAL["lesion_dark"], stroke=PAL["lesion_rim"], sw=1))

    elif apex == "sequestrum_acute":
        pts = [(ax - 13, ay - 3), (ax - 4, ay - 11), (ax + 10, ay - 6), (ax + 14, ay + 6),
               (ax + 4, ay + 16), (ax - 10, ay + 12), (ax - 16, ay + 3)]
        s.append(dict(t="polygon", pts=pts, fill=PAL["lesion_dark"], stroke=PAL["accent_warn"], sw=1.2))
        s.append(dict(t="polygon", pts=[(ax - 3, ay), (ax + 3, ay - 3), (ax + 5, ay + 4), (ax - 1, ay + 6)],
                       fill=PAL["radiopaque"]))

    elif apex == "sequestrum_chronic":
        pts = [(ax - 16, ay - 4), (ax - 2, ay - 14), (ax + 14, ay - 8), (ax + 19, ay + 8),
               (ax + 4, ay + 20), (ax - 13, ay + 15), (ax - 20, ay + 3)]
        s.append(dict(t="polygon", pts=pts, fill=PAL["lesion_dark"], stroke=PAL["lesion_rim"], sw=1.2))
        s.append(dict(t="polygon", pts=[(ax - 4, ay - 1), (ax + 3, ay - 5), (ax + 7, ay + 3), (ax - 1, ay + 8)],
                       fill=PAL["radiopaque"]))
        s.append(dict(t="polyline", pts=[(ax - 14, ay + 8), (ax - 20, ay + 18), (ax - 22, ay + 27)],
                       fill="none", stroke=PAL["lesion_rim"], sw=1.4, dash=[3, 2]))
        s.append(dict(t="circle", cx=ax - 23, cy=ay + 29, r=2.2, fill=PAL["lesion_rim"]))

    elif apex == "garre":
        for i, r in enumerate([16, 20, 24, 28]):
            s.append(dict(t="circle", cx=ax + 20, cy=ay - 6, r=r, fill="none",
                           stroke=PAL["radiopaque"], sw=1.3, opacity=0.9 - i * 0.12))

    if lateral and apex in ("cyst", "granuloma"):
        # reposiciona a ultima forma (lesao) para a lateral da raiz
        les = s.pop()
        if apex == "cyst":
            s.pop()  # remove stroke extra do cisto tambem
        s.append(dict(t="circle", cx=68, cy=62, r=9, fill=PAL["lesion_dark"], stroke=PAL["lesion_rim"], sw=1.3))

    return s


def _edentulous(apex):
    s = [dict(t="rect", x=0, y=0, w=100, h=130, fill=PAL["film"])]
    # rebordo alveolar arredondado (sem dentes)
    s.append(dict(t="ellipse", cx=50, cy=38, rx=38, ry=8, fill=PAL["bone"], stroke=PAL["bone_dark"], sw=1))
    s.append(dict(t="polygon", pts=[(14, 38), (86, 38), (82, 100), (18, 100)],
                   fill=PAL["bone"], stroke=PAL["bone_dark"], sw=1))
    s.append(dict(t="circle", cx=50, cy=70, r=15, fill=PAL["lesion_dark"], stroke=PAL["lesion_rim"], sw=1.4))
    return s


def _dry_socket():
    s = [dict(t="rect", x=0, y=0, w=100, h=130, fill=PAL["film"])]
    # dentes vizinhos intactos
    for cx in (24, 76):
        s.append(dict(t="polygon", pts=[(cx - 10, 36), (cx + 10, 36), (cx + 7, 90), (cx - 7, 90)],
                       fill=PAL["bone"], stroke=PAL["bone_dark"], sw=1))
        s.append(dict(t="polygon", pts=[(cx - 12, 14), (cx + 12, 14), (cx + 10, 36), (cx - 10, 36)],
                       fill=PAL["enamel"], stroke=PAL["bone_dark"], sw=1))
    # rebordo osseo ao redor do alveolo
    s.append(dict(t="polygon", pts=[(36, 30), (64, 30), (66, 95), (34, 95)],
                   fill=PAL["bone"], stroke=PAL["bone_dark"], sw=1))
    # alveolo vazio (irregular, sem coagulo)
    jagged = [(42, 34), (58, 34), (55, 45), (60, 55), (54, 66), (58, 78), (50, 88),
              (42, 78), (46, 66), (40, 55), (45, 45)]
    s.append(dict(t="polygon", pts=jagged, fill=PAL["lesion_dark"], stroke=PAL["accent_warn"], sw=1.3))
    for (x, y) in [(46, 48), (52, 60), (47, 72)]:
        s.append(dict(t="circle", cx=x, cy=y, r=1.3, fill=PAL["radiopaque"]))
    return s


def face_diagram(variant):
    s = [dict(t="rect", x=0, y=0, w=100, h=100, fill="#101418")]
    # cabeca simples (contorno)
    s.append(dict(t="ellipse", cx=50, cy=50, rx=30, ry=36, fill="#e7ded0", stroke="#3a332b", sw=1.4))
    # orelhas
    for cx in (21, 79):
        s.append(dict(t="ellipse", cx=cx, cy=50, rx=4, ry=7, fill="#e7ded0", stroke="#3a332b", sw=1))
    # olhos
    for cx in (40, 60):
        s.append(dict(t="circle", cx=cx, cy=44, r=2.6, fill="#3a332b"))
    # nariz / boca
    s.append(dict(t="line", x1=50, y1=46, x2=50, y2=56, stroke="#3a332b", sw=1.2))
    s.append(dict(t="line", x1=42, y1=63, x2=58, y2=63, stroke="#3a332b", sw=1.6))

    if variant == "cellulitis":
        s.append(dict(t="polygon",
                       pts=[(58, 45), (74, 40), (82, 55), (78, 72), (62, 78), (52, 66)],
                       fill=PAL["accent_warn"], opacity=0.55))
    elif variant == "cavernous":
        for cx in (40, 60):
            s.append(dict(t="ellipse", cx=cx, cy=44, rx=9, ry=8, fill=PAL["accent_warn"], opacity=0.5))
            s.append(dict(t="circle", cx=cx, cy=44, r=3.6, fill="#1a1a1a"))
            s.append(dict(t="line", x1=cx, y1=44, x2=cx + (10 if cx > 50 else -10), y2=40,
                           stroke=PAL["accent_warn"], sw=1.6))
            s.append(dict(t="polygon", pts=[(cx + (12 if cx > 50 else -12), 39), (cx + (9 if cx > 50 else -9), 37),
                                             (cx + (9 if cx > 50 else -9), 41)], fill=PAL["accent_warn"]))
    elif variant == "ludwig":
        s.append(dict(t="ellipse", cx=42, cy=78, rx=13, ry=10, fill=PAL["accent_warn"], opacity=0.55))
        s.append(dict(t="ellipse", cx=58, cy=78, rx=13, ry=10, fill=PAL["accent_warn"], opacity=0.55))
        s.append(dict(t="line", x1=50, y1=63, x2=50, y2=53, stroke=PAL["accent_ok"], sw=2.2))
        s.append(dict(t="polygon", pts=[(50, 51), (47, 56), (53, 56)], fill=PAL["accent_ok"]))
        s.append(dict(t="polygon", pts=[(86, 53), (94, 67), (78, 67)], fill="none", stroke=PAL["accent_warn"], sw=1.8))
        s.append(dict(t="line", x1=86, y1=58, x2=86, y2=62.5, stroke=PAL["accent_warn"], sw=1.6))
        s.append(dict(t="circle", cx=86, cy=64.5, r=0.9, fill=PAL["accent_warn"]))
    return s


# ----------------------------------------------------------------------
# RENDERERS
# ----------------------------------------------------------------------
_VIG_ID = [0]


def shapes_to_svg(shapes, vb, css_class="dg", vignette=True):
    vw, vh = vb
    _VIG_ID[0] += 1
    gid = f"vig{_VIG_ID[0]}"
    parts = [f'<svg viewBox="0 0 {vw} {vh}" class="{css_class}" role="img" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">']
    if vignette:
        parts.append(
            f'<defs><radialGradient id="{gid}" cx="50%" cy="42%" r="75%">'
            f'<stop offset="55%" stop-color="#000" stop-opacity="0"/>'
            f'<stop offset="100%" stop-color="#000" stop-opacity=".38"/>'
            f"</radialGradient></defs>"
        )
    for sh in shapes:
        op = sh.get("opacity", 1)
        opa = f' opacity="{op}"' if op != 1 else ""
        fill = sh.get("fill", "none")
        stroke = sh.get("stroke")
        sw = sh.get("sw", 0)
        dash = sh.get("dash")
        dasha = f' stroke-dasharray="{",".join(str(d) for d in dash)}"' if dash else ""
        stroke_attrs = f' stroke="{stroke}" stroke-width="{sw}"{dasha}' if stroke else ""
        t = sh["t"]
        if t == "rect":
            parts.append(f'<rect x="{sh["x"]}" y="{sh["y"]}" width="{sh["w"]}" height="{sh["h"]}" fill="{fill}"{stroke_attrs}{opa}/>')
        elif t == "circle":
            parts.append(f'<circle cx="{sh["cx"]}" cy="{sh["cy"]}" r="{sh["r"]}" fill="{fill}"{stroke_attrs}{opa}/>')
        elif t == "ellipse":
            parts.append(f'<ellipse cx="{sh["cx"]}" cy="{sh["cy"]}" rx="{sh["rx"]}" ry="{sh["ry"]}" fill="{fill}"{stroke_attrs}{opa}/>')
        elif t == "polygon":
            pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in sh["pts"])
            parts.append(f'<polygon points="{pts}" fill="{fill}"{stroke_attrs}{opa}/>')
        elif t == "polyline":
            pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in sh["pts"])
            parts.append(f'<polyline points="{pts}" fill="{fill}"{stroke_attrs}{opa}/>')
        elif t == "line":
            parts.append(f'<line x1="{sh["x1"]}" y1="{sh["y1"]}" x2="{sh["x2"]}" y2="{sh["y2"]}"{stroke_attrs}{opa}/>')
        elif t == "path":
            d = []
            for cmd in sh["cmds"]:
                if cmd[0] == "M":
                    d.append(f"M{cmd[1]:.2f},{cmd[2]:.2f}")
                elif cmd[0] == "L":
                    d.append(f"L{cmd[1]:.2f},{cmd[2]:.2f}")
                elif cmd[0] == "C":
                    d.append(f"C{cmd[1]:.2f},{cmd[2]:.2f} {cmd[3]:.2f},{cmd[4]:.2f} {cmd[5]:.2f},{cmd[6]:.2f}")
                elif cmd[0] == "Z":
                    d.append("Z")
            parts.append(f'<path d="{" ".join(d)}" fill="{fill}"{stroke_attrs}{opa}/>')
    if vignette:
        parts.append(f'<rect x="0" y="0" width="{vw}" height="{vh}" fill="url(#{gid})"/>')
    parts.append("</svg>")
    return "".join(parts)


def shapes_to_drawing(shapes, vb, size_pt):
    from reportlab.graphics.shapes import Drawing, Rect, Circle, Ellipse, Polygon, PolyLine, Line, Group
    vw, vh = vb
    scale = size_pt / vw
    d = Drawing(size_pt, size_pt * vh / vw)
    g = Group()
    g.transform = (scale, 0, 0, -scale, 0, size_pt * vh / vw)  # flip Y (SVG y-down -> reportlab y-up)
    for sh in shapes:
        fill = None if sh.get("fill") in (None, "none") else sh.get("fill")
        stroke = sh.get("stroke")
        sw = sh.get("sw", 0)
        t = sh["t"]
        obj = None
        if t == "rect":
            obj = Rect(sh["x"], sh["y"], sh["w"], sh["h"])
        elif t == "circle":
            obj = Circle(sh["cx"], sh["cy"], sh["r"])
        elif t == "ellipse":
            obj = Ellipse(sh["cx"], sh["cy"], sh["rx"], sh["ry"])
        elif t == "polygon":
            pts = []
            for x, y in sh["pts"]:
                pts.extend([x, y])
            obj = Polygon(pts)
        elif t == "polyline":
            pts = []
            for x, y in sh["pts"]:
                pts.extend([x, y])
            obj = PolyLine(pts)
            obj.strokeColor = _hexcolor(stroke) if stroke else None
            obj.strokeWidth = sw
            g.add(obj)
            continue
        elif t == "line":
            obj = Line(sh["x1"], sh["y1"], sh["x2"], sh["y2"])
            obj.strokeColor = _hexcolor(stroke) if stroke else None
            obj.strokeWidth = sw
            g.add(obj)
            continue
        elif t == "path":
            from reportlab.graphics.shapes import Path
            obj = Path()
            for cmd in sh["cmds"]:
                if cmd[0] == "M":
                    obj.moveTo(cmd[1], cmd[2])
                elif cmd[0] == "L":
                    obj.lineTo(cmd[1], cmd[2])
                elif cmd[0] == "C":
                    obj.curveTo(cmd[1], cmd[2], cmd[3], cmd[4], cmd[5], cmd[6])
                elif cmd[0] == "Z":
                    obj.closePath()
        if obj is None:
            continue
        obj.fillColor = _hexcolor(fill) if fill else None
        obj.strokeColor = _hexcolor(stroke) if stroke else None
        obj.strokeWidth = sw
        g.add(obj)
    d.add(g)
    return d


def _hexcolor(hexstr):
    from reportlab.lib.colors import HexColor
    return HexColor(hexstr)


def build_diagram_shapes(d):
    """d: dicionario 'diagram' de uma doenca -> lista de shapes."""
    kind = d.get("kind")
    if kind == "face":
        return face_diagram(d["variant"]), VB_FACE
    return tooth_diagram(
        pulp=d.get("pulp", "normal"),
        caries=d.get("caries", 0),
        apex=d.get("apex"),
        lateral=d.get("lateral", False),
        edentulous=d.get("edentulous", False),
        dry_socket=d.get("dry_socket", False),
    ), VB_TOOTH


# ----------------------------------------------------------------------
# DOENCAS
# ----------------------------------------------------------------------
DISEASES = [
    dict(
        id="pulpite_reversivel",
        nome="Pulpite Reversivel",
        categoria="pulpar",
        resumo="Dor curta ao frio/doce, some ao remover o estimulo.",
        clinico="Dor provocada, subita, de intensidade leve a moderada e curta duracao. "
                "Responde mais a estimulos FRIOS, doces e acidos (inclui refrigerante gelado). "
                "A dor CESSA assim que o estimulo e removido. Sem dor espontanea, edema ou febre.",
        localizacao="Camara pulpar do dente afetado, geralmente associada a carie inicial, "
                    "desgaste cervical ou restauracao recente.",
        etiologia="Qualquer injuria que atinja a dentina sem necrosar a polpa: carie incipiente, "
                  "trauma leve, procedimentos restauradores, desgastes cervicais, irritacao quimica.",
        sintomas="Dor de curta duracao, bem localizada, some ao retirar o estimulo.",
        testes="Vitalidade pulpar positiva; percussao negativa; mobilidade normal.",
        radiografico="Nenhuma alteracao radiografica (pode haver carie/restauracao visivel).",
        tratamento="Eliminar a causa e proteger o complexo dentino-pulpar (restauracao/capeamento). "
                   "Reavaliar a vitalidade apos os sintomas cessarem.",
        diferenciar="Pulpite irreversivel: na reversivel a dor SOME ao retirar o estimulo; "
                    "na irreversivel a dor CONTINUA mesmo sem o estimulo.",
        aparencia_curta="Dor de curta duracao ao frio, some rapido",
        causa_curta="Carie inicial / trauma leve / restauracao",
        tratamento_curto="Remover causa + proteger polpa",
        diagram=dict(kind="tooth", pulp="mild", caries=1, apex=None),
    ),
    dict(
        id="pulpite_irreversivel",
        nome="Pulpite Irreversivel",
        categoria="pulpar",
        resumo="Dor espontanea e continua; DOI ao calor, ALIVIA com frio.",
        clinico="Dor aguda e acentuada ao estimulo termico que CONTINUA apos a remocao do estimulo "
                "-  doi ao CALOR e alivia com FRIO. Piora ao deitar. Em estagios avancados a dor e "
                "espontanea, pulsatil e intensa (paciente nao dorme). No inicio o dente e bem "
                "identificado; com a evolucao a dor fica difusa e o paciente nao sabe apontar o dente.",
        localizacao="Estagio inicial: dente bem localizado. Estagio avancado: dor difusa "
                    "(inervacao C amielinica dissemina o estimulo).",
        etiologia="Progressao de injuria pulpar nao tratada: carie profunda atingindo a polpa, "
                  "trauma, procedimentos iatrogenicos.",
        sintomas="Dor espontanea, prolongada, continua, pode ser difusa; exacerbada ao deitar.",
        testes="Vitalidade positiva (em niveis mais baixos) ou ausente em fase final; percussao e "
               "mobilidade normais na maioria dos casos.",
        radiografico="Geralmente nenhuma alteracao; pode haver discreto aumento do espaco do "
                     "ligamento periodontal apical.",
        tratamento="Endodontia ou exodontia, dependendo da possibilidade de restauracao do "
                   "remanescente dental.",
        diferenciar="Pulpite reversivel: nesta a dor cessa ao remover o estimulo. Polipo pulpar: "
                    "forma cronica, geralmente indolor, com tecido de granulacao visivel.",
        aparencia_curta="Dor espontanea/pulsatil; doi ao calor, alivia no frio",
        causa_curta="Carie profunda / trauma nao tratados",
        tratamento_curto="Endodontia ou exodontia",
        diagram=dict(kind="tooth", pulp="severe", caries=3, apex=None),
    ),
    dict(
        id="pulpite_hiperplasica",
        nome="Pulpite Cronica Hiperplasica (Polipo Pulpar)",
        categoria="pulpar",
        resumo="Massa de tecido de granulacao ('carne') saindo da camara pulpar exposta.",
        clinico="Massa de tecido de granulacao avermelhado que cresce para fora da camara pulpar, "
                "preenchendo o defeito coronario. Padrao unico de inflamacao pulpar cronica.",
        localizacao="Molares deciduos e permanentes jovens, com camaras pulpares amplas e grande "
                    "exposicao pulpar.",
        etiologia="Irritacao mecanica cronica + invasao bacteriana de baixa virulencia sobre polpa "
                  "exposta; rizogenese incompleta favorece a irrigacao e mantem o dente vital.",
        sintomas="Geralmente assintomatico; pode ser sensivel a mastigacao e sangrar facilmente.",
        testes="Vitalidade positiva; SEM continuidade com a gengiva adjacente.",
        radiografico="Grande destruicao coronaria com camara pulpar amplamente exposta; apice "
                     "geralmente aberto (rizogenese incompleta).",
        tratamento="Endodontia (pulpectomia) ou exodontia conforme a viabilidade do remanescente.",
        diferenciar="Hiperplasia gengival sobre a cavidade: tem CONTINUIDADE com a gengiva. O "
                    "polipo pulpar NAO tem continuidade e tem coloracao mais escura.",
        aparencia_curta="Massa avermelhada saindo do dente destruido",
        causa_curta="Exposicao pulpar cronica em jovem (ápice aberto)",
        tratamento_curto="Pulpectomia/endodontia ou exodontia",
        diagram=dict(kind="tooth", pulp="polyp", caries=3, apex=None),
    ),
    dict(
        id="necrose_pulpar",
        nome="Necrose Pulpar",
        categoria="pulpar",
        resumo="Morte do tecido pulpar; nao responde a nenhum teste de vitalidade.",
        clinico="Destruicao tecidual ampla que torna praticamente impossivel identificar os "
                "componentes da polpa ao exame histopatologico.",
        localizacao="Toda a polpa (camara e canal) do dente acometido.",
        etiologia="Evolucao final de pulpite irreversivel nao tratada, trauma com ruptura vascular "
                  "apical, ou infeccao bacteriana avancada.",
        sintomas="Pode ser assintomatica (as vezes so ha escurecimento do dente) ou preceder "
                 "periodontite/abscesso apical.",
        testes="NAO responde a testes termicos nem eletricos de vitalidade.",
        radiografico="Pode nao mostrar alteracao inicialmente; com o tempo surgem sinais periapicais "
                     "(alargamento do ligamento, radioluscencia).",
        tratamento="Endodontia ou exodontia.",
        diferenciar="Calcificacao/metamorfose calcica: tambem altera o teste de vitalidade, mas SEM "
                    "sintomas e com canal obliterado (nao ha destruicao tecidual).",
        aparencia_curta="Sem resposta a nenhum teste de vitalidade",
        causa_curta="Pulpite irreversivel nao tratada / trauma",
        tratamento_curto="Endodontia ou exodontia",
        diagram=dict(kind="tooth", pulp="necrotic", caries=3, apex=None),
    ),
    dict(
        id="calcificacoes_pulpares",
        nome="Calcificacoes Pulpares (Denticulos / Calculos)",
        categoria="pulpar",
        resumo="Estruturas calcificadas dentro da polpa; geralmente assintomaticas.",
        clinico="Incidencia de 8 a 90%, aumenta com a idade; forte relacao com pulpites cronicas de "
                "longa duracao; pode ter tendencia familiar. Denticulos formam-se durante a "
                "rizogenese; calculos pulpares nas porcoes coronarias; calcificacoes lineares "
                "difusas nao sao visiveis ao raio-X.",
        localizacao="Denticulos: camara e canais, proximos as furcas de multirradiculares. "
                    "Calculos pulpares: porcao coronaria da polpa.",
        etiologia="Processo degenerativo/reparador da polpa frente a irritacao cronica de baixa "
                  "intensidade; pode ocorrer sem causa aparente.",
        sintomas="Assintomatica na grande maioria dos casos.",
        testes="Vitalidade geralmente positiva; pode diminuir se houver metamorfose calcica extensa.",
        radiografico="Imagem radiopaca puntiforme/nodular na camara ou canal; na metamorfose "
                     "calcica ha diminuicao do espaco pulpar e coroa com coloracao amarelada.",
        tratamento="Nenhum tratamento e necessario na maioria dos casos. Na metamorfose calcica, "
                   "endodontia so e indicada se houver evidencia radiografica de doenca periapical.",
        diferenciar="Metamorfose calcica pos-trauma: cursa com escurecimento amarelado da coroa e "
                    "obliteracao quase total do canal - calcificacao comum nao altera a cor do dente.",
        aparencia_curta="Pontos radiopacos na polpa, assintomatico",
        causa_curta="Irritacao pulpar cronica / idade",
        tratamento_curto="Nenhum (observacao)",
        diagram=dict(kind="tooth", pulp="calcified", caries=0, apex=None),
    ),
    dict(
        id="periodontite_apical_aguda",
        nome="Periodontite Apical Aguda (Pericementite)",
        categoria="periapical_aguda",
        resumo="Dor a mastigacao e percussao; PODE ocorrer em dente VITAL.",
        clinico="Dor pulsatil, nao localizada e constante; dor a PERCUSSAO e a OCLUSAO. "
                "Caracteristicas clinicas semelhantes as do abscesso periapical agudo - entra no "
                "diagnostico diferencial obrigatorio.",
        localizacao="Ligamento periodontal apical.",
        etiologia="Normalmente associada a dente desvitalizado, MAS PODE SER VITAL: trauma "
                  "oclusal, ponto de contato prematuro em restauracao recente, ou corpo estranho "
                  "(instrumento endodontico).",
        sintomas="Dor a mastigacao e percussao, geralmente sem edema facial evidente.",
        testes="Vitalidade negativa ou positiva retardada (se dente vital, positiva); dor nitida a "
               "percussao vertical/horizontal.",
        radiografico="Geralmente nenhuma alteracao, ou discreto aumento do espaco do ligamento "
                     "periodontal apical.",
        tratamento="Dente nao vital: endodontia ou exodontia. Dente vital: ajuste oclusal + "
                   "anti-inflamatorio + acompanhamento.",
        diferenciar="Abscesso periapical agudo: tem SUPURACAO (pus) e tende a evoluir com edema; "
                    "a periodontite apical aguda e so inflamacao do ligamento, sem colecao purulenta.",
        aparencia_curta="Dor a percussao/oclusao, pode ser dente vital",
        causa_curta="Trauma oclusal / dente desvitalizado",
        tratamento_curto="Ajuste oclusal (vital) ou endo/exo (nao vital)",
        diagram=dict(kind="tooth", pulp="necrotic", caries=2, apex="widened_pdl"),
    ),
    dict(
        id="abscesso_periapical_agudo",
        nome="Abscesso Periapical Agudo",
        categoria="periapical_aguda",
        resumo="Pus no apice; dor intensa, extrusao do dente, pode ter febre/calafrios.",
        clinico="Dor intensa, inicialmente localizada podendo tornar-se difusa; sensibilidade "
                "EXTREMA a percussao; extrusao do dente; tumefacao dos tecidos; pode haver cefaleia, "
                "mal-estar, febre e calafrios (toxemia).",
        localizacao="Apice de um dente desvitalizado; pode ser inicial ou agudizacao de lesao "
                    "cronica previa (abscesso fenix).",
        etiologia="Sequencia classica: carie/trauma -> pulpite -> necrose pulpar -> periodontite "
                  "apical aguda -> abscesso periapical agudo.",
        sintomas="Dor pulsatil intensa, edema, extrusao dentaria; sintomas sistemicos em casos "
                 "avancados.",
        testes="Vitalidade negativa; percussao extremamente dolorosa.",
        radiografico="Pode nao haver alteracao, mostrar so aumento do espaco do ligamento, ou "
                     "imagem radiolucida mal definida (agudizacao de processo cronico).",
        tratamento="Drenagem (trepanacao ou incisional) + eliminacao do foco + medicacao (AINE e "
                   "antibiotico se houver comprometimento sistemico). Sinais/sintomas reduzem "
                   "significativamente em 48h da drenagem. Desgaste oclusal se houver extrusao.",
        diferenciar="Abscesso periapical CRONICO: este e agudo, doloroso, com sinais sistemicos; "
                    "o cronico e silencioso, indolor e de longa duracao.",
        aparencia_curta="Dor intensa + extrusao + edema, pode ter febre",
        causa_curta="Necrose pulpar evoluida (sequencia classica)",
        tratamento_curto="Drenagem + antibiotico/AINE se sistemico",
        diagram=dict(kind="tooth", pulp="necrotic", caries=3, apex="abscess_acute"),
    ),
    dict(
        id="granuloma_periapical",
        nome="Granuloma Periapical (Periodontite Apical Cronica)",
        categoria="periapical_cronica",
        resumo="75% das lesoes periapicais; assintomatico; radioluscencia bem definida.",
        clinico="Massa de tecido de granulacao cronica (podendo agudizar) no apice de dente "
                "desvitalizado; representa 75% das lesoes inflamatorias periapicais. Normalmente "
                "ASSINTOMATICO, achado em radiografia de rotina.",
        localizacao="Apice radicular de dente nao vital.",
        etiologia="Resposta inflamatoria cronica a microrganismos/produtos toxicos que persistem "
                  "no canal radicular apos a necrose pulpar.",
        sintomas="Assintomatico; dor so se agudizar; mobilidade e percussao normais; tecido "
                 "sobrejacente pode estar sensivel.",
        testes="Vitalidade negativa (ou positiva se relacionada a apenas uma raiz de "
               "multirradicular).",
        radiografico="Imagem radiolucida arredondada, BEM delimitada, unida ao apice; ausencia de "
                     "lamina dura apical; pode haver reabsorcao radicular externa; de poucos mm a "
                     "mais de 2cm.",
        tratamento="Endodontia (reduz carga microbiana) ou exodontia + curetagem apical. Se nao "
                   "cicatrizar: retratamento e, por fim, cirurgia paraendodontica.",
        diferenciar="Cisto radicular: a imagem radiografica pode ser IDENTICA (a distincao "
                    "definitiva e HISTOPATOLOGICA - revestimento epitelial no cisto). Lesoes "
                    "maiores tendem a ser cisto.",
        aparencia_curta="Radioluscencia apical bem definida, assintomatica",
        causa_curta="Necrose pulpar + inflamacao cronica",
        tratamento_curto="Endodontia (ou exo) + curetagem se preciso",
        diagram=dict(kind="tooth", pulp="necrotic", caries=2, apex="granuloma"),
    ),
    dict(
        id="cisto_radicular",
        nome="Cisto Radicular (Periapical)",
        categoria="periapical_cronica",
        resumo="Cavidade cistica revestida por epitelio; 7-54% das radioluscencias periapicais.",
        clinico="Cavidade ossea patologica revestida por epitelio, preenchida por liquido/material "
                "semissolido, no apice de dente desvitalizado. Assintomatico exceto quando agudiza; "
                "tumefacao/mobilidade/deslocamento dentario apenas em lesoes grandes.",
        localizacao="Apice de dente nao vital; origem no epitelio residual de Malassez, epitelio "
                    "sinusal ou revestimento de trajeto fistuloso.",
        etiologia="Proliferacao epitelial estimulada por processo inflamatorio cronico periapical "
                  "de longa duracao.",
        sintomas="Geralmente assintomatico; vitalidade negativa.",
        testes="Vitalidade negativa.",
        radiografico="Imagem radiolucida bem delimitada, com osteogenese reacional, ausencia de "
                     "lamina dura, reabsorcao radicular comum; pode atingir grande extensao (ate um "
                     "quadrante inteiro).",
        tratamento="Endodontia ou exodontia; cirurgia quando de grande extensao. Raramente pode "
                   "haver transformacao maligna do epitelio (carcinoma epidermoide).",
        diferenciar="Granuloma periapical: imagem radiografica pode ser indistinguivel - a "
                    "confirmacao e HISTOPATOLOGICA (revestimento epitelial completo = cisto).",
        aparencia_curta="Radioluscencia apical bem definida, pode ser grande",
        causa_curta="Proliferacao epitelial (restos de Malassez)",
        tratamento_curto="Endodontia/exodontia +/- cirurgia",
        diagram=dict(kind="tooth", pulp="necrotic", caries=2, apex="cyst"),
    ),
    dict(
        id="cisto_radicular_lateral",
        nome="Cisto Radicular Lateral",
        categoria="periapical_cronica",
        resumo="Cisto radicular que surge na face LATERAL da raiz, via canal acessorio.",
        clinico="Variante do cisto radicular que se desenvolve na porcao LATERAL da raiz, e nao "
                "no apice.",
        localizacao="Face lateral da raiz de dente nao vital.",
        etiologia="Disseminacao da inflamacao atraves de um canal lateral (acessorio) do dente.",
        sintomas="Geralmente assintomatico.",
        testes="Vitalidade negativa.",
        radiografico="Imagem radiolucida bem delimitada na LATERAL da raiz; ausencia de lamina "
                     "dura.",
        tratamento="Endodontia ou exodontia.",
        diferenciar="Cisto periodontal lateral (origem NAO inflamatoria, dente vital): o cisto "
                    "radicular lateral esta sempre ligado a um dente com necrose pulpar/canal "
                    "lateral infectado.",
        aparencia_curta="Radioluscencia na lateral da raiz",
        causa_curta="Canal lateral infectado",
        tratamento_curto="Endodontia ou exodontia",
        diagram=dict(kind="tooth", pulp="necrotic", caries=1, apex="cyst", lateral=True),
    ),
    dict(
        id="cisto_residual",
        nome="Cisto Residual",
        categoria="periapical_cronica",
        resumo="Cisto radicular remanescente apos exodontia (curetagem incompleta).",
        clinico="Cisto radicular que permanece no osso apos a exodontia do dente que lhe deu "
                "origem, quando a curetagem foi incompleta.",
        localizacao="Processo alveolar EDENTULO (sem dente associado).",
        etiologia="Remocao do dente sem remocao completa do revestimento cistico periapical.",
        sintomas="Assintomatico; geralmente achado radiografico de rotina em area desdentada.",
        testes="Nao se aplica (area edentula, sem dente para testar).",
        radiografico="Imagem radiolucida bem delimitada, circular ou oval, tamanho variavel, "
                     "localizada em rebordo alveolar edentulo.",
        tratamento="Enucleacao cirurgica com curetagem.",
        diferenciar="So ocorre em area SEM dente. A historia de exodontia previa no local sugere "
                    "fortemente cisto residual (descartar outras lesoes de area edentula).",
        aparencia_curta="Radioluscencia em area sem dente (pos-exodontia)",
        causa_curta="Curetagem incompleta apos extracao",
        tratamento_curto="Enucleacao cirurgica",
        diagram=dict(kind="tooth", edentulous=True),
    ),
    dict(
        id="abscesso_periapical_cronico",
        nome="Abscesso Periapical Cronico",
        categoria="periapical_cronica",
        resumo="Pus cronico e silencioso, contorno radiolucido mal definido, +/- fistula.",
        clinico="Acumulo de material purulento no alveolo, de longa duracao, causado por agente de "
                "baixa intensidade. SEM sintomatologia clinica - desenvolve-se de maneira "
                "silenciosa. Pode originar-se primariamente ou a partir de um episodio agudo previo.",
        localizacao="Apice de dente nao vital; frequentemente associado a trajeto fistuloso "
                    "(drenagem cronica).",
        etiologia="Infeccao periapical cronica de baixa virulencia, com drenagem continua atraves "
                  "de fistula que impede o acumulo de pressao/dor.",
        sintomas="Assintomatico; pode haver fistula intraoral ou cutanea associada (ponto de "
                 "drenagem).",
        testes="Vitalidade negativa.",
        radiografico="Imagem radiolucida SEM limites definidos e ausencia de lamina dura (contorno "
                     "mal definido - diferente do contorno bem definido do granuloma/cisto).",
        tratamento="Endodontia ou exodontia + eliminacao do foco; rastreamento da fistula com cone "
                   "de guta-percha para confirmar o dente causador.",
        diferenciar="Granuloma/cisto: contorno BEM definido e sem fistula. Abscesso cronico: "
                    "contorno MAL definido e comumente COM fistula ativa.",
        aparencia_curta="Radioluscencia mal definida, silenciosa, +/- fistula",
        causa_curta="Infeccao periapical de baixa virulencia",
        tratamento_curto="Endodontia/exodontia + rastrear fistula",
        diagram=dict(kind="tooth", pulp="necrotic", caries=2, apex="abscess_chronic"),
    ),
    dict(
        id="celulite_facial",
        nome="Celulite Facial",
        categoria="disseminacao",
        resumo="Disseminacao DIFUSA de infeccao pelos planos faciais, sem colecao localizada.",
        clinico="Disseminacao AGUDA e edemaciada de um processo inflamatorio, sem limites "
                "definidos - ocorre quando o abscesso nao consegue drenar pela pele ou mucosa e se "
                "espalha pelos planos faciais dos tecidos moles.",
        localizacao="Tecidos moles da face/pescoco adjacentes ao dente causador (espaco bucal, "
                    "submandibular, canino etc.), conforme a relacao do apice com as insercoes "
                    "musculares.",
        etiologia="Complicacao de abscesso periapical agudo nao drenado, com bacterias de alta "
                  "virulencia ou defesa comprometida (ex.: diabetes nao controlada, "
                  "imunossupressao).",
        sintomas="Tumefacao facial difusa, dolorosa, quente, sem limite nitido; pode cursar com "
                 "febre e mal-estar; risco de evoluir para trombose de seio cavernoso, "
                 "mediastinite ou Angina de Ludwig.",
        testes="Dente causador com vitalidade negativa; avaliar se o edema e duro ou mole a "
               "palpacao (define se ha colecao passivel de drenagem).",
        radiografico="Depende do dente causador (sinais de necrose/lesao periapical); a celulite "
                     "em si e achado de tecido mole, nao osseo.",
        tratamento="Drenagem do foco odontogenico (endodontia/exodontia) + antibioticoterapia "
                   "sistemica + anti-inflamatorio; atencao especial em diabeticos ou "
                   "imunocomprometidos - reavaliacao diaria.",
        diferenciar="Abscesso periapical: colecao LOCALIZADA e passivel de drenagem pontual. "
                    "Celulite: disseminacao DIFUSA pelos planos faciais, sem colecao bem "
                    "localizada.",
        aparencia_curta="Edema facial difuso, sem limite definido",
        causa_curta="Abscesso nao drenado + defesa comprometida",
        tratamento_curto="Drenagem do foco + antibiotico sistemico",
        diagram=dict(kind="face", variant="cellulitis"),
    ),
    dict(
        id="trombose_seio_cavernoso",
        nome="Trombose do Seio Cavernoso",
        categoria="disseminacao",
        resumo="Emergencia rara e grave: edema periorbitario bilateral + protrusao ocular.",
        clinico="Complicacao rara (infeccoes bucodentarias respondem por ~10% dos casos) e grave: "
                "edema periorbitario com palpebras/conjuntiva envolvidas, protrusao e FIXACAO do "
                "globo ocular, dilatacao pupilar, dor ocular, perda de visao, podendo progredir "
                "para sinais de SNC (meningite, torpor, delirio).",
        localizacao="Seio cavernoso (seio dural entre as camadas da dura-mater), atingido por "
                    "disseminacao retrograda a partir da face.",
        etiologia="Via anterior: infeccao de dentes anteriores -> perfuracao vestibular -> espaco "
                  "canino -> veia facial/angular -> veia oftalmica inferior -> seio cavernoso. "
                  "Via posterior: infeccao de pre-molares/molares superiores.",
        sintomas="Edema periorbitario BILATERAL (caracteristico), febre, calafrios, cefaleia, "
                 "taquicardia, nauseas/vomitos, rigidez de nuca em casos avancados.",
        testes="Emergencia medica - diagnostico clinico + exames de imagem (TC/RM) em ambiente "
               "hospitalar.",
        radiografico="Nao avaliada por radiografia periapical; requer TC/RM em contexto "
                     "hospitalar.",
        tratamento="Drenagem cirurgica + antibioticos em ALTAS doses, internacao hospitalar "
                   "imediata. Mortalidade historica de ate 75%; hoje ainda proxima de 30%.",
        diferenciar="Celulite facial simples: edema unilateral, SEM protrusao/fixacao do globo "
                    "ocular e sem sinais de SNC. A trombose de seio cavernoso e bilateral e com "
                    "sinais oculares/neurologicos graves.",
        aparencia_curta="Edema periorbitario bilateral, olho fixo/protruso",
        causa_curta="Disseminacao retrograda via veia facial/oftalmica",
        tratamento_curto="Emergencia: drenagem + ATB em alta dose",
        diagram=dict(kind="face", variant="cavernous"),
    ),
    dict(
        id="angina_ludwig",
        nome="Angina de Ludwig",
        categoria="disseminacao",
        resumo="Celulite bilateral do assoalho bucal com risco de obstrucao de via aerea.",
        clinico="Celulite AGRESSIVA e bilateral da regiao submandibular (70% de origem em "
                "terceiros molares inferiores), com elevacao e protrusao da lingua, tumefacao "
                "volumosa do pescoco (ate as claviculas) e risco iminente de OBSTRUCAO DAS VIAS "
                "AEREAS.",
        localizacao="Espacos sublingual, submandibular e submentoniano bilateralmente; pode "
                    "progredir para espaco faringeo lateral, retrofaringeo e mediastino.",
        etiologia="Infeccao odontogenica grave (geralmente de molares inferiores) que se dissemina "
                  "abaixo da insercao do musculo milo-hioideo.",
        sintomas="Dor cervical/assoalho bucal, restricao de movimento do pescoco, garganta "
                 "dolorida, taquicardia, inquietacao, necessidade de ficar ereto (sinal de "
                 "obstrucao iminente), febre e calafrios.",
        testes="Emergencia - priorizar avaliacao de via aerea antes de qualquer exame odontologico "
               "de rotina.",
        radiografico="Nao e o foco diagnostico inicial (emergencia clinica); a imagem pode ajudar a "
                     "localizar o dente/foco causador.",
        tratamento="1) Manutencao das vias aereas (prioridade absoluta); 2) incisao e drenagem se "
                   "houver flutuacao; 3) antibioticoterapia em altas doses (penicilina de "
                   "escolha); 4) eliminacao do foco infeccioso original. Mortalidade historica "
                   ">50%; hoje ainda ha obitos por mediastinite, pericardite e obstrucao "
                   "respiratoria.",
        diferenciar="Celulite facial comum: nao compromete via aerea. Angina de Ludwig: risco de "
                    "vida IMEDIATO por obstrucao de via aerea - sempre tratar como emergencia.",
        aparencia_curta="Tumefacao bilateral do assoalho, lingua elevada",
        causa_curta="Infeccao de molar inferior abaixo do milo-hioideo",
        tratamento_curto="Emergencia: via aerea + drenagem + ATB",
        diagram=dict(kind="face", variant="ludwig"),
    ),
    dict(
        id="osteomielite_aguda",
        nome="Osteomielite Supurativa Aguda",
        categoria="osteomielite",
        resumo="Inflamacao aguda dos espacos medulares, menos de 1 mes, predomina em homens.",
        clinico="Processo inflamatorio agudo nos espacos medulares do osso, com MENOS DE 1 MES de "
                "evolucao (tempo insuficiente para o corpo reagir/encapsular). Forte predominancia "
                "em homens (75%), mais comum na MANDIBULA.",
        localizacao="Espacos medulares do osso maxilar/mandibular, a partir de um foco "
                    "odontogenico.",
        etiologia="Infeccao bacteriana odontogenica (dente com necrose/abscesso) associada a "
                  "fatores predisponentes: doencas sistemicas cronicas, imunocomprometimento, "
                  "diminuicao da vascularizacao ossea, higiene deficiente, tabagismo, diabetes.",
        sintomas="Febre, leucocitose, linfadenopatia, sensibilidade e tumefacao dos tecidos moles; "
                 "pode haver formacao e esfoliacao espontanea de sequestro osseo.",
        testes="Biopsia incomum; hemograma com leucocitose.",
        radiografico="Pode nao revelar alteracoes inicialmente, ou mostrar imagem radiolucida mal "
                     "definida.",
        tratamento="Antibiotico + drenagem + tratar a causa (extracao/endodontia do dente "
                   "causador). Antibioticos de escolha: penicilina, clindamicina, cefalexina.",
        diferenciar="Osteomielite CRONICA: sintomas agudos ha MENOS de 1 mes (aguda) x mais de 1 "
                    "mes, mais branda e com fistula (cronica).",
        aparencia_curta="Febre + leucocitose, evolucao < 1 mes",
        causa_curta="Infeccao odontogenica + fator predisponente",
        tratamento_curto="Antibiotico + drenagem + tratar a causa",
        diagram=dict(kind="tooth", pulp="necrotic", caries=3, apex="sequestrum_acute"),
    ),
    dict(
        id="osteomielite_cronica",
        nome="Osteomielite Supurativa Cronica",
        categoria="osteomielite",
        resumo="Evolucao >1 mes; fistula, sequestro, cirurgia obrigatoria.",
        clinico="Evolucao da forma aguda (a partir de ~1 mes) ou ja inicia cronica. Quadro mais "
                "brando: tumefacao, dor, formacao de FISTULA, sequestro osseo, perda dentaria e ate "
                "fratura patologica. Periodos de agudizacao intercalados com melhora.",
        localizacao="Espacos medulares e corticais do osso mandibular (mais comum); predominancia "
                    "em homens (75%).",
        etiologia="Persistencia de infeccao odontogenica com formacao de tecido de granulacao "
                  "denso (capsula fibrosa) que dificulta o acesso de antibioticos e a resposta "
                  "imune.",
        sintomas="Dor e tumefacao mais brandas que a forma aguda; fistula de drenagem; pode haver "
                 "perda de dentes e fratura patologica do osso enfraquecido.",
        testes="Biopsia do tecido mole/osseo em casos persistentes.",
        radiografico="Imagem radiolucida mal definida, disforme e irregular, com SEQUESTROS OSSEOS "
                     "radiopacos centrais; pode haver espessamento da cortical ao redor.",
        tratamento="Dificil resposta a antibioticos isolados (capsula fibrosa protege a area); "
                   "INTERVENCAO CIRURGICA OBRIGATORIA (remover todo tecido infectado ate osso "
                   "sadio sangrante) + antibioticos intravenosos em altas doses; casos persistentes "
                   "podem exigir ressecao e reconstrucao.",
        diferenciar="Osteite condensante: forma osso DENSO (radiopaco) reacional sem destruicao/"
                    "sequestro; a osteomielite cronica DESTROI o osso (radiolucida, com "
                    "sequestro).",
        aparencia_curta="Fistula + sequestro osseo, evolucao > 1 mes",
        causa_curta="Infeccao odontogenica persistente (capsula fibrosa)",
        tratamento_curto="Cirurgia obrigatoria + ATB IV em alta dose",
        diagram=dict(kind="tooth", pulp="necrotic", caries=3, apex="sequestrum_chronic"),
    ),
    dict(
        id="osteite_condensante",
        nome="Osteite Condensante",
        categoria="osteomielite",
        resumo="Radiopacidade reacional indolor no apice, achado casual em jovens.",
        clinico="Tambem chamada osteomielite esclerosante cronica focal. Area de esclerose ossea "
                "REACIONAL, indolor, associada ao apice de dente com pulpite ou necrose (carie "
                "extensa/restauracao profunda). Achado incidental em radiografia de rotina.",
        localizacao="Mais frequente na regiao de pre-molares e molares INFERIORES, em criancas e "
                    "adultos jovens.",
        etiologia="Resposta ossea reparadora a estimulo inflamatorio cronico de baixa intensidade "
                  "vindo da polpa (nao e infeccao ossea ativa como a osteomielite).",
        sintomas="Indolor; achado casual em exame radiografico.",
        testes="Vitalidade do dente associado geralmente alterada (pulpite/necrose).",
        radiografico="Area RADIOPACA (densa), SEM contorno radiolucido, contorno geralmente "
                     "uniforme, adjacente ao apice de dente com lesao inflamatoria apical; SEM "
                     "expansao ossea.",
        tratamento="Resolver o foco de infeccao odontogenica (endodontia ou exodontia). Regride em "
                   "~85% dos casos; em 15% permanece cicatriz ossea radiopaca residual.",
        diferenciar="Osteomielite com periostite proliferativa (Garre): forma camadas paralelas "
                    "('casca de cebola') EXPANDINDO a superficie ossea; a osteite condensante NAO "
                    "expande o osso e fica confinada ao redor do apice.",
        aparencia_curta="Radiopacidade uniforme no apice, indolor",
        causa_curta="Estimulo inflamatorio cronico de baixa intensidade",
        tratamento_curto="Tratar o dente causador (endo/exo)",
        diagram=dict(kind="tooth", pulp="necrotic", caries=2, apex="condensing"),
    ),
    dict(
        id="osteomielite_garre",
        nome="Osteomielite com Periostite Proliferativa (Garre)",
        categoria="osteomielite",
        resumo="Camadas osseas paralelas ('casca de cebola'), expande a cortical, jovens.",
        clinico="Reacao periosteal a inflamacao: o periosteo forma varias camadas paralelas de "
                "osso vital reacional ('casca de cebola'), EXPANDINDO a superficie ossea. Idade "
                "media: 13 anos; sem predilecao por sexo; maioria unifocal.",
        localizacao="Mais comum em pre-molares e molares inferiores; localizacao preferencial na "
                    "margem inferior da mandibula, podendo acometer a cortical vestibular.",
        etiologia="Causa mais frequente: carie e doenca periodontal associada; tambem relacionada "
                  "a fraturas, cistos e infeccoes odontogenicas secundarias, em paciente jovem com "
                  "periosteo muito reativo.",
        sintomas="Aumento de volume facial assimetrico e progressivo, geralmente pouco doloroso.",
        testes="Biopsia raramente necessaria (so se o diagnostico clinico/radiografico for "
               "questionado).",
        radiografico="Laminacoes osseas radiopacas PARALELAS entre si e a cortical subjacente "
                     "('casca de cebola'); tomografia computadorizada e o exame mais indicado. Pode "
                     "haver sequestros osseos no osso neoformado.",
        tratamento="Eliminacao da fonte de infeccao (dente causador); as camadas osseas se "
                   "consolidam/remodelam entre 6 e 12 meses. Biopsia reservada para diagnostico "
                   "diferencial com lesoes neoplasicas quando nao ha relacao clara com foco "
                   "infeccioso.",
        diferenciar="Osteite condensante: radiopacidade compacta e confinada ao apice, SEM "
                    "expansao nem laminacao. Garre tem expansao em camadas paralelas na cortical.",
        aparencia_curta="Camadas radiopacas paralelas ('casca de cebola')",
        causa_curta="Carie/infeccao odontogenica em jovem",
        tratamento_curto="Eliminar o foco; remodela em 6-12 meses",
        diagram=dict(kind="tooth", pulp="necrotic", caries=2, apex="garre"),
    ),
    dict(
        id="osteite_alveolar",
        nome="Osteite Alveolar (Alveolo Seco)",
        categoria="osteomielite",
        resumo="Perda do coagulo pos-exodontia; dor forte com odor fetido em 3-4 dias.",
        clinico="Tambem chamada alveolite. Perda/destruicao precoce do coagulo sanguineo apos "
                "exodontia, impedindo a cicatrizacao normal do alveolo. Dor ACENTUADA que surge "
                "3 a 4 dias apos a extracao, com odor fetido; osso exposto muito sensivel a "
                "sondagem.",
        localizacao="Mais frequente na regiao POSTERIOR da mandibula, principalmente apos "
                    "extracao de terceiros molares inferiores (20-25% dessas extracoes).",
        etiologia="Terceiros molares profundamente impactados, higiene bucal inadequada, "
                  "cirurgioes inexperientes, extracoes traumaticas, uso de contraceptivos orais, "
                  "tabagismo (20% em fumantes de 1 maco/dia, ate 40% se fumar nas 24h "
                  "pos-cirurgia), irrigacao inadequada, succao/cuspir excessivo, infeccao "
                  "pre-operatoria (pericoronarite).",
        sintomas="Dor intensa que pode irradiar para ouvido, regiao temporal ou olho; odor fetido; "
                 "trismo; tumefacao/linfadenopatia (menos comuns); sinais e sintomas duram de 10 a "
                 "40 dias sem tratamento.",
        testes="Sondagem do alveolo revela osso exposto e sensivel, sem coagulo.",
        radiografico="Solicitada para descartar fragmento dentario ou corpo estranho retido no "
                     "alveolo.",
        tratamento="NAO curetar o alveolo (aumenta a dor); irrigacao com solucao salina, remocao "
                   "de suturas se necessario, curativo alveolar sedativo, analgesicos potentes, "
                   "orientacao de higiene local.",
        diferenciar="Osteomielite: a osteite alveolar fica restrita ao alveolo pos-extracao (sem "
                    "destruicao ossea profunda/sequestro), enquanto a osteomielite envolve infeccao "
                    "ossea verdadeira com possivel sequestro.",
        aparencia_curta="Alveolo vazio, osso exposto, odor fetido",
        causa_curta="Perda do coagulo pos-exodontia (tabagismo, trauma)",
        tratamento_curto="Irrigacao + curativo sedativo (NAO curetar)",
        diagram=dict(kind="tooth", dry_socket=True),
    ),
]

DISEASE_BY_ID = {d["id"]: d for d in DISEASES}

# ----------------------------------------------------------------------
# BANCO DE QUESTOES (quiz)
# ----------------------------------------------------------------------
def _img_q(qid, disease_id, distractors, explain=None):
    d = DISEASE_BY_ID[disease_id]
    return dict(id=qid, kind="image", disease=disease_id,
                prompt="Com base no esquema (tipo radiografia anotada), qual o diagnostico mais provavel?",
                options=[d["nome"]] + distractors,
                correct_label=d["nome"],
                explain=explain or d["diferenciar"])


def _txt_q(qid, prompt, options, answer_nome, explain):
    return dict(id=qid, kind="text", disease=None, prompt=prompt,
                options=options, correct_label=answer_nome, explain=explain)


QUIZ = [
    _img_q("qi01", "pulpite_reversivel",
           ["Pulpite Irreversivel", "Periodontite Apical Aguda (Pericementite)", "Necrose Pulpar"]),
    _img_q("qi02", "pulpite_irreversivel",
           ["Pulpite Reversivel", "Pulpite Cronica Hiperplasica (Polipo Pulpar)", "Osteite Condensante"]),
    _img_q("qi03", "pulpite_hiperplasica",
           ["Pulpite Irreversivel", "Granuloma Periapical (Periodontite Apical Cronica)", "Necrose Pulpar"]),
    _img_q("qi04", "necrose_pulpar",
           ["Pulpite Reversivel", "Calcificacoes Pulpares (Denticulos / Calculos)", "Pulpite Irreversivel"]),
    _img_q("qi05", "calcificacoes_pulpares",
           ["Necrose Pulpar", "Osteite Condensante", "Pulpite Irreversivel"]),
    _img_q("qi06", "periodontite_apical_aguda",
           ["Abscesso Periapical Agudo", "Granuloma Periapical (Periodontite Apical Cronica)", "Pulpite Irreversivel"]),
    _img_q("qi07", "abscesso_periapical_agudo",
           ["Periodontite Apical Aguda (Pericementite)", "Abscesso Periapical Cronico", "Celulite Facial"]),
    _img_q("qi08", "granuloma_periapical",
           ["Cisto Radicular (Periapical)", "Abscesso Periapical Cronico", "Osteite Condensante"]),
    _img_q("qi09", "cisto_radicular",
           ["Granuloma Periapical (Periodontite Apical Cronica)", "Cisto Residual", "Abscesso Periapical Cronico"]),
    _img_q("qi10", "cisto_radicular_lateral",
           ["Cisto Radicular (Periapical)", "Cisto Residual", "Periodontite Apical Aguda (Pericementite)"]),
    _img_q("qi11", "cisto_residual",
           ["Cisto Radicular (Periapical)", "Cisto Radicular Lateral", "Granuloma Periapical (Periodontite Apical Cronica)"]),
    _img_q("qi12", "abscesso_periapical_cronico",
           ["Granuloma Periapical (Periodontite Apical Cronica)", "Cisto Radicular (Periapical)", "Abscesso Periapical Agudo"]),
    _img_q("qi13", "celulite_facial",
           ["Trombose do Seio Cavernoso", "Angina de Ludwig", "Abscesso Periapical Agudo"]),
    _img_q("qi14", "trombose_seio_cavernoso",
           ["Celulite Facial", "Angina de Ludwig", "Osteomielite Supurativa Aguda"]),
    _img_q("qi15", "angina_ludwig",
           ["Celulite Facial", "Trombose do Seio Cavernoso", "Osteomielite Supurativa Cronica"]),
    _img_q("qi16", "osteomielite_aguda",
           ["Osteomielite Supurativa Cronica", "Osteite Condensante", "Osteite Alveolar (Alveolo Seco)"]),
    _img_q("qi17", "osteomielite_cronica",
           ["Osteomielite Supurativa Aguda", "Osteite Condensante", "Osteomielite com Periostite Proliferativa (Garre)"]),
    _img_q("qi18", "osteite_condensante",
           ["Osteomielite com Periostite Proliferativa (Garre)", "Osteomielite Supurativa Cronica", "Granuloma Periapical (Periodontite Apical Cronica)"]),
    _img_q("qi19", "osteomielite_garre",
           ["Osteite Condensante", "Osteomielite Supurativa Cronica", "Cisto Residual"]),
    _img_q("qi20", "osteite_alveolar",
           ["Osteomielite Supurativa Aguda", "Abscesso Periapical Agudo", "Periodontite Apical Aguda (Pericementite)"]),

    _txt_q("qt01",
           "Paciente de 23 anos sente dor aguda no dente 34 ao tomar refrigerante gelado, sem edema facial "
           "e sem febre. A dor cessa imediatamente apos ela parar de beber. Qual o diagnostico mais provavel?",
           ["Pulpite Reversivel", "Pulpite Irreversivel", "Periodontite Apical Aguda (Pericementite)", "Necrose Pulpar"],
           "Pulpite Reversivel",
           "Dor CURTA e provocada pelo frio que CESSA ao remover o estimulo e o criterio classico de pulpite reversivel."),
    _txt_q("qt02",
           "Mesmo paciente do caso anterior, mas agora a dor NAO cessa ao parar de beber e continua latejando "
           "por horas, piorando quando ela deita. Qual a nova hipotese?",
           ["Pulpite Irreversivel", "Pulpite Reversivel", "Granuloma Periapical (Periodontite Apical Cronica)", "Osteite Alveolar (Alveolo Seco)"],
           "Pulpite Irreversivel",
           "Dor que CONTINUA apos remover o estimulo, piora ao deitar e pode ser espontanea define pulpite irreversivel."),
    _txt_q("qt03",
           "Crianca de 12 anos tem dor difusa e intensa na regiao superior esquerda, espontanea, que piora com "
           "quente e alivia com frio; ha extensa destruicao coronal no dente 26, sem edema facial ou febre. "
           "Qual a hipotese mais provavel?",
           ["Pulpite Irreversivel", "Pulpite Reversivel", "Abscesso Periapical Agudo", "Periodontite Apical Aguda (Pericementite)"],
           "Pulpite Irreversivel",
           "Dor espontanea, dificil de localizar (difusa), que piora com calor e alivia com frio e o quadro classico de pulpite irreversivel avancada."),
    _txt_q("qt04",
           "No caso anterior, por que o paciente NAO consegue apontar exatamente qual dente doi?",
           ["Porque nos estagios avancados da pulpite irreversivel a dor se torna difusa (fibras nervosas pulpares nao localizam bem o estimulo)",
            "Porque o nervo alveolar inferior foi anestesiado",
            "Porque ha uma fratura radicular associada",
            "Porque o paciente tem neuralgia do trigemeo"],
           "Porque nos estagios avancados da pulpite irreversivel a dor se torna difusa (fibras nervosas pulpares nao localizam bem o estimulo)",
           "Nos estagios iniciais o dente e facilmente identificado; com a evolucao da pulpite irreversivel a dor passa a ser difusa e mal localizada."),
    _txt_q("qt05",
           "Mulher de 38 anos, diabetica tipo I nao controlada, tem dor pulsatil intensa no dente 37 ha 1 dia, "
           "nao consegue comer nem dormir, com edema facial cervical iniciado ha 3h, febre de 37.8C e sem "
           "alteracao radiografica. Qual a hipotese mais provavel?",
           ["Abscesso Periapical Agudo com celulite facial", "Trombose do Seio Cavernoso", "Angina de Ludwig", "Granuloma Periapical (Periodontite Apical Cronica)"],
           "Abscesso Periapical Agudo com celulite facial",
           "Dor pulsatil aguda + edema facial evoluindo rapido + febre baixa + diabetes descompensada = abscesso periapical agudo se disseminando como celulite; sem sinais oculares (nao e trombose) nem obstrucao de via aerea (nao e Ludwig)."),
    _txt_q("qt06",
           "No caso da paciente diabetica, qual conduta inicial esta CORRETA?",
           ["Abrir o dente endodonticamente, prescrever antibiotico e analgesico, e reavaliar diariamente",
            "Apenas prescrever analgesico e aguardar reducao espontanea do edema",
            "Extrair o dente imediatamente sem qualquer medicacao",
            "Encaminhar direto para cirurgia de drenagem do seio cavernoso"],
           "Abrir o dente endodonticamente, prescrever antibiotico e analgesico, e reavaliar diariamente",
           "Paciente sistemicamente debilitada (diabetes + febre) exige antibioticoterapia associada ao tratamento odontologico do foco, com reavaliacao diaria."),
    _txt_q("qt07",
           "Radiografia de rotina mostra uma imagem radiolucida arredondada e BEM delimitada de 1 cm no apice "
           "de um pre-molar inferior desvitalizado, em paciente assintomatico. Qual exame CONFIRMA o "
           "diagnostico definitivo (granuloma x cisto)?",
           ["Exame histopatologico do tecido removido", "Nova radiografia periapical", "Teste de vitalidade pulpar", "Tomografia computadorizada"],
           "Exame histopatologico do tecido removido",
           "Granuloma e cisto radicular podem ter imagem radiografica identica; a distincao definitiva depende da presenca de revestimento epitelial, visto so na histopatologia."),
    _txt_q("qt08",
           "Paciente com fistula intraoral persistente proxima ao apice de um dente com necrose pulpar, sem "
           "dor, e radiografia mostrando radioluscencia com limites MAL definidos. Qual o diagnostico mais "
           "provavel?",
           ["Abscesso Periapical Cronico", "Granuloma Periapical (Periodontite Apical Cronica)", "Cisto Radicular (Periapical)", "Osteomielite Supurativa Cronica"],
           "Abscesso Periapical Cronico",
           "Contorno radiolucido MAL definido + fistula ativa + ausencia de dor e o padrao do abscesso periapical cronico (granuloma/cisto tem contorno bem definido)."),
    _txt_q("qt09",
           "Tres dias apos a exodontia de um terceiro molar inferior, um paciente fumante relata dor forte "
           "irradiando para o ouvido, com odor fetido e alveolo vazio (sem coagulo) e muito sensivel a "
           "sondagem. Qual o diagnostico?",
           ["Osteite Alveolar (Alveolo Seco)", "Osteomielite Supurativa Aguda", "Abscesso Periapical Agudo", "Pericoronarite"],
           "Osteite Alveolar (Alveolo Seco)",
           "Dor de inicio em 3-4 dias, odor fetido e alveolo sem coagulo (osso exposto e sensivel) sao classicos de alveolite, favorecida pelo tabagismo."),
    _txt_q("qt10",
           "No caso do alveolo seco, qual conduta esta CORRETA?",
           ["Irrigar com solucao salina e usar curativo sedativo, sem curetar o alveolo",
            "Curetar bem o alveolo para remover todo o tecido residual",
            "Prescrever apenas antibiotico sistemico, sem qualquer manejo local",
            "Realizar nova extracao do dente adjacente"],
           "Irrigar com solucao salina e usar curativo sedativo, sem curetar o alveolo",
           "A curetagem do alveolo seco e contraindicada por aumentar a dor; o manejo e irrigacao suave, curativo sedativo e analgesia potente."),
    _txt_q("qt11",
           "Adolescente de 13 anos apresenta aumento de volume assimetrico e indolor na mandibula; a "
           "tomografia mostra camadas osseas radiopacas paralelas ('casca de cebola') associadas a um molar "
           "cariado. Qual o diagnostico?",
           ["Osteomielite com Periostite Proliferativa (Garre)", "Osteite Condensante", "Osteomielite Supurativa Cronica", "Cisto Residual"],
           "Osteomielite com Periostite Proliferativa (Garre)",
           "Laminacoes radiopacas paralelas expandindo a cortical, em paciente jovem, sao o achado classico da osteomielite de Garre."),
    _txt_q("qt12",
           "Achado radiografico casual em jovem assintomatico: area radiopaca BEM definida e uniforme, SEM "
           "expansao ossea, junto ao apice de um pre-molar inferior com carie profunda. Qual o diagnostico?",
           ["Osteite Condensante", "Osteomielite com Periostite Proliferativa (Garre)", "Osteomielite Supurativa Cronica", "Granuloma Periapical (Periodontite Apical Cronica)"],
           "Osteite Condensante",
           "Radiopacidade uniforme, sem expansao, junto ao apice de dente com pulpite/necrose, indolor e achado casual: osteite condensante."),
    _txt_q("qt13",
           "Paciente com infeccao odontogenica evoluindo ha 2 meses, fistula cutanea, fragmentos osseos "
           "radiopacos soltos (sequestros) na radiografia e dor moderada. Qual o diagnostico?",
           ["Osteomielite Supurativa Cronica", "Osteomielite Supurativa Aguda", "Osteite Condensante", "Osteite Alveolar (Alveolo Seco)"],
           "Osteomielite Supurativa Cronica",
           "Evolucao maior que 1 mes, fistula e sequestros osseos caracterizam a forma cronica (a aguda dura menos de 1 mes e e mais intensa)."),
    _txt_q("qt14",
           "Paciente evolui apos abscesso dentario nao tratado com edema periorbitario BILATERAL, protrusao e "
           "FIXACAO do globo ocular, febre alta e cefaleia. Qual o diagnostico e a conduta?",
           ["Trombose do Seio Cavernoso - emergencia hospitalar com drenagem cirurgica e antibiotico em altas doses",
            "Celulite Facial - antibiotico oral ambulatorial",
            "Angina de Ludwig - manutencao de via aerea prioritaria",
            "Osteomielite Supurativa Aguda - antibiotico e drenagem odontologica"],
           "Trombose do Seio Cavernoso - emergencia hospitalar com drenagem cirurgica e antibiotico em altas doses",
           "Edema periorbitario BILATERAL com protrusao/fixacao ocular e sinal de alarme para trombose do seio cavernoso, emergencia com alta mortalidade se nao tratada rapido."),
    _txt_q("qt15",
           "Paciente com infeccao de molar inferior evolui com tumefacao bilateral do assoalho da boca, "
           "lingua elevada, dificuldade para respirar e necessidade de ficar sentado ereto. Qual o "
           "diagnostico e a prioridade de tratamento?",
           ["Angina de Ludwig - manter via aerea e depois drenar/tratar o foco",
            "Celulite Facial - antibiotico oral e observacao",
            "Trombose do Seio Cavernoso - avaliacao oftalmologica",
            "Abscesso Periapical Cronico - endodontia eletiva"],
           "Angina de Ludwig - manter via aerea e depois drenar/tratar o foco",
           "Tumefacao bilateral do assoalho bucal com elevacao da lingua e sinais de obstrucao respiratoria e Angina de Ludwig: a prioridade SEMPRE e garantir a via aerea."),
]

# categoria explicita para questoes de vinheta cujo texto da resposta correta
# nao bate literalmente com o nome da doenca (evita cair em "geral" no filtro)
_TXT_CATEGORY = {
    "qt01": "pulpar", "qt02": "pulpar", "qt03": "pulpar", "qt04": "pulpar",
    "qt05": "periapical_aguda", "qt06": "periapical_aguda",
    "qt07": "periapical_cronica", "qt08": "periapical_cronica",
    "qt09": "osteomielite", "qt10": "osteomielite", "qt11": "osteomielite",
    "qt12": "osteomielite", "qt13": "osteomielite",
    "qt14": "disseminacao", "qt15": "disseminacao",
}
for _q in QUIZ:
    if _q["id"] in _TXT_CATEGORY:
        _q["categoria"] = _TXT_CATEGORY[_q["id"]]

# embaralha as alternativas de cada questao (seed fixa = reprodutivel), para
# que o gabarito nao seja sempre a primeira opcao
import random as _random
_rng = _random.Random(20240817)
for _q in QUIZ:
    _opts = list(_q["options"])
    _rng.shuffle(_opts)
    _q["options"] = _opts

