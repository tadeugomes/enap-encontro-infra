"""
SCRIPT: Limpeza do Arquivo ICM Consolidado - V2 (Critério de Risco)
Objetivo: Remover duplicatas priorizando a PIOR faixa (maior vulnerabilidade) em casos de conflito.
Autor: Análise de Dados - ENAP
Data: 22/11/2025
"""

import pandas as pd
from pathlib import Path

print("=" * 80)
print("LIMPEZA DO ARQUIVO ICM CONSOLIDADO - V2 (CRITÉRIO DE RISCO)")
print("=" * 80)

BASE_DIR = Path(__file__).resolve().parent.parent
ARQUIVO_ORIGINAL = BASE_DIR / "dados" / "dados_faixa" / "ICM_Consolidado_Todas_Faixas.xlsx"

# 1. Carregar dados
print("\n📂 1. Carregando arquivo original...")
df = pd.read_excel(ARQUIVO_ORIGINAL)

print(f"Total de registros originais: {len(df):,}")

# 2. Limpeza básica (igual à V1)
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

# 3. Tratamento de Duplicatas com Critério de Risco
print("\n🔍 3. Tratando duplicatas com critério de PIOR FAIXA...")

# Definir ordem de risco (D é pior/maior risco que A)
ordem_risco = {'D': 4, 'C': 3, 'B': 2, 'A': 1}
df_limpo['Score_Risco'] = df_limpo['Faixa_ICM'].map(ordem_risco)

# Ordenar por Código IBGE e Score de Risco (decrescente)
# Assim, a faixa D (4) ficará antes da B (2) para o mesmo município
df_limpo = df_limpo.sort_values(by=['Codigo_IBGE', 'Score_Risco'], ascending=[True, False])

# Identificar duplicatas antes da remoção para log
duplicatas = df_limpo[df_limpo.duplicated(subset=['Codigo_IBGE'], keep=False)]
n_duplicatas = df_limpo['Codigo_IBGE'].duplicated().sum()

print(f"Encontrados {n_duplicatas} municípios duplicados.")

if n_duplicatas > 0:
    print("\nExemplos de resolução de conflito:")
    codigos_exemplo = duplicatas['Codigo_IBGE'].unique()[:5]
    for codigo in codigos_exemplo:
        grupo = df_limpo[df_limpo['Codigo_IBGE'] == codigo]
        mun = grupo['Municipio'].iloc[0]
        faixas = grupo['Faixa_ICM'].tolist()
        escolhida = faixas[0] # Como ordenamos por risco decrescente, a primeira é a pior
        print(f"  {mun}: Faixas encontradas {faixas} -> Mantida: {escolhida}")

# Remover duplicatas mantendo a primeira (que é a de maior risco devido à ordenação)
df_final = df_limpo.drop_duplicates(subset=['Codigo_IBGE'], keep='first')

# Remover coluna auxiliar
df_final = df_final.drop(columns=['Score_Risco'])

print(f"\nRegistros finais únicos: {len(df_final):,}")

# 4. Salvar arquivo V2
print("\n💾 4. Salvando arquivo limpo V2...")
arquivo_saida = BASE_DIR / "dados" / "dados_faixa" / "ICM_Consolidado_LIMPO_V2.xlsx"
df_final.to_excel(arquivo_saida, index=False)

print(f"Arquivo salvo em: {arquivo_saida}")

# 5. Atualizar arquivo principal (sobrescrever o LIMPO anterior ou manter V2?)
# Por segurança, vamos manter o V2 e atualizar o script de análise para usar o V2 se desejar.
# Mas o usuário pediu para "Refazer limpeza", então vou atualizar o arquivo "LIMPO" padrão também
# para que os scripts existentes funcionem com a nova lógica.

arquivo_padrao = BASE_DIR / "dados" / "dados_faixa" / "ICM_Consolidado_LIMPO.xlsx"
df_final.to_excel(arquivo_padrao, index=False)
print(f"Arquivo padrão atualizado: {arquivo_padrao}")

print("\n" + "=" * 80)
print("✅ LIMPEZA V2 CONCLUÍDA COM SUCESSO!")
print("=" * 80)
