# spacexdash/views.py
import os, json
from django.shortcuts import render
from django.conf import settings
from .metrics import load_metrics

CSV_PATH = os.path.join(settings.BASE_DIR, "data", "processed", "spacex_launches_clean_past.csv")

def dashboard(request):
    data = load_metrics(CSV_PATH)  # <- misma lógica que usarás en el notebook si quieres
    context = {k: json.dumps(v) for k, v in data.items()}
    return render(request, "spacexdash/dashboard.html", context)
