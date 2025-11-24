"""
SCRIPT: Limpeza do Arquivo ICM Consolidado - Critério de Benefício
Objetivo: Remover duplicatas priorizando a MELHOR faixa (maior capacidade) em casos de conflito.
Autor: Análise de Dados - ENAP
Data: 22/11/2025
"""

import pandas as pd
from pathlib import Path

print("=" * 80)
print("LIMPEZA DO ARQUIVO ICM CONSOLIDADO - CRITÉRIO DE BENEFÍCIO")
print("=" * 80)

BASE_DIR = Path(r"c:\Users\tadeu\Downloads\enap_infra_encontro")
ARQUIVO_ORIGINAL = BASE_DIR / "dados" / "dados_faixa" / "ICM_Consolidado_Todas_Faixas.xlsx"

# 1. Carregar dados
print("\n📂 1. Carregando arquivo original...")
df = pd.read_excel(ARQUIVO_ORIGINAL)

print(f"Total de registros originais: {len(df):,}")

# 2. Limpeza básica
print("\n🧹 2. Realizando limpeza básica...")

# Remover linhas de cabeçalho/título
df_limpo = df[~df.iloc[:, 0].astype(str).str.contains("Municípios na Faixa|Código IBGE", na=False, case=False)]

# Remover linhas vazias
nulos_por_linha = df_limpo.isnull().sum(axis=1)
df_limpo = df_limpo[nulos_por_linha <= 25]

# Renomear colunas
novos_nomes = {
    'Unnamed: 0': 'Codigo_IBGE',
    'Unnamed: 1': 'UF',
    'Unnamed: 2': 'Codigo_UF',
    'Unnamed: 3': 'Municipio',
    'Unnamed: 4': 'Faixa_Populacional',
    'Unnamed: 5': 'Regiao',
    'Faixa': 'Faixa_ICM'
}
df_limpo = df_limpo.rename(columns=novos_nomes)

# Converter Código IBGE
df_limpo['Codigo_IBGE'] = pd.to_numeric(df_limpo['Codigo_IBGE'], errors='coerce')
df_limpo = df_limpo.dropna(subset=['Codigo_IBGE'])

print(f"Registros após limpeza básica: {len(df_limpo):,}")

# 3. Tratamento de Duplicatas com Critério de BENEFÍCIO
print("\n🔍 3. Tratando duplicatas com critério de MELHOR FAIXA (Benefício)...")

# Definir ordem de benefício (A é melhor/maior capacidade que D)
# Quanto maior o score, melhor a faixa.
ordem_beneficio = {'A': 4, 'B': 3, 'C': 2, 'D': 1}
df_limpo['Score_Beneficio'] = df_limpo['Faixa_ICM'].map(ordem_beneficio)

# Ordenar por Código IBGE e Score de Benefício (decrescente)
# Assim, a faixa A (4) ficará antes da B (3) para o mesmo município
df_limpo = df_limpo.sort_values(by=['Codigo_IBGE', 'Score_Beneficio'], ascending=[True, False])

# Identificar duplicatas antes da remoção para log
duplicatas = df_limpo[df_limpo.duplicated(subset=['Codigo_IBGE'], keep=False)]
n_duplicatas = df_limpo['Codigo_IBGE'].duplicated().sum()

print(f"Encontrados {n_duplicatas} municípios duplicados.")

if n_duplicatas > 0:
    print("\nExemplos de resolução de conflito (Priorizando MELHOR faixa):")
    codigos_exemplo = duplicatas['Codigo_IBGE'].unique()[:5]
    for codigo in codigos_exemplo:
        grupo = df_limpo[df_limpo['Codigo_IBGE'] == codigo]
        mun = grupo['Municipio'].iloc[0]
        faixas = grupo['Faixa_ICM'].tolist()
        escolhida = faixas[0] # Como ordenamos por benefício decrescente, a primeira é a melhor
        print(f"  {mun}: Faixas encontradas {faixas} -> Mantida: {escolhida}")

# Remover duplicatas mantendo a primeira (que é a de maior benefício devido à ordenação)
df_final = df_limpo.drop_duplicates(subset=['Codigo_IBGE'], keep='first')

# Remover coluna auxiliar
df_final = df_final.drop(columns=['Score_Beneficio'])

print(f"\nRegistros finais únicos: {len(df_final):,}")

# 4. Salvar arquivos
print("\n💾 4. Salvando arquivos limpos...")

# Salvar versão específica
arquivo_saida_v3 = BASE_DIR / "dados" / "dados_faixa" / "ICM_Consolidado_LIMPO_Beneficio.xlsx"
df_final.to_excel(arquivo_saida_v3, index=False)
print(f"Arquivo específico salvo em: {arquivo_saida_v3}")

# Atualizar arquivo padrão usado pelos outros scripts
arquivo_padrao = BASE_DIR / "dados" / "dados_faixa" / "ICM_Consolidado_LIMPO.xlsx"
df_final.to_excel(arquivo_padrao, index=False)
print(f"Arquivo padrão atualizado: {arquivo_padrao}")

# Atualizar arquivo na pasta de processados também, para garantir consistência
arquivo_processado = BASE_DIR / "02_dados_processados" / "ICM_Consolidado_LIMPO.xlsx"
df_final.to_excel(arquivo_processado, index=False)
print(f"Arquivo processado atualizado: {arquivo_processado}")

print("\n" + "=" * 80)
print("✅ LIMPEZA (CRITÉRIO BENEFÍCIO) CONCLUÍDA COM SUCESSO!")
print("=" * 80)
