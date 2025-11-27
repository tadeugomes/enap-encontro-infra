import pandas as pd
import json

# Carregar dados
BASE_DIR = r"c:\Users\tadeu\Downloads\enap_infra_encontro"
arquivo_acomp = BASE_DIR + r"\dados\dados_gerenciamento\Relatório_Consolidado_Acompanhamento_2017_2025.xlsx"
arquivo_merged = BASE_DIR + r"\dados_merged_acompanhamento_icm.xlsx"

df_merged = pd.read_excel(arquivo_merged)
df_acomp = pd.read_excel(arquivo_acomp)

# Padronizar
df_acomp['Municipio_Padrao'] = df_acomp['Município'].str.upper().str.strip()
df_merged['Municipio_Padrao'] = df_merged['Municipio'].str.upper().str.strip()

# Merge
df_completo = pd.merge(
    df_acomp[['UF', 'Municipio_Padrao', 'Desastres', 'Valor Solicitado']],
    df_merged[['UF', 'Municipio_Padrao', 'Faixa_ICM']].drop_duplicates(),
    on=['UF', 'Municipio_Padrao'],
    how='inner'
)

# Converter valor
df_completo['Valor_Numerico'] = df_completo['Valor Solicitado'].astype(str).str.replace('R$', '').str.replace('.', '').str.replace(',', '.').str.strip()
df_completo['Valor_Numerico'] = pd.to_numeric(df_completo['Valor_Numerico'], errors='coerce')

# 1. Top 5 desastres por faixa
print("=== TOP 5 DESASTRES POR FAIXA ===\n")
top_desastres = {}
for faixa in ['A', 'B', 'C', 'D']:
    top = df_completo[df_completo['Faixa_ICM'] == faixa]['Desastres'].value_counts().head(5)
    top_desastres[f'Faixa_{faixa}'] = top.to_dict()
    print(f"Faixa {faixa}:")
    for desastre, count in top.items():
        print(f"  {desastre}: {count}")
    print()

# 2. Valor médio por tipo de desastre (top 10) e faixa
print("\n=== VALOR MÉDIO POR DESASTRE (TOP 10) E FAIXA ===\n")
top_10_desastres = df_completo['Desastres'].value_counts().head(10).index

tabela_valores = []
for desastre in top_10_desastres:
    linha = {'Desastre': desastre}
    df_desastre = df_completo[df_completo['Desastres'] == desastre]
    for faixa in ['A', 'B', 'C', 'D']:
        valores = df_desastre[df_desastre['Faixa_ICM'] == faixa]['Valor_Numerico'].dropna()
        if len(valores) > 0:
            linha[f'Faixa_{faixa}'] = f"R$ {valores.mean():,.2f}"
            linha[f'Faixa_{faixa}_casos'] = len(valores)
        else:
            linha[f'Faixa_{faixa}'] = "-"
            linha[f'Faixa_{faixa}_casos'] = 0
    tabela_valores.append(linha)
    
df_tabela = pd.DataFrame(tabela_valores)
print(df_tabela.to_string(index=False))

# Salvar em JSON para uso no HTML
with open(BASE_DIR + r'\dados_tabelas_fase1.json', 'w', encoding='utf-8') as f:
    json.dump({
        'top_desastres': top_desastres,
        'valores_medios': tabela_valores
    }, f, ensure_ascii=False, indent=2)

print("\n✓ Dados salvos em dados_tabelas_fase1.json")
