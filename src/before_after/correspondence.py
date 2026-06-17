"""Correspondência e tratamento dos dados de entrada.

Recebe uma tabela crua (como `dados_inicio` / `dados_final`), resolve o(s)
nome(s) de exibição ("Item") via `correspondencia.json` e devolve uma tabela
limpa, com uma linha por item, pronta para o pareamento.

A correspondência é 1-para-N: uma linha de entrada pode gerar vários itens
sinônimos (ex.: ``ADRENALINA`` → Adrenalina + Noradrenalina). Quando mais de
uma linha alimenta o mesmo item (duplicatas), as métricas são **somadas** —
regra extraída do Comparativo da equipe. O mesmo mecanismo (explode + soma)
cobre os dois casos.

Linhas cujo nome não casa com o mapa (ex: descrições de imagem/secção que não
existem no Comparativo) são descartadas e reportadas à parte.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from .models import METRICS
from .normalization import resolve

# Coluna da entrada que carrega o nome cru vindo do Oberon.
SOURCE_COLUMN = "SECÇÃO / ORGÃO / DESIGNAÇÃO"

# Nome da coluna canônica criada após a resolução.
ITEM_COLUMN = "item"


@dataclass
class Prepared:
    """Resultado do tratamento de uma tabela de entrada."""

    frame: pd.DataFrame  # uma linha por item (índice = `ITEM_COLUMN`), métricas somadas
    unmatched: list[str] = field(default_factory=list)  # nomes crus sem correspondência
    aggregated: dict[str, int] = field(default_factory=dict)  # item -> nº de linhas somadas


def prepare(
    df: pd.DataFrame,
    mapping: dict,
    *,
    source_column: str = SOURCE_COLUMN,
    metrics: list[str] = METRICS,
) -> Prepared:
    """Resolve nomes (1-para-N), descarta não-casados e soma métricas por item.

    Args:
        df: tabela crua de um período (início ou final).
        mapping: mapa de `correspondencia.json`.
        source_column: coluna com o nome cru do Oberon.
        metrics: colunas numéricas a somar por item.

    Returns:
        Prepared com o frame tratado (índice = item, métricas somadas) e
        relatórios de não-casados e de itens montados a partir de várias linhas.
    """
    if source_column not in df.columns:
        raise KeyError(f"Coluna-fonte ausente: {source_column!r}")

    work = df.copy()
    items = work[source_column].map(lambda v: resolve(v, mapping))

    unmatched = sorted(
        {str(raw).strip() for raw, its in zip(work[source_column], items) if not its}
    )

    work[ITEM_COLUMN] = items
    exploded = work[items.map(len) > 0].explode(ITEM_COLUMN)

    counts = exploded[ITEM_COLUMN].value_counts()
    aggregated = {item: int(n) for item, n in counts.items() if n > 1}

    frame = exploded.groupby(ITEM_COLUMN)[metrics].sum()
    return Prepared(frame=frame, unmatched=unmatched, aggregated=aggregated)
