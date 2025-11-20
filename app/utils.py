from flask import render_template # type: ignore
from xhtml2pdf import pisa # type: ignore
from io import BytesIO


def render_pdf_from_template(template_name: str, **context) -> bytes:
    html = render_template(template_name, **context)
    pdf_io = BytesIO()
    pisa.CreatePDF(src=html, dest=pdf_io)  
    return pdf_io.getvalue()


