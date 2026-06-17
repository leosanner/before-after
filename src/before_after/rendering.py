"""Preenche o template .xlsx (formato Comparativo) com o contexto do pipeline.

O template (`templates/comparativo.xlsx`, gerado por `scripts/build_template.py`)
traz a estrutura pronta — cabeçalho, agrupamento por Sistema e a coluna `Item` —
com as células numéricas vazias. Aqui casamos cada linha pelo nome do item e
escrevemos início/final/evolução de cada métrica, preservando estilo e formato.
"""

from __future__ import annotations

import io
from dataclasses import dataclass, field
from typing import IO

import openpyxl

from .models import METRICS

# Layout do template (1-based). A=Sistema, B=Item, depois 3 colunas por métrica.
ITEM_COL = 2
FIRST_DATA_ROW = 3
# Coluna inicial (início) de cada métrica; final = +1, evolução = +2.
METRIC_START_COL = {"KOD": 3, "E-level": 6, "Shape": 9}
# Aba oculta com a aplicabilidade por linha (ver scripts/build_template.py).
MASK_SHEET = "_aplicabilidade"


def _load_mask(wb) -> dict[int, set[str]] | None:
    """Lê a aba de aplicabilidade: linha do template -> métricas preenchíveis."""
    if MASK_SHEET not in wb.sheetnames:
        return None
    ws = wb[MASK_SHEET]
    rows = ws.iter_rows(values_only=True)
    header = next(rows, None)
    if header is None:
        return {}
    metrics = header[1:]
    return {
        int(row[0]): {m for m, flag in zip(metrics, row[1:]) if flag}
        for row in rows
        if row[0] is not None
    }


@dataclass
class RenderResult:
    """Bytes do .xlsx + relatório de itens que não casaram com o template."""

    data: bytes
    sem_dados: list[str] = field(default_factory=list)  # linhas do template sem item no contexto
    nao_colocados: list[str] = field(default_factory=list)  # itens do contexto ausentes no template


def render(template: str | IO[bytes], context: dict[str, dict[str, dict[str, float]]]) -> RenderResult:
    """Preenche o template com o contexto e devolve os bytes do .xlsx.

    `template` aceita caminho ou file-like. Itens com nome repetido no template
    (ex.: "Medula óssea", "Bexiga") recebem o mesmo valor em todas as linhas.
    """
    wb = openpyxl.load_workbook(template)
    mask = _load_mask(wb)
    if MASK_SHEET in wb.sheetnames:
        del wb[MASK_SHEET]  # mantém o documento final só com a aba visível
    ws = wb.active

    colocados: set[str] = set()
    sem_dados: list[str] = []

    for row in range(FIRST_DATA_ROW, ws.max_row + 1):
        nome = ws.cell(row, ITEM_COL).value
        if nome is None:
            continue
        nome = str(nome).strip()
        metrics = context.get(nome)
        if metrics is None:
            sem_dados.append(nome)
            continue
        aplicaveis = METRICS if mask is None else mask.get(row, METRICS)
        for metric in aplicaveis:
            col = METRIC_START_COL[metric]
            ws.cell(row, col).value = metrics[metric]["inicio"]
            ws.cell(row, col + 1).value = metrics[metric]["final"]
            ws.cell(row, col + 2).value = metrics[metric]["evolucao"]
        colocados.add(nome)

    buffer = io.BytesIO()
    wb.save(buffer)
    return RenderResult(
        data=buffer.getvalue(),
        sem_dados=sem_dados,
        nao_colocados=sorted(set(context) - colocados),
    )
