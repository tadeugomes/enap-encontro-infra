# 🔍 INVESTIGAÇÃO: Por que 5.613 registros se o Brasil tem 5.570 municípios?

## 📊 Resumo da Descoberta

**Resposta**: Os arquivos ICM contêm **linhas de cabeçalho e títulos** que foram incluídas na consolidação!

---

## 🎯 Problema Identificado

### Números Reais:
- **Total de registros no arquivo consolidado**: 5.613
- **Total de municípios no Brasil**: 5.570
- **Diferença**: +43 registros extras

### Causa Raiz:

Cada arquivo original de ICM (Faixa A, B, C, D) contém:
1. **Linha 0**: Título descritivo (ex: "Municípios na Faixa A (Alta)...")
2. **Linha 1**: Linha vazia
3. **Linha 2**: Cabeçalho das colunas (Código IBGE, UF, Município, etc.)
4. **Linhas 3+**: Dados dos municípios

Quando consolidamos os 4 arquivos, **incluímos acidentalmente**:
- ✅ 4 linhas de título (1 por faixa)
- ✅ 4 linhas vazias
- ✅ 4 linhas de cabeçalho duplicadas

**Total de linhas extras**: 4 + 4 + 4 = **12 linhas de cabeçalho**

Além disso, há **duplicatas reais** de municípios:
- `Unnamed: 0` (Código IBGE): 163 duplicatas
- `Unnamed: 3` (Município): 425 duplicatas

---

## 📋 Detalhamento por Faixa

### Números Declarados nos Títulos vs Realidade:

| Faixa | Declarado no Título | Linhas no Arquivo | Diferença |
|-------|---------------------|-------------------|-----------|
| A (Alta) | 585 municípios | 590 linhas | +5 |
| B (Intermediária Avançada) | 1.388 municípios | 1.393 linhas | +5 |
| C (Intermediária Inicial) | 2.016 municípios | 2.021 linhas | +5 |
| D (Inicial) | 1.604 municípios | 1.609 linhas | +5 |
| **TOTAL** | **5.593** | **5.613** | **+20** |

### Observações:
1. Cada faixa tem **+5 linhas extras** (título, vazia, cabeçalho, e mais 2 linhas não identificadas)
2. Somando os municípios declarados: **5.593** (ainda acima de 5.570!)
3. Isso sugere que há **23 municípios duplicados** nos arquivos originais

---

## 🔍 Análise das Colunas

### Colunas Identificadas:

| Coluna Original | Nome Real | Valores Únicos | Descrição |
|----------------|-----------|----------------|-----------|
| Unnamed: 0 | Código IBGE | 5.449 | Código IBGE do município |
| Unnamed: 1 | UF | 28 | Sigla da UF (26 UFs + 2 extras?) |
| Unnamed: 2 | Código UF | 28 | Código numérico da UF |
| Unnamed: 3 | Município | 5.187 | Nome do município |
| Unnamed: 4 | Faixa Populacional | 8 | Classificação por população |
| Unnamed: 5 | Região | 6 | Região geográfica |
| Unnamed: 6 | Variáveis (1 a 20) | 4 | Indicador binário |
| Unnamed: 7-25 | Métricas ICM | 3 cada | Scores/indicadores |
| Unnamed: 26-31 | Outras métricas | - | Classificações adicionais |

---

## ⚠️ Problemas Encontrados

### 1. Linhas de Cabeçalho (4 linhas)
```
Linha 0: "Municípios na Faixa A (Alta)..."
Linha 590: "Municípios na Faixa B (Intermediária Avançada)..."
Linha 1983: "Municípios na Faixa C (Intermediária Inicial)..."
Linha 4004: "Municípios na Faixa D (Inicial)..."
```

### 2. Duplicatas de Código IBGE (163 duplicatas)
- Alguns municípios aparecem mais de uma vez
- Possíveis causas:
  - Municípios em múltiplas faixas (mudança ao longo do tempo?)
  - Erros de digitação
  - Dados de diferentes anos

### 3. Duplicatas de Nome de Município (425 duplicatas)
- Mais duplicatas no nome do que no código IBGE
- Sugere que há municípios com mesmo nome em UFs diferentes

### 4. Mais UFs do que esperado (28 ao invés de 27)
- Brasil tem 26 UFs + DF = 27
- Arquivo tem 28 valores únicos
- Possível causa: Linha de cabeçalho "UF" sendo contada

---

## ✅ Solução Proposta

### Limpeza dos Dados:

1. **Remover linhas de cabeçalho**
   - Filtrar linhas que contenham "Municípios na Faixa"
   - Remover linhas com "Código IBGE" (cabeçalhos duplicados)

2. **Remover linhas vazias**
   - Filtrar linhas com mais de 25 valores nulos

3. **Tratar duplicatas**
   - Identificar municípios duplicados por Código IBGE
   - Decidir critério: manter primeira ocorrência, última, ou investigar

4. **Renomear colunas**
   - Substituir "Unnamed: X" pelos nomes reais

---

## 📊 Números Corretos Esperados

Após limpeza, esperamos:
- **~5.570 municípios** (total no Brasil)
- **Ou 5.593** se os títulos estiverem corretos
- **Diferença de 23** pode ser:
  - Municípios criados/extintos recentemente
  - Municípios em processo de emancipação
  - Erros nos dados

---

## 🔧 Próximos Passos

1. ✅ **Limpar arquivo consolidado**
   - Remover linhas de cabeçalho
   - Remover duplicatas
   - Renomear colunas

2. ✅ **Validar números**
   - Comparar com lista oficial do IBGE
   - Verificar se todos os 5.570 municípios estão presentes

3. ✅ **Investigar duplicatas**
   - Listar municípios duplicados
   - Entender por que estão duplicados

4. ✅ **Recriar arquivo consolidado limpo**
   - Versão final sem problemas
   - Pronta para análise de ML

---

## 📝 Conclusão

**A diferença de 43 registros** se deve a:
- **12 linhas de cabeçalho/título** (4 faixas × 3 linhas cada)
- **~31 linhas extras** (duplicatas ou linhas vazias)

**O número real de municípios únicos** no arquivo é provavelmente **~5.570** (ou próximo disso), mas está "inflado" por linhas de cabeçalho e possíveis duplicatas.

**Ação necessária**: Limpar o arquivo antes de usar em análises de Machine Learning!

---

**Data da Investigação**: 22/11/2025  
**Status**: ✅ Problema Identificado  
**Próximo**: Implementar limpeza dos dados
