import pandas as pd

file_path = r'c:\Users\tadeu\Downloads\enap_infra_encontro\02_dados_processados\dados_merged_acompanhamento_icm.xlsx'
df = pd.read_excel(file_path)
print("Columns:", df.columns.tolist())
print(df.head())
print(df.info())
