import pandas as pd
import json
import os

# Carregar dados
df = pd.read_excel('03_analises/fase4_regressao/auditoria_valores_reconstrucao.xlsx')

print("Colunas disponíveis:")
print(df.columns.tolist())
print(f"\nTotal de registros: {len(df)}")

# Filtrar apenas os casos de Alto Risco usando a coluna Alerta_Preco
alto_risco = df[df['Alerta_Preco'] == 'ALTO']
print(f"\nTotal de casos ALTO RISCO: {len(alto_risco)}")

# Ordenar por Valor_Numerico (maior para menor)
top10 = alto_risco.nlargest(10, 'Valor_Numerico')

print("\n" + "="*100)
print("TOP 10 CASOS DE ALTO RISCO - Maiores Valores")
print("="*100)
print(top10[['UF', 'Município', 'Desastres', 'Status', 'Valor_Numerico', 
            'Limite_Superior_P90', 'Desvio_Percentual']].to_string(index=False))

# Criar diretório se não existir
os.makedirs('docs/assets/data', exist_ok=True)

# Salvar em JSON para usar no HTML
top10_json = []
for _, row in top10.iterrows():
    top10_json.append({
        'uf': row['UF'],
        'municipio': row['Município'],
        'desastre': row['Desastres'],
        'status': row['Status'],
        'valor_solicitado': f"R$ {row['Valor_Numerico']:,.2f}",
        'valor_solicitado_num': row['Valor_Numerico'],
        'limite_p90': f"R$ {row['Limite_Superior_P90']:,.2f}",
        'limite_p90_num': row['Limite_Superior_P90'],
        'desvio_percentual': f"{row['Desvio_Percentual']:.1f}%"
    })

with open('docs/assets/data/top10_alto_risco.json', 'w', encoding='utf-8') as f:
    json.dump(top10_json, f, ensure_ascii=False, indent=2)

print("\n✅ Arquivo JSON salvo em: docs/assets/data/top10_alto_risco.json")
