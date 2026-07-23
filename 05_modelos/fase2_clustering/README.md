# fase2_clustering

`kmeans_clustering.pkl` — gerado por `07_scripts/ml_fase2_clustering.py`.

Dicionário com:

* `scaler`: `RobustScaler` ajustado às features de treino.
* `kmeans`: `KMeans` com K = 4 e `random_state=42`.
* `features`: `['Num_Processos', 'Log_Valor_Total', 'Log_Valor_Medio']`.

Os rótulos brutos do K-Means não são ordenados. O script reordena os clusters
por média de `Valor_Total` e grava o resultado na coluna `Cluster_Ordenado`,
que é a usada nas fases seguintes — reaplique essa mesma ordenação ao usar o
modelo diretamente.
