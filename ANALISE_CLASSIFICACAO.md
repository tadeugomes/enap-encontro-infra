# 🔮 Relatório de Classificação (Fase 3)

**Data**: 23/11/2025  
**Status**: ✅ Concluído  
**Modelo**: Random Forest Classifier  
**Objetivo**: Prever se um processo será **APROVADO** (Recurso Transferido) ou **REPROVADO/SOBRESTADO**.

---

## 📊 Performance do Modelo

O modelo atingiu uma capacidade preditiva **muito boa** para um problema complexo de gestão pública.

| Métrica | Resultado | Interpretação |
|:---:|:---:|:---|
| **ROC-AUC** | **0.7972** | O modelo tem **80% de chance** de distinguir corretamente entre um processo que será aprovado e um que será reprovado. |
| **Recall (Aprovados)** | **88%** | O modelo identifica corretamente **88% dos processos que seriam aprovados**. |
| **Precisão (Reprovados)** | **88%** | Quando o modelo diz que vai reprovar, ele acerta **88% das vezes**. |

---

## 💡 O que define a aprovação? (Feature Importance)

A análise de importância das variáveis revelou insights surpreendentes sobre o que realmente pesa na decisão:

1.  **💰 Valor Solicitado (63%)**: É, de longe, o fator mais determinante.
    - Processos com valores muito altos ou muito baixos (fora do padrão) tendem a ter desfechos diferentes.
    - Isso valida a hipótese de que **pedidos "fora da curva" sofrem mais escrutínio**.

2.  **📍 UF (10%)**: O estado de origem influencia a aprovação.
    - Pode indicar diferenças na qualidade técnica das equipes estaduais ou critérios regionais.

3.  **👥 População e Cluster (15%)**: O porte do município e seu perfil de comportamento (Cluster) são mais importantes que o tipo de desastre.

4.  **📉 Faixa ICM (5%)**: Surpreendentemente, a **Faixa ICM oficial tem POUCO peso** na decisão final.
    - Isso reforça a descoberta da Fase 2: O **comportamento real (Cluster)** é mais relevante que o rótulo oficial.

---

## 🎯 Aplicação Prática: Score de Viabilidade

Com este modelo, podemos criar um **"Semáforo de Processos"** para novos pedidos:

- 🟢 **Alta Probabilidade (>80%)**: Processo padrão, encaminhamento rápido (Fast Track).
- 🟡 **Média Probabilidade (40-80%)**: Requer análise técnica padrão.
- 🔴 **Baixa Probabilidade (<40%)**: Alto risco de indeferimento. **Alerta ao gestor**: "Revisar documentação e valores antes de submeter".

---

## 📂 Arquivos Gerados

- **Relatório de Erros**: `03_analises/fase3_classificacao/analise_erros_teste.xlsx`
- **Importância das Variáveis**: `03_analises/fase3_classificacao/feature_importance.xlsx`
- **Visualizações**:
  - `04_visualizacoes/fase3_classificacao/roc_curve.png`
  - `04_visualizacoes/fase3_classificacao/feature_importance.png`
