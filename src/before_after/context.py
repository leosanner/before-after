"""Transforma os pares início/final no contexto consumido pelo template.

Esta é a "cola" entre o domínio (PairingResult) e o template .docx, no formato
da aba "Comparativo": por item, as métricas KOD/E-level/Shape com início, final
e evolução (final - início).

Os nomes das chaves aqui devem casar com os placeholders Jinja do template.
"""

from __future__ import annotations

from .pairing import PairingResult


def build_context(result: PairingResult) -> dict:
    """Monta o dicionário de contexto para o `DocxTemplate.render`."""
    # TODO: definir o formato junto com o template real (etapa final).
    raise NotImplementedError("TODO: mapear PairingResult -> contexto do template")
