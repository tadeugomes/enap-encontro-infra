# fase3_classificacao

`random_forest_aprovacao.pkl` — gerado por `07_scripts/ml_fase3_classificacao.py`.

Dicionário com:

* `modelo`: `RandomForestClassifier` (100 árvores, `max_depth=10`,
  `class_weight='balanced'`, `random_state=42`).
* `encoders`: `LabelEncoder` por variável categórica (`UF`, `Desastres`,
  `Faixa_ICM`, `Cluster_Ordenado`, `Faixa_Populacional`).
* `features`: nomes das colunas na ordem esperada pelo modelo.

O alvo é binário: 1 = recurso transferido, 0 = indeferido, excluído ou
sobrestado. Processos "em análise" ficam fora do treino. Desempenho no conjunto
de teste: ROC-AUC 0,80.

Categorias não vistas no treino não têm código no encoder — trate-as antes de
prever, como faz o script da Fase 4 (mapeamento com `fillna(-1)` e descarte).
