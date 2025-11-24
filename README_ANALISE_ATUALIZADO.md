# 📊 RELATÓRIO ATUALIZADO: Estratégias de Machine Learning para Análise de Dados de Reconstrução

**Data**: 22/11/2025 (ATUALIZADO)  
**Projeto**: Análise de Relatórios Gerenciais de Reconstrução (2017-2025) + ICM  
**Status**: Análise Exploratória Concluída com Dados Limpos ✅

---

## ⚠️ ATUALIZAÇÃO IMPORTANTE

Este relatório foi **atualizado** após a limpeza dos dados do ICM, que removeu:
- ❌ 4 linhas de título
- ❌ 4 linhas de cabeçalho duplicadas
- ❌ 8 linhas vazias
- ❌ 152 municípios duplicados

**Total removido**: 168 registros problemáticos  
**Dados anteriores**: 5.613 registros → **Dados limpos**: 5.445 municípios únicos

---

## 🎯 Resumo Executivo

Este relatório apresenta **7 estratégias de Machine Learning** para analisar as relações entre:
1. **Relatórios de Acompanhamento de Processos de Reconstrução** (2017-2025)
2. **Índice de Capacidade Municipal (ICM)** por faixas (DADOS LIMPOS)

### Principais Descobertas da Análise Exploratória:

- 📈 **6.385 processos** de reconstrução analisados (2017-2025)
- 💰 **R$ 27,6 bilhões** em valores solicitados
- 🏛️ **2.076 municípios** únicos com processos
- 🗺️ **26 UFs** representadas
- 🌪️ **29 tipos** de desastres diferentes
- 📊 **5.445 municípios** classificados por ICM (A, B, C, D) - DADOS LIMPOS
- 🔗 **2.065 municípios** presentes em ambos os datasets (97,7% de cobertura)

### Insights Importantes:

1. **Crescimento significativo em 2024**: 1.490 processos (maior volume da série histórica)
2. **Rio Grande do Sul lidera**: Porto Alegre com 148 processos
3. **Valor médio por processo**: R$ 6,2 milhões (mediana: R$ 867 mil)
4. **Maioria dos municípios tem baixa capacidade**: 1.455 na Faixa D vs 586 na Faixa A
5. **97,7% dos municípios com processos têm dados de ICM** (excelente cobertura!)

---

## 📋 Dados Disponíveis (ATUALIZADOS)

### Arquivo 1: Relatório de Acompanhamento (2017-2025)

| Métrica | Valor |
|---------|-------|
| Total de Processos | 6.385 |
| Período | 2017-2025 |
| Municípios Únicos | 2.076 |
| UFs | 26 |
| Tipos de Desastres | 29 |
| Valor Total Solicitado | R$ 27.678.739.323,62 |
| Valor Médio | R$ 6.257.910,77 |
| Valor Mediano | R$ 867.320,83 |

### Arquivo 2: ICM por Faixas (DADOS LIMPOS)

| Faixa | Descrição | Municípios | % |
|-------|-----------|------------|---|
| A | Alta Capacidade | 586 | 10,8% |
| B | Média-Alta | 1.388 | 25,5% |
| C | Média-Baixa | 2.016 | 37,0% |
| D | Baixa Capacidade | 1.455 | 26,7% |
| **Total** | | **5.445** | **100%** |

### Arquivo 3: Dados Merged (Acompanhamento + ICM)

| Métrica | Valor |
|---------|-------|
| Municípios com processos | 2.113 |
| Municípios no ICM | 5.445 |
| Municípios em ambos | 2.065 |
| Taxa de cobertura | 97,7% |
| Municípios sem ICM | 48 (2,3%) |

---

## 📊 Análise de Processos por Faixa ICM

### Estatísticas por Faixa (Municípios com Processos):

| Faixa ICM | Municípios | Total Processos | Média Processos | Valor Total (R$) | Valor Médio (R$) |
|-----------|------------|-----------------|-----------------|------------------|------------------|
| **A (Alta)** | 225 | 746 | 3,32 | 2,19 bilhões | 9,74 milhões |
| **B** | 565 | 1.883 | 3,33 | 5,53 bilhões | 9,79 milhões |
| **C** | 779 | 2.305 | 2,96 | 5,16 bilhões | 6,63 milhões |
| **D (Baixa)** | 496 | 1.187 | 2,39 | 14,23 bilhões | 28,68 milhões |

### 🔍 Insights Críticos:

1. **Municípios de Faixa D (baixa capacidade) têm valores MUITO maiores**:
   - Valor médio: R$ 28,68 milhões (quase 3x maior que outras faixas!)
   - Valor total: R$ 14,23 bilhões (51% do total)
   - Possível explicação: Desastres mais graves ou menor capacidade de prevenção

2. **Faixas A e B têm mais processos por município**:
   - Média de 3,32-3,33 processos vs 2,39 na Faixa D
   - Pode indicar melhor capacidade de solicitar recursos

3. **Faixa C tem mais municípios afetados**:
   - 779 municípios (37,7% dos que têm processos)
   - Representa a maior parte dos municípios brasileiros

---

## 🤖 7 Estratégias de Machine Learning

### 1️⃣ **Análise de Clustering (Não Supervisionado)**

**Objetivo**: Identificar padrões e agrupamentos naturais nos municípios

**Algoritmos**:
- K-Means Clustering
- DBSCAN (para identificar outliers)
- Hierarchical Clustering
- Gaussian Mixture Models

**Features a utilizar**:
- Número de desastres por município
- Valor total solicitado
- Tempo médio de processamento
- Taxa de aprovação
- Faixa ICM
- Métricas de capacidade institucional

**Insights esperados**:
- ✅ Municípios com perfis similares de vulnerabilidade
- ✅ Identificação de municípios em risco (baixo ICM + muitos desastres)
- ✅ Padrões regionais e geográficos

---

### 2️⃣ **Classificação - Prever Outcomes**

**Problemas de Classificação**:

#### A) Prever Status do Processo
- **Target**: Status (aprovado, em análise, rejeitado)
- **Features**: ICM, tipo de desastre, UF, valor, ano
- **Algoritmos**: Random Forest, XGBoost, LightGBM

#### B) Prever Faixa ICM
- **Target**: Faixa ICM (A, B, C, D)
- **Features**: Histórico de desastres, valores, tempo de resposta
- **Aplicação**: Identificar municípios que podem melhorar/piorar de faixa

#### C) Identificar Municípios em Risco
- **Target**: Alto risco / Baixo risco (binário)
- **Critério**: Baixo ICM + Alta frequência de desastres
- **Aplicação**: Priorização de recursos e atenção

**Métricas de Avaliação**:
- Accuracy, Precision, Recall, F1-Score
- ROC-AUC
- Confusion Matrix

---

### 3️⃣ **Regressão - Prever Valores Contínuos**

**Problemas de Regressão**:

#### A) Prever Valor Necessário para Reconstrução
- **Target**: Valor solicitado
- **Features**: Tipo de desastre, população, ICM, histórico
- **Aplicação**: Planejamento orçamentário
- **Insight**: Faixa D precisa de valores 3x maiores!

#### B) Prever Tempo de Processamento
- **Target**: Dias entre criação e aprovação
- **Features**: Valor, tipo de desastre, ICM, UF, ano
- **Aplicação**: Gestão de expectativas

#### C) Prever Score ICM Futuro
- **Target**: Score ICM contínuo
- **Features**: Investimentos, histórico, políticas públicas
- **Aplicação**: Avaliar impacto de intervenções

**Algoritmos**:
- Random Forest Regressor
- XGBoost Regressor
- LightGBM
- Gradient Boosting

**Métricas**:
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- R² (Coefficient of Determination)

---

### 4️⃣ **Análise de Séries Temporais**

**Objetivo**: Analisar tendências e fazer previsões futuras

**Análises Possíveis**:

#### A) Tendência de Desastres por Região
- Identificar sazonalidade
- Prever picos de demanda
- Antecipar necessidades de recursos

#### B) Evolução do ICM ao Longo do Tempo
- Municípios melhorando/piorando capacidade
- Impacto de políticas públicas

#### C) Padrões de Aprovação por Ano
- Mudanças em processos administrativos
- Eficiência temporal

**Algoritmos**:
- ARIMA / SARIMA
- Prophet (Facebook)
- LSTM (Deep Learning)
- Exponential Smoothing

**Aplicações**:
- 📈 Previsão de demanda para 2026
- 📊 Identificar tendências de melhoria/piora
- 🎯 Planejamento estratégico de longo prazo

---

### 5️⃣ **Análise de Associação e Correlação**

**Objetivo**: Descobrir relações entre variáveis

**Análises**:

#### A) Correlação ICM vs Eficiência
- Municípios com maior ICM processam mais rápido?
- Maior ICM = maior taxa de aprovação?
- **Descoberta**: Faixa D tem valores MUITO maiores (investigar causas)

#### B) Tipos de Desastres vs Faixa ICM
- Certos desastres afetam mais municípios de baixo ICM?
- Municípios de baixo ICM sofrem desastres mais graves?

#### C) Análise Regional
- UFs mais eficientes
- Padrões geográficos de desastres

**Ferramentas**:
- Matriz de correlação (Pearson, Spearman)
- Heatmaps
- Scatter plots com regressão

---

### 6️⃣ **Detecção de Anomalias**

**Objetivo**: Identificar casos atípicos

**Aplicações**:

#### A) Detecção de Irregularidades
- Valores solicitados muito acima da média
- Processos aprovados muito rapidamente
- Padrões suspeitos de solicitação

#### B) Identificação de Emergências
- Municípios com súbito aumento de desastres
- Valores excepcionalmente altos
- Situações que requerem atenção imediata

**Algoritmos**:
- Isolation Forest
- One-Class SVM
- Local Outlier Factor (LOF)
- Autoencoders

**Benefícios**:
- 🚨 Alertas automáticos para casos críticos
- 🔍 Auditoria e compliance
- ⚡ Resposta rápida a emergências

---

### 7️⃣ **Análise de Rede e Grafos**

**Objetivo**: Modelar relações complexas

**Aplicações**:

#### A) Rede de Municípios Similares
- Conectar municípios com perfis parecidos
- Identificar comunidades regionais
- Compartilhamento de boas práticas

#### B) Rede de Desastres
- Desastres que ocorrem juntos
- Cascata de eventos (ex: chuva → enchente → deslizamento)

#### C) Análise de Influência
- Municípios que podem servir de modelo
- Disseminação de políticas eficazes

**Ferramentas**:
- NetworkX
- Graph Neural Networks (PyTorch Geometric)
- Community Detection Algorithms

---

## 📈 Principais Insights da Análise Exploratória

### 1. Evolução Temporal

| Ano | Processos | Valor Total (R$) |
|-----|-----------|------------------|
| 2017 | 567 | 1,2 bilhões |
| 2018 | 409 | 3,3 bilhões |
| 2019 | 287 | 771 milhões |
| 2020 | 488 | 1,3 bilhões |
| 2021 | 382 | 731 milhões |
| 2022 | 1.156 | 2,8 bilhões |
| 2023 | 979 | 2,8 bilhões |
| **2024** | **1.490** | **8,6 bilhões** ⚠️ |
| 2025 | 627 | 6,2 bilhões |

**⚠️ Alerta**: 2024 teve o maior volume de processos E valores da série histórica!

### 2. Top 10 Municípios com Mais Processos

| Posição | UF | Município | Processos |
|---------|----|-----------|-----------| 
| 1 | RS | Porto Alegre | 148 |
| 2 | RJ | Paraty | 63 |
| 3 | RS | Imigrante | 37 |
| 4 | RS | Sant'Ana do Livramento | 36 |
| 5 | RJ | Petrópolis | 34 |
| 6 | RS | Arroio do Meio | 33 |
| 7 | MG | Carmópolis de Minas | 32 |
| 8 | RS | Canoas | 32 |
| 9 | RS | Caxias do Sul | 26 |
| 10 | RS | Eldorado do Sul | 24 |

**Observação**: Rio Grande do Sul domina o ranking (7 de 10 municípios)

### 3. Distribuição por Capacidade Municipal (ICM) - ATUALIZADO

```
Faixa A (Alta):    586 municípios (10,8%) ✅
Faixa B:         1.388 municípios (25,5%) 
Faixa C:         2.016 municípios (37,0%)
Faixa D (Baixa): 1.455 municípios (26,7%) ⚠️
```

**Preocupação**: 63,7% dos municípios têm capacidade média-baixa ou baixa (C+D)

---

## 🛠️ Arquivos Gerados (ATUALIZADOS)

### Dados Processados
- ✅ `ICM_Consolidado_LIMPO.xlsx` - **NOVO**: Dados ICM sem duplicatas (5.445 municípios)
- ✅ `Relatório_Consolidado_Acompanhamento_2017_2025.xlsx` (6.385 processos)
- ✅ `dados_agregados_municipio_ATUALIZADO.xlsx` - Agregação por município
- ✅ `dados_merged_acompanhamento_icm.xlsx` - **NOVO**: Merge dos datasets (2.065 municípios)
- ✅ `municipios_duplicados.xlsx` - Lista dos 152 municípios removidos

### Visualizações (ATUALIZADAS)
- ✅ `graficos/distribuicao_icm_ATUALIZADO.png` - **NOVO**: Com números corretos
- ✅ `graficos/analise_por_faixa_icm.png` - **NOVO**: Processos e valores por faixa
- ✅ `graficos/distribuicao_por_regiao.png` - **NOVO**: Distribuição regional
- ✅ `graficos/evolucao_processos.png`
- ✅ `graficos/top_ufs.png`
- ✅ `graficos/top_desastres.png`

### Scripts
- ✅ `limpar_arquivo_icm.py` - **NOVO**: Limpeza dos dados ICM
- ✅ `analise_exploratoria_ATUALIZADA.py` - **NOVO**: Análise com dados limpos
- ✅ `investigar_duplicatas_icm.py` - **NOVO**: Investigação de duplicatas
- ✅ `juntar_relatorios.py` - Consolidação de acompanhamento
- ✅ `juntar_faixas.py` - Consolidação de ICM

### Documentação
- ✅ `README_ANALISE_ATUALIZADO.md` - **Este documento**
- ✅ `INVESTIGACAO_DUPLICATAS.md` - Relatório da investigação
- ✅ `ESTRATEGIAS_ML.md` - Estratégias detalhadas de ML
- ✅ `estrategias_machine_learning.py` - Código com exemplos

---

## 💡 Perguntas de Negócio a Responder

### Prioridade Alta 🔴
1. **Por que municípios de Faixa D (baixa capacidade) têm valores 3x maiores?**
2. **Municípios com baixo ICM têm processos mais lentos?**
3. **Quais municípios estão em maior risco e precisam atenção prioritária?**
4. **É possível prever quais municípios terão mais desastres em 2026?**
5. **Por que 2024 teve um pico tão alto de processos e valores?**

### Prioridade Média 🟡
6. Qual o valor médio de reconstrução por tipo de desastre e faixa ICM?
7. Quais UFs são mais eficientes no processamento?
8. Existe sazonalidade nos tipos de desastres?
9. Qual a relação entre ICM e taxa de aprovação?

### Prioridade Baixa 🟢
10. Quais fatores mais influenciam o tempo de processamento?
11. Existem padrões regionais de desastres?
12. Municípios estão melhorando sua capacidade ao longo do tempo?

---

## 🎯 Recomendações Imediatas

### 1. Investigar Valores Altos na Faixa D
- **Ação**: Análise detalhada dos municípios Faixa D
- **Motivo**: Valor médio de R$ 28,68 milhões (3x maior que outras faixas)
- **Objetivo**: Entender se é desastres mais graves ou má gestão

### 2. Investigar o Pico de 2024
- **Ação**: Analisar detalhadamente os dados de 2024
- **Motivo**: Aumento de 52% em processos e 213% em valores vs 2023
- **Possíveis causas**: Desastres climáticos extremos, mudanças de política

### 3. Foco no Rio Grande do Sul
- **Ação**: Análise específica para RS
- **Motivo**: 7 dos 10 municípios com mais processos são do RS
- **Objetivo**: Entender padrões regionais

### 4. Priorizar Municípios de Baixa Capacidade
- **Ação**: Criar programa de fortalecimento institucional
- **Motivo**: 63,7% dos municípios têm capacidade média-baixa ou baixa
- **Objetivo**: Melhorar ICM das faixas C e D

### 5. Implementar Sistema de Alertas
- **Ação**: Desenvolver modelo de detecção de anomalias
- **Motivo**: Identificar situações críticas rapidamente
- **Tecnologia**: Isolation Forest + Dashboard em tempo real

---

## 📞 Próximos Passos

1. ✅ **Revisar este relatório** com stakeholders
2. ✅ **Priorizar perguntas de negócio** a serem respondidas
3. ✅ **Investigar valores altos na Faixa D** (descoberta crítica!)
4. ✅ **Implementar primeiro modelo** (sugestão: clustering ou regressão)
5. ✅ **Criar dashboard inicial** com insights

---

## 📊 Mudanças em Relação à Versão Anterior

| Métrica | Antes | Depois | Diferença |
|---------|-------|--------|-----------|
| Total ICM | 5.613 | 5.445 | -168 (limpeza) |
| Faixa A | 590 | 586 | -4 |
| Faixa B | 1.393 | 1.388 | -5 |
| Faixa C | 2.021 | 2.016 | -5 |
| Faixa D | 1.609 | 1.455 | -154 |
| Cobertura | - | 97,7% | **NOVO** |
| Merge | - | 2.065 municípios | **NOVO** |

**Qualidade dos dados**: ✅ Significativamente melhorada!

---

**Documento criado em**: 22/11/2025  
**Última atualização**: 22/11/2025 16:56  
**Versão**: 2.0 (ATUALIZADA COM DADOS LIMPOS)  
**Status**: ✅ Análise Exploratória Concluída com Dados Validados
