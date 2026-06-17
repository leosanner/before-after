"""Renderização do documento final a partir de um template .docx + contexto."""

from __future__ import annotations

import io
from typing import IO

from docxtpl import DocxTemplate


def render(template: str | IO[bytes], context: dict) -> bytes:
    """Renderiza o template com o contexto e devolve os bytes do .docx.

    `template` aceita caminho ou file-like, então funciona tanto para um
    template versionado em `templates/` quanto para upload via UI.
    """
    doc = DocxTemplate(template)
    doc.render(context)

    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer.getvalue()
