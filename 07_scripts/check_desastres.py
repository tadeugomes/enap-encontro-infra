import pandas as pd

file_path = r'c:\Users\tadeu\Downloads\enap_infra_encontro\dados\dados_gerenciamento\Relatório_Consolidado_Acompanhamento_2017_2025.xlsx'
df = pd.read_excel(file_path)
print("Distinct Desastres:", df['Desastres'].nunique())
print(df['Desastres'].value_counts().head(10))
