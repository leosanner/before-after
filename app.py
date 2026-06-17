"""App Streamlit para geração de documentos a partir de templates .docx."""

from __future__ import annotations

import io
from datetime import date

import streamlit as st
from docxtpl import DocxTemplate

st.set_page_config(page_title="Before / After", page_icon="📄", layout="centered")

st.title("📄 Gerador de Documentos")
st.caption("Preencha os dados e gere um documento a partir de um template .docx.")

template_file = st.file_uploader(
    "Template (.docx com placeholders Jinja, ex: {{ nome }})",
    type=["docx"],
)

col1, col2 = st.columns(2)
with col1:
    nome = st.text_input("Nome do paciente")
with col2:
    data = st.date_input("Data", value=date.today())

observacoes = st.text_area("Observações")

if st.button("Gerar documento", type="primary", disabled=template_file is None):
    doc = DocxTemplate(template_file)
    context = {
        "nome": nome,
        "data": data.strftime("%d/%m/%Y"),
        "observacoes": observacoes,
    }
    doc.render(context)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.success("Documento gerado com sucesso!")
    st.download_button(
        "⬇️ Baixar documento",
        data=buffer,
        file_name=f"documento_{nome or 'sem_nome'}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
