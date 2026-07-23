import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

file_path = BASE_DIR / "dados" / "dados_gerenciamento" / "Relatório_Consolidado_Acompanhamento_2017_2025.xlsx"
df = pd.read_excel(file_path)
print("Columns:", df.columns.tolist())
print(df.head())
