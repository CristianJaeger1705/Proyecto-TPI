from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import user_passes_test
from usuarios.models import Usuario
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UsuarioAdminForm


# Solo permite acceso a usuarios administradores
def es_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(es_admin)
def panel_admin(request):
    return render(request, 'administracion/panel_admin.html')
@user_passes_test(es_admin)
def dashboard(request):
    return render(request, 'dashboard.html')
@user_passes_test(es_admin)
def admin_usuarios(request):
    return render(request, 'administracion/usuarios_admin.html')
@user_passes_test(es_admin)
def admin_empresas(request):
    return render(request, 'administracion/empresas_admin.html')
@user_passes_test(es_admin)
def admin_ofertas(request):
    return render(request, 'administracion/ofertas_admin.html')
@user_passes_test(es_admin)
def admin_postulaciones(request):
    return render(request, 'administracion/postulaciones_admin.html')

#trabajo para el area de ususarios 

# --- Lista de usuarios ---
def lista_usuarios(request):
    usuarios = Usuario.objects.all().order_by('-id')  # MOSTRAR TODOS
    return render(request, 'usuarios_admin.html', {'usuarios': usuarios })
# --- Detalle de usuario ---
@login_required
@user_passes_test(es_admin)
def usuario_detalle(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    return render(request, "administracion/usuario_detalle.html", {"usuario": usuario})

# --- Editar usuario ---
@login_required
@user_passes_test(es_admin)
def usuario_editar(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == "POST":
        form = UsuarioEditarForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect("lista_usuarios")
    else:
        form = UsuarioEditarForm(instance=usuario)

    return render(request, "administracion/usuario_editar.html", {"form": form, "usuario": usuario})

# --- Eliminar usuario ---
@login_required
@user_passes_test(es_admin)
def usuario_eliminar(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == "POST":
        usuario.delete()
        return redirect("lista_usuarios")

    return render(request, "administracion/usuario_confirmar_eliminar.html", {"usuario": usuario})


def gestionar_usuarios(request):
    usuarios = Usuario.objects.all().order_by('-fecha_registro')
    return render(request, 'administracion/usuarios_admin.html', {
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

#crear al usuario 
def crear_usuario(request):
    if request.method == "POST":
        form = UsuarioAdminForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password("12345678")  # contraseña temporal
            usuario.verificado = True
            usuario.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioAdminForm()
    return render(request, 'administracion/usuarios/usuario_forms.html', {'form': form})