"""Estruturas de dados que circulam entre as etapas do pipeline.

Fluxo:
    load (2x) -> prepare (2x) -> build_pairs -> build_context -> render

Manter os tipos aqui torna explícito o "contrato" de cada etapa e facilita
implementar/testar cada módulo isoladamente.
"""

from __future__ import annotations

from dataclasses import dataclass

# Métricas comparadas por item (colunas numéricas da entrada do Oberon).
METRICS = ["KOD", "E-level", "Shape"]


@dataclass
class ItemPair:
    """Um item pareado entre os dois períodos.

    `inicio` e `final` carregam as métricas (KOD, E-level, Shape) de cada período.
    A evolução (final - início) é derivada na etapa de contexto/documento.
    """

    nome: str
    inicio: dict
    final: dict
