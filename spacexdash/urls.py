from django.urls import path
from .views import dashboard, launch_sites_map, dashboard_dash

urlpatterns = [
    path("dashboard/", dashboard, name="spacex_dashboard"),
    path("map/", launch_sites_map, name="launch-sites-map"),
    path("dashboard-dash/", dashboard_dash, name="spacex_dashboard_dash"),
]
