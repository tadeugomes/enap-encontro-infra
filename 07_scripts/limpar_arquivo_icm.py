"""
SCRIPT: Limpeza do Arquivo ICM Consolidado
Objetivo: Remover linhas de cabeçalho, duplicatas e criar arquivo limpo
"""

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

print("=" * 80)
print("LIMPEZA DO ARQUIVO ICM CONSOLIDADO")
print("=" * 80)

# Carregar arquivo consolidado original
arquivo_original = BASE_DIR / "dados" / "dados_faixa" / "ICM_Consolidado_Todas_Faixas.xlsx"
df = pd.read_excel(arquivo_original)

print(f"\n📊 ANTES DA LIMPEZA:")
print(f"   Total de registros: {len(df):,}")

# ================================================================================
# 1. REMOVER LINHAS DE CABEÇALHO/TÍTULO
# ================================================================================
print("\n" + "-" * 80)
print("1. REMOVENDO LINHAS DE CABEÇALHO/TÍTULO")
print("-" * 80)

# Identificar linhas que contêm "Municípios na Faixa"
linhas_titulo = df[df.iloc[:, 0].astype(str).str.contains('Municípios na Faixa', na=False)]
print(f"   Linhas de título encontradas: {len(linhas_titulo)}")

# Identificar linhas que contêm "Código IBGE" (cabeçalhos duplicados)
linhas_cabecalho = df[df.iloc[:, 0].astype(str).str.contains('Código IBGE', na=False, case=False)]
print(f"   Linhas de cabeçalho duplicadas: {len(linhas_cabecalho)}")

# Remover essas linhas
df_limpo = df[~df.iloc[:, 0].astype(str).str.contains('Municípios na Faixa|Código IBGE', na=False, case=False)]
print(f"   ✓ Linhas removidas: {len(df) - len(df_limpo)}")
print(f"   Registros restantes: {len(df_limpo):,}")

# ================================================================================
# 2. REMOVER LINHAS VAZIAS/COM MUITOS NULOS
# ================================================================================
print("\n" + "-" * 80)
print("2. REMOVENDO LINHAS VAZIAS")
print("-" * 80)

nulos_por_linha = df_limpo.isnull().sum(axis=1)
linhas_vazias = df_limpo[nulos_por_linha > 25]
print(f"   Linhas com mais de 25 valores nulos: {len(linhas_vazias)}")

df_limpo = df_limpo[nulos_por_linha <= 25]
print(f"   ✓ Registros restantes: {len(df_limpo):,}")

# ================================================================================
# 3. RENOMEAR COLUNAS
# ================================================================================
print("\n" + "-" * 80)
print("3. RENOMEANDO COLUNAS")
print("-" * 80)

# Mapear nomes corretos baseado na análise
novos_nomes = {
    'Unnamed: 0': 'Codigo_IBGE',
    'Unnamed: 1': 'UF',
    'Unnamed: 2': 'Codigo_UF',
    'Unnamed: 3': 'Municipio',
    'Unnamed: 4': 'Faixa_Populacional',
    'Unnamed: 5': 'Regiao',
    'Unnamed: 6': 'Variavel_1_20',
    'Unnamed: 7': 'Metrica_1',
    'Unnamed: 8': 'Metrica_2',
    'Unnamed: 9': 'Metrica_3',
    'Unnamed: 10': 'Metrica_4',
    'Unnamed: 11': 'Metrica_5',
    'Unnamed: 12': 'Metrica_6',
    'Unnamed: 13': 'Metrica_7',
    'Unnamed: 14': 'Metrica_8',
    'Unnamed: 15': 'Metrica_9',
    'Unnamed: 16': 'Metrica_10',
    'Unnamed: 17': 'Metrica_11',
    'Unnamed: 18': 'Metrica_12',
    'Unnamed: 19': 'Metrica_13',
    'Unnamed: 20': 'Metrica_14',
    'Unnamed: 21': 'Metrica_15',
    'Unnamed: 22': 'Metrica_16',
    'Unnamed: 23': 'Metrica_17',
    'Unnamed: 24': 'Metrica_18',
    'Unnamed: 25': 'Metrica_19',
    'Unnamed: 26': 'Classificacao_1',
    'Unnamed: 27': 'Classificacao_2',
    'Unnamed: 28': 'Porte',
    'Unnamed: 29': 'Prioridade',
    'Unnamed: 30': 'Classificacao_3',
    'Unnamed: 31': 'Classificacao_4',
    'Faixa': 'Faixa_ICM'
}

df_limpo = df_limpo.rename(columns=novos_nomes)
print(f"   ✓ Colunas renomeadas: {len(novos_nomes)}")

# ================================================================================
# 4. VERIFICAR E TRATAR DUPLICATAS
# ================================================================================
print("\n" + "-" * 80)
print("4. VERIFICANDO DUPLICATAS")
print("-" * 80)

# Duplicatas por Código IBGE
duplicatas_codigo = df_limpo['Codigo_IBGE'].duplicated().sum()
print(f"   Duplicatas por Código IBGE: {duplicatas_codigo}")

if duplicatas_codigo > 0:
    # Mostrar exemplos de duplicatas
    codigos_duplicados = df_limpo[df_limpo['Codigo_IBGE'].duplicated(keep=False)]['Codigo_IBGE'].unique()
    print(f"   Códigos IBGE duplicados (primeiros 10): {codigos_duplicados[:10]}")
    
    # Salvar lista de duplicatas para análise
    df_duplicatas = df_limpo[df_limpo['Codigo_IBGE'].duplicated(keep=False)].sort_values('Codigo_IBGE')
    arquivo_duplicatas = BASE_DIR / "02_dados_processados" / "municipios_duplicados.xlsx"
    df_duplicatas.to_excel(arquivo_duplicatas, index=False)
    print(f"   ✓ Lista de duplicatas salva em: municipios_duplicados.xlsx")
    
    # Remover duplicatas (manter primeira ocorrência)
    print(f"\n   Removendo duplicatas (mantendo primeira ocorrência)...")
    df_limpo = df_limpo.drop_duplicates(subset='Codigo_IBGE', keep='first')
    print(f"   ✓ Duplicatas removidas: {duplicatas_codigo}")

# ================================================================================
# 5. VALIDAR TIPOS DE DADOS
# ================================================================================
print("\n" + "-" * 80)
print("5. VALIDANDO TIPOS DE DADOS")
print("-" * 80)

# Converter Código IBGE para inteiro (se possível)
try:
    df_limpo['Codigo_IBGE'] = pd.to_numeric(df_limpo['Codigo_IBGE'], errors='coerce')
    print(f"   ✓ Codigo_IBGE convertido para numérico")
except:
    print(f"   ✗ Não foi possível converter Codigo_IBGE")

# Converter Código UF para inteiro
try:
    df_limpo['Codigo_UF'] = pd.to_numeric(df_limpo['Codigo_UF'], errors='coerce')
    print(f"   ✓ Codigo_UF convertido para numérico")
except:
    print(f"   ✗ Não foi possível converter Codigo_UF")

# ================================================================================
# 6. ESTATÍSTICAS FINAIS
# ================================================================================
print("\n" + "-" * 80)
print("6. ESTATÍSTICAS DO ARQUIVO LIMPO")
print("-" * 80)

print(f"\n   Total de municípios: {len(df_limpo):,}")
print(f"   UFs únicas: {df_limpo['UF'].nunique()}")
print(f"   Municípios únicos (por nome): {df_limpo['Municipio'].nunique():,}")
print(f"   Códigos IBGE únicos: {df_limpo['Codigo_IBGE'].nunique():,}")

print(f"\n   Distribuição por Faixa ICM:")
dist_faixa = df_limpo['Faixa_ICM'].value_counts().sort_index()
for faixa, count in dist_faixa.items():
    print(f"      Faixa {faixa}: {count:,} municípios")

print(f"\n   Distribuição por Região:")
dist_regiao = df_limpo['Regiao'].value_counts()
for regiao, count in dist_regiao.items():
    if regiao not in ['Região', 'nan']:
        print(f"      {regiao}: {count:,} municípios")

# ================================================================================
# 7. SALVAR ARQUIVO LIMPO
# ================================================================================
print("\n" + "-" * 80)
print("7. SALVANDO ARQUIVO LIMPO")
print("-" * 80)

arquivo_saida = BASE_DIR / "dados" / "dados_faixa" / "ICM_Consolidado_LIMPO.xlsx"
df_limpo.to_excel(arquivo_saida, index=False)
print(f"   ✓ Arquivo salvo em: {arquivo_saida}")

# ================================================================================
# 8. RESUMO FINAL
# ================================================================================
print("\n" + "=" * 80)
print("📊 RESUMO DA LIMPEZA")
print("=" * 80)

print(f"""
ANTES:
  • Total de registros: {len(df):,}
  • Linhas de cabeçalho: {len(linhas_titulo) + len(linhas_cabecalho)}
  • Linhas vazias: {len(linhas_vazias)}
  • Duplicatas: {duplicatas_codigo}

DEPOIS:
  • Total de municípios: {len(df_limpo):,}
  • Códigos IBGE únicos: {df_limpo['Codigo_IBGE'].nunique():,}
  • Municípios únicos: {df_limpo['Municipio'].nunique():,}
  • UFs: {df_limpo['UF'].nunique()}

ARQUIVOS GERADOS:
  ✓ ICM_Consolidado_LIMPO.xlsx - Arquivo principal limpo
  ✓ municipios_duplicados.xlsx - Lista de duplicatas removidas

STATUS: ✅ Limpeza concluída com sucesso!
""")

print("=" * 80)

# Verificar se chegamos perto de 5.570
diferenca = abs(len(df_limpo) - 5570)
if diferenca <= 50:
    print(f"✅ VALIDAÇÃO: {len(df_limpo):,} municípios (diferença de {diferenca} em relação aos 5.570 oficiais)")
else:
    print(f"⚠️  ATENÇÃO: {len(df_limpo):,} municípios (diferença de {diferenca} em relação aos 5.570 oficiais)")
    print(f"   Pode haver municípios criados/extintos ou erros nos dados originais")

print("=" * 80)
