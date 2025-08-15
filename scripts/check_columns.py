import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

files = [
    "launchpads_raw.csv",
    "payloads_raw.csv",
    "launches_raw.csv"
]

for file in files:
    print(f"\n=== 📂 {file} ===")
    path = os.path.join(RAW_DIR, file)
    df = pd.read_csv(path)
    print("📌 Columnas:", df.columns.tolist())
    print("\n📄 Primeras filas:")
    print(df.head())
    print("-" * 80)
