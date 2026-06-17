"""Estruturas de dados que circulam entre as etapas do pipeline.

Fluxo:
    load (2x) -> compare -> build_context -> render

Manter os tipos aqui torna explícito o "contrato" de cada etapa e facilita
implementar/testar cada módulo isoladamente.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd


@dataclass
class ColumnDiff:
    """Diferença de uma coluna para uma mesma entidade (linha pareada por chave)."""

    column: str
    before: object
    after: object

    @property
    def changed(self) -> bool:
        return self.before != self.after


@dataclass
class RowComparison:
    """Resultado da comparação de uma entidade (identificada pela coluna-chave)."""

    key: object
    diffs: list[ColumnDiff] = field(default_factory=list)

    @property
    def changed_columns(self) -> list[str]:
        return [d.column for d in self.diffs if d.changed]


@dataclass
class ComparisonResult:
    """Resultado completo da comparação entre as planilhas 'antes' e 'depois'."""

    key_column: str
    compared_columns: list[str]
    rows: list[RowComparison] = field(default_factory=list)

    # Chaves presentes em apenas uma das planilhas.
    only_in_before: list[object] = field(default_factory=list)
    only_in_after: list[object] = field(default_factory=list)

    def to_frame(self) -> pd.DataFrame:
        """Visão tabular da comparação (útil para exibir/depurar na UI)."""
        raise NotImplementedError("TODO: serializar rows para DataFrame")
