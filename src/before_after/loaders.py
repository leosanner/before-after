"""Leitura das planilhas de entrada (.xlsx)."""

from __future__ import annotations

from typing import IO

import pandas as pd


def load_spreadsheet(source: str | IO[bytes], *, sheet_name: str | int = 0) -> pd.DataFrame:
    """Carrega uma planilha .xlsx em um DataFrame.

    `source` aceita tanto um caminho quanto um file-like (ex: o objeto retornado
    pelo `st.file_uploader`), então serve tanto para a UI quanto para testes.
    """
    return pd.read_excel(source, sheet_name=sheet_name, engine="openpyxl")


def common_columns(before: pd.DataFrame, after: pd.DataFrame) -> list[str]:
    """Colunas presentes nas duas planilhas, preservando a ordem do 'antes'."""
    after_cols = set(after.columns)
    return [c for c in before.columns if c in after_cols]
