# Estado do projeto — handoff de sessão

Doc breve para retomar o trabalho do zero. Atualizar ao final de cada sessão.

## Objetivo

Receber dados de exames de dois períodos (início/final), casar os nomes que vêm
do sistema **Oberon** com a nomenclatura de exibição, montar pares por item e
gerar um documento no formato da aba **Comparativo** (KOD/E-level/Shape com
início, final e evolução).

## Fluxo / arquitetura

```
load_table (xlsx/csv) ─┐
                       ├─ prepare (correspondência + soma) ─ build_pairs ─ build_context ─ render
load_table (xlsx/csv) ─┘
```

Módulos em `src/before_after/`:
- `loaders.py` — `load_table()` (xlsx/csv, infere por extensão/`filename`), `load_correspondence()`.
- `normalization.py` — `normalize()` (strip→MAIÚSCULAS→sem acento→espaços) e `resolve()` (devolve **lista** de itens, 1-para-N; `[]` = descartado).
- `correspondence.py` — `prepare()`: resolve nomes, descarta não-casados, **explode** (1-para-N) e **soma** métricas por item. Retorna `Prepared(frame, unmatched, aggregated)`.
- `pairing.py` — `build_pairs()`: casa início×final por item → `PairingResult(pairs, only_in_inicio, only_in_final)`.
- `models.py` — `ItemPair(nome, inicio, final)`, `METRICS = ["KOD","E-level","Shape"]`.
- `context.py` — `build_context(PairingResult)` → **stub (NotImplementedError)**, é a próxima etapa.
- `rendering.py` — `render(template, context)` → bytes do .docx (pronto, intacto).
- `app.py` — UI Streamlit do fluxo (upload início/final → tratamento → tabela de pares). Seção de documento é placeholder.

## Decisões de domínio (validadas contra a aba Comparativo da equipe = verdade de referência; 121/122 itens batem exatos, só Bexiga diverge por estar em branco na referência)

- **Correspondência 1-para-N**: um nome do Oberon pode gerar vários itens sinônimos com valores idênticos:
  `ADRENALINA` → [Adrenalina, Noradrenalina]; `VASOS RENAIS` → [Vasos renais, Veia renal]; `AMÍGDALAS` (acentuado) → [Amígdalas, Tonsilas].
- **Duplicatas somam**: várias linhas no mesmo item/período → métricas **somadas** (não "primeira linha"). Ex.: Hepatócito final KOD 1.005+0.937=1.942.
- **`AMIGDALAS` sem acento é descartada** (não está no relatório da equipe). Só a acentuada gera itens, tratada via `excecoes` (match exato antes de normalizar).
- Dados: período início = 27/Feb/2026, final = 25/May/2026 (derivados da aba `Original`).

## Arquivos de dados

- `data/dados_inicio.xlsx`, `data/dados_final.xlsx` — períodos separados (versionados).
- `data/correspondencia.json` — mapa `{excecoes, normalizado}`, valores em **lista**. Mapa fixo do repo (app usa este).
- `tmp/conteudo_basico.xlsx` — planilha-fonte original (abas `Original` e `Comparativo`). **Ignorada pelo git** (`tmp/`).
- Coluna-fonte do nome cru: `SECÇÃO / ORGÃO / DESIGNAÇÃO`.

## Estado atual

- Branch: **`pipeline-dados`** (a partir de `main`). 7 commits, working tree limpo. **Nada foi push**.
- Testes: `uv run pytest -q` → 3 passam (smoke do pipeline).
- App: `uv run streamlit run app.py` (ainda não rodado/visualizado nesta sessão).

## Próximos passos

1. **Template/documento** (etapa atual): implementar `build_context(PairingResult)` no formato da aba Comparativo e ligar à seção 4 do `app.py`.
   - **Decisão pendente**: não há `.docx` em `templates/` (pasta vazia). Opções: (a) gerar um `.docx` base replicando o layout da aba Comparativo, ou (b) a equipe fornece um template `.docx`.
2. Eventual: rodar/visualizar o app; decidir push do branch / PR.
