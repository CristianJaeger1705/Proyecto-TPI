from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from usuarios.models import Usuario
from django.shortcuts import redirect
from django.contrib import messages

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

#trabajo para el area de ususarios 
def gestionar_usuarios(request):
    usuarios = Usuario.objects.all().order_by('-fecha_registro')
    return render(request, 'administracion/usuarios.html', {
        'usuarios': usuarios
    })
#activa al usuario
def activar_usuario(request, user_id):
    usuario = Usuario.objects.get(id=user_id)
    usuario.is_active = True
    usuario.save()
    messages.success(request, "Usuario activado correctamente.")
    return redirect('gestionar_usuarios')

#desactiva al usuario
def desactivar_usuario(request, user_id):
    usuario = Usuario.objects.get(id=user_id)
    usuario.is_active = False
    usuario.save()
    messages.error(request, "Usuario desactivado.")
    return redirect('gestionar_usuarios')

#verifica al usuario
def verificar_usuario(request, user_id):
    usuario = Usuario.objects.get(id=user_id)
    usuario.verificado = True
    usuario.save()
    messages.success(request, "Usuario marcado como verificado.")
    return redirect('gestionar_usuarios')