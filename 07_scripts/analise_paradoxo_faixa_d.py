import pandas as pd
import numpy as np

# Carregar dados
df = pd.read_excel('02_dados_processados/dados_municipios_clusterizados.xlsx')

# Filtrar Faixa D
df_d = df[df['Faixa_ICM'] == 'D']

# Agrupar por Cluster
stats = df_d.groupby('Cluster_Ordenado').agg({
    'Municipio': 'count',
    'Valor_Total': ['sum', 'mean', 'median']
})

stats.columns = ['Qtd_Municipios', 'Valor_Total_Soma', 'Valor_Total_Media', 'Valor_Total_Mediana']

# Calcular percentuais
total_valor_d = df_d['Valor_Total'].sum()
stats['%_do_Valor_Total_Faixa_D'] = (stats['Valor_Total_Soma'] / total_valor_d) * 100
stats['%_da_Qtd_Municipios'] = (stats['Qtd_Municipios'] / len(df_d)) * 100

print("ANÁLISE DO PARADOXO DA FAIXA D")
print("="*50)
print(stats.round(2))
