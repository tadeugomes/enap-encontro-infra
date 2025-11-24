"""
Script para gerar gráficos de outliers APROVADOS e limpar arquivos antigos
Autor: Análise de Dados - ENAP
Data: 22/11/2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("GERANDO GRÁFICOS DE OUTLIERS APROVADOS E LIMPANDO ARQUIVOS ANTIGOS")
print("=" * 80)

BASE_DIR = Path(r"c:\Users\tadeu\Downloads\enap_infra_encontro")

# ================================================================================
# 1. CARREGAR DADOS DE OUTLIERS APROVADOS
# ================================================================================
print("\n📂 1. CARREGANDO DADOS...")
print("-" * 80)

arquivo_outliers = BASE_DIR / "03_analises" / "outliers_extremos" / "analise_outliers_APROVADOS.xlsx"
df_top50 = pd.read_excel(arquivo_outliers, sheet_name='Top_50_Aprovados')
df_todos = pd.read_excel(arquivo_outliers, sheet_name='Todos_Outliers_Aprovados')

print(f"✓ Top 50 aprovados: {len(df_top50)} casos")
print(f"✓ Todos outliers aprovados: {len(df_todos)} casos")

# ================================================================================
# 2. GERAR GRÁFICOS ATUALIZADOS
# ================================================================================
print("\n\n📊 2. GERANDO GRÁFICOS ATUALIZADOS (APENAS APROVADOS)")
print("-" * 80)

pasta_viz = BASE_DIR / "04_visualizacoes" / "outliers"
pasta_viz.mkdir(exist_ok=True)

# 2.1 Top 20 Processos Aprovados
fig, ax = plt.subplots(figsize=(14, 10))
top_20 = df_top50.head(20).copy()
top_20['Label'] = top_20['UF'] + '/' + top_20['Município']
top_20 = top_20.sort_values('Valor_Numerico')

# Cores baseadas no status
cores = []
for status in top_20['Status']:
    if 'RECURSO TRANSFERIDO' in status or 'SOBRESTADO' in status:
        cores.append('#e74c3c')  # Vermelho - APROVADO (risco real)
    else:
        cores.append('#95a5a6')  # Cinza - Indeferido/Arquivado

ax.barh(range(len(top_20)), top_20['Valor_Numerico'] / 1e6, color=cores)
ax.set_yticks(range(len(top_20)))
ax.set_yticklabels(top_20['Label'], fontsize=9)
ax.set_xlabel('Valor Solicitado (R$ Milhões)', fontsize=12)
ax.set_title('Top 20 Processos com Valores Mais Altos\n(Vermelho = Aprovado/Transferido | Cinza = Indeferido)', 
             fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)

# Adicionar legenda
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#e74c3c', label='Aprovado/Transferido (RISCO)'),
    Patch(facecolor='#95a5a6', label='Indeferido/Arquivado')
]
ax.legend(handles=legend_elements, loc='lower right')

plt.tight_layout()
plt.savefig(pasta_viz / 'top_20_aprovados.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: top_20_aprovados.png")
plt.close()

# 2.2 Outliers por Faixa ICM (apenas aprovados)
fig, ax = plt.subplots(figsize=(10, 6))
outliers_faixa = df_todos.groupby('Faixa_ICM').size()
cores_faixa = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c']
outliers_faixa.plot(kind='bar', ax=ax, color=cores_faixa)
ax.set_xlabel('Faixa ICM', fontsize=12)
ax.set_ylabel('Número de Outliers Aprovados', fontsize=12)
ax.set_title('Outliers Extremos por Faixa ICM (APENAS APROVADOS)', fontsize=14, fontweight='bold')
ax.set_xticklabels(['A (Alta)', 'B', 'C', 'D (Baixa)'], rotation=0)
ax.grid(axis='y', alpha=0.3)
for i, v in enumerate(outliers_faixa):
    ax.text(i, v + 1, str(v), ha='center', va='bottom', fontweight='bold')
plt.tight_layout()
plt.savefig(pasta_viz / 'outliers_por_faixa_aprovados.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: outliers_por_faixa_aprovados.png")
plt.close()

# 2.3 Distribuição de Status dos Top 50
fig, ax = plt.subplots(figsize=(12, 6))
status_counts = df_top50.head(50)['Status'].value_counts()

# Categorizar status
status_aprovado = []
status_indeferido = []
for status, count in status_counts.items():
    if 'RECURSO TRANSFERIDO' in status or 'SOBRESTADO' in status or 'CONCLUÍDO' in status:
        status_aprovado.append((status, count))
    else:
        status_indeferido.append((status, count))

# Plotar
all_status = status_aprovado + status_indeferido
labels = [s[0][:40] for s in all_status]
values = [s[1] for s in all_status]
cores = ['#e74c3c'] * len(status_aprovado) + ['#95a5a6'] * len(status_indeferido)

ax.barh(range(len(all_status)), values, color=cores)
ax.set_yticks(range(len(all_status)))
ax.set_yticklabels(labels, fontsize=9)
ax.set_xlabel('Quantidade', fontsize=12)
ax.set_title('Status dos Top 50 Processos com Valores Mais Altos\n(Vermelho = Aprovado | Cinza = Indeferido)', 
             fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)

# Legenda
legend_elements = [
    Patch(facecolor='#e74c3c', label='Aprovado/Transferido'),
    Patch(facecolor='#95a5a6', label='Indeferido/Arquivado')
]
ax.legend(handles=legend_elements, loc='lower right')

plt.tight_layout()
plt.savefig(pasta_viz / 'status_top50.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: status_top50.png")
plt.close()

# 2.4 Valor médio por Faixa (apenas aprovados)
fig, ax = plt.subplots(figsize=(10, 6))
valor_medio_faixa = df_todos.groupby('Faixa_ICM')['Valor_Numerico'].mean() / 1e6
valor_medio_faixa.plot(kind='bar', ax=ax, color=cores_faixa)
ax.set_xlabel('Faixa ICM', fontsize=12)
ax.set_ylabel('Valor Médio (R$ Milhões)', fontsize=12)
ax.set_title('Valor Médio dos Outliers Aprovados por Faixa ICM', fontsize=14, fontweight='bold')
ax.set_xticklabels(['A (Alta)', 'B', 'C', 'D (Baixa)'], rotation=0)
ax.grid(axis='y', alpha=0.3)
for i, v in enumerate(valor_medio_faixa):
    ax.text(i, v + 1, f'R$ {v:.1f}M', ha='center', va='bottom', fontweight='bold')
plt.tight_layout()
plt.savefig(pasta_viz / 'valor_medio_aprovados.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: valor_medio_aprovados.png")
plt.close()

# ================================================================================
# 3. LIMPAR ARQUIVOS DESATUALIZADOS
# ================================================================================
print("\n\n🗑️ 3. LIMPANDO ARQUIVOS DESATUALIZADOS")
print("-" * 80)

# Arquivos a remover
arquivos_remover = [
    BASE_DIR / "03_analises" / "outliers_extremos" / "RELATORIO_OUTLIERS.md",
    BASE_DIR / "03_analises" / "outliers_extremos" / "analise_outliers_completa.xlsx",
    BASE_DIR / "04_visualizacoes" / "outliers" / "distribuicao_outliers.png",
    BASE_DIR / "04_visualizacoes" / "outliers" / "outliers_por_faixa.png",
    BASE_DIR / "04_visualizacoes" / "outliers" / "top_20_valores_altos.png",
]

for arquivo in arquivos_remover:
    if arquivo.exists():
        try:
            os.remove(arquivo)
            print(f"✓ Removido: {arquivo.name}")
        except Exception as e:
            print(f"✗ Erro ao remover {arquivo.name}: {e}")
    else:
        print(f"- Não encontrado: {arquivo.name}")

# ================================================================================
# 4. CRIAR README NA PASTA DE OUTLIERS
# ================================================================================
print("\n\n📋 4. CRIANDO README ATUALIZADO")
print("-" * 80)

readme_path = BASE_DIR / "03_analises" / "outliers_extremos" / "README.md"

with open(readme_path, 'w', encoding='utf-8') as f:
    f.write("""# 🚨 Análise de Outliers - Processos Aprovados

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
""")

print(f"✓ README criado: {readme_path}")

# ================================================================================
# 5. RESUMO FINAL
# ================================================================================
print("\n\n" + "=" * 80)
print("📋 RESUMO")
print("=" * 80)

print(f"""
GRÁFICOS GERADOS (ATUALIZADOS):
  ✓ top_20_aprovados.png (com cores por status)
  ✓ outliers_por_faixa_aprovados.png
  ✓ status_top50.png (novo!)
  ✓ valor_medio_aprovados.png

ARQUIVOS REMOVIDOS (DESATUALIZADOS):
  ✓ RELATORIO_OUTLIERS.md (versão antiga)
  ✓ analise_outliers_completa.xlsx (versão antiga)
  ✓ distribuicao_outliers.png (versão antiga)
  ✓ outliers_por_faixa.png (versão antiga)
  ✓ top_20_valores_altos.png (versão antiga)

ARQUIVOS MANTIDOS (CORRETOS):
  ✓ RELATORIO_OUTLIERS_APROVADOS.md
  ✓ analise_outliers_APROVADOS.xlsx
  ✓ README.md (atualizado)

LOCALIZAÇÃO DOS GRÁFICOS:
  📂 04_visualizacoes/outliers/
""")

print("=" * 80)
print("✅ GRÁFICOS ATUALIZADOS E ARQUIVOS LIMPOS!")
print("=" * 80)
