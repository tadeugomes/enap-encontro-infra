import pandas as pd

file_path = r'c:\Users\tadeu\Downloads\enap_infra_encontro\dados\dados_faixa\ICM_Consolidado_LIMPO_V2.xlsx'
df = pd.read_excel(file_path)
print("Columns:", df.columns.tolist())
print(df.head())
