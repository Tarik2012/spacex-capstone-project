from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def resumen(request):
    return render(request, 'core/resumen.html')

def data_collection(request):
    return render(request, 'core/data_collection.html')

def eda(request):
    return render(request, 'core/eda.html')


