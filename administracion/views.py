from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

# Solo permite acceso a usuarios administradores
def es_admin(user):
    return user.is_staff or user.is_superuser

@user_passes_test(es_admin)
def panel_admin(request):
    return render(request, 'panel_admin.html')
@user_passes_test(es_admin)
def dashboard(request):
    return render(request, 'dashboard.html')
@user_passes_test(es_admin)
def admin_usuarios(request):
    return render(request, 'admin_usuarios.html')
@user_passes_test(es_admin)
def admin_empresas(request):
    return render(request, 'admin_empresas.html')
@user_passes_test(es_admin)
def admin_ofertas(request):
    return render(request, 'admin_ofertas.html')
@user_passes_test(es_admin)
def admin_postulaciones(request):
    return render(request, 'admin_postulaciones.html')