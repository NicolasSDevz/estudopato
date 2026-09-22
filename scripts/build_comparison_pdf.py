# -*- coding: utf-8 -*-
"""Gera a PLANILHA COMPARATIVA (PDF) - uma tabela detalhada, por categoria,
com colunas padronizadas (dor, mobilidade, percussao, necrose, vitalidade,
radiografia, caracteristica-chave) para comparar rapidamente todas as
doencas da polpa e do periapice lado a lado. Formato inspirado em planilhas
de revisao ("compare patologias"), pensado para impressao e consulta rapida."""
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
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, HRFlowable,
)

OUT = os.path.join(os.path.dirname(__file__), "..", "Planilha_Comparativa_Patologias.pdf")

INK = HexColor("#1c2420")
INK_SOFT = HexColor("#5b6a62")
LINE = HexColor("#d8d2c0")
ROW_ALT = HexColor("#f5f3e9")
WHITE = HexColor("#ffffff")

CAT_HEX = {
    "pulpar": "#0f6e5c",
    "periapical_aguda": "#a8402f",
    "periapical_cronica": "#96731a",
    "disseminacao": "#7a2f3a",
    "osteomielite": "#3d5a73",
}
CAT_SOFT_HEX = {
    "pulpar": "#e2f3ee",
    "periapical_aguda": "#fbe9e4",
    "periapical_cronica": "#f8f0da",
    "disseminacao": "#f6e6ea",
    "osteomielite": "#e7edf4",
}
CAT_COLOR = {k: HexColor(v) for k, v in CAT_HEX.items()}
CAT_SOFT = {k: HexColor(v) for k, v in CAT_SOFT_HEX.items()}

styleCell = ParagraphStyle("cell", fontName="Helvetica", fontSize=7.3, leading=9, textColor=INK)
styleCellB = ParagraphStyle("cellB", fontName="Helvetica-Bold", fontSize=7.6, leading=9.3, textColor=INK)
styleName = ParagraphStyle("name", fontName="Helvetica-Bold", fontSize=8, leading=9.6, textColor=INK)
styleHead = ParagraphStyle("head", fontName="Helvetica-Bold", fontSize=7.6, leading=9, textColor=WHITE)


def cover():
    story = []
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("PLANILHA COMPARATIVA — DOENÇAS DA POLPA E DO PERIÁPICE", ParagraphStyle(
        "T", fontName="Helvetica-Bold", fontSize=21, leading=24, textColor=INK)))
    story.append(Paragraph(
        "Compare rapidamente dor, mobilidade, percussão, necrose, teste de vitalidade, radiografia e o "
        "achado-chave de cada uma das 20 entidades — organizado por categoria, para revisão de prova.",
        ParagraphStyle("Sub", fontName="Helvetica-Oblique", fontSize=11, leading=14, textColor=INK_SOFT, spaceBefore=4)))
    story.append(Spacer(1, 3 * mm))
    story.append(HRFlowable(width="100%", thickness=1.4, color=INK, spaceAfter=8))
    story.append(Paragraph(
        "Como usar: cubra as colunas da direita com a mão e tente responder pelo nome da doença; ou cubra o "
        "nome e tente adivinhar a doença pelas características. As cores das linhas seguem a categoria "
        "(legenda abaixo).", styleCell))
    story.append(Spacer(1, 3 * mm))
    legend = []
    for cid, label in pd.CATEGORIES:
        legend.append(Paragraph(f'<font color="{CAT_HEX[cid]}">&#9632;</font> {label}', styleCell))
    lt = Table([legend], colWidths=[52 * mm] * len(legend))
    lt.setStyle(TableStyle([("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    story.append(lt)
    story.append(Spacer(1, 5 * mm))
    return story


def table_for_category(cid, label):
    header = [
        Paragraph("Doença", styleHead),
        Paragraph("Dor / sintoma inicial", styleHead),
        Paragraph("Mobilidade", styleHead),
        Paragraph("Percussão", styleHead),
        Paragraph("Necrose", styleHead),
        Paragraph("Teste de vitalidade", styleHead),
        Paragraph("Radiografia", styleHead),
        Paragraph("Característica-chave", styleHead),
    ]
    rows = [header]
    for d in pd.DISEASES:
        if d["categoria"] != cid:
            continue
        rows.append([
            Paragraph(d["nome"], styleName),
            Paragraph(d.get("dor", ""), styleCell),
            Paragraph(d.get("mobilidade", ""), styleCell),
            Paragraph(d.get("percussao", ""), styleCell),
            Paragraph(d.get("necrose", ""), styleCell),
            Paragraph(d.get("vitalidade", ""), styleCell),
            Paragraph(d.get("radiografia_curta", ""), styleCell),
            Paragraph(d["aparencia_curta"], styleCellB),
        ])

    col_widths = [34 * mm, 36 * mm, 20 * mm, 20 * mm, 24 * mm, 30 * mm, 42 * mm, 44 * mm]
    t = Table(rows, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), CAT_COLOR[cid]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("BACKGROUND", (0, 1), (-1, -1), WHITE),
    ]
    for i in range(1, len(rows)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
    t.setStyle(TableStyle(style))
    return t


def build():
    doc = SimpleDocTemplate(
        OUT, pagesize=landscape(A4),
        leftMargin=12 * mm, rightMargin=12 * mm, topMargin=12 * mm, bottomMargin=12 * mm,
        title="Planilha Comparativa - Doencas da Polpa e Periapice",
        author="Patologia Bucal - UNESC",
    )
    story = []
    story.extend(cover())
    for i, (cid, label) in enumerate(pd.CATEGORIES):
        story.append(Paragraph(label.upper(), ParagraphStyle(
            "CatTitle", fontName="Helvetica-Bold", fontSize=12.5, leading=15,
            textColor=CAT_COLOR[cid], spaceAfter=4)))
        story.append(table_for_category(cid, label))
        story.append(Spacer(1, 6 * mm))
        if i < len(pd.CATEGORIES) - 1 and i % 2 == 1:
            story.append(PageBreak())

    doc.build(story)
    print("PDF gerado em:", os.path.abspath(OUT))


if __name__ == "__main__":
    build()
