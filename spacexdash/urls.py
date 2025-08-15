from django.urls import path
from .views import dashboard,launch_sites_map

urlpatterns = [
    path("dashboard/", dashboard, name="spacex_dashboard"),
    path("map/", launch_sites_map, name="launch-sites-map"),

]
