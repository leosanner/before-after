"""Smoke tests: garantem que o pacote importa e o pipeline está conectado.

Os testes de lógica (comparison/context) entram quando a implementação for feita.
"""

from before_after import __version__
from before_after.loaders import common_columns
import pandas as pd


def test_version():
    assert __version__


def test_common_columns_preserva_ordem_do_before():
    before = pd.DataFrame({"id": [], "a": [], "b": []})
    after = pd.DataFrame({"b": [], "id": [], "c": []})
    assert common_columns(before, after) == ["id", "b"]
