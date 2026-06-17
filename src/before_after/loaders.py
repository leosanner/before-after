"""Leitura das tabelas de entrada (.xlsx ou .csv) e do mapa de correspondência."""

from __future__ import annotations

import json
from pathlib import Path
from typing import IO

import pandas as pd


def load_spreadsheet(source: str | IO[bytes], *, sheet_name: str | int = 0) -> pd.DataFrame:
    """Carrega uma planilha .xlsx em um DataFrame.

    `source` aceita tanto um caminho quanto um file-like (ex: o objeto retornado
    pelo `st.file_uploader`), então serve tanto para a UI quanto para testes.
    """
    return pd.read_excel(source, sheet_name=sheet_name, engine="openpyxl")


def load_table(
    source: str | IO[bytes],
    *,
    filename: str | None = None,
    sheet_name: str | int = 0,
) -> pd.DataFrame:
    """Carrega uma tabela de entrada aceitando .xlsx ou .csv.

    O formato é inferido pela extensão. Para um file-like (upload), a extensão
    vem do `filename` (ex: `st.file_uploader` expõe `.name`); para um caminho,
    do próprio caminho.
    """
    name = filename if filename is not None else (source if isinstance(source, str) else "")
    suffix = Path(name).suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(source)
    if suffix in (".xlsx", ".xls", ""):
        return load_spreadsheet(source, sheet_name=sheet_name)
    raise ValueError(f"Formato não suportado: {suffix!r} (use .xlsx ou .csv)")


def load_correspondence(source: str | IO[bytes]) -> dict:
    """Carrega o `correspondencia.json` ({'excecoes': {...}, 'normalizado': {...}})."""
    if isinstance(source, str):
        return json.loads(Path(source).read_text(encoding="utf-8"))
    return json.load(source)


def common_columns(before: pd.DataFrame, after: pd.DataFrame) -> list[str]:
    """Colunas presentes nas duas planilhas, preservando a ordem do 'antes'."""
    after_cols = set(after.columns)
    return [c for c in before.columns if c in after_cols]
