import shutil
from pathlib import Path
import os

BASE_DIR = Path(r"c:\Users\tadeu\Downloads\enap_infra_encontro")

def move_file(src_name, dest_folder):
    src = BASE_DIR / src_name
    dest_dir = BASE_DIR / dest_folder
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src_name
    
    if src.exists():
        print(f"Movendo {src.name} para {dest_folder}...")
        shutil.move(str(src), str(dest))
    else:
        print(f"⚠️ Arquivo não encontrado na origem: {src_name}")

def move_dir_contents(src_folder_name, dest_folder_name):
    src_dir = BASE_DIR / src_folder_name
    dest_dir = BASE_DIR / dest_folder_name
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    if src_dir.exists():
        print(f"\nMovendo conteúdo de {src_folder_name} para {dest_folder_name}...")
        for item in src_dir.glob("*"):
            if item.is_file():
                dest = dest_dir / item.name
                shutil.move(str(item), str(dest))
                print(f"  ✓ {item.name}")
        # Opcional: remover diretório vazio
        try:
            src_dir.rmdir()
            print(f"  ✓ Diretório {src_folder_name} removido.")
        except:
            pass
    else:
        print(f"⚠️ Diretório origem não encontrado: {src_folder_name}")

print("="*80)
print("ORGANIZANDO ARQUIVOS GERADOS")
print("="*80)

# 1. Mover arquivos da raiz para pastas corretas
move_file("analise_detalhada_por_faixa.xlsx", "03_analises/fase1_regressao")
move_file("dados_agregados_municipio_ATUALIZADO.xlsx", "02_dados_processados")
move_file("dados_merged_acompanhamento_icm.xlsx", "02_dados_processados")
move_file("analise_estrutura.txt", "03_analises/exploratoria")

# 2. Mover gráficos
move_dir_contents("graficos", "04_visualizacoes/exploratoria")
move_dir_contents("graficos_ml", "04_visualizacoes/fase1_regressao")

print("\n" + "="*80)
print("✅ ORGANIZAÇÃO CONCLUÍDA!")
print("="*80)
