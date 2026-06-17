"""Transforma os pares início/final no contexto consumido pelo template.

Esta é a "cola" entre o domínio (`PairingResult`) e o template .xlsx no formato
da aba "Comparativo": por item, as métricas KOD/E-level/Shape com início, final
e evolução. A evolução respeita o sinal de cada métrica (Shape é invertida —
ver `models.evolucao`).

O contexto é um dicionário **indexado pelo nome de exibição do item**, que é a
chave usada pelo renderer para casar cada item com a sua linha no template.
"""

from __future__ import annotations

from .models import METRICS, evolucao
from .pairing import PairingResult


def build_context(result: PairingResult) -> dict[str, dict[str, dict[str, float]]]:
    """Monta o contexto `{item: {métrica: {inicio, final, evolucao}}}`.

    Só os pares casados (presentes nos dois períodos) entram; itens exclusivos
    de um período ficam de fora (sem início ou sem final para comparar).
    """
    context: dict[str, dict[str, dict[str, float]]] = {}
    for par in result.pairs:
        context[par.nome] = {
            metric: {
                "inicio": par.inicio[metric],
                "final": par.final[metric],
                "evolucao": evolucao(metric, par.inicio[metric], par.final[metric]),
            }
            for metric in METRICS
        }
    return context
