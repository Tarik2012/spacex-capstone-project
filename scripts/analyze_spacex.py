# analyze_spacex.py
# -*- coding: utf-8 -*-
import sys
import re
from pathlib import Path
import pandas as pd

# ---------- utils ----------
def coalesce_col(df, *candidates):
    """Devuelve el nombre de la 1ª columna existente entre candidates."""
    for c in candidates:
        if c in df.columns:
            return c
    return None

def norm_str(x):
    if pd.isna(x):
        return ""
    return str(x).strip()

def contains_any(value, keys):
    s = norm_str(value).upper()
    return any(k.upper() in s for k in keys)

# ---------- core ----------
def load_df(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    # normalizaciones ligeras comunes
    # éxito
    col_success = coalesce_col(df, "is_success", "success", "launch_success")
    if col_success:
        df[col_success] = df[col_success].map(
            lambda v: True if str(v).lower() in {"1","true","t","yes","y"} else (False if str(v).lower() in {"0","false","f","no","n"} else v)
        )
    # nombres/etiquetas a texto
    for c in df.columns:
        if df[c].dtype == "O":
            df[c] = df[c].astype(str).str.strip()
    return df

def q1_count_from_slc40(df):
    col_site = coalesce_col(df, "launchpad_name", "launch_site", "site_name", "launchpad")
    if not col_site:
        return None, "No encuentro columna de sitio de lanzamiento."
    # Variantes frecuentes del nombre
    variants = ["CCAFS SLC 40", "CCSFS SLC 40", "Cape Canaveral SLC 40", "SLC-40"]
    m = df[col_site].apply(lambda v: contains_any(v, variants))
    return int(m.sum()), f"Columna usada: {col_site}"

def q2_success_rate(df):
    col_success = coalesce_col(df, "is_success", "success", "launch_success")
    if not col_success:
        return None, "No encuentro columna de éxito."
    valid = df[col_success].isin([True, False])
    if valid.sum() == 0:
        return None, "No hay valores booleanos de éxito."
    rate = 100.0 * df.loc[valid, col_success].mean()
    return round(rate, 2), f"Columna usada: {col_success}; n={valid.sum()}"

def q3_num_to_geo(df):
    # orbits pueden estar en una sola columna (string) o lista/CSV.
    col_orbit = coalesce_col(df, "payload_orbits", "payload_orbit", "orbit", "target_orbit")
    if not col_orbit:
        return None, "No encuentro columna de órbita."
    # Contamos misiones que vayan a GEO o su transferencia GTO (suele contarse como GEO en cursos).
    GEO_KEYS = ["GEO", "GSO", "GEOSTATIONARY"]
    GTO_KEYS = ["GTO", "GEOSTATIONARY TRANSFER"]
    def is_geo(row_val: str):
        s = norm_str(row_val).upper()
        # dividir listas si vienen separadas
        parts = re.split(r"[;,/|]", s) if any(ch in s for ch in ";,/|") else [s]
        parts = [p.strip() for p in parts if p.strip()]
        return any(any(k in p for k in GEO_KEYS+GTO_KEYS) for p in parts)
    m = df[col_orbit].apply(is_geo)
    return int(m.sum()), f"Columna usada: {col_orbit} (contando GEO y GTO)"

def q4_drone_ship_landings(df):
    """
    'nave no tripulada' suele referirse a aterrizajes de la 1ª etapa en
    una plataforma no tripulada ('droneship' / ASDS). Contamos aterrizajes
    exitosos en droneship.
    """
    col_land_type = coalesce_col(df, "landing_type", "landing", "landing_method", "landing_pad_type")
    col_land_success = coalesce_col(df, "landing_success", "land_success", "booster_landing_success")
    if not col_land_type:
        return None, "No encuentro columna de tipo de aterrizaje."
    if not col_land_success:
        # si no hay éxito explícito, contamos todos los ASDS
        col_land_success = None

    DRONE_KEYS = ["ASDS", "DRONESHIP", "AUTONOMOUS SPACEPORT DRONE SHIP"]
    def is_droneship(x): return contains_any(x, DRONE_KEYS)

    if col_land_success:
        m = df[col_land_type].apply(is_droneship) & df[col_land_success].isin([True, "True", "true", 1])
    else:
        m = df[col_land_type].apply(is_droneship)
    return int(m.sum()), f"Columnas usadas: {col_land_type}" + (f", {col_land_success}" if col_land_success else "")

def main(path):
    df = load_df(path)
    print(f"\nArchivo: {Path(path).resolve()}")
    print(f"Filas: {len(df):,}  |  Columnas: {len(df.columns)}")
    print("\nColumnas disponibles:\n - " + "\n - ".join(df.columns))

    print("\n--- RESULTADOS TEST ---")
    v1, msg1 = q1_count_from_slc40(df); print(f"1) Lanzamientos desde CCAFS/CCSFS SLC 40: {v1}   [{msg1}]")
    v2, msg2 = q2_success_rate(df);    print(f"2) Tasa de éxito (%): {v2}   [{msg2}]")
    v3, msg3 = q3_num_to_geo(df);      print(f"3) Nº lanzamientos a órbita GEO/GTO: {v3}   [{msg3}]")
    v4, msg4 = q4_drone_ship_landings(df); print(f"4) Aterrizajes en nave no tripulada (ASDS): {v4}   [{msg4}]")

    # extra: tablas rápidas para revisar
    print("\n--- COMPROBACIONES RÁPIDAS ---")
    site_col = coalesce_col(df, "launchpad_name", "launch_site", "site_name", "launchpad")
    if site_col:
        print("\nLanzamientos por sitio (top):")
        print(df[site_col].value_counts().head(10))

    orbit_col = coalesce_col(df, "payload_orbits", "payload_orbit", "orbit", "target_orbit")
    if orbit_col:
        print("\nÓrbitas únicas (muestra):")
        print(df[orbit_col].value_counts().head(20))

    land_col = coalesce_col(df, "landing_type", "landing", "landing_method", "landing_pad_type")
    if land_col:
        print("\nTipos de aterrizaje (muestra):")
        print(df[land_col].value_counts().head(20))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python analyze_spacex.py <ruta_al_csv>")
        sys.exit(1)
    main(sys.argv[1])
