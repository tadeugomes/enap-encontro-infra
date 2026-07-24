# 🕵️ Análise Exploratória e Limpeza de Dados

Esta pasta contém os diagnósticos iniciais sobre a qualidade dos dados e as decisões tomadas para garantir a integridade da análise.

## Arquivos Principais

*   **`INVESTIGACAO_DUPLICATAS_DETALHADA.md`**: Relatório sobre a duplicidade de registros de municípios nas bases de dados. O critério de desempate adotado na versão final foi o de benefício (assumir a melhor faixa de ICM em caso de conflito), conforme `../../CORRECAO_DADOS_ICM.md` e `../../ANALISE_CRITERIO_BENEFICIO.md`. Menções a "Risco Máximo" em documentos internos referem-se a uma versão anterior, substituída.
*   **`IMPACTO_LIMPEZA_DADOS.md`**: Análise do impacto quantitativo da limpeza de dados no tamanho da amostra e na distribuição das classes.
*   **`investigacao_duplicatas.txt`**: Log bruto da investigação de duplicatas.

## Objetivo
Garantir que os dados utilizados nas fases subsequentes (Machine Learning) sejam confiáveis, consistentes e livres de ruído que possa enviesar os modelos.
