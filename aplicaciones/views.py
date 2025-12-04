from django.shortcuts import render

def hola_mundo(request):
    return render(request, 'admin/hola_mundo.html')

def dashboard_empresa(request):
    return render(request, 'admin/dashboard_empresa.html')

#def dashboard_admin(request):
#   return render(request, 'dashboard_admin.html')
