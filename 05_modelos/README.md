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

Os arquivos atuais foram gerados com scikit-learn 1.5.2 e joblib 1.5.3 (ver
`requirements.txt`), todos com `random_state=42`. Com essas versões o pipeline
reproduz os resultados publicados: a Fase 2 gera artefatos idênticos aos
versionados, a Fase 3 mantém o ranking de importância e o ROC-AUC de 0,80 e a
Fase 4 reproduz exatamente os 580 alertas "ALTO", 757 "BAIXO" e 2.556
"NORMAL" da auditoria.

**A versão do scikit-learn importa.** Com 1.9.0, o mesmo código e os mesmos
dados produzem 593 alertas "ALTO" em vez de 580, porque o
`GradientBoostingRegressor` com `loss='quantile'` e `alpha=0.9` mudou de
comportamento entre as versões — 45 processos trocam de classificação. Os
quantis P10 e P50 são estáveis. Não atualize o scikit-learn sem reconferir a
auditoria da Fase 4 contra os números publicados no artigo e no site.
