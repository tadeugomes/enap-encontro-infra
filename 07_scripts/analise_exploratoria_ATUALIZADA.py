"""
SCRIPT ATUALIZADO: Análise Exploratória com Dados Limpos
Autor: Análise de Dados - ENAP
Data: 22/11/2025 (ATUALIZADO)

Este script realiza:
1. Análise com arquivo ICM LIMPO (sem duplicatas)
2. Estatísticas descritivas atualizadas
3. Visualizações corrigidas
4. Merge preliminar dos datasets
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configurar estilo de visualização
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Caminhos dos arquivos
BASE_DIR = Path(__file__).resolve().parent.parent
arquivo_acompanhamento = BASE_DIR / "dados" / "dados_gerenciamento" / "Relatório_Consolidado_Acompanhamento_2017_2025.xlsx"
arquivo_icm_limpo = BASE_DIR / "dados" / "dados_faixa" / "ICM_Consolidado_LIMPO.xlsx"  # ARQUIVO LIMPO!

print("=" * 80)
print("ANÁLISE EXPLORATÓRIA ATUALIZADA - DADOS LIMPOS")
print("=" * 80)
print("\n⚠️  USANDO ARQUIVO ICM LIMPO (sem duplicatas e cabeçalhos)")

# ================================================================================
# 1. CARREGAR DADOS
# ================================================================================
print("\n📂 1. CARREGANDO DADOS...")
print("-" * 80)

df_acomp = pd.read_excel(arquivo_acompanhamento)
print(f"✓ Acompanhamento carregado: {df_acomp.shape[0]:,} linhas x {df_acomp.shape[1]} colunas")

df_icm = pd.read_excel(arquivo_icm_limpo)
print(f"✓ ICM LIMPO carregado: {df_icm.shape[0]:,} linhas x {df_icm.shape[1]} colunas")

# ================================================================================
# 2. ANÁLISE EXPLORATÓRIA - ACOMPANHAMENTO
# ================================================================================
print("\n\n📊 2. ANÁLISE EXPLORATÓRIA - ACOMPANHAMENTO")
print("-" * 80)

# 2.1 Distribuição temporal
print("\n2.1 Distribuição por Ano:")
dist_ano = df_acomp['Ano_Relatorio'].value_counts().sort_index()
print(dist_ano)

# 2.2 Top 10 UFs com mais processos
print("\n2.2 Top 10 UFs com mais processos:")
top_ufs = df_acomp['UF'].value_counts().head(10)
print(top_ufs)

# 2.3 Top 10 tipos de desastres
print("\n2.3 Top 10 tipos de desastres:")
top_desastres = df_acomp['Desastres'].value_counts().head(10)
print(top_desastres)

# 2.4 Análise de valores solicitados
print("\n2.4 Análise de Valores Solicitados:")
df_acomp['Valor_Numerico'] = df_acomp['Valor Solicitado'].astype(str).str.replace('R$', '').str.replace('.', '').str.replace(',', '.').str.strip()
df_acomp['Valor_Numerico'] = pd.to_numeric(df_acomp['Valor_Numerico'], errors='coerce')

valores_validos = df_acomp['Valor_Numerico'].dropna()
if len(valores_validos) > 0:
    print(f"  Total de valores válidos: {len(valores_validos):,}")
    print(f"  Valor médio: R$ {valores_validos.mean():,.2f}")
    print(f"  Valor mediano: R$ {valores_validos.median():,.2f}")
    print(f"  Valor total: R$ {valores_validos.sum():,.2f}")

# ================================================================================
# 3. ANÁLISE EXPLORATÓRIA - ICM (DADOS LIMPOS)
# ================================================================================
print("\n\n📊 3. ANÁLISE EXPLORATÓRIA - ICM (DADOS LIMPOS)")
print("-" * 80)

# 3.1 Distribuição por faixa
print("\n3.1 Distribuição por Faixa ICM:")
dist_faixa = df_icm['Faixa_ICM'].value_counts().sort_index()
print(dist_faixa)
print(f"\nTotal: {dist_faixa.sum():,} municípios")

# 3.2 Distribuição por região
print("\n3.2 Distribuição por Região:")
dist_regiao = df_icm['Regiao'].value_counts()
for regiao, count in dist_regiao.items():
    if 'Região' not in str(regiao):
        print(f"  {regiao}: {count:,} municípios")

# 3.3 Distribuição por faixa populacional
print("\n3.3 Distribuição por Faixa Populacional:")
dist_pop = df_icm['Faixa_Populacional'].value_counts()
for faixa, count in dist_pop.items():
    if 'Faixa' not in str(faixa):
        print(f"  {faixa}: {count:,} municípios")

# ================================================================================
# 4. AGREGAÇÕES POR MUNICÍPIO (ACOMPANHAMENTO)
# ================================================================================
print("\n\n📈 4. AGREGAÇÕES POR MUNICÍPIO - ACOMPANHAMENTO")
print("-" * 80)

agg_municipio = df_acomp.groupby(['UF', 'Município']).agg({
    'Protocolo': 'count',
    'Valor_Numerico': ['sum', 'mean', 'median'],
    'Desastres': lambda x: x.value_counts().index[0] if len(x) > 0 else None,
    'Ano_Relatorio': ['min', 'max']
}).reset_index()

agg_municipio.columns = ['UF', 'Municipio', 'Num_Processos', 'Valor_Total', 
                         'Valor_Medio', 'Valor_Mediano', 'Desastre_Mais_Comum',
                         'Primeiro_Ano', 'Ultimo_Ano']

print(f"Total de municípios únicos: {len(agg_municipio):,}")
print(f"\nTop 10 municípios com mais processos:")
print(agg_municipio.nlargest(10, 'Num_Processos')[['UF', 'Municipio', 'Num_Processos', 'Valor_Total']])

# ================================================================================
# 5. ANÁLISE DE COBERTURA (MERGE PRELIMINAR)
# ================================================================================
print("\n\n🔗 5. ANÁLISE DE COBERTURA - MERGE DOS DATASETS")
print("-" * 80)

# Padronizar nomes de municípios para merge
df_acomp['Municipio_Padrao'] = df_acomp['Município'].str.upper().str.strip()
df_icm['Municipio_Padrao'] = df_icm['Municipio'].str.upper().str.strip()

# Contar municípios únicos em cada dataset
municipios_acomp = set(df_acomp[['UF', 'Municipio_Padrao']].drop_duplicates().apply(tuple, axis=1))
municipios_icm = set(df_icm[['UF', 'Municipio_Padrao']].drop_duplicates().apply(tuple, axis=1))

print(f"\nMunicípios únicos em Acompanhamento: {len(municipios_acomp):,}")
print(f"Municípios únicos em ICM: {len(municipios_icm):,}")
print(f"Municípios em ambos os datasets: {len(municipios_acomp.intersection(municipios_icm)):,}")
print(f"Municípios apenas em Acompanhamento: {len(municipios_acomp - municipios_icm):,}")
print(f"Municípios apenas em ICM: {len(municipios_icm - municipios_acomp):,}")

# Fazer merge
df_merged = pd.merge(
    agg_municipio,
    df_icm[['UF', 'Municipio', 'Faixa_ICM', 'Regiao', 'Faixa_Populacional', 'Codigo_IBGE']],
    left_on=['UF', 'Municipio'],
    right_on=['UF', 'Municipio'],
    how='left'
)

print(f"\nMunicípios após merge: {len(df_merged):,}")
print(f"Municípios com dados de ICM: {df_merged['Faixa_ICM'].notna().sum():,}")
print(f"Municípios sem dados de ICM: {df_merged['Faixa_ICM'].isna().sum():,}")

# ================================================================================
# 6. ANÁLISE POR FAIXA ICM
# ================================================================================
print("\n\n📊 6. ANÁLISE DE PROCESSOS POR FAIXA ICM")
print("-" * 80)

# Análise apenas dos municípios com dados de ICM
df_com_icm = df_merged[df_merged['Faixa_ICM'].notna()]

print(f"\nMunicípios com processos E dados ICM: {len(df_com_icm):,}")

analise_faixa = df_com_icm.groupby('Faixa_ICM').agg({
    'Num_Processos': ['count', 'sum', 'mean', 'median'],
    'Valor_Total': ['sum', 'mean', 'median']
}).round(2)

print("\nEstatísticas por Faixa ICM:")
print(analise_faixa)

# ================================================================================
# 7. SALVAR DADOS PROCESSADOS
# ================================================================================
print("\n\n💾 7. SALVANDO DADOS PROCESSADOS ATUALIZADOS")
print("-" * 80)

# Salvar agregação por município
arquivo_saida_municipio = (BASE_DIR / "02_dados_processados" /
                           "dados_agregados_municipio_ATUALIZADO.xlsx")
agg_municipio.to_excel(arquivo_saida_municipio, index=False)
print(f"✓ Dados agregados salvos em: dados_agregados_municipio_ATUALIZADO.xlsx")

# Salvar merge
arquivo_saida_merged = (BASE_DIR / "02_dados_processados" /
                        "dados_merged_acompanhamento_icm.xlsx")
df_merged.to_excel(arquivo_saida_merged, index=False)
print(f"✓ Dados merged salvos em: dados_merged_acompanhamento_icm.xlsx")

# ================================================================================
# 8. VISUALIZAÇÕES ATUALIZADAS
# ================================================================================
print("\n\n📊 8. GERANDO VISUALIZAÇÕES ATUALIZADAS")
print("-" * 80)

dir_graficos = BASE_DIR / "04_visualizacoes" / "exploratoria"
dir_graficos.mkdir(parents=True, exist_ok=True)

# 8.1 Distribuição por Faixa ICM (ATUALIZADA)
fig, ax = plt.subplots(figsize=(10, 6))
cores_faixa = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c']
dist_faixa.plot(kind='bar', ax=ax, color=cores_faixa)
ax.set_xlabel('Faixa ICM', fontsize=12)
ax.set_ylabel('Número de Municípios', fontsize=12)
ax.set_title('Distribuição de Municípios por Faixa ICM (DADOS LIMPOS)', fontsize=14, fontweight='bold')
ax.set_xticklabels(['A (Alta)', 'B', 'C', 'D (Baixa)'], rotation=0)
ax.grid(axis='y', alpha=0.3)
# Adicionar valores nas barras
for i, v in enumerate(dist_faixa):
    ax.text(i, v + 20, str(v), ha='center', va='bottom', fontweight='bold')
plt.tight_layout()
plt.savefig(dir_graficos / 'distribuicao_icm_ATUALIZADO.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: distribuicao_icm_ATUALIZADO.png")
plt.close()

# 8.2 Processos por Faixa ICM
if len(df_com_icm) > 0:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Número de processos por faixa
    processos_faixa = df_com_icm.groupby('Faixa_ICM')['Num_Processos'].sum().sort_index()
    processos_faixa.plot(kind='bar', ax=ax1, color=cores_faixa)
    ax1.set_xlabel('Faixa ICM', fontsize=12)
    ax1.set_ylabel('Total de Processos', fontsize=12)
    ax1.set_title('Total de Processos de Reconstrução por Faixa ICM', fontsize=13, fontweight='bold')
    ax1.set_xticklabels(['A (Alta)', 'B', 'C', 'D (Baixa)'], rotation=0)
    ax1.grid(axis='y', alpha=0.3)
    # Add labels
    for i, v in enumerate(processos_faixa):
        ax1.text(i, v, str(v), ha='center', va='bottom', fontweight='bold')
    
    # Valor total por faixa
    valor_faixa = df_com_icm.groupby('Faixa_ICM')['Valor_Total'].sum().sort_index() / 1e9  # Em bilhões
    valor_faixa.plot(kind='bar', ax=ax2, color=cores_faixa)
    ax2.set_xlabel('Faixa ICM', fontsize=12)
    ax2.set_ylabel('Valor Total (R$ Bilhões)', fontsize=12)
    ax2.set_title('Valor Total Solicitado por Faixa ICM', fontsize=13, fontweight='bold')
    ax2.set_xticklabels(['A (Alta)', 'B', 'C', 'D (Baixa)'], rotation=0)
    ax2.grid(axis='y', alpha=0.3)
    # Add labels
    for i, v in enumerate(valor_faixa):
        ax2.text(i, v, f'{v:.1f}B', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(dir_graficos / 'analise_por_faixa_icm.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfico salvo: analise_por_faixa_icm.png")
    plt.close()

# 8.3 Distribuição por Região
fig, ax = plt.subplots(figsize=(12, 6))
dist_regiao_limpa = dist_regiao[~dist_regiao.index.astype(str).str.contains('Região', na=False)]
dist_regiao_limpa.plot(kind='barh', ax=ax, color='skyblue')
ax.set_xlabel('Número de Municípios', fontsize=12)
ax.set_ylabel('Região', fontsize=12)
ax.set_title('Distribuição de Municípios por Região (ICM)', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(dir_graficos / 'distribuicao_por_regiao.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: distribuicao_por_regiao.png")
plt.close()

# ================================================================================
# 9. RESUMO FINAL ATUALIZADO
# ================================================================================
print("\n\n" + "=" * 80)
print("📋 RESUMO DA ANÁLISE ATUALIZADA (DADOS LIMPOS)")
print("=" * 80)

print(f"""
DADOS DE ACOMPANHAMENTO:
  • Total de processos: {len(df_acomp):,}
  • Período: 2017-2025
  • Municípios únicos: {df_acomp['Município'].nunique():,}
  • UFs: {df_acomp['UF'].nunique()}
  • Tipos de desastres: {df_acomp['Desastres'].nunique()}
  • Valor total solicitado: R$ {valores_validos.sum():,.2f}

DADOS ICM (LIMPOS):
  • Total de municípios: {len(df_icm):,}
  • Faixas: A, B, C, D
  • Faixa A (Alta capacidade): {dist_faixa.get('A', 0):,} municípios
  • Faixa B: {dist_faixa.get('B', 0):,} municípios
  • Faixa C: {dist_faixa.get('C', 0):,} municípios
  • Faixa D (Baixa capacidade): {dist_faixa.get('D', 0):,} municípios
  • UFs: {df_icm['UF'].nunique()}

MERGE DOS DATASETS:
  • Municípios com processos: {len(municipios_acomp):,}
  • Municípios no ICM: {len(municipios_icm):,}
  • Municípios em ambos: {len(municipios_acomp.intersection(municipios_icm)):,}
  • Taxa de cobertura: {len(municipios_acomp.intersection(municipios_icm))/len(municipios_acomp)*100:.1f}%

ARQUIVOS GERADOS (ATUALIZADOS):
  ✓ ICM_Consolidado_LIMPO.xlsx (dados ICM sem duplicatas)
  ✓ dados_agregados_municipio_ATUALIZADO.xlsx
  ✓ dados_merged_acompanhamento_icm.xlsx
  ✓ graficos/distribuicao_icm_ATUALIZADO.png
  ✓ graficos/analise_por_faixa_icm.png
  ✓ graficos/distribuicao_por_regiao.png

DIFERENÇA vs ANÁLISE ANTERIOR:
  • ICM: 5.613 → {len(df_icm):,} municípios ({5613 - len(df_icm)} removidos)
  • Removidos: cabeçalhos, linhas vazias e duplicatas
""")

print("=" * 80)
print("✅ ANÁLISE ATUALIZADA CONCLUÍDA COM SUCESSO!")
print("=" * 80)
