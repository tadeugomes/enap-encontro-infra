# PROGRESSO DA IMPLEMENTAÇÃO

**Última atualização**: 23/07/2026
**Status geral**: pipeline analítico concluído; artigo científico em revisão

---

## Situação atual

As cinco fases previstas no plano de ML foram implementadas, documentadas e
publicadas no site do projeto (`docs/`). O trabalho corrente é o artigo
científico e a manutenção da reprodutibilidade do repositório.

| Fase | Técnica | Situação | Artefatos |
|---|---|---|---|
| 1 — Diagnóstico e regressão descritiva | Estatística por faixa ICM | Concluída | `03_analises/fase1_regressao/`, `04_visualizacoes/fase1_regressao/` |
| 1b — Detecção de anomalias | Isolation Forest | Concluída | `05_modelos/isolation_forest_model.pkl`, `RELATORIO_ANOMALIAS_FASE1.md` |
| 2 — Clusterização | K-Means (K = 4) | Concluída | `03_analises/fase2_clustering/`, `05_modelos/fase2_clustering/` |
| 3 — Classificação | Random Forest | Concluída (ROC-AUC 0,80) | `03_analises/fase3_classificacao/`, `05_modelos/fase3_classificacao/` |
| 4 — Valor justo | Regressão quantílica | Concluída (580 alertas) | `03_analises/fase4_regressao/`, `05_modelos/fase4_regressao/` |
| 5 — Simulador | App Streamlit externo | Publicado | `docs/fase5.html` |

---

## Base de dados

* 6.385 processos de acompanhamento (2017–2025).
* 5.445 municípios no ICM consolidado, após remoção de 168 registros
  problemáticos pelo critério de risco (assume-se a pior faixa em conflitos).
* 2.065 municípios no merge, com 97,7% de cobertura.
* R$ 27,68 bilhões em valores solicitados.

## Principais resultados

**O paradoxo da capacidade institucional.** Municípios de Faixa D (menor
capacidade) apresentam valor médio de R$ 28,68 milhões, 2,94 vezes o da Faixa A,
e concentram 51% do valor total. A mediana da Faixa D, porém, é a menor de
todas — poucos casos extremos puxam a média, o que motivou as fases de
clusterização e detecção de anomalias.

| Faixa | Municípios | Valor médio | Mediana | Total |
|---|---|---|---|---|
| A (alta) | 225 | R$ 9,74 M | R$ 1,53 M | R$ 2,19 B |
| B | 565 | R$ 9,79 M | R$ 1,22 M | R$ 5,53 B |
| C | 779 | R$ 6,63 M | R$ 1,40 M | R$ 5,16 B |
| D (baixa) | 496 | R$ 28,68 M | R$ 915 K | R$ 14,23 B |

**Clusterização.** Quatro perfis comportamentais que não coincidem com as faixas
oficiais: baixo impacto, alto custo, outlier extremo e alta frequência.

**Classificação.** ROC-AUC de 0,80 na previsão de aprovação; o valor solicitado
é a variável de maior importância.

**Valor justo.** 580 processos (15%) acima do P90 estimado e 757 abaixo do P10,
sobre uma base auditada de 3.893 processos.

---

## Reprodutibilidade

Ambiente fixado em `requirements.txt`; todos os modelos usam `random_state=42`.
Os scripts devem ser executados a partir da raiz do repositório e resolvem
caminhos relativos a `__file__` — não há mais caminhos absolutos no código.

Verificação de julho de 2026, em macOS com scikit-learn 1.9.0:

* Fase 2 e Fase 3 reproduzem os resultados publicados (ROC-AUC 0,8001).
* Fase 4 sinaliza 593 processos "ALTO" contra os 580 publicados — variação de
  2,2% atribuível à versão do `GradientBoostingRegressor`. Os artefatos
  versionados em `03_analises/fase4_regressao/` seguem correspondendo aos
  números do artigo e do site.
* `gerar_artigo_docx.py` regenera o artigo com texto idêntico ao versionado.

---

## Pendências

* Publicar o código-fonte do simulador da Fase 5, hoje mantido fora deste
  repositório.
* Revisão final do artigo científico.
