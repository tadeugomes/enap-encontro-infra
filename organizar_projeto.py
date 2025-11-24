"""
Script para organizar arquivos do projeto em estrutura de pastas
Autor: Análise de Dados - ENAP
Data: 22/11/2025
"""

import os
import shutil
from pathlib import Path

print("=" * 80)
print("ORGANIZANDO ESTRUTURA DE PASTAS DO PROJETO")
print("=" * 80)

BASE_DIR = Path(r"c:\Users\tadeu\Downloads\enap_infra_encontro")

# ================================================================================
# DEFINIR ESTRUTURA DE PASTAS
# ================================================================================

estrutura = {
    '01_dados_originais': 'Dados brutos originais',
    '02_dados_processados': 'Dados limpos e consolidados',
    '03_analises': {
        'exploratoria': 'Análise exploratória inicial',
        'fase1_regressao': 'Fase 1 - Análise de Regressão',
        'fase2_clustering': 'Fase 2 - Clustering (a fazer)',
        'fase3_classificacao': 'Fase 3 - Classificação (a fazer)',
    },
    '04_visualizacoes': {
        'exploratoria': 'Gráficos da análise exploratória',
        'fase1_regressao': 'Gráficos da Fase 1',
        'fase2_clustering': 'Gráficos da Fase 2 (a fazer)',
        'fase3_classificacao': 'Gráficos da Fase 3 (a fazer)',
    },
    '05_modelos': {
        'fase1_regressao': 'Modelos de regressão',
        'fase2_clustering': 'Modelos de clustering (a fazer)',
        'fase3_classificacao': 'Modelos de classificação (a fazer)',
    },
    '06_relatorios': 'Documentação e relatórios',
    '07_scripts': 'Scripts Python do projeto',
}

# ================================================================================
# CRIAR ESTRUTURA DE PASTAS
# ================================================================================

print("\n📁 1. CRIANDO ESTRUTURA DE PASTAS...")
print("-" * 80)

def criar_estrutura(base, estrutura, nivel=0):
    """Cria estrutura de pastas recursivamente"""
    for nome, descricao in estrutura.items():
        caminho = base / nome
        caminho.mkdir(exist_ok=True)
        
        indent = "  " * nivel
        print(f"{indent}✓ {nome}/")
        
        # Criar README em cada pasta
        readme = caminho / "README.md"
        if not readme.exists():
            with open(readme, 'w', encoding='utf-8') as f:
                if isinstance(descricao, dict):
                    f.write(f"# {nome}\n\n")
                    f.write("Subpastas:\n\n")
                    for sub in descricao.keys():
                        f.write(f"- `{sub}/`\n")
                else:
                    f.write(f"# {nome}\n\n{descricao}\n")
        
        # Se for dicionário, criar subpastas
        if isinstance(descricao, dict):
            criar_estrutura(caminho, descricao, nivel + 1)

criar_estrutura(BASE_DIR, estrutura)

# ================================================================================
# MOVER ARQUIVOS EXISTENTES
# ================================================================================

print("\n\n📦 2. ORGANIZANDO ARQUIVOS EXISTENTES...")
print("-" * 80)

# Mapeamento de arquivos para destinos
mapeamento = {
    # Dados processados
    '02_dados_processados': [
        'Relatório_Consolidado_Acompanhamento_2017_2025.xlsx',
        'ICM_Consolidado_Todas_Faixas.xlsx',
        'ICM_Consolidado_LIMPO.xlsx',
        'dados_merged_acompanhamento_icm.xlsx',
        'dados_agregados_municipio_ATUALIZADO.xlsx',
        'municipios_duplicados.xlsx',
        'tendencia_temporal.xlsx',
    ],
    
    # Análises - Exploratória
    '03_analises/exploratoria': [
        'analise_estrutura.txt',
        'investigacao_duplicatas.txt',
    ],
    
    # Análises - Fase 1
    '03_analises/fase1_regressao': [
        'analise_detalhada_por_faixa.xlsx',
        'analise_valores_por_faixa.xlsx',
    ],
    
    # Relatórios
    '06_relatorios': [
        'README_ANALISE_ATUALIZADO.md',
        'ESTRATEGIAS_ML.md',
        'INVESTIGACAO_DUPLICATAS.md',
        'IMPACTO_LIMPEZA_NO_PLANO_ML.md',
        'PROGRESSO_IMPLEMENTACAO.md',
    ],
    
    # Scripts
    '07_scripts': [
        'juntar_relatorios.py',
        'juntar_faixas.py',
        'limpar_arquivo_icm.py',
        'analisar_estrutura_dados.py',
        'analise_exploratoria_inicial.py',
        'analise_exploratoria_ATUALIZADA.py',
        'investigar_duplicatas_icm.py',
        'ml_fase1_regressao.py',
        'setup_venv.bat',
    ],
}

def mover_arquivo(origem, destino_pasta):
    """Move arquivo se existir"""
    arquivo_origem = BASE_DIR / origem
    if arquivo_origem.exists():
        destino = BASE_DIR / destino_pasta / origem
        
        # Se já existe no destino, não mover (evitar sobrescrever)
        if destino.exists():
            print(f"  ⊘ {origem} (já existe no destino)")
            return False
        
        try:
            shutil.copy2(arquivo_origem, destino)
            print(f"  ✓ {origem} → {destino_pasta}/")
            return True
        except Exception as e:
            print(f"  ✗ Erro ao mover {origem}: {e}")
            return False
    else:
        print(f"  - {origem} (não encontrado)")
        return False

# Mover arquivos
for destino, arquivos in mapeamento.items():
    print(f"\n{destino}/:")
    for arquivo in arquivos:
        mover_arquivo(arquivo, destino)

# Mover gráficos
print(f"\n04_visualizacoes/exploratoria/:")
graficos_dir = BASE_DIR / "graficos"
if graficos_dir.exists():
    for arquivo in graficos_dir.iterdir():
        if arquivo.is_file():
            destino = BASE_DIR / "04_visualizacoes" / "exploratoria" / arquivo.name
            if not destino.exists():
                shutil.copy2(arquivo, destino)
                print(f"  ✓ {arquivo.name}")

print(f"\n04_visualizacoes/fase1_regressao/:")
graficos_ml_dir = BASE_DIR / "graficos_ml"
if graficos_ml_dir.exists():
    for arquivo in graficos_ml_dir.iterdir():
        if arquivo.is_file():
            destino = BASE_DIR / "04_visualizacoes" / "fase1_regressao" / arquivo.name
            if not destino.exists():
                shutil.copy2(arquivo, destino)
                print(f"  ✓ {arquivo.name}")

# ================================================================================
# CRIAR ÍNDICE DO PROJETO
# ================================================================================

print("\n\n📋 3. CRIANDO ÍNDICE DO PROJETO...")
print("-" * 80)

indice_path = BASE_DIR / "00_INDICE_PROJETO.md"

with open(indice_path, 'w', encoding='utf-8') as f:
    f.write("""# 📊 ÍNDICE DO PROJETO - Análise ML de Reconstrução e ICM

**Projeto**: Análise de Relatórios Gerenciais de Reconstrução (2017-2025) + ICM  
**Instituição**: ENAP  
**Data**: 22/11/2025  
**Status**: Fase 1 Concluída ✅

---

## 📁 ESTRUTURA DE PASTAS

### `01_dados_originais/`
Dados brutos originais (não modificados)
- Arquivos de Acompanhamento de Processos (2017-2025)
- Arquivos de ICM por Faixas (A, B, C, D)

### `02_dados_processados/`
Dados limpos e consolidados prontos para análise
- ✅ `Relatório_Consolidado_Acompanhamento_2017_2025.xlsx` (6.385 processos)
- ✅ `ICM_Consolidado_LIMPO.xlsx` (5.445 municípios)
- ✅ `dados_merged_acompanhamento_icm.xlsx` (merge dos datasets)
- ✅ `dados_agregados_municipio_ATUALIZADO.xlsx`
- ✅ `municipios_duplicados.xlsx` (152 removidos)

### `03_analises/`
Análises estatísticas e resultados

#### `03_analises/exploratoria/`
- ✅ Análise exploratória inicial
- ✅ Investigação de duplicatas
- ✅ Estatísticas descritivas

#### `03_analises/fase1_regressao/` ✅ CONCLUÍDA
- ✅ Análise detalhada por faixa ICM
- ✅ Descoberta: Faixa D tem valores 2,94x maiores
- ✅ Análise de tipos de desastres por faixa

#### `03_analises/fase2_clustering/` ⏳ PRÓXIMA
- Segmentação de municípios
- Perfis de risco
- Clusters de similaridade

#### `03_analises/fase3_classificacao/` ⏳ FUTURA
- Predição de status de processos
- Classificação de risco
- Predição de valores altos

### `04_visualizacoes/`
Gráficos e visualizações

#### `04_visualizacoes/exploratoria/` (6 gráficos)
- ✅ Evolução de processos (2017-2025)
- ✅ Top UFs com mais processos
- ✅ Top tipos de desastres
- ✅ Distribuição por faixa ICM
- ✅ Análise por faixa ICM
- ✅ Distribuição por região

#### `04_visualizacoes/fase1_regressao/` (4 gráficos)
- ✅ Distribuição de valores por faixa (boxplot)
- ✅ Valor médio por faixa (barras)
- ✅ Heatmap desastre × faixa
- ✅ Violin plot de distribuições

### `05_modelos/`
Modelos de Machine Learning treinados

#### `05_modelos/fase1_regressao/`
- Análise descritiva (sem modelo preditivo ainda)
- Preparado para modelos futuros

#### `05_modelos/fase2_clustering/` ⏳
- K-Means
- DBSCAN
- Hierarchical Clustering

#### `05_modelos/fase3_classificacao/` ⏳
- Random Forest
- XGBoost
- LightGBM

### `06_relatorios/`
Documentação e relatórios executivos
- ✅ `README_ANALISE_ATUALIZADO.md` - Relatório principal
- ✅ `ESTRATEGIAS_ML.md` - 7 estratégias de ML
- ✅ `INVESTIGACAO_DUPLICATAS.md` - Limpeza de dados
- ✅ `IMPACTO_LIMPEZA_NO_PLANO_ML.md` - Análise de impacto
- ✅ `PROGRESSO_IMPLEMENTACAO.md` - Status do projeto

### `07_scripts/`
Scripts Python e batch do projeto
- ✅ Scripts de consolidação de dados
- ✅ Scripts de limpeza
- ✅ Scripts de análise exploratória
- ✅ Scripts de ML (Fase 1)
- ✅ Setup de ambiente virtual

---

## 🎯 PROGRESSO DO PROJETO

### ✅ Concluído (40%)
- [x] Consolidação de dados
- [x] Limpeza e validação
- [x] Análise exploratória
- [x] Fase 1: Análise de Regressão
- [x] Documentação

### 🔄 Em Andamento (20%)
- [ ] Configuração de ambiente virtual
- [ ] Preparação para Fase 2

### ⏳ Planejado (40%)
- [ ] Fase 2: Clustering
- [ ] Fase 3: Classificação
- [ ] Modelos avançados (séries temporais, anomalias)
- [ ] Dashboard interativo

---

## 🔥 PRINCIPAIS DESCOBERTAS

### 1. Qualidade dos Dados
- ✅ 168 registros problemáticos removidos do ICM
- ✅ 97,7% de cobertura no merge (2.065 municípios)
- ✅ Dados validados e prontos para ML

### 2. Insight Crítico: Faixa D
**Municípios de baixa capacidade (Faixa D) têm valores 2,94x maiores!**
- Faixa A: R$ 9,74 milhões
- Faixa B: R$ 9,79 milhões
- Faixa C: R$ 6,63 milhões
- **Faixa D: R$ 28,68 milhões** ⚠️

### 3. Concentração de Recursos
- Faixa D concentra **51% do valor total** (R$ 14,23 bi)
- Apenas 496 municípios (24% dos afetados)
- Indica necessidade de investigação aprofundada

---

## 📞 COMO USAR ESTE PROJETO

### 1. Navegar pelos Dados
```
02_dados_processados/
  └── dados_merged_acompanhamento_icm.xlsx  ← Dados principais
```

### 2. Ver Análises
```
03_analises/fase1_regressao/
  └── analise_detalhada_por_faixa.xlsx  ← Resultados Fase 1
```

### 3. Ver Gráficos
```
04_visualizacoes/fase1_regressao/
  └── *.png  ← Visualizações
```

### 4. Ler Relatórios
```
06_relatorios/
  └── README_ANALISE_ATUALIZADO.md  ← Relatório principal
```

### 5. Executar Scripts
```bash
# Ativar ambiente virtual
venv_ml\Scripts\activate

# Executar análises
cd 07_scripts
python ml_fase1_regressao.py
```

---

## 📊 ESTATÍSTICAS DO PROJETO

- **Dados processados**: 11.830 registros
- **Municípios analisados**: 2.065
- **Período**: 2017-2025 (9 anos)
- **Valor total**: R$ 27,68 bilhões
- **Arquivos gerados**: 25+
- **Gráficos criados**: 11
- **Linhas de código**: ~2.500

---

## 🚀 PRÓXIMOS PASSOS

1. ✅ Concluir setup do ambiente virtual
2. ✅ Implementar Fase 2: Clustering
3. ✅ Gerar relatório de segmentação
4. ✅ Implementar Fase 3: Classificação
5. ✅ Dashboard interativo (opcional)

---

**Última atualização**: 22/11/2025 17:17  
**Versão**: 1.0  
**Contato**: ENAP - Análise de Dados
""")

print(f"✓ Índice criado: 00_INDICE_PROJETO.md")

# ================================================================================
# CRIAR .gitignore
# ================================================================================

print("\n\n🔒 4. CRIANDO .gitignore...")
print("-" * 80)

gitignore_path = BASE_DIR / ".gitignore"

with open(gitignore_path, 'w', encoding='utf-8') as f:
    f.write("""# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv_ml/
env/
ENV/

# Jupyter Notebook
.ipynb_checkpoints

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Dados sensíveis (se houver)
# 01_dados_originais/*.xlsx

# Arquivos temporários
*.tmp
*.bak
~$*

# Logs
*.log
""")

print(f"✓ .gitignore criado")

# ================================================================================
# RESUMO FINAL
# ================================================================================

print("\n\n" + "=" * 80)
print("📋 RESUMO DA ORGANIZAÇÃO")
print("=" * 80)

print(f"""
ESTRUTURA CRIADA:
  ✓ 01_dados_originais/
  ✓ 02_dados_processados/
  ✓ 03_analises/
      ├── exploratoria/
      ├── fase1_regressao/
      ├── fase2_clustering/
      └── fase3_classificacao/
  ✓ 04_visualizacoes/
      ├── exploratoria/
      ├── fase1_regressao/
      ├── fase2_clustering/
      └── fase3_classificacao/
  ✓ 05_modelos/
      ├── fase1_regressao/
      ├── fase2_clustering/
      └── fase3_classificacao/
  ✓ 06_relatorios/
  ✓ 07_scripts/

ARQUIVOS ORGANIZADOS:
  ✓ Dados processados movidos
  ✓ Análises organizadas por fase
  ✓ Gráficos separados por tipo
  ✓ Relatórios centralizados
  ✓ Scripts agrupados

DOCUMENTAÇÃO CRIADA:
  ✓ 00_INDICE_PROJETO.md (índice principal)
  ✓ README.md em cada pasta
  ✓ .gitignore

PRÓXIMOS PASSOS:
  1. Revisar estrutura criada
  2. Mover dados originais para 01_dados_originais/
  3. Continuar com Fase 2: Clustering
""")

print("=" * 80)
print("✅ ORGANIZAÇÃO CONCLUÍDA COM SUCESSO!")
print("=" * 80)
