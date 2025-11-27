"""
IMPLEMENTAÇÃO DO PLANO DE ML - FASE 3: CLASSIFICAÇÃO (PREDIÇÃO DE RISCO)
Objetivo: Prever a probabilidade de um processo ser APROVADO (Recurso Transferido) vs REJEITADO/SOBRESTADO.

Autor: Análise de Dados - ENAP
Data: 23/11/2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.preprocessing import LabelEncoder
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# Configuração de estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("viridis")

print("=" * 80)
print("FASE 3: CLASSIFICAÇÃO - PREDIÇÃO DE APROVAÇÃO DE PROCESSOS")
print("=" * 80)

# ================================================================================
# 1. CARREGAR DADOS
# ================================================================================
print("\n📂 1. CARREGANDO E INTEGRANDO DADOS...")
BASE_DIR = Path(r"c:\Users\tadeu\Downloads\enap_infra_encontro")

# Arquivo de transações (Processos)
arquivo_processos = BASE_DIR / "dados" / "dados_gerenciamento" / "Relatório_Consolidado_Acompanhamento_2017_2025.xlsx"
df_processos = pd.read_excel(arquivo_processos)
print(f"✓ Processos carregados: {len(df_processos):,} registros")

# Arquivo de Municípios (Clusters + ICM)
arquivo_municipios = BASE_DIR / "02_dados_processados" / "dados_municipios_clusterizados.xlsx"
df_municipios = pd.read_excel(arquivo_municipios)
print(f"✓ Dados municipais carregados: {len(df_municipios):,} registros")

# ================================================================================
# 2. PREPARAÇÃO DOS DADOS (MERGE E LIMPEZA)
# ================================================================================
print("\n⚙️ 2. PREPARANDO DATASET DE TREINO...")

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
print(f"✓ Registros após merge: {len(df_full):,}")

# Limpar Valor Solicitado
def limpar_valor(val):
    if pd.isna(val): return 0.0
    s = str(val).replace('R$', '').replace('.', '').replace(',', '.').strip()
    try:
        return float(s)
    except:
        return 0.0

df_full['Valor_Numerico'] = df_full['Valor Solicitado'].apply(limpar_valor)

# Definir Target (Alvo)
# 1 = Sucesso (Recurso Transferido)
# 0 = Fracasso (Indeferido, Excluído, Sobrestado)
# Ignorar = Em Análise

status_sucesso = ['ACOMPANHAMENTO - RECURSO TRANSFERIDO']
status_fracasso = [
    'ARQUIVADO - PLANO DE TRABALHO INDEFERIDO',
    'ARQUIVADO - PLANO DE TRABALHO EXCLUÍDO',
    'ACOMPANHAMENTO - SOBRESTADO'
]

# Filtrar apenas status finais
df_model = df_full[df_full['Status'].isin(status_sucesso + status_fracasso)].copy()
df_model['Target'] = df_model['Status'].apply(lambda x: 1 if x in status_sucesso else 0)

print(f"✓ Registros finais para modelagem: {len(df_model):,}")
print(f"  - Aprovados (1): {df_model['Target'].sum()} ({df_model['Target'].mean():.1%})")
print(f"  - Reprovados (0): {len(df_model) - df_model['Target'].sum()}")

# ================================================================================
# 3. FEATURE ENGINEERING
# ================================================================================
print("\n🔧 3. ENGENHARIA DE FEATURES...")

# Selecionar features
features_cat = ['UF', 'Desastres', 'Faixa_ICM', 'Cluster_Ordenado', 'Faixa_Populacional']
features_num = ['Valor_Numerico']

# Encoding de categóricas
encoders = {}
for col in features_cat:
    le = LabelEncoder()
    # Converter para string para evitar erro com números/mistos
    df_model[col] = df_model[col].astype(str)
    df_model[f'{col}_Code'] = le.fit_transform(df_model[col])
    encoders[col] = le

# Montar X e y
X_cols = [f'{col}_Code' for col in features_cat] + features_num
X = df_model[X_cols]
y = df_model['Target']

# Split Treino/Teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"✓ Dataset dividido: Treino={len(X_train)}, Teste={len(X_test)}")

# ================================================================================
# 4. TREINAMENTO DO MODELO
# ================================================================================
print("\n🤖 4. TREINANDO RANDOM FOREST...")

rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, class_weight='balanced')
rf.fit(X_train, y_train)

# ================================================================================
# 5. AVALIAÇÃO
# ================================================================================
print("\n📊 5. AVALIAÇÃO DO MODELO...")

y_pred = rf.predict(X_test)
y_prob = rf.predict_proba(X_test)[:, 1]

print("\nRelatório de Classificação:")
print(classification_report(y_test, y_pred))

auc = roc_auc_score(y_test, y_prob)
print(f"ROC-AUC Score: {auc:.4f}")

# Matriz de Confusão
cm = confusion_matrix(y_test, y_pred)

# Feature Importance
importances = pd.DataFrame({
    'Feature': X_cols,
    'Importance': rf.feature_importances_
}).sort_values('Importance', ascending=False)

print("\nImportância das Variáveis:")
print(importances)

# ================================================================================
# 6. VISUALIZAÇÕES
# ================================================================================
print("\n🎨 6. GERANDO VISUALIZAÇÕES...")

dir_output = BASE_DIR / "04_visualizacoes" / "fase3_classificacao"
dir_output.mkdir(parents=True, exist_ok=True)

# 6.1 Matriz de Confusão
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.title('Matriz de Confusão (Predição de Aprovação)', fontsize=14)
plt.ylabel('Real (0=Reprovado, 1=Aprovado)')
plt.xlabel('Predito')
plt.tight_layout()
plt.savefig(dir_output / 'confusion_matrix.png', dpi=300)
print("✓ Gráfico salvo: confusion_matrix.png")

# 6.2 Feature Importance
plt.figure(figsize=(10, 6))
ax = sns.barplot(data=importances, x='Importance', y='Feature', palette='viridis')
plt.title('O que define a aprovação de um processo?', fontsize=14)
for i in ax.containers:
    ax.bar_label(i, fmt='%.3f', padding=3)
plt.tight_layout()
plt.savefig(dir_output / 'feature_importance.png', dpi=300)
print("✓ Gráfico salvo: feature_importance.png")

# 6.3 Curva ROC
fpr, tpr, _ = roc_curve(y_test, y_prob)
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f'Random Forest (AUC = {auc:.2f})')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('Taxa de Falsos Positivos')
plt.ylabel('Taxa de Verdadeiros Positivos')
plt.title('Curva ROC', fontsize=14)
plt.legend()
plt.tight_layout()
plt.savefig(dir_output / 'roc_curve.png', dpi=300)
print("✓ Gráfico salvo: roc_curve.png")

# ================================================================================
# 7. SALVAR RESULTADOS
# ================================================================================
print("\n💾 7. SALVANDO RESULTADOS...")

dir_analises = BASE_DIR / "03_analises" / "fase3_classificacao"
dir_analises.mkdir(parents=True, exist_ok=True)

# Salvar importâncias
importances.to_excel(dir_analises / "feature_importance.xlsx", index=False)

# Salvar previsões no conjunto de teste para análise de erros
df_test_results = X_test.copy()
df_test_results['Real'] = y_test
df_test_results['Predito'] = y_pred
df_test_results['Probabilidade'] = y_prob
df_test_results.to_excel(dir_analises / "analise_erros_teste.xlsx", index=False)

print(f"✓ Resultados salvos em: {dir_analises}")

print("\n" + "=" * 80)
print("✅ FASE 3 (CLASSIFICAÇÃO) CONCLUÍDA!")
print("=" * 80)
