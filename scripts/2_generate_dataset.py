import os
import pandas as pd
import ast

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

# === 1. Cargar datos crudos ===
launches = pd.read_csv(os.path.join(RAW_DIR, "launches_raw.csv"))
rockets = pd.read_csv(os.path.join(RAW_DIR, "rockets_raw.csv"))
pads = pd.read_csv(os.path.join(RAW_DIR, "launchpads_raw.csv"))
payloads = pd.read_csv(os.path.join(RAW_DIR, "payloads_raw.csv"))

# === 2. Filtrar solo Falcon 9 ===
if "name" in rockets.columns:
    falcon9_ids = rockets.loc[rockets["name"].str.contains("Falcon 9", case=False), "id"]
else:
    falcon9_ids = rockets["id"]  # seguridad, si cambia el nombre
launches = launches[launches["rocket"].isin(falcon9_ids)]

# === 3. FlightNumber y Date ===
launches["FlightNumber"] = launches["flight_number"]
launches["Date"] = pd.to_datetime(launches["date_utc"]).dt.date

# === 4. Booster Version ===
rockets_name_col = "name" if "name" in rockets.columns else rockets.columns[0]
launches = launches.merge(
    rockets[["id", rockets_name_col]],
    left_on="rocket", right_on="id", how="left"
).rename(columns={rockets_name_col: "BoosterVersion"})
if "id" in launches.columns:
    launches = launches.drop(columns=["id"])
if "BoosterVersion" not in launches.columns:
    launches["BoosterVersion"] = None

# === 5. Payload info ===
launches["payload_id"] = launches["payloads"].apply(
    lambda x: ast.literal_eval(x)[0] if pd.notnull(x) and x != "[]" else None
)
payloads_cols = ["id"]
if "mass_kg" in payloads.columns:
    payloads_cols.append("mass_kg")
if "orbit" in payloads.columns:
    payloads_cols.append("orbit")
launches = launches.merge(
    payloads[payloads_cols],
    left_on="payload_id", right_on="id", how="left"
)
if "mass_kg" in launches.columns:
    launches = launches.rename(columns={"mass_kg": "PayloadMass"})
else:
    launches["PayloadMass"] = None
if "orbit" in launches.columns:
    launches = launches.rename(columns={"orbit": "Orbit"})
else:
    launches["Orbit"] = None
if "id" in launches.columns:
    launches = launches.drop(columns=["id"])

# === 6. Launch Site ===
pads_cols = ["id"]
for col in ["name", "latitude", "longitude"]:
    if col in pads.columns:
        pads_cols.append(col)
launches = launches.merge(
    pads[pads_cols],
    left_on="launchpad", right_on="id", how="left"
)
if "name" in launches.columns:
    launches = launches.rename(columns={"name": "LaunchSite"})
else:
    launches["LaunchSite"] = None
if "latitude" in launches.columns:
    launches = launches.rename(columns={"latitude": "Latitude"})
else:
    launches["Latitude"] = None
if "longitude" in launches.columns:
    launches = launches.rename(columns={"longitude": "Longitude"})
else:
    launches["Longitude"] = None
if "id" in launches.columns:
    launches = launches.drop(columns=["id"])

# === 7. Core data ===
def get_core_data(core_str):
    try:
        cores_list = ast.literal_eval(core_str)
        return cores_list[0] if isinstance(cores_list, list) and len(cores_list) > 0 else {}
    except:
        return {}

launches["core_data"] = launches["cores"].apply(get_core_data)
launches["GridFins"] = launches["core_data"].apply(lambda x: x.get("gridfins", None))
launches["Reused"] = launches["core_data"].apply(lambda x: x.get("reused", None))
launches["Legs"] = launches["core_data"].apply(lambda x: x.get("legs", None))
launches["LandingPad"] = launches["core_data"].apply(lambda x: x.get("landpad", None))
launches["Block"] = launches["core_data"].apply(lambda x: x.get("block", None))
launches["ReusedCount"] = launches["core_data"].apply(lambda x: x.get("reuse_count", None))
launches["Serial"] = launches["core_data"].apply(lambda x: x.get("core", None))
launches["Outcome"] = launches["core_data"].apply(
    lambda x: f"{'True' if x.get('landing_success') else 'False'} {x.get('landing_type', 'Unknown')}"
)
launches["Class"] = launches["core_data"].apply(lambda x: 1 if x.get("landing_success") else 0)
launches["Flights"] = launches["ReusedCount"].apply(lambda x: x + 1 if pd.notnull(x) else 1)

# === 8. Columnas finales ===
final_cols = [
    "FlightNumber", "Date", "BoosterVersion", "PayloadMass", "Orbit", "LaunchSite",
    "Outcome", "Flights", "GridFins", "Reused", "Legs",
    "LandingPad", "Block", "ReusedCount", "Serial", "Longitude", "Latitude", "Class"
]
for col in final_cols:
    if col not in launches.columns:
        launches[col] = None

df_final = launches[final_cols]

# === 9. Guardar dataset procesado ===
output_path = os.path.join(PROCESSED_DIR, "dataset_part_2.csv")
df_final.to_csv(output_path, index=False)

print(f"✅ Dataset procesado guardado en: {output_path}")
