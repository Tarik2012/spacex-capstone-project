# spacexdash/metrics.py
import pandas as pd

def load_metrics(csv_path: str):
    df = pd.read_csv(csv_path)

    # Tipos
    df["year"] = pd.to_numeric(df.get("year"), errors="coerce").astype("Int64")
    df["is_success"] = df.get("is_success").astype(bool)
    df["payload_total_mass_kg"] = pd.to_numeric(df.get("payload_total_mass_kg"), errors="coerce")

    # 1) lanzamientos/año
    launches_per_year = df.groupby("year")["id"].count().sort_index()

    # 2) éxito/año (%)
    success_rate = (df.groupby("year")["is_success"].mean() * 100).round(2).sort_index()

    # 3) masa total por año
    mass_per_year = (
        df.groupby("year")["payload_total_mass_kg"]
          .sum(min_count=1).fillna(0).sort_index()
    )

    # 4) top clientes
    clients = (
        df["payload_customers"].fillna("Unknown").astype(str)
          .str.split(",").explode().str.strip().replace({"": "Unknown"})
    )
    top_clients = clients.value_counts().head(10)

    # 5) lanzamientos por rampa
    top_pads = df["launchpad_name"].fillna("Unknown").value_counts().head(10)

    # IMPORTANTÍSIMO: devolver tipos nativos de Python (listas de int/float/str)
    return {
        "launches_year_labels": [int(x) for x in launches_per_year.index.dropna().tolist()],
        "launches_year_values": [int(x) for x in launches_per_year.tolist()],

        "success_year_labels": [int(x) for x in success_rate.index.dropna().tolist()],
        "success_year_values": [float(x) for x in success_rate.tolist()],

        "mass_year_labels": [int(x) for x in mass_per_year.index.dropna().tolist()],
        "mass_year_values": [float(x) for x in mass_per_year.tolist()],

        "clients_labels": [str(x) for x in top_clients.index.tolist()],
        "clients_values": [int(x) for x in top_clients.tolist()],

        "pads_labels": [str(x) for x in top_pads.index.tolist()],
        "pads_values": [int(x) for x in top_pads.tolist()],
    }
