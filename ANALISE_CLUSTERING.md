# 🧩 Relatório de Clusterização (Fase 2)

**Data**: 23/11/2025  
**Status**: ✅ Concluído  
**Algoritmo**: K-Means (K=4)  
**Base**: 2.113 Municípios com processos

---

## 🎯 Objetivo
Identificar grupos de municípios com **comportamento similar** de solicitações de recursos, independentemente da sua classificação oficial no ICM (Indicador de Capacidade Municipal).

---

## 📊 Resultados da Segmentação

O algoritmo identificou 4 perfis distintos de comportamento:

| Cluster | Nome Sugerido | Qtd Municípios | Média Processos | Média Valor Total | Perfil |
|:---:|:---|:---:|:---:|:---:|:---|
| **0** | **Baixo Impacto** | 1.614 (76%) | 1.7 | R$ 3,8 M | Municípios com poucos eventos e valores baixos. A grande maioria. |
| **1** | **Alto Custo** | 470 (22%) | 6.1 | R$ 42,8 M | Municípios com desastres caros e frequência média. |
| **3** | **Alta Frequência** | 28 (1%) | 24.8 | R$ 49,6 M | Municípios atingidos repetidamente. |
| **2** | **Outlier Extremo** | 1 (<0.1%) | 148.0 | R$ 47,9 M | **Porto Alegre (RS)**. Caso único de altíssima frequência. |

---

## 🔍 Cruzamento: Realidade vs ICM

A análise revelou que a **Faixa ICM não determina o destino** do município.

### 1. O Mito da "Faixa D Problemática"
- **402 municípios de Faixa D** estão no Cluster 0 (Baixo Impacto).
- Ou seja, **81% dos municípios de Faixa D** analisados têm baixo volume de solicitações.
- **Conclusão**: Ser vulnerável (Faixa D) não significa necessariamente ter altos prejuízos recorrentes.

### 2. A "Faixa A" não é imune
- **46 municípios de Faixa A** (Alta Capacidade) estão no Cluster 1 (Alto Custo).
- **7 municípios de Faixa A** estão no Cluster 3 (Alta Frequência).
- **Conclusão**: Capacidade institucional não blinda o município contra grandes desastres.

---

## 💡 Insights para Gestão

1.  **Foco nos Clusters 1 e 3**:
    - Estes 498 municípios (23% do total) concentram a maior parte dos recursos e processos.
    - Estratégia: Auditoria prioritária e apoio técnico focado.

2.  **Monitoramento de Transição**:
    - O objetivo preditivo (Fase 3) deve ser: **Identificar quais municípios do Cluster 0 estão em risco de migrar para o Cluster 1**.

3.  **Caso Porto Alegre**:
    - Deve ser tratado como uma anomalia estatística nos modelos (remover ou tratar separadamente) para não distorcer as previsões gerais.

---

## 📂 Arquivos Gerados

- **Dados**: `02_dados_processados/dados_municipios_clusterizados.xlsx`
- **Relatório**: `03_analises/fase2_clustering/perfil_clusters.xlsx`
- **Visualizações**:
  - `04_visualizacoes/fase2_clustering/mapa_clusters_pca.png`
  - `04_visualizacoes/fase2_clustering/heatmap_cluster_vs_icm.png`
