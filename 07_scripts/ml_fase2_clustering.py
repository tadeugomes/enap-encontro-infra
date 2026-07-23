"""
IMPLEMENTAÇÃO DO PLANO DE ML - FASE 2: CLUSTERIZAÇÃO (SEGMENTAÇÃO DE MUNICÍPIOS)
Objetivo: Agrupar municípios por comportamento real de solicitações, independente da Faixa ICM.

Autor: Análise de Dados - ENAP
Data: 23/11/2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from pathlib import Path
import joblib
import warnings

warnings.filterwarnings('ignore')

# Configuração de estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("viridis")

print("=" * 80)
print("FASE 2: CLUSTERIZAÇÃO - SEGMENTAÇÃO DE MUNICÍPIOS")
print("=" * 80)

# ================================================================================
# 1. CARREGAR DADOS
# ================================================================================
print("\n📂 1. CARREGANDO DADOS...")
BASE_DIR = Path(__file__).resolve().parent.parent
arquivo_merged = BASE_DIR / "dados" / "dados_processados" / "dados_merged_acompanhamento_icm.xlsx"

# Tentar carregar do local padrão ou do local organizado
if not arquivo_merged.exists():
    arquivo_merged = BASE_DIR / "02_dados_processados" / "dados_merged_acompanhamento_icm.xlsx"

df = pd.read_excel(arquivo_merged)
print(f"✓ Dados carregados: {len(df):,} municípios")

# Filtrar apenas municípios com dados numéricos válidos
df_cluster = df.dropna(subset=['Num_Processos', 'Valor_Total']).copy()
print(f"✓ Municípios iniciais: {len(df_cluster):,}")

# Garantir que não há valores negativos para o Log
df_cluster['Valor_Total'] = df_cluster['Valor_Total'].clip(lower=0)
df_cluster['Valor_Medio'] = df_cluster['Valor_Medio'].clip(lower=0)

# Preencher NaNs em Valor_Medio com 0 (caso exista)
df_cluster['Valor_Medio'] = df_cluster['Valor_Medio'].fillna(0)

print("\n⚙️ 2. PREPARANDO FEATURES...")

# Criar features derivadas
# Log do valor total (para lidar com a assimetria/outliers)
df_cluster['Log_Valor_Total'] = np.log1p(df_cluster['Valor_Total'])
df_cluster['Log_Valor_Medio'] = np.log1p(df_cluster['Valor_Medio'])

# Selecionar features para o modelo
features_cols = ['Num_Processos', 'Log_Valor_Total', 'Log_Valor_Medio']
X = df_cluster[features_cols]

# Verificar e limpar NaNs/Infs resultantes
X = X.replace([np.inf, -np.inf], np.nan)
X = X.fillna(0) # Preencher qualquer NaN restante com 0

# Sincronizar df_cluster com X limpo (caso tenhamos removido linhas, mas aqui preenchemos)
# Se tivéssemos removido linhas, precisaríamos fazer: df_cluster = df_cluster.loc[X.index]

print("Features selecionadas:")
for col in features_cols:
    print(f"  - {col} (Min: {X[col].min():.2f}, Max: {X[col].max():.2f})")

# Escalonamento (RobustScaler é melhor com outliers)
scaler = RobustScaler()
X_scaled = scaler.fit_transform(X)

# ================================================================================
# 3. DETERMINAR NÚMERO IDEAL DE CLUSTERS (ELBOW METHOD)
# ================================================================================
print("\n🔍 3. DEFININDO NÚMERO DE CLUSTERS...")

inertia = []
silhouette_scores = []
K_range = range(2, 8)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))

# Decisão automática: Melhor Silhouette Score
best_k = K_range[np.argmax(silhouette_scores)]
print(f"✓ Melhor K sugerido (Silhouette): {best_k}")

# Vamos forçar 4 clusters para comparar com as 4 faixas do ICM, 
# a menos que o score seja muito ruim.
n_clusters = 4
print(f"✓ Definido K = {n_clusters} para comparabilidade com Faixas ICM")

# ================================================================================
# 4. APLICAR K-MEANS
# ================================================================================
print(f"\n🤖 4. APLICANDO K-MEANS (K={n_clusters})...")

kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
df_cluster['Cluster'] = kmeans.fit_predict(X_scaled)

# Reordenar clusters para que 0 seja "Menor Impacto" e 3 seja "Maior Impacto"
# Baseado na média de Valor Total
cluster_means = df_cluster.groupby('Cluster')['Valor_Total'].mean().sort_values()
mapping = {old: new for new, old in enumerate(cluster_means.index)}
df_cluster['Cluster_Ordenado'] = df_cluster['Cluster'].map(mapping)

# Nomes descritivos para os clusters (baseado na análise posterior, mas definindo aqui)
# Será ajustado dinamicamente
print("✓ Clusterização concluída")

# ================================================================================
# 5. ANÁLISE DOS CLUSTERS
# ================================================================================
print("\n📊 5. ANALISANDO RESULTADOS...")

# Estatísticas por Cluster
stats_cluster = df_cluster.groupby('Cluster_Ordenado').agg({
    'Num_Processos': 'mean',
    'Valor_Total': 'mean',
    'Valor_Medio': 'mean',
    'Municipio': 'count'
}).round(2)

stats_cluster.columns = ['Média Processos', 'Média Valor Total', 'Média Valor Processo', 'Qtd Municípios']
print("\nPerfil dos Clusters:")
print(stats_cluster)

# Cruzamento: Cluster vs Faixa ICM
crosstab = pd.crosstab(df_cluster['Cluster_Ordenado'], df_cluster['Faixa_ICM'])
print("\nMatriz de Confusão (Cluster vs Faixa ICM):")
print(crosstab)

# ================================================================================
# 6. VISUALIZAÇÃO
# ================================================================================
print("\n🎨 6. GERANDO VISUALIZAÇÕES...")

dir_output = BASE_DIR / "04_visualizacoes" / "fase2_clustering"
dir_output.mkdir(parents=True, exist_ok=True)

# 6.1 Scatter Plot (PCA 2D)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
df_cluster['PCA1'] = X_pca[:, 0]
df_cluster['PCA2'] = X_pca[:, 1]

plt.figure(figsize=(10, 8))
sns.scatterplot(data=df_cluster, x='PCA1', y='PCA2', hue='Cluster_Ordenado', palette='viridis', s=60, alpha=0.7)
plt.title('Mapa de Clusters dos Municípios (PCA)', fontsize=14, fontweight='bold')
plt.xlabel('Componente Principal 1 (Intensidade Financeira)')
plt.ylabel('Componente Principal 2 (Frequência)')
plt.legend(title='Cluster')
plt.tight_layout()
plt.savefig(dir_output / 'mapa_clusters_pca.png', dpi=300)
print("✓ Gráfico salvo: mapa_clusters_pca.png")

# 6.2 Boxplot Valor Total por Cluster
plt.figure(figsize=(10, 6))
sns.boxplot(data=df_cluster, x='Cluster_Ordenado', y='Log_Valor_Total', palette='viridis')
plt.title('Distribuição de Valores por Cluster (Escala Log)', fontsize=14)
plt.ylabel('Log(Valor Total)')
plt.xlabel('Cluster')
plt.tight_layout()
plt.savefig(dir_output / 'boxplot_valor_cluster.png', dpi=300)
print("✓ Gráfico salvo: boxplot_valor_cluster.png")

# 6.3 Heatmap Cluster vs Faixa ICM
plt.figure(figsize=(10, 6))
sns.heatmap(crosstab, annot=True, fmt='d', cmap='Blues')
plt.title('Cluster Comportamental vs Faixa ICM Oficial', fontsize=14)
plt.ylabel('Cluster (Comportamento Real)')
plt.xlabel('Faixa ICM (Capacidade Teórica)')
plt.tight_layout()
plt.savefig(dir_output / 'heatmap_cluster_vs_icm.png', dpi=300)
print("✓ Gráfico salvo: heatmap_cluster_vs_icm.png")

# ================================================================================
# 7. SALVAR RESULTADOS
# ================================================================================
print("\n💾 7. SALVANDO RESULTADOS...")

dir_analises = BASE_DIR / "03_analises" / "fase2_clustering"
dir_analises.mkdir(parents=True, exist_ok=True)

# Salvar dataset com clusters
arquivo_final = BASE_DIR / "02_dados_processados" / "dados_municipios_clusterizados.xlsx"
df_cluster.to_excel(arquivo_final, index=False)
print(f"✓ Dados clusterizados salvos em: {arquivo_final.name}")

# Salvar relatório de estatísticas
arquivo_stats = dir_analises / "perfil_clusters.xlsx"
with pd.ExcelWriter(arquivo_stats) as writer:
    stats_cluster.to_excel(writer, sheet_name='Perfil_Clusters')
    crosstab.to_excel(writer, sheet_name='Cluster_vs_ICM')

print(f"✓ Relatório salvo em: {arquivo_stats.name}")

# Salvar modelo treinado (scaler + KMeans + features usadas)
dir_modelos = BASE_DIR / "05_modelos" / "fase2_clustering"
dir_modelos.mkdir(parents=True, exist_ok=True)
joblib.dump({'scaler': scaler, 'kmeans': kmeans, 'features': features_cols},
            dir_modelos / "kmeans_clustering.pkl")
print(f"✓ Modelo salvo em: 05_modelos/fase2_clustering/kmeans_clustering.pkl")

print("\n" + "=" * 80)
print("✅ FASE 2 (CLUSTERIZAÇÃO) CONCLUÍDA!")
print("=" * 80)
