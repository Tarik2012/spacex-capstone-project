import os
import pandas as pd
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

API = "https://api.spacexdata.com/v4"
endpoints = ["launches", "rockets", "launchpads", "payloads", "cores"]

for endpoint in endpoints:
    print(f"📥 Descargando {endpoint}...")
    url = f"{API}/{endpoint}"
    data = requests.get(url).json()
    df = pd.json_normalize(data)
    df.to_csv(os.path.join(RAW_DIR, f"{endpoint}_raw.csv"), index=False)

print("✅ Datos guardados en data/raw/")
