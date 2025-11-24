# 📁 ÍNDICE DO PROJETO: Análise de Reconstrução e ICM

**Última Atualização**: 22/11/2025
**Status**: Fase 1 Concluída (Regressão/Outliers) | Dados Corrigidos ✅

---

## 📚 DOCUMENTAÇÃO PRINCIPAL

1. **[RESUMO_FINAL.md](RESUMO_FINAL.md)** - Resumo executivo do projeto e entregas.
2. **[CORRECAO_DADOS_ICM.md](CORRECAO_DADOS_ICM.md)** - 🚨 Detalhes sobre a correção crítica de duplicatas (Critério de Risco).
3. **[06_relatorios/README_ANALISE_ATUALIZADO.md](06_relatorios/README_ANALISE_ATUALIZADO.md)** - Relatório detalhado da análise exploratória.
4. **[06_relatorios/ESTRATEGIAS_ML.md](06_relatorios/ESTRATEGIAS_ML.md)** - Plano estratégico de Machine Learning.
5. **[06_relatorios/PROGRESSO_IMPLEMENTACAO.md](06_relatorios/PROGRESSO_IMPLEMENTACAO.md)** - Log de progresso do projeto.

---

## 📂 ESTRUTURA DE PASTAS E ARQUIVOS

### 1. Dados (`01_dados_originais` e `02_dados_processados`)
- **`ICM_Consolidado_LIMPO.xlsx`**: Base ICM oficial (limpa com critério de risco).
- **`dados_merged_acompanhamento_icm.xlsx`**: Base unificada (Processos + ICM).
- **`dados_agregados_municipio_ATUALIZADO.xlsx`**: Estatísticas por município.

### 2. Análises (`03_analises`)
- **`exploratoria/`**:
  - `IMPACTO_LIMPEZA_DADOS.md`: Validação da limpeza inicial.
  - `INVESTIGACAO_DUPLICATAS_DETALHADA.md`: Diagnóstico das duplicatas conflitantes.
- **`outliers_extremos/`**:
  - `RELATORIO_OUTLIERS_APROVADOS.md`: Análise de risco em processos aprovados.
  - `analise_outliers_APROVADOS.xlsx`: Planilha detalhada de outliers.

### 3. Visualizações (`04_visualizacoes`)
- **`exploratoria/`**: Gráficos gerais (distribuição, faixas, etc.).
- **`outliers/`**: Gráficos de risco (Top 20, status, valores médios).

### 4. Scripts (`07_scripts`)

#### Processamento e Limpeza:
- `juntar_relatorios.py`: Consolida relatórios de processos.
- `juntar_faixas.py`: Consolida arquivos ICM.
- `limpar_arquivo_icm_v2.py`: **Script Oficial de Limpeza ICM** (Critério de Risco).

#### Análise e ML:
- `analise_exploratoria_ATUALIZADA.py`: Gera estatísticas e gráficos gerais.
- `analise_outliers_aprovados.py`: Identifica e relata outliers de risco.
- `ml_fase1_regressao.py`: Análise descritiva focada em regressão (Fase 1).

#### Utilitários:
- `atualizar_graficos_outliers.py`: Regenera gráficos de outliers.
- `organizar_projeto.py`: Organiza estrutura de pastas.
- `setup_venv.bat`: Configura ambiente virtual.

---

## 🚀 COMO EXECUTAR

1. **Ativar ambiente virtual**:
   ```bash
   venv_ml\Scripts\activate
   ```

2. **Atualizar dados e análises** (se necessário):
   ```bash
   python 07_scripts/limpar_arquivo_icm_v2.py
   python 07_scripts/analise_exploratoria_ATUALIZADA.py
   python 07_scripts/analise_outliers_aprovados.py
   python 07_scripts/atualizar_graficos_outliers.py
   ```

---

## ⚠️ NOTAS IMPORTANTES

- **Critério de Risco**: Em caso de conflito de dados no ICM, o sistema assume a **PIOR FAIXA** (maior vulnerabilidade).
- **Foco em Aprovados**: A análise de outliers prioriza processos com recursos transferidos ou aprovados.
