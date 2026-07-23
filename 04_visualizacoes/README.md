# 04_visualizacoes

Gráficos gerados pelos scripts, organizados por fase. Esta pasta é a **fonte**
das imagens publicadas em `docs/assets/images/` — ao atualizar um gráfico aqui,
copie-o para lá para manter o site sincronizado.

| Subpasta | Gerada por |
|---|---|
| `exploratoria/` | `analise_exploratoria_ATUALIZADA.py`, `analise_exploratoria_inicial.py` |
| `fase1_regressao/` | `ml_fase1_regressao.py` |
| `fase2_clustering/` | `ml_fase2_clustering.py` |
| `fase3_classificacao/` | `ml_fase3_classificacao.py` |
| `fase4_regressao/` | `ml_fase4_regressao_preditiva.py` |
| `outliers/` | `analise_outliers_aprovados.py`, `atualizar_graficos_outliers.py` |

## Atenção ao reexecutar

Os arquivos versionados são exatamente os publicados no site. Reexecutar
`analise_exploratoria_ATUALIZADA.py` regenera os gráficos de `exploratoria/`
com rótulos de valor sobre as barras — uma versão mais recente do que a
publicada. Se adotá-la, atualize também `docs/assets/images/`.
