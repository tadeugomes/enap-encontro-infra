# fase4_regressao

`regressao_quantilica.pkl` — gerado por `07_scripts/ml_fase4_regressao_preditiva.py`.

Dicionário com:

* `p10`, `p50`, `p90`: três `GradientBoostingRegressor` com
  `loss='quantile'` (alpha 0,1 / 0,5 / 0,9) e `random_state=42`.
* `encoders`: `LabelEncoder` por variável categórica.
* `features`: nomes das colunas na ordem esperada pelos modelos.

Os modelos preveem o **logaritmo** do valor solicitado — aplique `np.expm1()`
para voltar a reais. O treino usa apenas processos com recurso transferido
(valores validados tecnicamente), excluindo Porto Alegre por ser outlier
extremo. Um processo é sinalizado como "ALTO" quando o valor solicitado
ultrapassa o P90 previsto e "BAIXO" quando fica abaixo do P10.

Cobertura do intervalo P10–P90 no conjunto de teste: cerca de 76%.
