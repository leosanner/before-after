"""Comparação antes/depois, pareando linhas por uma coluna-chave."""

from __future__ import annotations

import pandas as pd

from .models import ComparisonResult


def compare(
    before: pd.DataFrame,
    after: pd.DataFrame,
    *,
    key_column: str,
    columns: list[str] | None = None,
) -> ComparisonResult:
    """Compara `before` e `after` pareando as linhas pela `key_column`.

    Args:
        before: planilha do estado "antes".
        after: planilha do estado "depois".
        key_column: coluna identificadora presente nas duas planilhas.
        columns: colunas a comparar. Se None, usa todas as colunas comuns
            (exceto a coluna-chave).

    Returns:
        ComparisonResult com, por chave, as diferenças coluna a coluna,
        além das chaves exclusivas de cada planilha.
    """
    # TODO: implementar
    #   1. validar que key_column existe nas duas planilhas
    #   2. definir `columns` (default = colunas comuns - key_column)
    #   3. indexar before/after por key_column
    #   4. para cada chave em comum, montar RowComparison com ColumnDiff
    #   5. preencher only_in_before / only_in_after
    raise NotImplementedError("TODO: lógica de comparação por chave")
