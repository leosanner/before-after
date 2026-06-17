"""Streamlit: comparação início/final de exames e geração de documento.

Pipeline:
    1. upload das planilhas de INÍCIO e FINAL (.xlsx ou .csv)
    2. correspondência + tratamento (resolve nomes, soma duplicatas)
    3. pareamento por item -> tabela início/final/evolução
    4. geração do documento (formato da aba "Comparativo")  [em construção]
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from before_after.correspondence import prepare
from before_after.loaders import load_correspondence, load_table
from before_after.models import METRICS
from before_after.pairing import build_pairs

CORRESPONDENCE_PATH = Path(__file__).parent / "data" / "correspondencia.json"

st.set_page_config(page_title="Início / Final", page_icon="📊", layout="wide")
st.title("📊 Comparador Início / Final")


def pairs_to_frame(pairs) -> pd.DataFrame:
    """Tabela por item com início, final e evolução (final - início) de cada métrica."""
    rows = []
    for p in pairs:
        row = {"Item": p.nome}
        for m in METRICS:
            row[f"{m} início"] = p.inicio[m]
            row[f"{m} final"] = p.final[m]
            row[f"{m} evolução"] = p.final[m] - p.inicio[m]
        rows.append(row)
    return pd.DataFrame(rows)


# --- 1. Upload ------------------------------------------------------------
st.subheader("1. Planilhas")
col_ini, col_fim = st.columns(2)
with col_ini:
    file_ini = st.file_uploader("INÍCIO (.xlsx ou .csv)", type=["xlsx", "csv"], key="inicio")
with col_fim:
    file_fim = st.file_uploader("FINAL (.xlsx ou .csv)", type=["xlsx", "csv"], key="final")

if not (file_ini and file_fim):
    st.info("Envie as planilhas de início e final para continuar.")
    st.stop()

mapping = load_correspondence(str(CORRESPONDENCE_PATH))
ini = prepare(load_table(file_ini, filename=file_ini.name), mapping)
fim = prepare(load_table(file_fim, filename=file_fim.name), mapping)

# --- 2. Tratamento --------------------------------------------------------
st.subheader("2. Correspondência e tratamento")
c1, c2 = st.columns(2)
c1.metric("Itens (início)", len(ini.frame))
c2.metric("Itens (final)", len(fim.frame))

with st.expander("Detalhes do tratamento"):
    if ini.aggregated or fim.aggregated:
        st.write("**Itens somados (várias linhas → um item)**")
        st.write({"início": ini.aggregated, "final": fim.aggregated})
    st.write(f"**Não-casados (início): {len(ini.unmatched)}**", ini.unmatched)
    st.write(f"**Não-casados (final): {len(fim.unmatched)}**", fim.unmatched)

# --- 3. Pareamento --------------------------------------------------------
st.subheader("3. Pares início × final")
result = build_pairs(ini.frame, fim.frame)
st.session_state["result"] = result

if result.only_in_inicio:
    st.warning(f"Só no início: {result.only_in_inicio}")
if result.only_in_final:
    st.warning(f"Só no final: {result.only_in_final}")

st.dataframe(pairs_to_frame(result.pairs), use_container_width=True, hide_index=True)

# --- 4. Documento ---------------------------------------------------------
st.subheader("4. Documento")
st.info("Geração do documento (formato da aba Comparativo) — próxima etapa.")
