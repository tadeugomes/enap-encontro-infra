import pandas as pd
from pathlib import Path

# Carregar arquivo ICM consolidado
arquivo_icm = Path(r"c:\Users\tadeu\Downloads\enap_infra_encontro\dados\dados_faixa\ICM_Consolidado_Todas_Faixas.xlsx")
df_icm = pd.read_excel(arquivo_icm)

# Arquivo de saída
arquivo_saida = Path(r"c:\Users\tadeu\Downloads\enap_infra_encontro\investigacao_duplicatas.txt")

with open(arquivo_saida, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("INVESTIGAÇÃO: POR QUE 5.613 REGISTROS SE O BRASIL TEM 5.570 MUNICÍPIOS?\n")
    f.write("=" * 80 + "\n\n")
    
    f.write(f"Total de registros no arquivo: {len(df_icm):,}\n")
    f.write(f"Total de municípios no Brasil: 5.570\n")
    f.write(f"Diferença: {len(df_icm) - 5570:,} registros a mais\n\n")
    
    # Examinar arquivo original de cada faixa
    f.write("-" * 80 + "\n")
    f.write("EXAMINANDO ARQUIVOS ORIGINAIS POR FAIXA:\n")
    f.write("-" * 80 + "\n\n")
    
    base_dir = Path(r"c:\Users\tadeu\Downloads\enap_infra_encontro\dados\dados_faixa")
    
    total_original = 0
    for faixa in ['A', 'B', 'C', 'D']:
        arquivo_original = base_dir / f"ICM Faixa {faixa}.xlsx"
        df_original = pd.read_excel(arquivo_original)
        
        # Contar linhas que não são cabeçalhos (procurar por linhas com dados válidos)
        # Geralmente a primeira linha pode ser um título
        linhas_validas = len(df_original)
        
        f.write(f"\nFaixa {faixa}:\n")
        f.write(f"  Total de linhas no arquivo original: {linhas_validas}\n")
        f.write(f"  Primeiras 3 linhas:\n")
        f.write(df_original.head(3).to_string(max_cols=5) + "\n")
        
        total_original += linhas_validas
    
    f.write(f"\n\nTotal de linhas nos arquivos originais: {total_original:,}\n")
    f.write(f"Total após consolidação: {len(df_icm):,}\n")
    f.write(f"Diferença: {len(df_icm) - total_original:,}\n")
    
    # Verificar se há linhas de cabeçalho duplicadas
    f.write("\n" + "-" * 80 + "\n")
    f.write("VERIFICANDO LINHAS DE CABEÇALHO/TÍTULO:\n")
    f.write("-" * 80 + "\n\n")
    
    # Procurar linhas que contenham texto como "Municípios na Faixa"
    linhas_titulo = df_icm[df_icm.iloc[:, 0].astype(str).str.contains('Municípios na Faixa', na=False)]
    f.write(f"Linhas com 'Municípios na Faixa': {len(linhas_titulo)}\n")
    
    if len(linhas_titulo) > 0:
        f.write("\nExemplos:\n")
        f.write(linhas_titulo.head(10).to_string() + "\n")
    
    # Verificar linhas com muitos valores nulos
    f.write("\n" + "-" * 80 + "\n")
    f.write("LINHAS COM MUITOS VALORES NULOS:\n")
    f.write("-" * 80 + "\n\n")
    
    nulos_por_linha = df_icm.isnull().sum(axis=1)
    linhas_problematicas = df_icm[nulos_por_linha > 25]
    f.write(f"Linhas com mais de 25 valores nulos: {len(linhas_problematicas)}\n")
    
    # Tentar identificar município
    f.write("\n" + "-" * 80 + "\n")
    f.write("IDENTIFICANDO POSSÍVEL COLUNA DE MUNICÍPIO:\n")
    f.write("-" * 80 + "\n\n")
    
    for col in df_icm.columns[:10]:
        unicos = df_icm[col].nunique()
        f.write(f"\n{col}:\n")
        f.write(f"  Valores únicos: {unicos:,}\n")
        if unicos < 20:
            f.write(f"  Valores: {df_icm[col].value_counts().head(10).to_dict()}\n")
        else:
            f.write(f"  Primeiros 5: {df_icm[col].dropna().head(5).tolist()}\n")

print(f"✓ Investigação salva em: {arquivo_saida}")

# Também fazer uma análise mais direta
print("\n" + "=" * 80)
print("RESUMO DA INVESTIGAÇÃO")
print("=" * 80)

# Verificar se há linhas de cabeçalho
linhas_titulo = df_icm[df_icm.iloc[:, 0].astype(str).str.contains('Municípios na Faixa', na=False)]
print(f"\n1. Linhas de título/cabeçalho encontradas: {len(linhas_titulo)}")

# Verificar duplicatas reais
# Tentar identificar coluna de município (geralmente a que tem ~5500 valores únicos)
print(f"\n2. Análise de valores únicos por coluna:")
for col in df_icm.columns[:10]:
    unicos = df_icm[col].nunique()
    if 5000 <= unicos <= 5700:
        print(f"   {col}: {unicos:,} valores únicos ← Possível coluna de município")
        
        # Verificar duplicatas nesta coluna
        duplicatas = df_icm[col].duplicated().sum()
        print(f"      Duplicatas: {duplicatas}")

print(f"\n3. Total de registros: {len(df_icm):,}")
print(f"   Municípios no Brasil: 5.570")
print(f"   Diferença: +{len(df_icm) - 5570} registros")

# Verificar distribuição por faixa
print(f"\n4. Distribuição por faixa:")
print(df_icm['Faixa'].value_counts().sort_index())

soma_faixas = df_icm['Faixa'].value_counts().sum()
print(f"\n   Soma das faixas: {soma_faixas:,}")
