# spacexdash/metrics.py
import pandas as pd

def load_metrics(csv_path: str):
    df = pd.read_csv(csv_path)

    # Convertir fecha y extraer año
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["year"] = df["Date"].dt.year

    # Definir éxito (Class: 1 = éxito, 0 = fallo)
    df["is_success"] = df["Class"].astype(bool)

    # Renombrar masa para mantener compatibilidad
    df["payload_total_mass_kg"] = pd.to_numeric(df["PayloadMass"], errors="coerce")

    # 1) lanzamientos/año
    launches_per_year = df.groupby("year")["FlightNumber"].count().sort_index()

    # 2) éxito/año (%)
    success_rate = (df.groupby("year")["is_success"].mean() * 100).round(2).sort_index()

    # 3) masa total por año
    mass_per_year = (
        df.groupby("year")["payload_total_mass_kg"]
          .sum(min_count=1).fillna(0).sort_index()
    )

    # 4) top sitios de lanzamiento
    top_sites = df["LaunchSite"].fillna("Unknown").value_counts().head(10)

    # 5) top resultados Outcome
    top_outcomes = df["Outcome"].fillna("Unknown").value_counts().head(10)

    return {
        "launches_year_labels": launches_per_year.index.dropna().astype(int).tolist(),
        "launches_year_values": launches_per_year.astype(int).tolist(),

        "success_year_labels": success_rate.index.dropna().astype(int).tolist(),
        "success_year_values": success_rate.astype(float).tolist(),

        "mass_year_labels": mass_per_year.index.dropna().astype(int).tolist(),
        "mass_year_values": mass_per_year.astype(float).tolist(),

        "pads_labels": top_sites.index.astype(str).tolist(),
        "pads_values": top_sites.astype(int).tolist(),

        "outcome_labels": top_outcomes.index.astype(str).tolist(),
        "outcome_values": top_outcomes.astype(int).tolist(),
    }
