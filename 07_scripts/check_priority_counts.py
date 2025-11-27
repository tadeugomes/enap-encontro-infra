
import pandas as pd
from pathlib import Path

base_dir = Path(r"c:\Users\tadeu\Downloads\enap_infra_encontro")
file_path = base_dir / "02_dados_processados" / "dados_municipios_clusterizados.xlsx"

try:
    df = pd.read_excel(file_path)
    print("Colunas:", df.columns.tolist())
    
    if 'Cluster_Ordenado' in df.columns:
        counts = df['Cluster_Ordenado'].value_counts().sort_index()
        print("\nContagem por Cluster:")
        print(counts)
        
        # Cluster 0 = Baixo Impacto
        # Cluster 1 = Alto Custo
        # Cluster 2 = Outlier (Porto Alegre)
        # Cluster 3 = Alta Frequência
        
        # Assumindo Prioritários = 1, 2, 3
        nao_prioritarios = counts.get(0, 0)
        prioritarios = counts.get(1, 0) + counts.get(2, 0) + counts.get(3, 0)
        
        print(f"\nNão Prioritários (Cluster 0): {nao_prioritarios}")
        print(f"Prioritários (Clusters 1, 2, 3): {prioritarios}")
        print(f"Total: {nao_prioritarios + prioritarios}")
        
    else:
        print("Coluna 'Cluster_Ordenado' não encontrada.")

except Exception as e:
    print(f"Erro ao ler arquivo: {e}")
