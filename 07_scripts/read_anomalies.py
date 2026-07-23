import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

file_path = BASE_DIR / "05_modelos" / "anomalias_isolation_forest.xlsx"
df = pd.read_excel(file_path)
print(df.head(20))
