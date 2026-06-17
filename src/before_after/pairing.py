"""Pareamento dos itens entre os períodos de início e final.

Recebe duas tabelas já tratadas (`correspondence.prepare`) e monta, por item
presente nos dois períodos, um `ItemPair` com as métricas de cada lado.
Itens presentes em só um dos períodos são reportados à parte.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from .models import METRICS, ItemPair


@dataclass
class PairingResult:
    """Pares casados + itens exclusivos de cada período."""

    pairs: list[ItemPair] = field(default_factory=list)
    only_in_inicio: list[str] = field(default_factory=list)
    only_in_final: list[str] = field(default_factory=list)


def build_pairs(
    inicio: pd.DataFrame,
    final: pd.DataFrame,
    *,
    metrics: list[str] = METRICS,
) -> PairingResult:
    """Casa `inicio` e `final` (indexados por item) em pares {nome, inicio, final}.

    Args:
        inicio: frame tratado do período inicial, indexado pelo nome do item.
        final: frame tratado do período final, indexado pelo nome do item.
        metrics: colunas de métrica a carregar em cada lado do par.

    Returns:
        PairingResult com os pares em comum (ordenados por nome) e os itens
        exclusivos de cada período.
    """
    nomes_inicio, nomes_final = set(inicio.index), set(final.index)
    comuns = sorted(nomes_inicio & nomes_final)

    pairs = [
        ItemPair(
            nome=nome,
            inicio={m: inicio.at[nome, m] for m in metrics},
            final={m: final.at[nome, m] for m in metrics},
        )
        for nome in comuns
    ]
    return PairingResult(
        pairs=pairs,
        only_in_inicio=sorted(nomes_inicio - nomes_final),
        only_in_final=sorted(nomes_final - nomes_inicio),
    )
