import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import unicodedata
import joblib
import os

# Configuração de caminhos
BASE_DIR = r'c:\Users\tadeu\Downloads\enap_infra_encontro'
DATA_PROCESSOS = os.path.join(BASE_DIR, 'dados', 'dados_gerenciamento', 'Relatório_Consolidado_Acompanhamento_2017_2025.xlsx')
DATA_ICM = os.path.join(BASE_DIR, 'dados', 'dados_faixa', 'ICM_Consolidado_LIMPO_V2.xlsx')
OUTPUT_DIR = os.path.join(BASE_DIR, '05_modelos')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'anomalias_isolation_forest.xlsx')
MODEL_FILE = os.path.join(OUTPUT_DIR, 'isolation_forest_model.pkl')

def normalize_text(text):
    if not isinstance(text, str):
        return str(text)
    return ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn').upper().strip()

def load_and_prepare_data():
    print("Carregando dados...")
    df_proc = pd.read_excel(DATA_PROCESSOS)
    df_icm = pd.read_excel(DATA_ICM)

    # Normalizar nomes para merge
    print("Normalizando nomes...")
    df_proc['Municipio_Norm'] = df_proc['Município'].apply(normalize_text)
    df_proc['UF_Norm'] = df_proc['UF'].apply(normalize_text)
    
    df_icm['Municipio_Norm'] = df_icm['Municipio'].apply(normalize_text)
    df_icm['UF_Norm'] = df_icm['UF'].apply(normalize_text)

    # Merge
    print("Realizando merge...")
    df = pd.merge(df_proc, df_icm[['UF_Norm', 'Municipio_Norm', 'Faixa_ICM', 'Codigo_IBGE']], 
                  on=['UF_Norm', 'Municipio_Norm'], how='left')
    
    print(f"Total de registros: {len(df)}")
    print(f"Registros sem ICM: {df['Faixa_ICM'].isna().sum()}")

    # Tratamento de Valor Solicitado
    # Remove 'R$', pontos de milhar e converte vírgula decimal
    def clean_currency(x):
        if isinstance(x, str):
            x = x.replace('R$', '').replace('.', '').replace(',', '.').strip()
        return pd.to_numeric(x, errors='coerce')

    df['Valor_Solicitado_Clean'] = df['Valor Solicitado'].apply(clean_currency)
    
    # Preencher valores nulos ou zero com valor pequeno para log
    df['Valor_Solicitado_Clean'] = df['Valor_Solicitado_Clean'].fillna(0)
    df['log_valor'] = np.log1p(df['Valor_Solicitado_Clean'])

    # Frequência de solicitações
    df['frequencia_municipio'] = df.groupby(['UF', 'Município'])['Processo'].transform('count')

    # Mapeamento Faixa ICM
    mapa_icm = {'A': 4, 'B': 3, 'C': 2, 'D': 1}
    df['faixa_icm_num'] = df['Faixa_ICM'].map(mapa_icm)
    
    # Preencher nulos em Faixa ICM com mediana ou valor específico (vamos usar mediana por enquanto ou 1=D se conservador)
    # O plano diz "Pior Faixa assumida em conflitos", então para nulos talvez D seja seguro, mas vamos usar mediana dos dados
    median_icm = df['faixa_icm_num'].median()
    df['faixa_icm_num'] = df['faixa_icm_num'].fillna(median_icm)

    return df

def train_isolation_forest(df):
    print("Treinando Isolation Forest...")
    
    # Features
    features = ['log_valor', 'faixa_icm_num', 'frequencia_municipio', 'Desastres']
    
    X = df[features].copy()
    
    # Pipeline para pré-processamento
    categorical_features = ['Desastres']
    numeric_features = ['log_valor', 'faixa_icm_num', 'frequencia_municipio']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
        ])

    # Modelo
    # Contamination: estimativa da proporção de outliers. Vamos começar com 'auto' ou 0.05
    model = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', IsolationForest(contamination=0.05, random_state=42, n_jobs=-1))
    ])

    model.fit(X)
    
    # Predição (-1 = anomalia, 1 = normal)
    df['anomaly_score'] = model.decision_function(X)
    df['is_anomaly'] = model.predict(X)
    
    return df, model

def main():
    df = load_and_prepare_data()
    
    # Filtrar apenas linhas com Valor Solicitado > 0 para evitar ruído de processos vazios/cancelados se houver
    # Mas o plano diz para analisar solicitações. Vamos manter tudo, mas log_valor cuida do zero.
    
    df_result, model = train_isolation_forest(df)
    
    # Salvar modelo
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    joblib.dump(model, MODEL_FILE)
    print(f"Modelo salvo em {MODEL_FILE}")
    
    # Filtrar anomalias
    anomalies = df_result[df_result['is_anomaly'] == -1].copy()
    anomalies = anomalies.sort_values('anomaly_score') # Menores scores são mais anômalos
    
    print(f"Total de anomalias detectadas: {len(anomalies)}")
    
    # Selecionar colunas para exportação
    cols_export = ['UF', 'Município', 'Processo', 'Desastres', 'Valor Solicitado', 
                   'Faixa_ICM', 'frequencia_municipio', 'anomaly_score', 'is_anomaly']
    
    anomalies[cols_export].to_excel(OUTPUT_FILE, index=False)
    print(f"Relatório de anomalias salvo em {OUTPUT_FILE}")

    # Exibir top 10
    print("\nTop 10 Anomalias (Mais extremas):")
    print(anomalies[cols_export].head(10))

if __name__ == "__main__":
    main()
