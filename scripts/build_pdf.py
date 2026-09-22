# -*- coding: utf-8 -*-
"""Gera o PDF de revisao (tabela para impressao) - Doencas da Polpa e Periapice."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import pathdata as pd
import accents

accents.patch_pathdata(pd)

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak,
    Flowable, KeepTogether, HRFlowable,
)

OUT = os.path.join(os.path.dirname(__file__), "..", "Guia_Revisao_Doencas_Polpa_Periapice.pdf")

INK = HexColor("#1c2420")
INK_SOFT = HexColor("#5b6a62")
PAPER = HexColor("#faf8f2")
ACCENT = HexColor("#0f6e5c")
WARN = HexColor("#a8402f")
GOLD = HexColor("#96731a")
LINE = HexColor("#d8d2c0")
ROW_ALT = HexColor("#f1efe4")

CAT_HEX = {
    "pulpar": "#0f6e5c",
    "periapical_aguda": "#a8402f",
    "periapical_cronica": "#96731a",
    "disseminacao": "#7a2f3a",
    "osteomielite": "#3d5a73",
}
CAT_COLOR = {k: HexColor(v) for k, v in CAT_HEX.items()}

styleN = ParagraphStyle("N", fontName="Helvetica", fontSize=7.6, leading=9.4, textColor=INK)
styleB = ParagraphStyle("B", fontName="Helvetica-Bold", fontSize=8.2, leading=10, textColor=INK)
styleSmall = ParagraphStyle("S", fontName="Helvetica-Oblique", fontSize=7, leading=8.6, textColor=INK_SOFT)
styleHead = ParagraphStyle("H", fontName="Helvetica-Bold", fontSize=8.6, leading=10, textColor=HexColor("#ffffff"))


class IconFlowable(Flowable):
    """Embrulha um Drawing (icone vetorial) como Flowable de celula de tabela."""

    def __init__(self, shapes, vb, size):
        super().__init__()
        self.drawing = pd.shapes_to_drawing(shapes, vb, size)
        self.width = size
        self.height = size * vb[1] / vb[0]

    def draw(self):
        self.drawing.drawOn(self.canv, 0, 0)


def icon_for(d, size=46):
    shapes, vb = pd.build_diagram_shapes(d["diagram"])
    return IconFlowable(shapes, vb, size)


def cover_flowables():
    story = []
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("DOENÇAS DA POLPA E DO PERIÁPICE", ParagraphStyle(
        "Title", fontName="Helvetica-Bold", fontSize=25, leading=28, textColor=INK)))
    story.append(Paragraph("Guia de revisão para prova — Patologia Bucal (UNESC)", ParagraphStyle(
        "Sub", fontName="Helvetica-Oblique", fontSize=12.5, leading=16, textColor=INK_SOFT, spaceBefore=4)))
    story.append(Spacer(1, 3 * mm))
    story.append(HRFlowable(width="100%", thickness=1.4, color=ACCENT, spaceAfter=6))
    story.append(Paragraph(
        "Baseado nos slides \"Doenças da Polpa e Periápice\" (Profa. Ângela Catarina Maragno) e no gabarito "
        "da Atividade Discente 1 da disciplina de Patologia Bucal. Cobre as aulas de 10/08, 17/08 e 24/08.",
        styleN))
    story.append(Spacer(1, 5 * mm))

    story.append(Paragraph("COMO LER OS ESQUEMAS", styleB))
    story.append(Paragraph(
        "Cada linha traz um esquema autoral no padrão \"raio-X anotado\" — o mesmo código visual usado em "
        "aula para descrever características radiográficas (radiolúcido × radiopaco, contorno bem × mal "
        "definido). Não são fotografias clínicas.",
        styleN))
    story.append(Spacer(1, 2 * mm))

    legend_rows = [
        [IconFlowable(pd.tooth_diagram(pulp="severe", caries=2), pd.VB_TOOTH, 30),
         Paragraph("<b>Laranja/vermelho na polpa</b> = inflamação pulpar vital (mais escuro = mais intenso).", styleN)],
        [IconFlowable(pd.tooth_diagram(pulp="necrotic", caries=2), pd.VB_TOOTH, 30),
         Paragraph("<b>Cinza-escuro na polpa/canal</b> = necrose pulpar (sem vitalidade).", styleN)],
        [IconFlowable(pd.tooth_diagram(pulp="necrotic", apex="granuloma"), pd.VB_TOOTH, 30),
         Paragraph("<b>Círculo escuro de contorno nítido no ápice</b> = radiolúcido bem definido (granuloma/cisto).", styleN)],
        [IconFlowable(pd.tooth_diagram(pulp="necrotic", apex="abscess_acute"), pd.VB_TOOTH, 30),
         Paragraph("<b>Mancha escura irregular no ápice</b> = radiolúcido mal definido, agudo (abscesso).", styleN)],
        [IconFlowable(pd.tooth_diagram(pulp="necrotic", apex="condensing"), pd.VB_TOOTH, 30),
         Paragraph("<b>Área clara/densa</b> = radiopaco (osteíte condensante, sequestro, Garré).", styleN)],
    ]
    t = Table(legend_rows, colWidths=[13 * mm, 150 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(t)
    story.append(Spacer(1, 6 * mm))

    story.append(Paragraph("CATEGORIAS", styleB))
    cat_rows = []
    for cid, label in pd.CATEGORIES:
        n = sum(1 for d in pd.DISEASES if d["categoria"] == cid)
        cat_rows.append([
            Paragraph(f'<font color="{CAT_HEX[cid]}"><b>&#9632;</b></font> {label}', styleN),
            Paragraph(f"{n} entidades", styleSmall),
        ])
    tc = Table(cat_rows, colWidths=[130 * mm, 33 * mm])
    tc.setStyle(TableStyle([("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 2)]))
    story.append(tc)
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph(
        "Perguntas-chave de anamnese (repita para cada caso clínico): dor provocada ou espontânea? "
        "o paciente sabe localizar o dente? há sensibilidade à percussão? há expressão radiográfica? "
        "há sintomatologia sistêmica (febre, mal-estar)? o paciente está debilitado sistemicamente "
        "(ex.: diabetes)? houve procedimento odontológico recente?",
        ParagraphStyle("box", fontName="Helvetica", fontSize=8.4, leading=11.5, textColor=INK,
                       borderColor=LINE, borderWidth=0.8, borderPadding=6, backColor=ROW_ALT)))
    story.append(PageBreak())
    return story


def table_for_category(cid, label):
    header = [
        Paragraph("Esquema", styleHead), Paragraph("Doença", styleHead),
        Paragraph("Aparência clínica / achado-chave", styleHead),
        Paragraph("Como diferenciar", styleHead),
        Paragraph("Localização", styleHead), Paragraph("Causa / etiologia", styleHead),
        Paragraph("Tratamento", styleHead),
    ]
    rows = [header]
    for d in pd.DISEASES:
        if d["categoria"] != cid:
            continue
        rows.append([
            icon_for(d, size=42),
            Paragraph(d["nome"], styleB),
            Paragraph(d["aparencia_curta"], styleN),
            Paragraph(d["diferenciar"], styleN),
            Paragraph(d["localizacao"], styleN),
            Paragraph(d["causa_curta"], styleN),
            Paragraph(d["tratamento_curto"], styleN),
        ])

    col_widths = [15 * mm, 30 * mm, 46 * mm, 52 * mm, 38 * mm, 38 * mm, 40 * mm]
    t = Table(rows, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), CAT_COLOR[cid]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 1), (0, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(rows)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
    t.setStyle(TableStyle(style))
    return t


def build():
    doc = SimpleDocTemplate(
        OUT, pagesize=landscape(A4),
        leftMargin=14 * mm, rightMargin=14 * mm, topMargin=12 * mm, bottomMargin=12 * mm,
        title="Guia de Revisao - Doencas da Polpa e Periapice",
        author="Patologia Bucal - UNESC",
    )
    story = []
    story.extend(cover_flowables())
    for i, (cid, label) in enumerate(pd.CATEGORIES):
        story.append(Paragraph(label.upper(), ParagraphStyle(
            "CatTitle", fontName="Helvetica-Bold", fontSize=13, leading=16,
            textColor=CAT_COLOR[cid], spaceAfter=4)))
        story.append(table_for_category(cid, label))
        if i < len(pd.CATEGORIES) - 1:
            story.append(PageBreak())

    story.append(PageBreak())
    story.append(Paragraph("BANCO DE QUESTÕES — CASOS CLÍNICOS (para autoavaliação)", ParagraphStyle(
        "QTitle", fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=ACCENT, spaceAfter=6)))
    for q in pd.QUIZ:
        if q["kind"] != "text":
            continue
        opts = "  ".join(f"({chr(97+i)}) {o}" for i, o in enumerate(q["options"]))
        story.append(KeepTogether([
            Paragraph(q["prompt"], ParagraphStyle("qp", fontName="Helvetica-Bold", fontSize=8.6,
                                                    leading=11, textColor=INK, spaceBefore=6)),
            Paragraph(opts, styleN),
        ]))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("GABARITO", styleB))
    gab = []
    for q in pd.QUIZ:
        if q["kind"] != "text":
            continue
        idx = q["options"].index(q["correct_label"])
        gab.append(f"{q['id'][-2:]}: ({chr(97+idx)})")
    story.append(Paragraph("   ".join(gab), styleN))

    doc.build(story)
    print("PDF gerado em:", os.path.abspath(OUT))


if __name__ == "__main__":
    build()
