# scripts/build_dataset_past.py
import os
import requests
import pandas as pd
from pandas import json_normalize

API = "https://api.spacexdata.com/v4"
URL = {
    "launches": f"{API}/launches",      # past + upcoming
    "rockets":  f"{API}/rockets",
    "pads":     f"{API}/launchpads",
    "payloads": f"{API}/payloads",
}

OUT_RAW_DIR = "data/raw"
OUT_PROC_DIR = "data/processed"
OUT_CSV = os.path.join(OUT_PROC_DIR, "spacex_launches_clean_past.csv")

def fetch_df(url: str) -> pd.DataFrame:
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    return json_normalize(r.json())

def join_unique(series):
    out = []
    for x in series.dropna():
        if isinstance(x, list):
            out += x
        else:
            out.append(x)
    out = [str(v).strip() for v in out if str(v).strip()]
    return ", ".join(sorted(set(out))) if out else None

def main():
    os.makedirs(OUT_RAW_DIR, exist_ok=True)
    os.makedirs(OUT_PROC_DIR, exist_ok=True)

    # ====== Descarga ======
    launches = fetch_df(URL["launches"])
    rockets  = fetch_df(URL["rockets"])
    pads     = fetch_df(URL["pads"])
    payloads = fetch_df(URL["payloads"])

    # Copias RAW (opcional)
    launches.to_csv(os.path.join(OUT_RAW_DIR, "launches_raw.csv"), index=False)

    # ====== Limpieza base ======
    launches["date_utc"] = pd.to_datetime(launches["date_utc"], errors="coerce", utc=True)
    launches["is_past"]  = launches["upcoming"].eq(False)
    launches["is_success"] = launches["success"].fillna(False).astype(bool)

    # Solo lanzamientos pasados + fecha válida
    launches = launches[launches["is_past"] & launches["date_utc"].notna()].copy()

    # Partes temporales
    launches["date"]  = launches["date_utc"].dt.date
    launches["year"]  = launches["date_utc"].dt.year
    launches["month"] = launches["date_utc"].dt.month
    launches["day"]   = launches["date_utc"].dt.day
    launches["quarter"] = launches["date_utc"].dt.to_period("Q").astype(str)
    launches["weekday"] = launches["date_utc"].dt.day_name()

    keep_base = [
        "id","flight_number","name","date_utc","date","year","month","day","quarter","weekday",
        "rocket","launchpad","is_past","is_success","details","links.webcast","links.article","payloads"
    ]
    launches = launches[[c for c in keep_base if c in launches.columns]].copy()

    # ====== Enriquecer: Rockets ======
    rockets = rockets.rename(columns={"id":"rocket_id","name":"rocket_name","type":"rocket_type"})
    rockets_keep = ["rocket_id","rocket_name","rocket_type","first_flight","stages","boosters","active"]
    launches = launches.merge(rockets[rockets_keep], left_on="rocket", right_on="rocket_id", how="left")

    # ====== Enriquecer: Launchpads ======
    pads = pads.rename(columns={"id":"launchpad_id","name":"launchpad_name"})
    pads_keep = ["launchpad_id","launchpad_name","full_name","region","locality","latitude","longitude"]
    launches = launches.merge(pads[pads_keep], left_on="launchpad", right_on="launchpad_id", how="left")

    # ====== Enriquecer: Payloads (agregado por lanzamiento) ======
    pl = launches[["id","payloads"]].explode("payloads").rename(columns={"payloads":"payload_id"})
    pl = pl.merge(payloads.rename(columns={"id":"payload_id"}), on="payload_id", how="left")

    # Masa total
    agg_mass = pl.groupby("id", dropna=False)["mass_kg"].sum(min_count=1).rename("payload_total_mass_kg")
    # Clientes/órbitas como listas únicas
    agg_clients = pl.groupby("id", dropna=False)["customers"].apply(join_unique).rename("payload_customers")
    agg_orbits  = pl.groupby("id", dropna=False)["orbit"].apply(join_unique).rename("payload_orbits")

    launches = launches.merge(agg_mass, left_on="id", right_index=True, how="left")
    launches = launches.merge(agg_clients, left_on="id", right_index=True, how="left")
    launches = launches.merge(agg_orbits, left_on="id", right_index=True, how="left")

    # ====== Normalizaciones de texto / NaNs ======
    # Clientes / órbitas sin NaN (como pediste)
# Rellenar campos vacíos
    launches["payload_customers"] = launches["payload_customers"].fillna("Unknown")
    launches["payload_orbits"]    = launches["payload_orbits"].fillna("Unknown")

    # Filtrar solo Falcon 9
    launches = launches[launches["rocket_name"].str.contains("Falcon 9", case=False, na=False)]

    # Nombre de rampa “normalizado” (minúsculas, sin dobles espacios) para facilitar filtros/join futuros
    for col in ["launchpad_name","full_name","region","locality"]:
        if col in launches.columns:
            launches[col] = (
                launches[col]
                .astype(str).str.strip()
                .str.replace(r"\s+", " ", regex=True)
            )

    # ====== Orden final ======
    ordered = [
        # claves
        "id","flight_number","name",
        # fechas
        "date_utc","date","year","month","day","quarter","weekday",
        # resultado
        "is_success",
        # rocket
        "rocket_id","rocket_name","rocket_type","stages","boosters","active","first_flight",
        # launchpad
        "launchpad_id","launchpad_name","full_name","region","locality","latitude","longitude",
        # payload agregado
        "payload_total_mass_kg","payload_orbits","payload_customers",
        # extras
        "details","links.webcast","links.article",
    ]
    launches = launches[[c for c in ordered if c in launches.columns]].sort_values("date_utc")

    # ====== Guardar ======
    launches.to_csv(OUT_CSV, index=False)
    print(f"✅ Guardado: {OUT_CSV} ({len(launches)} filas)")
    print("🗓️ Rango:", launches["date_utc"].min(), "→", launches["date_utc"].max())
    print("📦 Con masa total conocida:", launches["payload_total_mass_kg"].notna().sum())
    print("👤 Clientes vacíos? ->", (launches['payload_customers'] == 'Unknown').sum(), "filas (rellenas con 'Unknown')")
    print("🛰️ Órbitas vacías?  ->", (launches['payload_orbits'] == 'Unknown').sum(), "filas (rellenas con 'Unknown')")

if __name__ == "__main__":
    main()
