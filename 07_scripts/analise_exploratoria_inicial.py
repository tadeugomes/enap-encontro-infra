"""
SCRIPT INICIAL: Análise Exploratória e Preparação dos Dados
Autor: Análise de Dados - ENAP
Data: 22/11/2025

Este script realiza:
1. Limpeza e padronização dos dados
2. Merge dos datasets
3. Análise exploratória inicial
4. Visualizações básicas
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
arquivo_faixas = BASE_DIR / "dados" / "dados_faixa" / "ICM_Consolidado_Todas_Faixas.xlsx"

print("=" * 80)
print("ANÁLISE EXPLORATÓRIA INICIAL - DADOS DE RECONSTRUÇÃO E ICM")
print("=" * 80)

# ================================================================================
# 1. CARREGAR DADOS
# ================================================================================
print("\n📂 1. CARREGANDO DADOS...")
print("-" * 80)

df_acomp = pd.read_excel(arquivo_acompanhamento)
print(f"✓ Acompanhamento carregado: {df_acomp.shape[0]:,} linhas x {df_acomp.shape[1]} colunas")

df_icm = pd.read_excel(arquivo_faixas)
print(f"✓ ICM carregado: {df_icm.shape[0]:,} linhas x {df_icm.shape[1]} colunas")

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

# 2.4 Status mais comuns
print("\n2.4 Top 10 Status:")
top_status = df_acomp['Status'].value_counts().head(10)
print(top_status)

# 2.5 Análise de valores solicitados
print("\n2.5 Análise de Valores Solicitados:")
# Converter valores para numérico (remover R$, pontos, vírgulas)
df_acomp['Valor_Numerico'] = df_acomp['Valor Solicitado'].astype(str).str.replace('R$', '').str.replace('.', '').str.replace(',', '.').str.strip()
df_acomp['Valor_Numerico'] = pd.to_numeric(df_acomp['Valor_Numerico'], errors='coerce')

valores_validos = df_acomp['Valor_Numerico'].dropna()
if len(valores_validos) > 0:
    print(f"  Total de valores válidos: {len(valores_validos):,}")
    print(f"  Valor médio: R$ {valores_validos.mean():,.2f}")
    print(f"  Valor mediano: R$ {valores_validos.median():,.2f}")
    print(f"  Valor mínimo: R$ {valores_validos.min():,.2f}")
    print(f"  Valor máximo: R$ {valores_validos.max():,.2f}")
    print(f"  Valor total: R$ {valores_validos.sum():,.2f}")

# ================================================================================
# 3. ANÁLISE EXPLORATÓRIA - ICM
# ================================================================================
print("\n\n📊 3. ANÁLISE EXPLORATÓRIA - ICM")
print("-" * 80)

# 3.1 Distribuição por faixa
print("\n3.1 Distribuição por Faixa ICM:")
dist_faixa = df_icm['Faixa'].value_counts().sort_index()
print(dist_faixa)

# ================================================================================
# 4. AGREGAÇÕES POR MUNICÍPIO
# ================================================================================
print("\n\n📈 4. AGREGAÇÕES POR MUNICÍPIO")
print("-" * 80)

# Criar dataset agregado por município
agg_municipio = df_acomp.groupby(['UF', 'Município']).agg({
    'Protocolo': 'count',  # Número de processos
    'Valor_Numerico': ['sum', 'mean', 'median'],
    'Desastres': lambda x: x.value_counts().index[0] if len(x) > 0 else None,  # Desastre mais comum
    'Ano_Relatorio': ['min', 'max']  # Primeiro e último ano
}).reset_index()

# Renomear colunas
agg_municipio.columns = ['UF', 'Municipio', 'Num_Processos', 'Valor_Total', 
                         'Valor_Medio', 'Valor_Mediano', 'Desastre_Mais_Comum',
                         'Primeiro_Ano', 'Ultimo_Ano']

print(f"Total de municípios únicos: {len(agg_municipio):,}")
print(f"\nTop 10 municípios com mais processos:")
print(agg_municipio.nlargest(10, 'Num_Processos')[['UF', 'Municipio', 'Num_Processos', 'Valor_Total']])

# ================================================================================
# 5. ANÁLISE TEMPORAL
# ================================================================================
print("\n\n📅 5. ANÁLISE TEMPORAL")
print("-" * 80)

# Tendência ao longo dos anos
tendencia = df_acomp.groupby('Ano_Relatorio').agg({
    'Protocolo': 'count',
    'Valor_Numerico': 'sum'
}).reset_index()
tendencia.columns = ['Ano', 'Num_Processos', 'Valor_Total']

print("\nTendência de Processos e Valores por Ano:")
print(tendencia)

# ================================================================================
# 6. CORRELAÇÕES INICIAIS
# ================================================================================
print("\n\n🔗 6. ANÁLISE DE CORRELAÇÕES INICIAIS")
print("-" * 80)

# Criar features numéricas para correlação
features_numericas = agg_municipio[['Num_Processos', 'Valor_Total', 'Valor_Medio']].dropna()

if len(features_numericas) > 0:
    correlacao = features_numericas.corr()
    print("\nMatriz de Correlação:")
    print(correlacao)

# ================================================================================
# 7. SALVAR DADOS PROCESSADOS
# ================================================================================
print("\n\n💾 7. SALVANDO DADOS PROCESSADOS")
print("-" * 80)

# Salvar agregação por município
arquivo_saida_municipio = BASE_DIR / "02_dados_processados" / "dados_agregados_municipio.xlsx"
agg_municipio.to_excel(arquivo_saida_municipio, index=False)
print(f"✓ Dados agregados por município salvos em:")
print(f"  {arquivo_saida_municipio}")

# Salvar tendência temporal
arquivo_saida_temporal = BASE_DIR / "02_dados_processados" / "tendencia_temporal.xlsx"
tendencia.to_excel(arquivo_saida_temporal, index=False)
print(f"✓ Tendência temporal salva em:")
print(f"  {arquivo_saida_temporal}")

# ================================================================================
# 8. VISUALIZAÇÕES
# ================================================================================
print("\n\n📊 8. GERANDO VISUALIZAÇÕES")
print("-" * 80)

# Criar diretório para gráficos
dir_graficos = BASE_DIR / "04_visualizacoes" / "exploratoria"
dir_graficos.mkdir(parents=True, exist_ok=True)

# 8.1 Distribuição temporal
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(tendencia['Ano'], tendencia['Num_Processos'], color='steelblue', alpha=0.7)
ax.set_xlabel('Ano', fontsize=12)
ax.set_ylabel('Número de Processos', fontsize=12)
ax.set_title('Evolução do Número de Processos de Reconstrução (2017-2025)', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
# Add labels on bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}',
            ha='center', va='bottom', fontweight='bold')
plt.tight_layout()
plt.savefig(dir_graficos / 'evolucao_processos.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: evolucao_processos.png")
plt.close()

# 8.2 Top 10 UFs
fig, ax = plt.subplots(figsize=(12, 6))
top_ufs.plot(kind='barh', ax=ax, color='coral')
ax.set_xlabel('Número de Processos', fontsize=12)
ax.set_ylabel('UF', fontsize=12)
ax.set_title('Top 10 UFs com Mais Processos de Reconstrução', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
# Add labels on bars
for i, v in enumerate(top_ufs):
    ax.text(v, i, f' {v}', ha='left', va='center', fontweight='bold')
plt.tight_layout()
plt.savefig(dir_graficos / 'top_ufs.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: top_ufs.png")
plt.close()

# 8.3 Top 10 Desastres
fig, ax = plt.subplots(figsize=(12, 8))
top_desastres.plot(kind='barh', ax=ax, color='lightgreen')
ax.set_xlabel('Número de Ocorrências', fontsize=12)
ax.set_ylabel('Tipo de Desastre', fontsize=12)
ax.set_title('Top 10 Tipos de Desastres Mais Frequentes', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
# Add labels on bars
for i, v in enumerate(top_desastres):
    ax.text(v, i, f' {v}', ha='left', va='center', fontweight='bold')
plt.tight_layout()
plt.savefig(dir_graficos / 'top_desastres.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: top_desastres.png")
plt.close()

# 8.4 Distribuição por Faixa ICM
fig, ax = plt.subplots(figsize=(10, 6))
dist_faixa.plot(kind='bar', ax=ax, color=['#2ecc71', '#3498db', '#f39c12', '#e74c3c'])
ax.set_xlabel('Faixa ICM', fontsize=12)
ax.set_ylabel('Número de Municípios', fontsize=12)
ax.set_title('Distribuição de Municípios por Faixa ICM', fontsize=14, fontweight='bold')
ax.set_xticklabels(['A (Alta)', 'B', 'C', 'D (Baixa)'], rotation=0)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(dir_graficos / 'distribuicao_icm.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: distribuicao_icm.png")
plt.close()

# ================================================================================
# 9. RESUMO FINAL
# ================================================================================
print("\n\n" + "=" * 80)
print("📋 RESUMO DA ANÁLISE")
print("=" * 80)

print(f"""
DADOS DE ACOMPANHAMENTO:
  • Total de processos: {len(df_acomp):,}
  • Período: 2017-2025
  • Municípios únicos: {df_acomp['Município'].nunique():,}
  • UFs: {df_acomp['UF'].nunique()}
  • Tipos de desastres: {df_acomp['Desastres'].nunique()}
  • Valor total solicitado: R$ {valores_validos.sum():,.2f}

DADOS ICM:
  • Total de registros: {len(df_icm):,}
  • Faixas: A, B, C, D
  • Faixa A (Alta capacidade): {dist_faixa.get('A', 0):,} municípios
  • Faixa D (Baixa capacidade): {dist_faixa.get('D', 0):,} municípios

ARQUIVOS GERADOS:
  ✓ dados_agregados_municipio.xlsx
  ✓ tendencia_temporal.xlsx
  ✓ graficos/evolucao_processos.png
  ✓ graficos/top_ufs.png
  ✓ graficos/top_desastres.png
  ✓ graficos/distribuicao_icm.png

PRÓXIMOS PASSOS:
  1. Limpar cabeçalhos do arquivo ICM
  2. Padronizar nomes de municípios
  3. Fazer merge dos datasets
  4. Implementar modelos de ML
""")

print("=" * 80)
print("✅ ANÁLISE EXPLORATÓRIA CONCLUÍDA COM SUCESSO!")
print("=" * 80)
