import pandas as pd
import os
from pathlib import Path

# Diretório com os arquivos
data_dir = Path(r"c:\Users\tadeu\Downloads\enap_infra_encontro\dados\dados_faixa")

# Lista de arquivos de ICM por faixa
faixas = ['A', 'B', 'C', 'D']
arquivos_faixa = [
    data_dir / f"ICM Faixa {faixa}.xlsx"
    for faixa in faixas
]

# Lista para armazenar os dataframes
dfs = []

print("Processando arquivos de ICM por Faixa...")
print("-" * 60)

for arquivo in arquivos_faixa:
    if arquivo.exists():
        print(f"Lendo: {arquivo.name}")
        try:
            # Ler o arquivo Excel
            df = pd.read_excel(arquivo)
            
            # Extrair a faixa do nome do arquivo
            faixa = arquivo.stem.split()[-1]  # Pega a última palavra (A, B, C ou D)
            
            # Adicionar coluna com a faixa
            df['Faixa'] = faixa
            
            # Adicionar à lista
            dfs.append(df)
            print(f"  ✓ {len(df)} linhas carregadas (Faixa {faixa})")
            
        except Exception as e:
            print(f"  ✗ Erro ao ler {arquivo.name}: {e}")
    else:
        print(f"  ✗ Arquivo não encontrado: {arquivo.name}")

print("-" * 60)

if dfs:
    # Concatenar todos os dataframes
    df_consolidado = pd.concat(dfs, ignore_index=True)
    
    print(f"\nTotal de linhas consolidadas: {len(df_consolidado)}")
    print(f"\nColunas disponíveis:")
    for i, col in enumerate(df_consolidado.columns, 1):
        print(f"  {i}. {col}")
    
    # Salvar o arquivo consolidado
    arquivo_saida = data_dir / "ICM_Consolidado_Todas_Faixas.xlsx"
    df_consolidado.to_excel(arquivo_saida, index=False, engine='openpyxl')
    
    print(f"\n✓ Arquivo consolidado salvo em:")
    print(f"  {arquivo_saida}")
    
    # Mostrar resumo por faixa
    print("\nResumo por faixa:")
    resumo = df_consolidado['Faixa'].value_counts().sort_index()
    for faixa, count in resumo.items():
        print(f"  Faixa {faixa}: {count} registros")
    
    # Mostrar estatísticas adicionais se houver coluna de UF
    if 'UF' in df_consolidado.columns:
        print(f"\nTotal de UFs únicas: {df_consolidado['UF'].nunique()}")
    
    if 'Município' in df_consolidado.columns or 'Municipio' in df_consolidado.columns:
        col_municipio = 'Município' if 'Município' in df_consolidado.columns else 'Municipio'
        print(f"Total de municípios únicos: {df_consolidado[col_municipio].nunique()}")
    
else:
    print("\n✗ Nenhum arquivo foi processado com sucesso.")

print("\n" + "=" * 60)
print("Consolidação concluída!")
print("=" * 60)
