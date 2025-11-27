# 📂 Análises Técnicas e Documentação

Este diretório contém o detalhamento técnico, logs de execução e resultados intermediários de cada fase do pipeline de Machine Learning.

## Estrutura das Análises

### 1. [Exploratória](exploratoria/)
Diagnóstico inicial dos dados, validação da limpeza e investigação de duplicatas.
*   **Destaque:** `INVESTIGACAO_DUPLICATAS_DETALHADA.md` - Análise crítica sobre a qualidade dos dados.

### 2. [Fase 1: Regressão](fase1_regressao/)
Estudos iniciais sobre a correlação entre variáveis e o valor solicitado.
*   **Foco:** Entender a relação entre Capacidade Municipal (ICM) e custos de reconstrução.

### 3. [Fase 2: Clusterização](fase2_clustering/)
Segmentação não-supervisionada dos municípios.
*   **Resultado:** Definição dos 4 perfis comportamentais (Clusters 0 a 3).

### 4. [Fase 3: Classificação](fase3_classificacao/)
Modelagem preditiva para aprovação de processos.
*   **Artefatos:** Matrizes de confusão, curvas ROC e análise de importância de variáveis.

### 5. [Fase 4: Regressão Preditiva (Anomalias)](fase4_regressao/)
Modelagem para estimativa de "Fair Value" e detecção de outliers.
*   **Resultado:** Lista de processos auditados com indícios de anomalia.

### 6. [Fase 5: Simulador](fase5_simulador/)
Documentação e links para a ferramenta interativa de simulação de alertas.

---

**Nota:** Para uma visão mais gerencial e visual dos resultados, consulte a pasta `../docs/` ou o website do projeto.
