from django.shortcuts import render

def hola_mundo(request):
    return render(request, 'hola_mundo.html')

def dashboard_empresa(request):
    return render(request, 'dashboard_empresa.html')
