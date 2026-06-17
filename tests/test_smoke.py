"""Smoke tests: garantem que o pacote importa e o pipeline está conectado."""

from pathlib import Path

from before_after import __version__
from before_after.correspondence import prepare
from before_after.loaders import load_correspondence, load_table
from before_after.models import METRICS
from before_after.pairing import build_pairs

DATA = Path(__file__).resolve().parent.parent / "data"


def test_version():
    assert __version__


def test_pipeline_pareia_inicio_e_final():
    mapping = load_correspondence(str(DATA / "correspondencia.json"))
    ini = prepare(load_table(str(DATA / "dados_inicio.xlsx")), mapping)
    fim = prepare(load_table(str(DATA / "dados_final.xlsx")), mapping)

    result = build_pairs(ini.frame, fim.frame)

    assert result.pairs, "deveria produzir pares"
    # estrutura de cada par
    p = result.pairs[0]
    assert set(p.inicio) == set(METRICS)
    assert set(p.final) == set(METRICS)


def test_correspondencia_um_para_n_gera_sinonimo():
    # ADRENALINA (1 linha) -> Adrenalina + Noradrenalina (sinônimos).
    mapping = load_correspondence(str(DATA / "correspondencia.json"))
    fim = prepare(load_table(str(DATA / "dados_final.xlsx")), mapping)
    assert "Noradrenalina" in fim.frame.index
