import pandas as pd
import numpy as np
from pathlib import Path

# Caminhos dos arquivos consolidados
arquivo_acompanhamento = Path(r"c:\Users\tadeu\Downloads\enap_infra_encontro\dados\dados_gerenciamento\Relatório_Consolidado_Acompanhamento_2017_2025.xlsx")
arquivo_faixas = Path(r"c:\Users\tadeu\Downloads\enap_infra_encontro\dados\dados_faixa\ICM_Consolidado_Todas_Faixas.xlsx")

# Arquivo de saída
arquivo_saida = Path(r"c:\Users\tadeu\Downloads\enap_infra_encontro\analise_estrutura.txt")

with open(arquivo_saida, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("ANÁLISE DA ESTRUTURA DOS DADOS CONSOLIDADOS\n")
    f.write("=" * 80 + "\n\n")

    # Analisar arquivo de Acompanhamento
    f.write("📊 ARQUIVO 1: Relatório de Acompanhamento (2017-2025)\n")
    f.write("-" * 80 + "\n")
    df_acomp = pd.read_excel(arquivo_acompanhamento)
    f.write(f"Dimensões: {df_acomp.shape[0]} linhas x {df_acomp.shape[1]} colunas\n\n")
    f.write("Colunas:\n")
    for i, col in enumerate(df_acomp.columns, 1):
        dtype = df_acomp[col].dtype
        nulls = df_acomp[col].isnull().sum()
        unique = df_acomp[col].nunique()
        f.write(f"  {i:2d}. {col:30s} | Tipo: {str(dtype):10s} | Nulos: {nulls:5d} | Únicos: {unique:5d}\n")

    # Analisar arquivo de Faixas ICM
    f.write("\n\n📊 ARQUIVO 2: ICM por Faixas (A, B, C, D)\n")
    f.write("-" * 80 + "\n")
    df_faixas = pd.read_excel(arquivo_faixas)
    f.write(f"Dimensões: {df_faixas.shape[0]} linhas x {df_faixas.shape[1]} colunas\n\n")
    f.write("Colunas:\n")
    for i, col in enumerate(df_faixas.columns, 1):
        dtype = df_faixas[col].dtype
        nulls = df_faixas[col].isnull().sum()
        unique = df_faixas[col].nunique()
        f.write(f"  {i:2d}. {col:30s} | Tipo: {str(dtype):10s} | Nulos: {nulls:5d} | Únicos: {unique:5d}\n")

    # Identificar possíveis chaves de junção
    f.write("\n\n🔗 ANÁLISE DE POSSÍVEIS CHAVES DE JUNÇÃO\n")
    f.write("-" * 80 + "\n")

    # Verificar colunas comuns
    colunas_acomp = set(df_acomp.columns)
    colunas_faixas = set(df_faixas.columns)
    colunas_comuns = colunas_acomp.intersection(colunas_faixas)

    f.write(f"Colunas em comum: {colunas_comuns if colunas_comuns else 'Nenhuma coluna exatamente igual'}\n\n")

    # Verificar colunas que podem ser chaves (município, UF, etc)
    f.write("Possíveis chaves de junção:\n")
    chaves_potenciais = ['Município', 'Municipio', 'UF', 'Estado', 'Código', 'IBGE', 'Cod_IBGE']
    for chave in chaves_potenciais:
        em_acomp = chave in df_acomp.columns
        em_faixas = chave in df_faixas.columns
        if em_acomp or em_faixas:
            f.write(f"  • {chave:20s} - Acompanhamento: {'✓' if em_acomp else '✗'}  |  Faixas: {'✓' if em_faixas else '✗'}\n")

    # Estatísticas descritivas básicas
    f.write("\n\n📈 ESTATÍSTICAS DESCRITIVAS\n")
    f.write("-" * 80 + "\n")

    f.write("\nAcompanhamento - Distribuição temporal:\n")
    if 'Ano_Relatorio' in df_acomp.columns:
        f.write(str(df_acomp['Ano_Relatorio'].value_counts().sort_index()) + "\n")

    f.write("\nFaixas ICM - Distribuição por faixa:\n")
    if 'Faixa' in df_faixas.columns:
        f.write(str(df_faixas['Faixa'].value_counts().sort_index()) + "\n")

    # Verificar colunas numéricas
    f.write("\n\nColunas numéricas em Acompanhamento:\n")
    num_cols_acomp = df_acomp.select_dtypes(include=[np.number]).columns.tolist()
    f.write(f"  {num_cols_acomp}\n")

    f.write("\nColunas numéricas em Faixas ICM:\n")
    num_cols_faixas = df_faixas.select_dtypes(include=[np.number]).columns.tolist()
    f.write(f"  {num_cols_faixas}\n")

    f.write("\n" + "=" * 80 + "\n")

print(f"✓ Análise salva em: {arquivo_saida}")

# Também imprimir resumo na tela
print("\n" + "=" * 80)
print("RESUMO DA ANÁLISE")
print("=" * 80)
print(f"\n📊 Acompanhamento: {df_acomp.shape[0]} linhas x {df_acomp.shape[1]} colunas")
print(f"   Colunas: {list(df_acomp.columns)}")
print(f"\n📊 Faixas ICM: {df_faixas.shape[0]} linhas x {df_faixas.shape[1]} colunas")
print(f"   Colunas: {list(df_faixas.columns)}")
