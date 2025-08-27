import requests
import os

# URL oficial del CSV
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv"

# Ruta donde quieres guardarlo
save_path = os.path.join("data", "processed", "spacex_launch_geo.csv")

# Descargar el archivo
response = requests.get(url)

if response.status_code == 200:
    with open(save_path, "wb") as file:
        file.write(response.content)
    print(f"✅ Archivo descargado y guardado en: {save_path}")
else:
    print(f"❌ Error al descargar el archivo. Código de estado: {response.status_code}")
