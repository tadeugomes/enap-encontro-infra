import pandas as pd
import os
from pathlib import Path

# Diretório com os arquivos
data_dir = Path(r"c:\Users\tadeu\Downloads\enap_infra_encontro\dados\dados_gerenciamento")

# Lista de arquivos de Acompanhamento de Processos (2017-2025)
anos = range(2017, 2026)
arquivos_acompanhamento = [
    data_dir / f"Relatório Gerencial de Reconstrução - Acompanhamento de Processos {ano}.xls"
    for ano in anos
]

# Lista para armazenar os dataframes
dfs = []

print("Processando arquivos de Acompanhamento de Processos...")
print("-" * 60)

for arquivo in arquivos_acompanhamento:
    if arquivo.exists():
        print(f"Lendo: {arquivo.name}")
        try:
            # Ler o arquivo Excel
            df = pd.read_excel(arquivo)
            
            # Extrair o ano do nome do arquivo
            ano = arquivo.stem.split()[-1]
            
            # Adicionar coluna com o ano
            df['Ano_Relatorio'] = ano
            
            # Adicionar à lista
            dfs.append(df)
            print(f"  ✓ {len(df)} linhas carregadas")
            
        except Exception as e:
            print(f"  ✗ Erro ao ler {arquivo.name}: {e}")
    else:
        print(f"  ✗ Arquivo não encontrado: {arquivo.name}")

print("-" * 60)

if dfs:
    # Concatenar todos os dataframes
    df_consolidado = pd.concat(dfs, ignore_index=True)
    
    print(f"\nTotal de linhas consolidadas: {len(df_consolidado)}")
    print(f"Colunas: {list(df_consolidado.columns)}")
    
    # Salvar o arquivo consolidado
    arquivo_saida = data_dir / "Relatório_Consolidado_Acompanhamento_2017_2025.xlsx"
    df_consolidado.to_excel(arquivo_saida, index=False, engine='openpyxl')
    
    print(f"\n✓ Arquivo consolidado salvo em:")
    print(f"  {arquivo_saida}")
    
    # Mostrar resumo por ano
    print("\nResumo por ano:")
    print(df_consolidado['Ano_Relatorio'].value_counts().sort_index())
    
else:
    print("\n✗ Nenhum arquivo foi processado com sucesso.")

print("\n" + "=" * 60)
print("NOTA: Os arquivos de 'Recursos Liberados' foram mantidos")
print("separados conforme solicitado, pois possuem estrutura diferente.")
print("=" * 60)
