# ESTRATÉGIAS DE MACHINE LEARNING PARA ANÁLISE DOS DADOS
# Relatório Gerencial de Reconstrução (2017-2025) + ICM por Faixas

"""
Este documento apresenta estratégias de Machine Learning para analisar as relações
entre os dados de Acompanhamento de Processos de Reconstrução e o Índice de 
Capacidade Municipal (ICM).
"""

## ================================================================================
## 1. ANÁLISE EXPLORATÓRIA E PRÉ-PROCESSAMENTO
## ================================================================================

"""
DADOS DISPONÍVEIS:

A) Relatório de Acompanhamento (6.385 registros, 2017-2025):
   - UF, Município (2.076 únicos)
   - Desastres (29 tipos)
   - Processo, Protocolo
   - Datas (Criação, Solicitação)
   - Valor Solicitado
   - Status (42 diferentes)
   - Analista
   - Ano_Relatorio (2017-2025)

B) ICM por Faixas (5.613 registros):
   - Faixas: A (Alta), B, C, D (Baixa capacidade)
   - Múltiplas métricas numéricas (19 colunas)
   - Dados por município

DESAFIO: As colunas não têm nomes claros no arquivo ICM (Unnamed: 0-31)
SOLUÇÃO: Precisamos primeiro identificar os cabeçalhos corretos
"""

## ================================================================================
## 2. ESTRATÉGIAS DE MACHINE LEARNING RECOMENDADAS
## ================================================================================

"""
═══════════════════════════════════════════════════════════════════════════════
ESTRATÉGIA 1: ANÁLISE DE CLUSTERING (Não Supervisionado)
═══════════════════════════════════════════════════════════════════════════════

OBJETIVO: Identificar padrões e agrupamentos naturais nos municípios

ALGORITMOS SUGERIDOS:
├─ K-Means Clustering
├─ DBSCAN (para identificar outliers)
├─ Hierarchical Clustering
└─ Gaussian Mixture Models

FEATURES A UTILIZAR:
├─ Número de desastres por município
├─ Valor total solicitado por município
├─ Tempo médio de processamento
├─ Taxa de aprovação de processos
├─ Faixa ICM do município
├─ Métricas do ICM (capacidade institucional)
└─ Distribuição temporal dos desastres

INSIGHTS ESPERADOS:
✓ Municípios com perfis similares de desastres e capacidade de resposta
✓ Identificação de municípios vulneráveis (baixo ICM + alto número de desastres)
✓ Padrões regionais (por UF)

CÓDIGO EXEMPLO:
```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Agregar dados por município
features = ['num_desastres', 'valor_total', 'tempo_medio_processo', 
            'taxa_aprovacao', 'icm_score']
X = df_municipios[features]

# Normalizar
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Clustering
kmeans = KMeans(n_clusters=5, random_state=42)
clusters = kmeans.fit_predict(X_scaled)
```
"""

"""
═══════════════════════════════════════════════════════════════════════════════
ESTRATÉGIA 2: ANÁLISE PREDITIVA - CLASSIFICAÇÃO
═══════════════════════════════════════════════════════════════════════════════

OBJETIVO: Prever outcomes de processos com base em características do município

PROBLEMAS DE CLASSIFICAÇÃO:

A) PREVER STATUS DO PROCESSO
   Target: Status do processo (aprovado, em análise, rejeitado, etc.)
   Features: ICM, tipo de desastre, UF, valor solicitado, ano
   
   Algoritmos:
   ├─ Random Forest Classifier
   ├─ XGBoost
   ├─ LightGBM
   └─ Logistic Regression (baseline)

B) PREVER FAIXA ICM A PARTIR DE HISTÓRICO DE DESASTRES
   Target: Faixa ICM (A, B, C, D)
   Features: Histórico de desastres, valores solicitados, tempo de resposta
   
   Algoritmos:
   ├─ Random Forest
   ├─ Gradient Boosting
   └─ Neural Networks (se houver dados suficientes)

C) IDENTIFICAR MUNICÍPIOS EM RISCO
   Target: Binário (alto risco / baixo risco)
   Critério: Baixo ICM + Alta frequência de desastres
   
   Algoritmos:
   ├─ Random Forest
   ├─ SVM
   └─ Ensemble Methods

CÓDIGO EXEMPLO:
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Preparar dados
X = df[['icm_score', 'num_desastres_historico', 'valor_medio', 
        'populacao', 'pib_per_capita']]
y = df['status_aprovado']  # binário

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Treinar
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Avaliar
y_pred = rf.predict(X_test)
print(classification_report(y_test, y_pred))

# Feature importance
importances = pd.DataFrame({
    'feature': X.columns,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)
```
"""

"""
═══════════════════════════════════════════════════════════════════════════════
ESTRATÉGIA 3: ANÁLISE PREDITIVA - REGRESSÃO
═══════════════════════════════════════════════════════════════════════════════

OBJETIVO: Prever valores contínuos

PROBLEMAS DE REGRESSÃO:

A) PREVER VALOR NECESSÁRIO PARA RECONSTRUÇÃO
   Target: Valor solicitado
   Features: Tipo de desastre, população, ICM, histórico
   
   Algoritmos:
   ├─ Random Forest Regressor
   ├─ XGBoost Regressor
   ├─ LightGBM
   └─ Linear Regression (baseline)

B) PREVER TEMPO DE PROCESSAMENTO
   Target: Dias entre criação e aprovação
   Features: Valor, tipo de desastre, ICM, UF, ano
   
C) PREVER SCORE ICM
   Target: Score ICM contínuo
   Features: Histórico de desastres, capacidade de resposta

CÓDIGO EXEMPLO:
```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import xgboost as xgb

# Preparar dados
X = df[['icm_score', 'tipo_desastre_encoded', 'populacao', 
        'area_afetada', 'ano']]
y = df['valor_solicitado']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# XGBoost
model = xgb.XGBRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42
)
model.fit(X_train, y_train)

# Avaliar
y_pred = model.predict(X_test)
print(f'MAE: {mean_absolute_error(y_test, y_pred):,.2f}')
print(f'R²: {r2_score(y_test, y_pred):.3f}')
```
"""

"""
═══════════════════════════════════════════════════════════════════════════════
ESTRATÉGIA 4: ANÁLISE DE SÉRIES TEMPORAIS
═══════════════════════════════════════════════════════════════════════════════

OBJETIVO: Analisar tendências temporais e fazer previsões futuras

ANÁLISES POSSÍVEIS:

A) TENDÊNCIA DE DESASTRES POR REGIÃO
   - Identificar sazonalidade
   - Prever picos de demanda
   
   Algoritmos:
   ├─ ARIMA / SARIMA
   ├─ Prophet (Facebook)
   ├─ LSTM (Deep Learning)
   └─ Exponential Smoothing

B) EVOLUÇÃO DO ICM AO LONGO DO TEMPO
   - Municípios melhorando/piorando capacidade
   
C) PADRÕES DE APROVAÇÃO POR ANO
   - Mudanças em políticas públicas

CÓDIGO EXEMPLO:
```python
from prophet import Prophet
import pandas as pd

# Preparar dados temporais
df_temporal = df.groupby('data_criacao').agg({
    'protocolo': 'count',
    'valor_solicitado': 'sum'
}).reset_index()
df_temporal.columns = ['ds', 'y', 'valor_total']

# Prophet
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=False,
    daily_seasonality=False
)
model.fit(df_temporal[['ds', 'y']])

# Previsão para próximos 12 meses
future = model.make_future_dataframe(periods=365)
forecast = model.predict(future)
model.plot(forecast)
```
"""

"""
═══════════════════════════════════════════════════════════════════════════════
ESTRATÉGIA 5: ANÁLISE DE ASSOCIAÇÃO E CORRELAÇÃO
═══════════════════════════════════════════════════════════════════════════════

OBJETIVO: Descobrir relações entre variáveis

ANÁLISES:

A) CORRELAÇÃO ICM vs EFICIÊNCIA DE PROCESSOS
   - Municípios com maior ICM processam mais rápido?
   - Maior ICM = maior taxa de aprovação?

B) TIPOS DE DESASTRES vs FAIXA ICM
   - Certos desastres afetam mais municípios de baixo ICM?

C) ANÁLISE DE REGRAS DE ASSOCIAÇÃO
   - Market Basket Analysis adaptado
   - Padrões: "Se município tem baixo ICM E sofre enchentes 
              ENTÃO tempo de processo > 180 dias"

CÓDIGO EXEMPLO:
```python
import seaborn as sns
import matplotlib.pyplot as plt

# Matriz de correlação
correlation_matrix = df_features.corr()

plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Correlação entre Features')
plt.tight_layout()
plt.savefig('correlation_matrix.png')

# Análise específica
from scipy.stats import pearsonr, spearmanr

# ICM vs Tempo de Processo
corr, p_value = pearsonr(df['icm_score'], df['tempo_processo_dias'])
print(f'Correlação ICM vs Tempo: {corr:.3f} (p={p_value:.4f})')
```
"""

"""
═══════════════════════════════════════════════════════════════════════════════
ESTRATÉGIA 6: ANÁLISE DE ANOMALIAS
═══════════════════════════════════════════════════════════════════════════════

OBJETIVO: Identificar casos atípicos que requerem atenção especial

APLICAÇÕES:

A) DETECÇÃO DE FRAUDES OU IRREGULARIDADES
   - Valores solicitados muito acima da média para tipo de desastre
   - Processos aprovados muito rapidamente
   - Municípios com padrões suspeitos

B) IDENTIFICAÇÃO DE EMERGÊNCIAS
   - Municípios com súbito aumento de desastres
   - Valores excepcionalmente altos

Algoritmos:
├─ Isolation Forest
├─ One-Class SVM
├─ Local Outlier Factor (LOF)
└─ Autoencoders (Deep Learning)

CÓDIGO EXEMPLO:
```python
from sklearn.ensemble import IsolationForest

# Features para detecção de anomalias
X = df[['valor_solicitado', 'tempo_processo', 'num_processos_simultaneos']]

# Normalizar
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Isolation Forest
iso_forest = IsolationForest(
    contamination=0.05,  # 5% de anomalias esperadas
    random_state=42
)
anomalies = iso_forest.fit_predict(X_scaled)

# Identificar anomalias
df['is_anomaly'] = anomalies == -1
anomalous_cases = df[df['is_anomaly']]
print(f'Casos anômalos detectados: {len(anomalous_cases)}')
```
"""

"""
═══════════════════════════════════════════════════════════════════════════════
ESTRATÉGIA 7: ANÁLISE DE REDE E GRAFOS
═══════════════════════════════════════════════════════════════════════════════

OBJETIVO: Modelar relações complexas entre entidades

APLICAÇÕES:

A) REDE DE MUNICÍPIOS
   - Conectar municípios similares (mesmo ICM, mesmos desastres)
   - Identificar comunidades regionais

B) REDE DE DESASTRES
   - Desastres que ocorrem juntos
   - Cascata de eventos

C) ANÁLISE DE INFLUÊNCIA
   - Municípios que podem servir de modelo
   - Disseminação de boas práticas

Bibliotecas:
├─ NetworkX
├─ Graph-tool
└─ PyTorch Geometric (Graph Neural Networks)

CÓDIGO EXEMPLO:
```python
import networkx as nx
import matplotlib.pyplot as plt

# Criar grafo de municípios similares
G = nx.Graph()

# Adicionar nós (municípios)
for idx, row in df_municipios.iterrows():
    G.add_node(row['municipio'], 
               icm=row['icm_score'],
               faixa=row['faixa'])

# Adicionar arestas (similaridade)
from sklearn.metrics.pairwise import cosine_similarity

similarity_matrix = cosine_similarity(features_matrix)
threshold = 0.8

for i in range(len(municipios)):
    for j in range(i+1, len(municipios)):
        if similarity_matrix[i, j] > threshold:
            G.add_edge(municipios[i], municipios[j], 
                      weight=similarity_matrix[i, j])

# Análise de comunidades
from networkx.algorithms import community
communities = community.greedy_modularity_communities(G)
print(f'Comunidades detectadas: {len(communities)}')
```
"""

## ================================================================================
## 3. PIPELINE RECOMENDADO DE IMPLEMENTAÇÃO
## ================================================================================

"""
FASE 1: PREPARAÇÃO DOS DADOS (1-2 semanas)
├─ 1.1 Limpar e padronizar nomes de colunas do ICM
├─ 1.2 Tratar valores faltantes
├─ 1.3 Converter tipos de dados (datas, valores monetários)
├─ 1.4 Criar chave de junção (UF + Município normalizado)
├─ 1.5 Fazer merge dos datasets
└─ 1.6 Feature Engineering inicial

FASE 2: ANÁLISE EXPLORATÓRIA (1 semana)
├─ 2.1 Estatísticas descritivas
├─ 2.2 Visualizações (distribuições, tendências)
├─ 2.3 Análise de correlações
├─ 2.4 Identificação de outliers
└─ 2.5 Análise temporal

FASE 3: FEATURE ENGINEERING (1-2 semanas)
├─ 3.1 Agregações por município (total, média, mediana)
├─ 3.2 Features temporais (tendências, sazonalidade)
├─ 3.3 Features de interação (ICM * num_desastres)
├─ 3.4 Encoding de variáveis categóricas
└─ 3.5 Normalização/Padronização

FASE 4: MODELAGEM (2-3 semanas)
├─ 4.1 Baseline models (simples)
├─ 4.2 Clustering (não supervisionado)
├─ 4.3 Modelos de classificação
├─ 4.4 Modelos de regressão
├─ 4.5 Séries temporais
└─ 4.6 Ensemble methods

FASE 5: VALIDAÇÃO E INTERPRETAÇÃO (1 semana)
├─ 5.1 Cross-validation
├─ 5.2 Feature importance
├─ 5.3 SHAP values (interpretabilidade)
├─ 5.4 Análise de erros
└─ 5.5 Validação com especialistas

FASE 6: DEPLOYMENT E MONITORAMENTO (contínuo)
├─ 6.1 Dashboard interativo (Streamlit/Dash)
├─ 6.2 API para predições
├─ 6.3 Relatórios automatizados
└─ 6.4 Monitoramento de performance
"""

## ================================================================================
## 4. MÉTRICAS DE AVALIAÇÃO
## ================================================================================

"""
CLASSIFICAÇÃO:
├─ Accuracy, Precision, Recall, F1-Score
├─ ROC-AUC, PR-AUC
├─ Confusion Matrix
└─ Classification Report

REGRESSÃO:
├─ MAE (Mean Absolute Error)
├─ RMSE (Root Mean Squared Error)
├─ R² (Coefficient of Determination)
├─ MAPE (Mean Absolute Percentage Error)
└─ Residual Analysis

CLUSTERING:
├─ Silhouette Score
├─ Davies-Bouldin Index
├─ Calinski-Harabasz Index
└─ Inertia (Within-cluster sum of squares)

SÉRIES TEMPORAIS:
├─ MASE (Mean Absolute Scaled Error)
├─ SMAPE (Symmetric MAPE)
└─ Forecast Accuracy
"""

## ================================================================================
## 5. FERRAMENTAS E BIBLIOTECAS RECOMENDADAS
## ================================================================================

"""
MANIPULAÇÃO DE DADOS:
├─ pandas
├─ numpy
└─ polars (para datasets grandes)

VISUALIZAÇÃO:
├─ matplotlib
├─ seaborn
├─ plotly (interativo)
└─ altair

MACHINE LEARNING:
├─ scikit-learn (fundamental)
├─ XGBoost
├─ LightGBM
├─ CatBoost
└─ imbalanced-learn (para dados desbalanceados)

DEEP LEARNING (se necessário):
├─ TensorFlow / Keras
├─ PyTorch
└─ FastAI

SÉRIES TEMPORAIS:
├─ statsmodels
├─ Prophet
└─ pmdarima

INTERPRETABILIDADE:
├─ SHAP
├─ LIME
└─ ELI5

DEPLOYMENT:
├─ Streamlit (dashboards)
├─ FastAPI (APIs)
├─ MLflow (tracking)
└─ Docker (containerização)
"""

## ================================================================================
## 6. PERGUNTAS DE NEGÓCIO QUE PODEM SER RESPONDIDAS
## ================================================================================

"""
1. Municípios com baixo ICM têm processos mais lentos?
2. Qual o valor médio de reconstrução por tipo de desastre e faixa ICM?
3. Quais UFs são mais eficientes no processamento de solicitações?
4. Existe sazonalidade nos tipos de desastres?
5. É possível prever quais municípios terão mais desastres em 2026?
6. Qual a relação entre ICM e taxa de aprovação de processos?
7. Quais fatores mais influenciam o tempo de processamento?
8. Existem padrões regionais de desastres?
9. Municípios estão melhorando sua capacidade (ICM) ao longo do tempo?
10. Quais municípios estão em maior risco e precisam de atenção prioritária?
"""

print("=" * 80)
print("DOCUMENTO DE ESTRATÉGIAS DE MACHINE LEARNING CRIADO COM SUCESSO!")
print("=" * 80)
print("\nPróximos passos:")
print("1. Limpar e padronizar os dados do ICM")
print("2. Fazer merge dos datasets por município")
print("3. Começar com análise exploratória")
print("4. Implementar modelos baseline")
print("5. Iterar e refinar")
