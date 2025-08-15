# spacexdash/views.py
import os
import json
from django.shortcuts import render
from django.conf import settings
from .metrics import load_metrics
import pandas as pd
import folium
from django.shortcuts import render

# Ruta al nuevo CSV
CSV_PATH = os.path.join(settings.BASE_DIR, "data", "processed", "dataset_part_2.csv")

def dashboard(request):
    # Cargar métricas desde el CSV
    data = load_metrics(CSV_PATH)

    # Convertir todos los valores a JSON para pasarlos a la plantilla
    context = {k: json.dumps(v) for k, v in data.items()}

    return render(request, "spacexdash/dashboard.html", context)





def launch_sites_map(request):
    spacex_csv_url = (
        "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
        "IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv"
    )
    df = pd.read_csv(spacex_csv_url)

    m = folium.Map(location=[28.5623, -80.5774], zoom_start=4)

    # Colores por sitio
    site_colors = {
        "CCAFS LC-40": "blue",
        "KSC LC-39A": "red",
        "VAFB SLC-4E": "green",
        "CCAFS SLC-40": "purple"
    }

    # Añadir marcadores con colores distintos
    for site, g in df.groupby("Launch Site"):
        lat = g["Lat"].iloc[0]
        lon = g["Long"].iloc[0]
        color = site_colors.get(site, "blue")  # Azul por defecto si no está en el diccionario
        folium.Marker(
            location=[lat, lon],
            popup=site,
            icon=folium.Icon(color=color, icon="rocket")
        ).add_to(m)

    # Ajustar zoom para mostrar todos
    coords = df.groupby("Launch Site")[["Lat", "Long"]].first().values.tolist()
    m.fit_bounds(coords)

    map_html = m._repr_html_()
    return render(request, "spacexdash/launch_sites_map.html", {"map_html": map_html})
    return render(request, "spacexdash/launch_sites_map.html", {"map_html": map_html})
