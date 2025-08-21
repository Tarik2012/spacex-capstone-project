import os
import json
import pandas as pd
import folium
from django.conf import settings
from django.shortcuts import render
from .metrics import load_metrics
from folium.plugins import MarkerCluster
import math

# === Rutas de los CSV ===
CSV_METRICS = os.path.join(settings.BASE_DIR, "data", "processed", "dataset_part_2.csv")
CSV_MAP = os.path.join(settings.BASE_DIR, "data", "processed", "spacex_launch_geo.csv")


# === Dashboard (no lo tocamos) ===
def dashboard(request):
    data = load_metrics(CSV_METRICS)
    context = {k: json.dumps(v) for k, v in data.items()}
    return render(request, "spacexdash/dashboard.html", context)


# === Mapa de sitios y lanzamientos ===
# --- Función Haversine para calcular distancias ---
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radio de la Tierra en km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))


def launch_sites_map(request):
    # Cargar dataset
    df = pd.read_csv(CSV_MAP)
    df["class"] = pd.to_numeric(df["class"], errors="coerce")

    # Crear mapa centrado
    avg_lat, avg_lon = df["Lat"].mean(), df["Long"].mean()
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=3)

    # --- Marcadores de sitios (azules) ---
    sites = df.groupby("Launch Site")[["Lat", "Long"]].first().reset_index()
    for _, row in sites.iterrows():
        folium.Marker(
            location=[row["Lat"], row["Long"]],
            popup=f"Launch Site: {row['Launch Site']}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

    # --- Cluster de lanzamientos (verde/rojo) ---
    marker_cluster = MarkerCluster().add_to(m)
    for _, row in df.iterrows():
        color = "green" if row["class"] == 1 else "red"
        folium.CircleMarker(
            location=[row["Lat"], row["Long"]],
            radius=5,
            color=color,
            fill=True,
            fill_opacity=0.7,
            popup=f"{row['Launch Site']}<br>Outcome: {'Success' if row['class']==1 else 'Failure'}"
        ).add_to(marker_cluster)

    # --- Análisis por sitio ---
    analysis = []
    for site, group in df.groupby("Launch Site"):
        total = len(group)
        success = int(group["class"].sum())
        failure = total - success
        success_rate = round((success / total) * 100, 1)
        analysis.append({
            "name": site,
            "total": total,
            "success": success,
            "failure": failure,
            "success_rate": success_rate,
        })

    # --- Distancias a ciudades cercanas ---
    cities = {
        "Orlando": (28.5383, -81.3792),
        "Los Angeles": (34.0522, -118.2437),
        "New York": (40.7128, -74.0060),
        "Houston": (29.7604, -95.3698),
    }

    distances = []
    for _, site in sites.iterrows():
        site_name, site_lat, site_lon = site["Launch Site"], site["Lat"], site["Long"]
        for city, (city_lat, city_lon) in cities.items():
            d = round(haversine(site_lat, site_lon, city_lat, city_lon), 1)
            distances.append({
                "site": site_name,
                "city": city,
                "distance_km": d
            })

    # Renderizar
    return render(request, "spacexdash/launch_sites_map.html", {
        "map_html": m._repr_html_(),
        "analysis": analysis,
        "distances": distances
    })



def dashboard_dash(request):
    return render(request, "spacexdash/dashboard-dash.html")

