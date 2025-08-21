from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('resumen/', views.resumen, name='resumen'),
    path('data-collection/', views.data_collection, name='data_collection'),
    path('eda/', views.eda, name='eda'),
    path('data_wrangling/', views.data_wrangling, name='data_wrangling'),
    path('modeling/', views.modeling, name='modeling'),
]
