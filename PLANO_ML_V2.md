# 🧠 PLANO ESTRATÉGICO DE MACHINE LEARNING (V2.0)

**Status**: Atualizado Pós-Limpeza de Dados (Critério de Risco)  
**Data**: 22/11/2025  
**Base de Dados**: `ICM_Consolidado_LIMPO_V2.xlsx` (5.444 municípios)

---

## 🎯 OBJETIVO CENTRAL
Utilizar inteligência artificial para **otimizar a alocação de recursos** e **mitigar riscos** na reconstrução de infraestrutura, focando na disparidade identificada entre a capacidade institucional (ICM) e os valores solicitados.

---

## 🔄 CICLO DE VIDA DO PROJETO

### ✅ FASE 1: Análise de Regressão Exploratória (CONCLUÍDA)
*Investigação inicial das disparidades de valores.*

- **Conquista**: Identificação de que a **Faixa D** possui valores médios **2,94x superiores** à Faixa A.
- **Entregas**:
  - Script `ml_fase1_regressao.py`.
  - Relatório `analise_detalhada_por_faixa.xlsx`.
  - Visualizações de distribuição e boxplots.
- **Status**: ✅ Concluído (Base atualizada com Critério de Benefício).

### 🚀 FASE 2: Clusterização e Segmentação (PRÓXIMA)
*Entender grupos de comportamento além da Faixa ICM.*

- **Objetivo**: Agrupar municípios não apenas pelo ICM oficial, mas pelo **comportamento real** de solicitações.
- **Algoritmo**: **K-Means** (para grupos) e **Isolation Forest** (para anomalias dentro dos grupos).
- **Hipótese**: Existem municípios classificados como "Faixa B" que se comportam como "Faixa D"?
- **Features**:
  - Valor total solicitado acumulado.
  - Taxa de aprovação histórica.
  - Diversidade de tipos de desastres.
- **Entrega**: Mapa de Clusters (ex: "Municípios de Alta Demanda e Baixa Eficiência").

### 🔮 FASE 3: Classificação (Predição de Risco)
*Prever o resultado antes da análise humana.*

- **Objetivo**: Estimar a probabilidade de um processo ser **INDEFERIDO** ou ficar **SOBRESTADO**.
- **Algoritmo**: **XGBoost Classifier** ou **Random Forest**.
- **Target**: Status (Binário: 1=Aprovado/Transferido, 0=Outros).
- **Aplicação**: Score de Viabilidade para novos processos.

### 📉 FASE 4: Regressão Preditiva (Estimativa de Valor Justo)
*Modelagem avançada para prever valores.*

- **Objetivo**: Criar um modelo de referência para o "Custo Esperado" de um desastre.
- **Algoritmo**: **Quantile Regression**.
- **Entrega**: Estimativa de range de valor aceitável para cada tipo de desastre.

---

## 🛠️ PIPELINE TÉCNICA

### 1. Engenharia de Features (Feature Engineering)
Precisamos criar novas variáveis para enriquecer os modelos:
- `log_valor`: Logaritmo do valor (para reduzir impacto de outliers extremos).
- `taxa_aprovacao_mun`: % de processos aprovados do município nos últimos anos.
- `dias_analise`: Tempo médio de análise (se disponível futuramente).
- `sazonalidade`: Mês do desastre (chuvas vs seca).

### 2. Tratamento de Dados
- **Normalização**: StandardScaler para algoritmos de distância (K-Means).
- **Encoding**: Transformar `Faixa ICM` e `Tipo de Desastre` em números.
- **Imputação**: Tratar nulos (embora a limpeza V2 já tenha resolvido a maioria).

### 3. Validação
- **Cross-Validation**: K-Fold (5 folds) para garantir robustez.
- **Métricas**:
  - Anomalias: Precision@K (quantos dos top K alertas são reais problemas).
  - Classificação: ROC-AUC e F1-Score (balancear precisão e recall).
  - Clusterização: Silhouette Score.

---

## 📅 CRONOGRAMA SUGERIDO

1. **Semana 1 (Atual)**: 
   - Implementar **Isolation Forest** (Fase 1).
   - Comparar anomalias automáticas com os outliers manuais já identificados.
   
2. **Semana 2**:
   - Engenharia de Features (criar variáveis agregadas).
   - Implementar **K-Means** (Fase 2) para segmentação.

3. **Semana 3**:
   - Treinar modelo de **Classificação de Aprovação** (Fase 3).
   - Gerar relatório final de inteligência.

---

## ⚠️ PONTOS DE ATENÇÃO

- **Viés da Faixa D**: Como assumimos a pior faixa na limpeza, o modelo pode "aprender" que Faixa D é inerentemente mais problemática. Devemos monitorar isso.
- **Volume de Dados**: Temos ~6.000 processos. É um dataset pequeno para Deep Learning, mas suficiente para Tree-based models (XGBoost).

---

**Autor**: Agente de IA (Antigravity)  
**Aprovação**: ENAP / Infra Encontro
