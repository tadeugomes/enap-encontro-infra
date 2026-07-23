import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

file_path = BASE_DIR / "02_dados_processados" / "dados_merged_acompanhamento_icm.xlsx"
df = pd.read_excel(file_path)
print("Columns:", df.columns.tolist())
print(df.head())
print(df.info())
