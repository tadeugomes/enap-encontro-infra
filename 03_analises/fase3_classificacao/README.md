# ⚖️ Fase 3: Classificação de Risco

Desenvolvimento de um modelo preditivo supervisionado (Random Forest) para antecipar a decisão técnica (Aprovação ou Reprovação) de novos processos.

## Arquivos Principais

*   **`feature_importance.xlsx`**: Ranking das variáveis que mais influenciam a decisão do modelo. O "Valor Solicitado" é o fator predominante.
*   **`analise_erros_teste.xlsx`**: Planilha com os casos onde o modelo errou a previsão no conjunto de teste, útil para entender os limites da IA e refinar as regras de negócio.

## Performance
*   **ROC-AUC:** 0.80 (Excelente capacidade de discriminação).
*   **Recall:** 88% (Alta segurança em não rejeitar falsamente processos legítimos).
