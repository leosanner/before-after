"""Nomes seguros para os arquivos disponibilizados pelo app."""

from __future__ import annotations

import re

INVALID_FILENAME_CHARS = re.compile(r'[\\/:*?"<>|]+')


def comparative_filename(patient_name: str) -> str:
    """Monta o nome do comparativo, preservando acentos do nome do paciente."""
    safe_name = INVALID_FILENAME_CHARS.sub("-", patient_name)
    safe_name = re.sub(r"(?:\s*-\s*)+", " - ", safe_name)
    safe_name = " ".join(safe_name.split()).strip(" .-")
    if not safe_name:
        return "Quadro comparativo.xlsx"
    return f"Quadro comparativo - {safe_name}.xlsx"
