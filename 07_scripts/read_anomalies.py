import pandas as pd

file_path = r'c:\Users\tadeu\Downloads\enap_infra_encontro\05_modelos\anomalias_isolation_forest.xlsx'
df = pd.read_excel(file_path)
print(df.head(20))
