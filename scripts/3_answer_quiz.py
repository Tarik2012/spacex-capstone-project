import pandas as pd
import os

# Ruta al CSV procesado
DATA_PATH = os.path.join("data", "processed", "dataset_part_2.csv")

# Cargar dataset
df = pd.read_csv(DATA_PATH)

# 🔹 Asegurar que BoosterVersion sea string
df["BoosterVersion"] = df["BoosterVersion"].astype(str)

# 🔹 Filtrar solo Falcon 9
df = df[df["BoosterVersion"].str.contains("Falcon 9", case=False, na=False)]

# 1) Lanzamientos desde CCSFS SLC 40
launches_ccsfs = df[df["LaunchSite"] == "CCSFS SLC 40"].shape[0]

# 2) Tasa de éxito (%)
success_rate = round(df["Class"].mean() * 100, 0)

# 3) Lanzamientos a órbita GEO
geo_launches = df[df["Orbit"] == "GEO"].shape[0]

# 4) Aterrizajes exitosos en ASDS
asds_landings = df[df["LandingPad"].astype(str).str.contains("ASDS", na=False) & (df["Class"] == 1)].shape[0]

# Mostrar resultados
print("=== QUIZ RESPUESTAS ===")
print(f"1) Lanzamientos desde CCSFS SLC 40: {launches_ccsfs}")
print(f"2) Tasa de éxito: {success_rate}%")
print(f"3) Lanzamientos a órbita GEO: {geo_launches}")
print(f"4) Aterrizajes exitosos en ASDS: {asds_landings}")


