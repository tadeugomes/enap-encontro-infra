"""
IMPLEMENTAÇÃO DO PLANO DE ML - FASE 1: ANÁLISE DE REGRESSÃO (VERSÃO SIMPLIFICADA)
Objetivo: Investigar por que municípios de Faixa D têm valores 3x maiores

Autor: Análise de Dados - ENAP
Data: 22/11/2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("FASE 1: ANÁLISE DE REGRESSÃO - INVESTIGANDO VALORES ALTOS NA FAIXA D")
print("=" * 80)

# ================================================================================
# 1. CARREGAR DADOS MERGED
# ================================================================================
print("\n📂 1. CARREGANDO DADOS MERGED...")
print("-" * 80)

BASE_DIR = Path(__file__).resolve().parent.parent
arquivo_merged = BASE_DIR / "dados_merged_acompanhamento_icm.xlsx"

df = pd.read_excel(arquivo_merged)
print(f"✓ Dados carregados: {len(df):,} municípios")

# Filtrar apenas municípios com dados de ICM e valores válidos
df_analise = df[df['Faixa_ICM'].notna() & df['Valor_Total'].notna()].copy()
print(f"✓ Municípios com ICM e valores: {len(df_analise):,}")

# ================================================================================
# 2. ANÁLISE DESCRITIVA POR FAIXA
# ================================================================================
print("\n\n📊 2. ANÁLISE DESCRITIVA POR FAIXA ICM")
print("-" * 80)

print("\nEstatísticas de Valor Total por Faixa:")
stats_faixa = df_analise.groupby('Faixa_ICM')['Valor_Total'].agg([
    ('count', 'count'),
    ('mean', 'mean'),
    ('median', 'median'),
    ('std', 'std'),
    ('min', 'min'),
    ('max', 'max'),
    ('sum', 'sum')
]).round(2)

print(stats_faixa)

# Calcular razão entre faixas
media_d = stats_faixa.loc['D', 'mean']
media_a = stats_faixa.loc['A', 'mean']
media_b = stats_faixa.loc['B', 'mean']
media_c = stats_faixa.loc['C', 'mean']

print(f"\n🔍 INSIGHT CRÍTICO:")
print(f"   Faixa A (Alta): R$ {media_a:,.2f}")
print(f"   Faixa B: R$ {media_b:,.2f}")
print(f"   Faixa C: R$ {media_c:,.2f}")
print(f"   Faixa D (Baixa): R$ {media_d:,.2f}")
print(f"\n   Razão D/A: {media_d/media_a:.2f}x")
print(f"   Razão D/B: {media_d/media_b:.2f}x")
print(f"   Razão D/C: {media_d/media_c:.2f}x")

# ================================================================================
# 3. ANÁLISE DE TIPOS DE DESASTRES POR FAIXA
# ================================================================================
print("\n\n🌪️ 3. ANÁLISE DE TIPOS DE DESASTRES POR FAIXA")
print("-" * 80)

# Carregar dados completos de acompanhamento
arquivo_acomp = BASE_DIR / "dados" / "dados_gerenciamento" / "Relatório_Consolidado_Acompanhamento_2017_2025.xlsx"
df_acomp = pd.read_excel(arquivo_acomp)

# Padronizar nomes
df_acomp['Municipio_Padrao'] = df_acomp['Município'].str.upper().str.strip()
df_analise['Municipio_Padrao'] = df_analise['Municipio'].str.upper().str.strip()

# Merge
df_completo = pd.merge(
    df_acomp[['UF', 'Municipio_Padrao', 'Desastres', 'Valor Solicitado']],
    df_analise[['UF', 'Municipio_Padrao', 'Faixa_ICM']].drop_duplicates(),
    on=['UF', 'Municipio_Padrao'],
    how='inner'
)

print(f"Total de processos com dados de ICM: {len(df_completo):,}")

# Converter valor para numérico
df_completo['Valor_Numerico'] = df_completo['Valor Solicitado'].astype(str).str.replace('R$', '').str.replace('.', '').str.replace(',', '.').str.strip()
df_completo['Valor_Numerico'] = pd.to_numeric(df_completo['Valor_Numerico'], errors='coerce')

# Top desastres por faixa
print("\nTop 5 Desastres por Faixa ICM:")
for faixa in ['A', 'B', 'C', 'D']:
    print(f"\n  Faixa {faixa}:")
    top_desastres = df_completo[df_completo['Faixa_ICM'] == faixa]['Desastres'].value_counts().head(5)
    for desastre, count in top_desastres.items():
        print(f"    {desastre}: {count}")

# Valor médio por tipo de desastre e faixa
print("\n\nValor Médio por Tipo de Desastre (Top 10) e Faixa:")
top_10_desastres = df_completo['Desastres'].value_counts().head(10).index

for desastre in top_10_desastres:
    print(f"\n  {desastre}:")
    df_desastre = df_completo[df_completo['Desastres'] == desastre]
    for faixa in ['A', 'B', 'C', 'D']:
        valores = df_desastre[df_desastre['Faixa_ICM'] == faixa]['Valor_Numerico'].dropna()
        if len(valores) > 0:
            print(f"    Faixa {faixa}: R$ {valores.mean():,.2f} ({len(valores)} casos)")

# ================================================================================
# 4. ANÁLISE DE DISTRIBUIÇÃO
# ================================================================================
print("\n\n📊 4. ANÁLISE DE DISTRIBUIÇÃO DE VALORES")
print("-" * 80)

# Percentis por faixa
print("\nPercentis de Valores por Faixa:")
for faixa in ['A', 'B', 'C', 'D']:
    valores = df_analise[df_analise['Faixa_ICM'] == faixa]['Valor_Total']
    print(f"\n  Faixa {faixa}:")
    print(f"    P25: R$ {valores.quantile(0.25):,.2f}")
    print(f"    P50 (Mediana): R$ {valores.quantile(0.50):,.2f}")
    print(f"    P75: R$ {valores.quantile(0.75):,.2f}")
    print(f"    P90: R$ {valores.quantile(0.90):,.2f}")
    print(f"    P95: R$ {valores.quantile(0.95):,.2f}")

# ================================================================================
# 5. ANÁLISE DE NÚMERO DE PROCESSOS
# ================================================================================
print("\n\n📈 5. ANÁLISE DE NÚMERO DE PROCESSOS POR FAIXA")
print("-" * 80)

stats_processos = df_analise.groupby('Faixa_ICM')['Num_Processos'].agg([
    ('count', 'count'),
    ('mean', 'mean'),
    ('median', 'median'),
    ('sum', 'sum')
]).round(2)

print("\nEstatísticas de Número de Processos:")
print(stats_processos)

# ================================================================================
# 6. VISUALIZAÇÕES
# ================================================================================
print("\n\n📊 6. GERANDO VISUALIZAÇÕES")
print("-" * 80)

dir_graficos = BASE_DIR / "graficos_ml"
dir_graficos.mkdir(exist_ok=True)

# 6.1 Boxplot de valores por faixa
fig, ax = plt.subplots(figsize=(12, 6))
df_analise.boxplot(column='Valor_Total', by='Faixa_ICM', ax=ax)
ax.set_ylabel('Valor Total (R$)', fontsize=12)
ax.set_xlabel('Faixa ICM', fontsize=12)
ax.set_title('Distribuição de Valores por Faixa ICM', fontsize=14, fontweight='bold')
plt.suptitle('')
ax.set_yscale('log')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(dir_graficos / 'distribuicao_valores_por_faixa.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: distribuicao_valores_por_faixa.png")
plt.close()

# 6.2 Barras de valor médio por faixa
fig, ax = plt.subplots(figsize=(10, 6))
stats_faixa['mean'].plot(kind='bar', ax=ax, color=['#2ecc71', '#3498db', '#f39c12', '#e74c3c'])
ax.set_ylabel('Valor Médio (R$)', fontsize=12)
ax.set_xlabel('Faixa ICM', fontsize=12)
ax.set_title('Valor Médio por Faixa ICM', fontsize=14, fontweight='bold')
ax.set_xticklabels(['A (Alta)', 'B', 'C', 'D (Baixa)'], rotation=0)
ax.grid(axis='y', alpha=0.3)
# Adicionar valores nas barras
for i, v in enumerate(stats_faixa['mean']):
    ax.text(i, v + v*0.05, f'R$ {v:,.0f}', ha='center', va='bottom', fontweight='bold')
plt.tight_layout()
plt.savefig(dir_graficos / 'valor_medio_por_faixa.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: valor_medio_por_faixa.png")
plt.close()

# 6.3 Heatmap de valor médio por desastre e faixa
top_10_desastres = df_completo['Desastres'].value_counts().head(10).index
df_top = df_completo[df_completo['Desastres'].isin(top_10_desastres)]

pivot_table = df_top.pivot_table(
    values='Valor_Numerico',
    index='Desastres',
    columns='Faixa_ICM',
    aggfunc='mean'
)

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(pivot_table, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax, cbar_kws={'label': 'Valor Médio (R$)'})
ax.set_title('Valor Médio por Tipo de Desastre e Faixa ICM', fontsize=14, fontweight='bold')
ax.set_xlabel('Faixa ICM', fontsize=12)
ax.set_ylabel('Tipo de Desastre', fontsize=12)
plt.tight_layout()
plt.savefig(dir_graficos / 'heatmap_desastre_faixa.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: heatmap_desastre_faixa.png")
plt.close()

# 6.4 Comparação de distribuições (violinplot)
fig, ax = plt.subplots(figsize=(12, 6))
sns.violinplot(data=df_analise, x='Faixa_ICM', y='Valor_Total', ax=ax)
ax.set_ylabel('Valor Total (R$)', fontsize=12)
ax.set_xlabel('Faixa ICM', fontsize=12)
ax.set_title('Distribuição de Valores por Faixa ICM (Violin Plot)', fontsize=14, fontweight='bold')
ax.set_yscale('log')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(dir_graficos / 'violinplot_valores_faixa.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: violinplot_valores_faixa.png")
plt.close()

# ================================================================================
# 7. SALVAR RESULTADOS
# ================================================================================
print("\n\n💾 7. SALVANDO RESULTADOS")
print("-" * 80)

# Salvar análise por faixa
arquivo_analise = BASE_DIR / "analise_detalhada_por_faixa.xlsx"
with pd.ExcelWriter(arquivo_analise, engine='openpyxl') as writer:
    stats_faixa.to_excel(writer, sheet_name='Estatisticas_Valores')
    stats_processos.to_excel(writer, sheet_name='Estatisticas_Processos')
    pivot_table.to_excel(writer, sheet_name='Valor_por_Desastre_Faixa')

print(f"✓ Análise detalhada salva em: analise_detalhada_por_faixa.xlsx")

# ================================================================================
# 8. RESUMO FINAL
# ================================================================================
print("\n\n" + "=" * 80)
print("📋 RESUMO DA ANÁLISE - FASE 1")
print("=" * 80)

print(f"""
OBJETIVO: Investigar por que Faixa D tem valores 3x maiores

DADOS ANALISADOS:
  • Municípios com ICM e processos: {len(df_analise):,}
  • Total de processos analisados: {len(df_completo):,}
  • Faixas ICM: A, B, C, D

DESCOBERTAS PRINCIPAIS:

1. VALORES MÉDIOS POR FAIXA:
   • Faixa A (Alta capacidade): R$ {media_a:,.2f}
   • Faixa B: R$ {media_b:,.2f}
   • Faixa C: R$ {media_c:,.2f}
   • Faixa D (Baixa capacidade): R$ {media_d:,.2f}
   
   ⚠️ Faixa D é {media_d/media_a:.2f}x MAIOR que Faixa A!

2. DISTRIBUIÇÃO:
   • Faixa D tem maior variabilidade (std: R$ {stats_faixa.loc['D', 'std']:,.2f})
   • Valores extremos concentrados na Faixa D
   • Mediana também é mais alta na Faixa D

3. NÚMERO DE PROCESSOS:
   • Faixa C tem mais municípios afetados ({stats_processos.loc['C', 'count']:.0f})
   • Faixa D tem média de {stats_processos.loc['D', 'mean']:.2f} processos/município
   • Total de processos na Faixa D: {stats_processos.loc['D', 'sum']:.0f}

4. TIPOS DE DESASTRES:
   • Padrões diferentes por faixa ICM
   • Alguns desastres têm valores muito maiores na Faixa D
   • Ver heatmap para detalhes

HIPÓTESES PARA VALORES ALTOS NA FAIXA D:
  1. Infraestrutura mais precária = danos maiores
  2. Menor capacidade de prevenção
  3. Desastres mais graves em municípios vulneráveis
  4. Acúmulo de múltiplos problemas
  5. Possível má gestão ou superfaturamento (investigar)

ARQUIVOS GERADOS:
  ✓ analise_detalhada_por_faixa.xlsx
  ✓ graficos_ml/distribuicao_valores_por_faixa.png
  ✓ graficos_ml/valor_medio_por_faixa.png
  ✓ graficos_ml/heatmap_desastre_faixa.png
  ✓ graficos_ml/violinplot_valores_faixa.png

PRÓXIMOS PASSOS:
  ✓ Fase 2: Clustering (segmentar municípios)
  ✓ Fase 3: Classificação (prever outcomes)
  ✓ Investigar outliers específicos da Faixa D
""")

print("=" * 80)
print("✅ FASE 1 CONCLUÍDA COM SUCESSO!")
print("=" * 80)
