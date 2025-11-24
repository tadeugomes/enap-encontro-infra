# 🚨 Análise de Outliers - Processos Aprovados

## 📁 Arquivos Nesta Pasta

### Relatórios:
- ✅ **RELATORIO_OUTLIERS_APROVADOS.md** - Relatório principal (USAR ESTE!)
  - Análise de processos APROVADOS/DEFERIDOS
  - Identifica casos reais de risco
  - Exclui processos indeferidos/arquivados

### Dados:
- ✅ **analise_outliers_APROVADOS.xlsx** - Dados detalhados
  - Top 50 processos aprovados
  - Faixa D aprovados (se houver)
  - Municípios com múltiplos outliers
  - Todos os outliers aprovados

### Visualizações:
Ver pasta: `04_visualizacoes/outliers/`
- ✅ top_20_aprovados.png
- ✅ outliers_por_faixa_aprovados.png
- ✅ status_top50.png
- ✅ valor_medio_aprovados.png

---

## 🎯 Principais Descobertas

### ✅ Sistema de Aprovação Funcionou:
- Processos de Faixa D com valores extremos foram **INDEFERIDOS**
- Massapê do Piauí (R$ 5 bi) → BARRADO
- Nova Monte Verde (R$ 2,5 bi) → NÃO APROVADO

### ⚠️ Casos para Monitoramento:
- **189 outliers aprovados** (6,3% dos processos aprovados)
- Maioria são de Faixas A e B (boa capacidade)
- Focar em municípios com múltiplos outliers

### 📊 Estatísticas:
- Total de processos: 6.385
- Processos aprovados: 3.039 (47,6%)
- Outliers extremos aprovados: 189 (6,3%)

---

## 📖 Como Usar

1. **Leia o relatório principal**:
   ```
   RELATORIO_OUTLIERS_APROVADOS.md
   ```

2. **Veja os dados detalhados**:
   ```
   analise_outliers_APROVADOS.xlsx
   ```

3. **Visualize os gráficos**:
   ```
   ../../../04_visualizacoes/outliers/
   ```

---

**Atualizado em**: 22/11/2025  
**Versão**: 2.0 (Corrigida - Apenas Aprovados)
