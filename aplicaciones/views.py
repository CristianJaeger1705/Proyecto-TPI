from django.shortcuts import render

from django.contrib.auth.decorators import login_required

def hola_mundo(request):
    return render(request, 'hola_mundo.html')

def dashboard_empresa(request):
    return render(request, 'dashboard_empresa.html')

def politicas(request):
    return render(request, 'privacidad.html')

def terminos(request):
    return render(request, 'terminos.html')

def preguntas(request):
    return render(request, 'preguntas.html')

def custom_404(request, exception):
    return render(request, "404.html", status=404)
