# 05_modelos

Modelos treinados, serializados com `joblib`. Cada arquivo `.pkl` guarda um
dicionário com o estimador e os objetos auxiliares necessários para reaplicá-lo
(scaler, encoders e a lista de features na ordem esperada).

| Arquivo | Fase | Conteúdo |
|---|---|---|
| `isolation_forest_model.pkl` | 1 — Anomalias | Isolation Forest |
| `fase2_clustering/kmeans_clustering.pkl` | 2 — Clusterização | `scaler`, `kmeans`, `features` |
| `fase3_classificacao/random_forest_aprovacao.pkl` | 3 — Classificação | `modelo`, `encoders`, `features` |
| `fase4_regressao/regressao_quantilica.pkl` | 4 — Fair value | `p10`, `p50`, `p90`, `encoders`, `features` |

## Como carregar

```python
import joblib
pacote = joblib.load("05_modelos/fase3_classificacao/random_forest_aprovacao.pkl")
modelo, encoders, features = pacote["modelo"], pacote["encoders"], pacote["features"]
proba = modelo.predict_proba(X[features])[:, 1]
```

## Versões e reprodutibilidade

Os arquivos atuais foram gerados com scikit-learn 1.9.0 e joblib 1.5.3 (ver
`requirements.txt`), todos com `random_state=42`. Ao reexecutar os scripts, a
Fase 3 reproduz o ROC-AUC publicado (0,80); a Fase 4 apresenta variação de
cerca de 2% na contagem de alertas "ALTO" em relação aos artefatos publicados,
atribuível à diferença de versão do `GradientBoostingRegressor`. Os artefatos
versionados em `03_analises/` correspondem aos números do artigo e do site.
