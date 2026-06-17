"""Streamlit: comparação antes/depois de planilhas e geração de documento.

Pipeline:
    1. upload das planilhas 'antes' e 'depois'
    2. escolha da coluna-chave e das colunas a comparar
    3. comparação
    4. geração do documento a partir de um template .docx
"""

from __future__ import annotations

import streamlit as st

from before_after.comparison import compare
from before_after.context import build_context
from before_after.loaders import common_columns, load_spreadsheet
from before_after.rendering import render

st.set_page_config(page_title="Before / After", page_icon="📊", layout="wide")
st.title("📊 Comparador Antes / Depois")

# --- 1. Upload ------------------------------------------------------------
st.subheader("1. Planilhas")
col_before, col_after = st.columns(2)
with col_before:
    file_before = st.file_uploader("Planilha ANTES (.xlsx)", type=["xlsx"], key="before")
with col_after:
    file_after = st.file_uploader("Planilha DEPOIS (.xlsx)", type=["xlsx"], key="after")

if not (file_before and file_after):
    st.info("Envie as duas planilhas para continuar.")
    st.stop()

df_before = load_spreadsheet(file_before)
df_after = load_spreadsheet(file_after)

cols = common_columns(df_before, df_after)
if not cols:
    st.error("As planilhas não têm colunas em comum.")
    st.stop()

with st.expander("Pré-visualização"):
    st.write("**Antes**", df_before.head())
    st.write("**Depois**", df_after.head())

# --- 2. Configuração ------------------------------------------------------
st.subheader("2. Configuração da comparação")
key_column = st.selectbox("Coluna-chave (pareia as linhas)", cols)
compare_cols = st.multiselect(
    "Colunas a comparar",
    [c for c in cols if c != key_column],
    default=[c for c in cols if c != key_column],
)

# --- 3. Comparação --------------------------------------------------------
st.subheader("3. Resultado")
if st.button("Comparar", type="primary"):
    result = compare(df_before, df_after, key_column=key_column, columns=compare_cols)
    st.session_state["result"] = result
    st.dataframe(result.to_frame())

# --- 4. Documento ---------------------------------------------------------
st.subheader("4. Documento")
template_file = st.file_uploader("Template (.docx)", type=["docx"], key="template")
result = st.session_state.get("result")

if st.button("Gerar documento", disabled=not (template_file and result)):
    context = build_context(result)
    doc_bytes = render(template_file, context)
    st.download_button(
        "⬇️ Baixar documento",
        data=doc_bytes,
        file_name="comparacao.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
