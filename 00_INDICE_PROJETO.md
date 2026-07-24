# ÍNDICE DO PROJETO: Análise de Reconstrução e ICM

**Última atualização**: 23/07/2026
**Status**: cinco fases concluídas e publicadas | artigo científico em revisão

---

## Documentação principal

1. [README.md](README.md) — visão geral do projeto e das cinco fases.
2. [06_relatorios/PROGRESSO_IMPLEMENTACAO.md](06_relatorios/PROGRESSO_IMPLEMENTACAO.md) — situação atual, resultados e reprodutibilidade.
3. [06_relatorios/README_ANALISE_ATUALIZADO.md](06_relatorios/README_ANALISE_ATUALIZADO.md) — relatório detalhado da análise exploratória.
4. [06_relatorios/ESTRATEGIAS_ML.md](06_relatorios/ESTRATEGIAS_ML.md) — plano estratégico de machine learning.
5. [CORRECAO_DADOS_ICM.md](CORRECAO_DADOS_ICM.md) — correção crítica de duplicatas (critério de benefício).
6. [06_relatorios/artigo_cientifico_enap.docx](06_relatorios/artigo_cientifico_enap.docx) — artigo científico, gerado por `07_scripts/gerar_artigo_docx.py`.

---

## Estrutura de pastas

| Pasta | Conteúdo |
|---|---|
| `dados/` | Dados brutos: relatórios de acompanhamento (2017–2025) e ICM por faixa. |
| `01_dados_originais/` | Reservada a dados originais não versionados. |
| `02_dados_processados/` | Bases limpas e consolidadas prontas para análise. |
| `03_analises/` | Planilhas e relatórios por fase, mais a análise exploratória e de outliers. |
| `04_visualizacoes/` | Gráficos por fase. É a origem das imagens publicadas em `docs/assets/images/`. |
| `05_modelos/` | Modelos treinados em `.pkl` — ver o README da pasta para o formato. |
| `06_relatorios/` | Relatórios gerenciais, log de progresso e artigo científico. |
| `07_scripts/` | Todo o código-fonte Python. |
| `docs/` | Site do projeto (GitHub Pages). |

Bases de referência: `02_dados_processados/ICM_Consolidado_LIMPO.xlsx` (ICM
oficial limpo), `dados_merged_acompanhamento_icm.xlsx` (processos + ICM) e
`dados_municipios_clusterizados.xlsx` (com os clusters da Fase 2, insumo das
Fases 3 e 4).

---

## Scripts

**Preparação e limpeza**
* `juntar_relatorios.py` — consolida os relatórios de acompanhamento.
* `juntar_faixas.py` — consolida os arquivos ICM por faixa.
* `limpar_arquivo_icm.py` — limpeza oficial do ICM (critério de benefício), gera `ICM_Consolidado_LIMPO.xlsx`, base efetivamente usada nas análises.
* `investigar_duplicatas_icm.py` — diagnóstico de duplicatas conflitantes.

**Análise e modelagem**
* `analise_exploratoria_ATUALIZADA.py` — estatísticas e gráficos gerais.
* `analise_outliers_aprovados.py` — outliers em processos aprovados.
* `ml_fase1_regressao.py` — análise descritiva por faixa ICM.
* `ml_fase1_isolation_forest.py` — detecção de anomalias.
* `ml_fase2_clustering.py` — K-Means.
* `ml_fase3_classificacao.py` — Random Forest de aprovação.
* `ml_fase4_regressao_preditiva.py` — regressão quantílica (valor justo).

**Publicação**
* `gerar_artigo_docx.py` — gera o artigo científico em `.docx`.
* `adicionar_top10_fase4.py`, `extrair_top10_alto_risco.py` — tabelas do site.

---

## Como executar

```bash
# 1. Ambiente (macOS/Linux)
python3 -m venv venv_ml
source venv_ml/bin/activate
pip install -r requirements.txt

# 2. Pipeline de ML, a partir da raiz do repositório e nesta ordem
python 07_scripts/ml_fase2_clustering.py        # gera os clusters usados adiante
python 07_scripts/ml_fase3_classificacao.py
python 07_scripts/ml_fase4_regressao_preditiva.py
```

No Windows, ative o ambiente com `venv_ml\Scripts\activate`.

A Fase 2 precisa rodar antes das Fases 3 e 4: ambas consomem
`02_dados_processados/dados_municipios_clusterizados.xlsx`.

---

## Notas importantes

* **Critério de benefício**: em conflito de faixa para o mesmo município no
  ICM, assume-se a melhor faixa (maior capacidade), para não penalizar o
  município por inconsistência de registro. A base oficial é
  `ICM_Consolidado_LIMPO.xlsx` (idêntica a `ICM_Consolidado_LIMPO_Beneficio.xlsx`).
  Ver [CORRECAO_DADOS_ICM.md](CORRECAO_DADOS_ICM.md) e
  [ANALISE_CRITERIO_BENEFICIO.md](ANALISE_CRITERIO_BENEFICIO.md).
* **Foco em aprovados**: a análise de outliers e o modelo de valor justo
  priorizam processos com recursos transferidos.
* **Reexecução sobrescreve artefatos publicados**: os números do artigo e do
  site vêm dos arquivos versionados. Ver a seção de reprodutibilidade em
  `06_relatorios/PROGRESSO_IMPLEMENTACAO.md` antes de regravá-los.
