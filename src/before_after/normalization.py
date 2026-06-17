"""Padronização de nomes e resolução para o nome de exibição ("Item").

O Oberon exporta os nomes em grafias inconsistentes (maiúsculas/minúsculas,
acentos, espaços), então padronizamos antes de casar com o mapa de
correspondência. A *mesma* `normalize` é aplicada às chaves do mapa e aos dados
de entrada, garantindo que os dois lados sejam comparados da mesma forma.

O mapa é **1-para-N**: um nome cru do Oberon pode gerar vários itens de
exibição (sinônimos que a equipe lista separados — ex.: ``ADRENALINA`` →
``[Adrenalina, Noradrenalina]``, com valores idênticos). Por isso `resolve`
devolve sempre uma *lista* (vazia quando não há correspondência).

Algumas grafias colidem ao normalizar mas devem ser tratadas diferente (ex.:
``AMÍGDALAS`` acentuado gera itens; ``AMIGDALAS`` sem acento é descartado).
Esses casos vão numa lista de exceções resolvida por match exato (após `strip`)
ANTES de normalizar.
"""

from __future__ import annotations

import re
import unicodedata


def normalize(value: object) -> str:
    """Padroniza um nome: strip → MAIÚSCULAS → sem acentos → espaços colapsados."""
    text = str(value).strip().upper()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", text)


def resolve(value: object, mapping: dict) -> list[str]:
    """Resolve um nome cru para a lista de "Itens" de exibição (1-para-N).

    `mapping` segue o formato de ``correspondencia.json``:
        {"excecoes": {grafia_exata: [item, ...]},
         "normalizado": {chave_normalizada: [item, ...]}}

    Ordem de resolução:
        1. match exato (após strip) na lista de exceções;
        2. match pela chave normalizada;
        3. lista vazia se nenhum casar (linha descartada).
    """
    raw = str(value).strip()
    excecoes = mapping.get("excecoes", {})
    if raw in excecoes:
        return excecoes[raw]
    return mapping.get("normalizado", {}).get(normalize(raw), [])
