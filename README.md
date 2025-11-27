# 🏗️ Inteligência Artificial na Reconstrução de Infraestrutura

> **Uma abordagem data-driven para otimizar a alocação de recursos, identificar riscos e prever resultados em processos de reconstrução nacional.**

Este projeto utiliza técnicas avançadas de Ciência de Dados e Machine Learning para analisar solicitações de recursos federais para reconstrução de municípios atingidos por desastres. O objetivo é aumentar a eficiência, transparência e precisão na gestão pública.

---

## 🚀 Visão Geral do Projeto

O projeto está estruturado em 5 fases estratégicas, cobrindo desde o diagnóstico inicial até a criação de ferramentas interativas de simulação.

### 📊 [Fase 1: Diagnóstico & Regressão](docs/fase1.html)
**Objetivo:** Entender o cenário atual e testar hipóteses sobre a capacidade municipal.
*   **Insight:** Municípios com menor capacidade institucional (Faixa D) demandam **3x mais recursos** que os de alta capacidade, contrariando o senso comum.
*   **Técnica:** Análise Exploratória de Dados (EDA) e Estatística Descritiva.

### 🧩 [Fase 2: Clusterização Comportamental](docs/fase2.html)
**Objetivo:** Agrupar municípios por comportamento real, não apenas por rótulos burocráticos.
*   **Insight:** Identificação de 4 perfis reais de risco. A "Faixa A" (ricos) não é um escudo contra desastres caros.
*   **Técnica:** K-Means Clustering.

### ⚖️ [Fase 3: Classificação de Risco](docs/fase3.html)
**Objetivo:** Antecipar a aprovação ou reprovação de novos pedidos.
*   **Resultado:** Modelo preditivo com **80% de precisão (ROC-AUC)**.
*   **Técnica:** Random Forest Classifier.

### 🔍 [Fase 4: Detecção de Anomalias (Fair Value)](docs/fase4.html)
**Objetivo:** Estimar o "Preço Justo" de uma reconstrução e identificar superfaturamentos ou subdimensionamentos.
*   **Resultado:** Identificação de 580 processos com indícios de anomalia (valores extremos).
*   **Técnica:** Regressão Quantílica (Quantile Regression).

### 🌪️ [Fase 5: Simulador de Alertas](docs/fase5.html)
**Objetivo:** Ferramenta interativa para simulação de cenários e visualização de alertas em tempo real.
*   **Ferramenta:** Aplicação Web interativa (Streamlit).

---

## 📂 Estrutura do Repositório

*   `01_dados_originais/`: Dados brutos recebidos (não versionados por sigilo/tamanho).
*   `02_dados_processados/`: Dados limpos e tratados prontos para análise.
*   `03_analises/`: Notebooks, relatórios e documentação técnica de cada fase.
*   `04_visualizacoes/`: Gráficos e imagens gerados pelos modelos.
*   `05_modelos/`: Arquivos binários dos modelos treinados (.pkl, .joblib).
*   `06_relatorios/`: Relatórios gerenciais e logs de progresso.
*   `07_scripts/`: Código fonte Python para limpeza, análise e modelagem.
*   `docs/`: Código fonte do website de apresentação do projeto.

---

## 💻 Como Executar

### Pré-requisitos
*   Python 3.8+
*   Virtualenv

### Instalação

1.  Clone o repositório:
    ```bash
    git clone https://github.com/tadeugomes/enap-encontro-infra.git
    cd enap-encontro-infra
    ```

2.  Crie e ative o ambiente virtual:
    ```bash
    # Windows
    python -m venv venv_ml
    venv_ml\Scripts\activate
    ```

3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

### Executando as Análises
Os scripts principais estão na pasta `07_scripts`. Exemplo para rodar a análise exploratória:

```bash
python 07_scripts/analise_exploratoria_ATUALIZADA.py
```

---

## 🌐 Website do Projeto

O projeto conta com uma documentação interativa completa disponível na pasta `docs/`. Para visualizar, basta abrir o arquivo `docs/index.html` em seu navegador ou acessar a versão online (se disponível).

---

**Desenvolvido para o Encontro de Infraestrutura da ENAP - 2025**
