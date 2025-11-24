"""
SCRIPT: Limpeza de Arquivos Obsoletos
Objetivo: Remover scripts e arquivos que não são mais utilizados no projeto.
"""

import os
from pathlib import Path

print("=" * 80)
print("LIMPEZA DE ARQUIVOS OBSOLETOS")
print("=" * 80)

BASE_DIR = Path(r"c:\Users\tadeu\Downloads\enap_infra_encontro")
SCRIPTS_DIR = BASE_DIR / "07_scripts"
RELATORIOS_DIR = BASE_DIR / "06_relatorios"

# Lista de arquivos para remover (caminhos relativos ou nomes)
arquivos_para_remover = [
    # Scripts na raiz ou pasta scripts (verificaremos ambos)
    "analise_exploratoria_inicial.py",
    "limpar_arquivo_icm.py",
    "analise_outliers.py",
    "investigar_duplicatas_icm.py",
    
    # Scripts de investigação temporária
    "verificar_impacto_limpeza.py",
    "investigar_duplicatas_detalhado.py",
    "analisar_padrao_duplicatas.py",
    "analise_cirurgica_duplicatas.py",
    "inspecionar_original.py",
    
    # Relatórios antigos (podem estar na raiz ou em relatorios)
    "README_ANALISE.md",
]

locais_busca = [BASE_DIR, SCRIPTS_DIR, RELATORIOS_DIR]

count_removidos = 0

print("\nProcurando e removendo arquivos...")

for nome_arquivo in arquivos_para_remover:
    removido = False
    for pasta in locais_busca:
        arquivo = pasta / nome_arquivo
        if arquivo.exists():
            try:
                os.remove(arquivo)
                print(f"✓ Removido: {arquivo}")
                removido = True
                count_removidos += 1
                # Se encontrou em uma pasta, para de procurar nas outras (evita erro se duplicado, embora improvável)
                break 
            except Exception as e:
                print(f"✗ Erro ao remover {arquivo}: {e}")
    
    if not removido:
        print(f"- Não encontrado: {nome_arquivo}")

print("-" * 80)
print(f"Total de arquivos removidos: {count_removidos}")
print("=" * 80)
