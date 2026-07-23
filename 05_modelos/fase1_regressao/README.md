# fase1_regressao

A Fase 1 é descritiva: `07_scripts/ml_fase1_regressao.py` produz estatísticas e
gráficos por faixa ICM, sem estimador treinado para serializar. Não há `.pkl`
nesta pasta por definição.

Saídas da fase:

* `03_analises/fase1_regressao/analise_detalhada_por_faixa.xlsx`
* `04_visualizacoes/fase1_regressao/` (quatro gráficos)

A detecção de anomalias por Isolation Forest, historicamente também chamada de
"Fase 1", tem seu modelo em `05_modelos/isolation_forest_model.pkl`.
