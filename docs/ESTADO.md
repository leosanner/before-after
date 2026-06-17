# Estado do projeto — handoff de sessão

Doc breve para retomar o trabalho do zero. Atualizar ao final de cada sessão.

## Objetivo

Receber dados de exames de dois períodos (início/final), casar os nomes que vêm
do sistema **Oberon** com a nomenclatura de exibição, montar pares por item e
gerar um documento **.xlsx no formato da aba Comparativo** (KOD/E-level/Shape com
início, final e evolução), preenchendo um template derivado dessa aba.

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
- `models.py` — `ItemPair(nome, inicio, final)`, `METRICS`, e `evolucao(metric, inicio, final)` (sinal por métrica; Shape é invertida).
- `context.py` — `build_context(PairingResult)` → dict `{item: {métrica: {inicio, final, evolucao}}}`, indexado pelo nome de exibição.
- `rendering.py` — `render(template, context)` → `RenderResult(data, sem_dados, nao_colocados)` com os bytes do **.xlsx**; casa cada item pela coluna `Item` e respeita a máscara de aplicabilidade.
- `scripts/build_template.py` — gera `templates/comparativo.xlsx` a partir da aba Comparativo (remove col A, zera numéricos, embute aba oculta `_aplicabilidade`). Roda quando o layout de referência mudar.
- `templates/comparativo.xlsx` — template versionado (estrutura + Sistema + aba oculta de aplicabilidade).
- `app.py` — UI Streamlit completa: upload início/final → tratamento → tabela de pares → **download do .xlsx**.

## Decisões de domínio (validadas contra a aba Comparativo da equipe = verdade de referência; 121/122 itens batem exatos, só Bexiga diverge por estar em branco na referência)

- **Correspondência 1-para-N**: um nome do Oberon pode gerar vários itens sinônimos com valores idênticos:
  `ADRENALINA` → [Adrenalina, Noradrenalina]; `VASOS RENAIS` → [Vasos renais, Veia renal]; `AMÍGDALAS` (acentuado) → [Amígdalas, Tonsilas].
- **Duplicatas somam**: várias linhas no mesmo item/período → métricas **somadas** (não "primeira linha"). Ex.: Hepatócito final KOD 1.005+0.937=1.942.
- **`AMIGDALAS` sem acento é descartada** (não está no relatório da equipe). Só a acentuada gera itens, tratada via `excecoes` (match exato antes de normalizar).
- **Evolução de Shape é invertida**: KOD/E-level usam `final-início`; Shape usa `início-final` — confirmado pela fórmula da própria equipe (`=início-final` vs `=final-início`). Centralizado em `models.evolucao`.
- **KOD em branco de propósito**: a equipe deixa a coluna KOD vazia em 28 itens (não há fórmula na célula da fonte). O documento **espelha** esses brancos via a aba oculta `_aplicabilidade` (por linha, pois o mesmo nome pode ter aplicabilidades diferentes — ex.: "Medula óssea" aparece com e sem KOD).
- **Nomes de Item não são únicos** ("Medula óssea", "Bexiga" aparecem em 2 sistemas). O renderer preenche por nome; linhas homônimas recebem o mesmo valor. A **Bexiga** (POSTERIOR HOMEM = 0 na referência) é a divergência conhecida (4 células) — limitação aceita.
- Dados: período início = 27/Feb/2026, final = 25/May/2026 (derivados da aba `Original`).
- **Validação**: render comparado célula-a-célula contra a Comparativo (cache) → todos os valores calculados batem; divergências restantes só nos casos conhecidos (Bexiga + 8 itens fora dos dados, que na referência eram `0`/`#VALUE!`).

## Arquivos de dados

- `data/dados_inicio.xlsx`, `data/dados_final.xlsx` — períodos separados (versionados).
- `data/correspondencia.json` — mapa `{excecoes, normalizado}`, valores em **lista**. Mapa fixo do repo (app usa este).
- `tmp/conteudo_basico.xlsx` — planilha-fonte original (abas `Original` e `Comparativo`). **Ignorada pelo git** (`tmp/`).
- Coluna-fonte do nome cru: `SECÇÃO / ORGÃO / DESIGNAÇÃO`.

## Estado atual

- Branch: **`pipeline-dados`** (a partir de `main`). **Nada foi push**.
- Pipeline ponta-a-ponta completo: upload → tratamento → pares → contexto → **render .xlsx** → download.
- `docxtpl` removido das deps (migramos de .docx para .xlsx via `openpyxl`).
- Testes: `uv run pytest -q` → 5 passam (smoke + evolução Shape + render/aplicabilidade).
- App: `uv run streamlit run app.py` (ainda não rodado/visualizado nesta sessão).

## Próximos passos

1. Rodar/visualizar o app e abrir o `.xlsx` gerado para conferência visual (estilos/mesclagens) com a equipe.
2. Confirmar com a equipe os casos conhecidos: **Bexiga** (HOMEM vs MULHER) e os **8 itens** ausentes dos dados (Músculos corpo ant/post, Reprodutor Masculino) — definir se devem entrar no relatório.
3. Commitar a etapa do template; decidir push do branch / PR.
