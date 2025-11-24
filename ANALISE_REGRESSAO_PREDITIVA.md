# 📉 Relatório de Regressão Preditiva (Fase 4)

**Data**: 23/11/2025  
**Status**: ✅ Concluído  
**Modelo**: Gradient Boosting Regressor (Quantile Loss)  
**Objetivo**: Estimar o "Valor Justo" de reconstrução e identificar anomalias de preço.

---

## 🎯 Resultados da Auditoria Automática

O modelo analisou **3.893 processos** com valores válidos e classificou-os com base no intervalo de confiança (P10-P90) esperado para seu perfil (Tipo de desastre, UF, Cluster, etc.).

| Classificação | Qtd Processos | % do Total | Significado |
|:---:|:---:|:---:|:---|
| **NORMAL** | 2.556 | 66% | Valor dentro do esperado (Faixa Aceitável). |
| **BAIXO** | 757 | 19% | Valor muito abaixo do padrão (Risco de subdimensionamento ou erro). |
| **ALTO** | 580 | 15% | **Alerta de Superfaturamento Potencial**. Valor acima do limite superior (P90). |

---

## 🚩 Top 5 Anomalias Detectadas (Valores Extremos)

Estes processos solicitam valores centenas de vezes superiores ao esperado para o tipo de desastre e perfil do município:

1.  **Nova Monte Verde (MT)**: Desvio de **+235.558%** (Solicitou R$ 2,5 Bilhões vs Esperado R$ 1,06 Milhão). *Provável erro de digitação ou outlier extremo.*
2.  **Jaboatão dos Guararapes (PE)**: Desvio de **+29.866%**.
3.  **Rio de Janeiro (RJ)**: Desvio de **+10.219%**.
4.  **Osasco (SP)**: Desvio de **+9.160%**.
5.  **Roca Sales (RS)**: Desvio de **+9.058%**.

> **Ação Recomendada**: Auditoria imediata nestes 580 processos classificados como "ALTO".

---

## 📊 Performance do Modelo

- **Cobertura**: O modelo conseguiu "enquadrar" **76,3%** dos processos de teste dentro do seu intervalo de confiança previsto.
- **Dificuldade**: O R² baixo (0.11) indica que a variabilidade dos valores é **extremamente alta** e difícil de prever apenas com as variáveis disponíveis. Isso reforça a necessidade de análise humana para os casos complexos, mas o modelo serve bem como **filtro de triagem**.

---

## 📂 Arquivos Gerados

- **Relatório Completo**: `03_analises/fase4_regressao/auditoria_valores_reconstrucao.xlsx`
- **Visualizações**:
  - `04_visualizacoes/fase4_regressao/real_vs_previsto.png`
  - `04_visualizacoes/fase4_regressao/distribuicao_desvios.png`
