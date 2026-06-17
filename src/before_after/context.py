"""Transforma o resultado da comparação no contexto consumido pelo template.

Esta é a "cola" entre o domínio (ComparisonResult) e o template .docx.
Os nomes das chaves aqui devem casar com os placeholders Jinja do template
(ex: {{ total_alteracoes }}, {% for linha in linhas %}).
"""

from __future__ import annotations

from .models import ComparisonResult


def build_context(result: ComparisonResult) -> dict:
    """Monta o dicionário de contexto para o `DocxTemplate.render`."""
    # TODO: definir o formato junto com o template real. Esqueleto inicial:
    raise NotImplementedError("TODO: mapear ComparisonResult -> contexto do template")
