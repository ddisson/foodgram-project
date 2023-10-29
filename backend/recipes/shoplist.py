import io
import os

from django.http import FileResponse
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

FONTS_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
FONT_NAME = 'arial'
FONT_PATH = os.path.join(FONTS_ROOT, 'arial.ttf')
pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))

HEADER_FONT_SIZE = 30
HEADER_TOP_MARGIN = 20
HEADER_BOTTOM_MARGIN = 35

BODY_FONT_SIZE = 16
BODY_LINE_SPACING = 10

TEXT_MARGINS = {
    'top': 10,
    'bottom': 12,
    'right': 12,
    'left': 50
}

SPACER = 1


def create_paragraph(text, size, alignment=TA_LEFT, font=FONT_NAME):
    return Paragraph(
        text, ParagraphStyle(
            fontName=font,
            fontSize=size,
            alignment=alignment)
    )


def add_header_to_document(document, title):
    document.append(Spacer(SPACER, HEADER_TOP_MARGIN))
    document.append(create_paragraph(title, HEADER_FONT_SIZE, TA_CENTER))
    document.append(Spacer(SPACER, HEADER_BOTTOM_MARGIN))
    return document


def add_body_to_document(document, text_lines):
    for line in text_lines:
        document.append(create_paragraph(line, BODY_FONT_SIZE))
        document.append(Spacer(SPACER, BODY_LINE_SPACING))
    return document


def download_shopping_list(data):
    buffer = io.BytesIO()

    document = add_header_to_document([], 'Список покупок')
    add_body_to_document(document, data)

    pdf = SimpleDocTemplate(buffer, pagesize=A4, **TEXT_MARGINS)
    pdf.build(document)

    buffer.seek(0)
    return FileResponse(
        buffer, as_attachment=True,
        filename='shopping_list.pdf'
    )
