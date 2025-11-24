# 🚨 RELATÓRIO DE DETECÇÃO DE ANOMALIAS (FASE 1)

**Data**: 22/11/2025  
**Modelo**: Isolation Forest (Contamination=0.05)  
**Total de Processos Analisados**: 6.385  
**Anomalias Detectadas**: 320 (5.0%)

---

## 📋 Resumo Executivo

A aplicação do algoritmo **Isolation Forest** identificou 320 processos com comportamento atípico. Estes casos desviam significativamente do padrão esperado considerando:
1.  Valor Solicitado (em relação à média)
2.  Faixa ICM do Município
3.  Frequência de solicitações do município
4.  Tipo de Desastre

### 🏆 Top 10 Casos Mais Atípicos

| Rank | UF | Município | Processo | Desastre | Valor Solicitado | Faixa ICM | Score |
|------|----|-----------|----------|----------|------------------|-----------|-------|
| 1 | RS | Porto Alegre | 59056.004296/2024-21 | Inundações | R$ 6.239.226.482,00 | B | -0.0888 |
| 2 | RS | Imigrante | 59056.010316/2024-61 | Enxurradas | R$ 2.175.175,60 | B | -0.0587 |
| 3 | GO | Petrolina de Goiás | 59056.000472/2017-11 | Tempestade Local | R$ 9.000.000,00 | C | -0.0510 |
| 4 | RS | Canoas | 59056.006204/2024-11 | Inundações | R$ 375.670.771,00 | B | -0.0498 |
| 5 | RS | Imigrante | 59056.010318/2024-50 | Enxurradas | R$ 2.175.175,60 | B | -0.0405 |
| 6 | RS | Imigrante | 59056.010319/2024-02 | Enxurradas | R$ 2.175.175,60 | B | -0.0405 |
| 7 | RS | Imigrante | 59056.010317/2024-13 | Enxurradas | R$ 2.175.175,60 | B | -0.0405 |
| 8 | RS | Canoas | 59056.006205/2024-66 | Inundações | R$ 375.670.771,00 | B | -0.0403 |
| 9 | MG | Bom Jesus do Galho | 59056.002234/2023-37 | Tempestade Local | R$ 1.699.483,59 | D | -0.0400 |
| 10 | MG | Bom Jesus do Galho | 59056.002235/2023-81 | Tempestade Local | R$ 1.699.483,59 | D | -0.0400 |

> **Nota**: O score negativo indica o grau de anomalia. Quanto menor (mais negativo), mais anômalo.

---

## 🔍 Análise dos Resultados

1.  **Valores Extremos**: O caso de Porto Alegre (R$ 6,2 Bilhões) é um outlier extremo óbvio, provavelmente devido à catástrofe recente ou erro de digitação/consolidação se não for um valor agregado de reconstrução massiva.
2.  **Repetição de Padrões**: O município de **Imigrante (RS)** aparece múltiplas vezes com o **mesmo valor exato** (R$ 2.175.175,60) em processos diferentes. Isso é um forte indício de duplicidade ou desmembramento de processos que o modelo capturou como anômalo pela frequência/valor.
3.  **Municípios de Faixa D**: Bom Jesus do Galho (MG) aparece com valores altos para Faixa D, o que o modelo considerou atípico dado o perfil esperado para essa faixa (embora Faixa D tenha média alta, a combinação com outros fatores gerou o alerta).

## 🚀 Próximos Passos

1.  **Auditoria**: Verificar os processos listados no arquivo Excel.
2.  **Refinamento**: Investigar se os casos de "Imigrante" são duplicatas reais.
3.  **Feedback**: Marcar quais anomalias são erros de dados vs. fraudes potenciais para retreinar o modelo (Human-in-the-loop).

---
**Arquivo Completo**: `05_modelos/anomalias_isolation_forest.xlsx`
