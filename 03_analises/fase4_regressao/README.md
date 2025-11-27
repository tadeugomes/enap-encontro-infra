# 🔍 Fase 4: Detecção de Anomalias (Fair Value)

Aplicação de Regressão Quantílica para estimar o "Valor Justo" de cada reconstrução e identificar desvios significativos (anomalias).

## Arquivos Principais

*   **`auditoria_valores_reconstrucao.xlsx`**: **[ARTEFATO CRÍTICO]** Lista completa dos processos analisados, contendo:
    *   Valor Solicitado Original.
    *   Faixa de Preço Justo Estimada (P10 - P90).
    *   Status da Auditoria (Normal, Baixo, Alto Risco).
    *   Sinalização de Outliers (580 processos identificados).

## Metodologia
O modelo calcula um intervalo de confiança personalizado para cada pedido, considerando o tipo de desastre, a localização e o perfil do município. Valores fora desse intervalo são flagrados para auditoria humana prioritária.
