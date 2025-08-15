# scripts/check_dataset_part_2.py
import pandas as pd
from pathlib import Path

# Ruta al dataset procesado
dataset_path = Path("data/processed/dataset_part_2.csv")

if dataset_path.exists():
    df = pd.read_csv(dataset_path)
    print(f"📌 Columnas del archivo {dataset_path.name}:")
    print(list(df.columns))
    print("\n📄 Primeras filas:")
    print(df.head())
else:
    print(f"❌ No se encontró el archivo {dataset_path}")
