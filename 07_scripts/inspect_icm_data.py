import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

file_path = BASE_DIR / "dados" / "dados_faixa" / "ICM_Consolidado_LIMPO_V2.xlsx"
df = pd.read_excel(file_path)
print("Columns:", df.columns.tolist())
print(df.head())
