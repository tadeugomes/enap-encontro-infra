"""
IMPLEMENTAÇÃO DO PLANO DE ML - FASE 4: REGRESSÃO PREDITIVA (ESTIMATIVA DE VALOR JUSTO)
Objetivo: Criar um modelo para estimar o "Valor Esperado" (Fair Value) de um processo de reconstrução
          e identificar solicitações com valores anômalos (muito acima ou abaixo do esperado).

Autor: Análise de Dados - ENAP
Data: 23/11/2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# Configuração de estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("viridis")

print("=" * 80)
print("FASE 4: REGRESSÃO PREDITIVA - ESTIMATIVA DE VALOR JUSTO")
print("=" * 80)

# ================================================================================
# 1. CARREGAR DADOS
# ================================================================================
print("\n📂 1. CARREGANDO E INTEGRANDO DADOS...")
BASE_DIR = Path(r"c:\Users\tadeu\Downloads\enap_infra_encontro")

# Arquivo de transações (Processos)
arquivo_processos = BASE_DIR / "dados" / "dados_gerenciamento" / "Relatório_Consolidado_Acompanhamento_2017_2025.xlsx"
df_processos = pd.read_excel(arquivo_processos)

# Arquivo de Municípios (Clusters + ICM)
arquivo_municipios = BASE_DIR / "02_dados_processados" / "dados_municipios_clusterizados.xlsx"
df_municipios = pd.read_excel(arquivo_municipios)

# Padronizar chaves para merge
df_processos['Municipio_Padrao'] = df_processos['Município'].str.upper().str.strip()
df_municipios['Municipio_Padrao'] = df_municipios['Municipio'].str.upper().str.strip()

# Merge
df_full = pd.merge(
    df_processos,
    df_municipios[['UF', 'Municipio_Padrao', 'Faixa_ICM', 'Cluster_Ordenado', 'Faixa_Populacional']],
    on=['UF', 'Municipio_Padrao'],
    how='inner'
)

# Limpar Valor Solicitado
def limpar_valor(val):
    if pd.isna(val): return 0.0
    s = str(val).replace('R$', '').replace('.', '').replace(',', '.').strip()
    try:
        return float(s)
    except:
        return 0.0

df_full['Valor_Numerico'] = df_full['Valor Solicitado'].apply(limpar_valor)

# Filtrar apenas valores positivos e remover outliers extremos (ex: Porto Alegre) para treino
# Vamos considerar apenas processos com status "RECURSO TRANSFERIDO" para treinar o modelo de "Valor Justo"
# Pois assumimos que esses valores foram validados tecnicamente.
df_treino = df_full[
    (df_full['Status'] == 'ACOMPANHAMENTO - RECURSO TRANSFERIDO') & 
    (df_full['Valor_Numerico'] > 1000) & # Remover valores irrisórios
    (df_full['Municipio_Padrao'] != 'PORTO ALEGRE') # Remover outlier extremo conhecido
].copy()

print(f"✓ Base de Treino (Aprovados): {len(df_treino):,} registros")

# ================================================================================
# 2. FEATURE ENGINEERING
# ================================================================================
print("\n🔧 2. ENGENHARIA DE FEATURES...")

# Target: Log do Valor (para normalizar a distribuição)
df_treino['Log_Valor'] = np.log1p(df_treino['Valor_Numerico'])

# Features
features_cat = ['UF', 'Desastres', 'Faixa_ICM', 'Cluster_Ordenado', 'Faixa_Populacional']
X_cols = []

# Encoding
encoders = {}
for col in features_cat:
    le = LabelEncoder()
    df_treino[col] = df_treino[col].astype(str)
    df_treino[f'{col}_Code'] = le.fit_transform(df_treino[col])
    encoders[col] = le
    X_cols.append(f'{col}_Code')

X = df_treino[X_cols]
y = df_treino['Log_Valor']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ================================================================================
# 3. TREINAMENTO (QUANTILE REGRESSION)
# ================================================================================
print("\n🤖 3. TREINANDO MODELOS DE REGRESSÃO QUANTÍLICA...")
print("   (Estimando Faixas de Valor Aceitável: P10, P50, P90)")

# Modelo Mediano (Tendência Central)
gbr_50 = GradientBoostingRegressor(loss='quantile', alpha=0.5, n_estimators=100, random_state=42)
gbr_50.fit(X_train, y_train)

# Modelo Limite Inferior (P10 - Muito Barato)
gbr_10 = GradientBoostingRegressor(loss='quantile', alpha=0.1, n_estimators=100, random_state=42)
gbr_10.fit(X_train, y_train)

# Modelo Limite Superior (P90 - Muito Caro/Suspeito)
gbr_90 = GradientBoostingRegressor(loss='quantile', alpha=0.9, n_estimators=100, random_state=42)
gbr_90.fit(X_train, y_train)

print("✓ Modelos treinados com sucesso.")

# ================================================================================
# 4. AVALIAÇÃO E PREDIÇÃO
# ================================================================================
print("\n📊 4. AVALIANDO RESULTADOS...")

# Predizer no conjunto de teste
pred_50 = gbr_50.predict(X_test)
pred_10 = gbr_10.predict(X_test)
pred_90 = gbr_90.predict(X_test)

# Converter de volta de Log para Reais
y_test_real = np.expm1(y_test)
pred_50_real = np.expm1(pred_50)
pred_10_real = np.expm1(pred_10)
pred_90_real = np.expm1(pred_90)

# Métricas (apenas para a mediana)
mae = mean_absolute_error(y_test_real, pred_50_real)
r2 = r2_score(y_test, pred_50) # R2 no log space é mais estável

print(f"Erro Médio Absoluto (MAE): R$ {mae:,.2f}")
print(f"R² (Log Space): {r2:.4f}")

# Calcular Cobertura (Quantos dados reais caíram dentro do intervalo P10-P90?)
dentro_intervalo = ((y_test_real >= pred_10_real) & (y_test_real <= pred_90_real)).mean()
print(f"Cobertura do Intervalo de Confiança (P10-P90): {dentro_intervalo:.1%}")

# ================================================================================
# 5. APLICAÇÃO: IDENTIFICAR ANOMALIAS EM TODA A BASE
# ================================================================================
print("\n🔍 5. APLICANDO MODELO EM TODA A BASE (AUDITORIA)...")

# Preparar toda a base (incluindo reprovados) para predição
df_audit = df_full[df_full['Valor_Numerico'] > 1000].copy()

for col in features_cat:
    le = encoders[col]
    # Tratar novos valores não vistos no treino (se houver)
    df_audit[col] = df_audit[col].astype(str)
    # Usar map com fillna para evitar erro de label desconhecido
    mapping = dict(zip(le.classes_, le.transform(le.classes_)))
    df_audit[f'{col}_Code'] = df_audit[col].map(mapping).fillna(-1).astype(int)

# Filtrar apenas onde conseguimos codificar tudo (remove categorias novas raras)
df_audit = df_audit[df_audit[X_cols].min(axis=1) >= 0].copy()

X_audit = df_audit[X_cols]

# Predizer faixas
df_audit['Valor_Esperado_P50'] = np.expm1(gbr_50.predict(X_audit))
df_audit['Limite_Superior_P90'] = np.expm1(gbr_90.predict(X_audit))
df_audit['Limite_Inferior_P10'] = np.expm1(gbr_10.predict(X_audit))

# Identificar Anomalias
# Valor > Limite Superior (Superfaturamento Potencial)
df_audit['Alerta_Preco'] = np.where(df_audit['Valor_Numerico'] > df_audit['Limite_Superior_P90'], 'ALTO', 
                           np.where(df_audit['Valor_Numerico'] < df_audit['Limite_Inferior_P10'], 'BAIXO', 'NORMAL'))

# Calcular Desvio
df_audit['Desvio_Percentual'] = ((df_audit['Valor_Numerico'] - df_audit['Valor_Esperado_P50']) / df_audit['Valor_Esperado_P50']) * 100

resumo_auditoria = df_audit['Alerta_Preco'].value_counts()
print("\nResultado da Auditoria Automática:")
print(resumo_auditoria)

top_anomalias = df_audit[df_audit['Alerta_Preco'] == 'ALTO'].nlargest(10, 'Desvio_Percentual')
print("\nTop 5 Processos com Valor Muito Acima do Esperado:")
print(top_anomalias[['Município', 'UF', 'Desastres', 'Valor_Numerico', 'Valor_Esperado_P50', 'Desvio_Percentual']])

# ================================================================================
# 6. VISUALIZAÇÕES
# ================================================================================
print("\n🎨 6. GERANDO VISUALIZAÇÕES...")

dir_output = BASE_DIR / "04_visualizacoes" / "fase4_regressao"
dir_output.mkdir(parents=True, exist_ok=True)

# 6.1 Real vs Previsto (Scatter)
plt.figure(figsize=(10, 6))
sns.scatterplot(x=y_test_real, y=pred_50_real, alpha=0.6)
plt.plot([y_test_real.min(), y_test_real.max()], [y_test_real.min(), y_test_real.max()], 'r--')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Valor Real (R$)')
plt.ylabel('Valor Previsto (R$)')
plt.title('Precisão do Modelo de Valor Justo (Log Scale)', fontsize=14)
plt.tight_layout()
plt.savefig(dir_output / 'real_vs_previsto.png', dpi=300)
print("✓ Gráfico salvo: real_vs_previsto.png")

# 6.2 Distribuição dos Desvios
plt.figure(figsize=(10, 6))
sns.histplot(df_audit['Desvio_Percentual'], bins=50, kde=True, color='purple')
plt.xlim(-100, 500) # Limitar visualização
plt.xlabel('Desvio Percentual (%)')
plt.title('Distribuição de Desvios (Real vs Esperado)', fontsize=14)
plt.axvline(0, color='k', linestyle='--')
plt.tight_layout()
plt.savefig(dir_output / 'distribuicao_desvios.png', dpi=300)
print("✓ Gráfico salvo: distribuicao_desvios.png")

# ================================================================================
# 7. SALVAR RESULTADOS
# ================================================================================
print("\n💾 7. SALVANDO RESULTADOS...")

dir_analises = BASE_DIR / "03_analises" / "fase4_regressao"
dir_analises.mkdir(parents=True, exist_ok=True)

# Salvar base auditada
colunas_saida = ['UF', 'Município', 'Desastres', 'Status', 'Valor_Numerico', 
                 'Valor_Esperado_P50', 'Limite_Superior_P90', 'Alerta_Preco', 'Desvio_Percentual']
df_audit[colunas_saida].to_excel(dir_analises / "auditoria_valores_reconstrucao.xlsx", index=False)

print(f"✓ Relatório de auditoria salvo em: {dir_analises}")

print("\n" + "=" * 80)
print("✅ FASE 4 (REGRESSÃO PREDITIVA) CONCLUÍDA!")
print("=" * 80)
