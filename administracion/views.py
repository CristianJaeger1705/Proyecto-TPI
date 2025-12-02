from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import user_passes_test
from usuarios.models import Usuario
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import UsuarioAdminForm
from ofertas.models import OfertaLaboral
from django.shortcuts import render, get_object_or_404, redirect
from postulaciones.models import Postulacion
from django.contrib import messages
from .forms import UsuarioAdminForm
from django.db.models import Q
from django.core.paginator import Paginator





# Solo permite acceso a usuarios administradores
def es_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(es_admin)
def panel_admin(request):
    total_ofertas = OfertaLaboral.objects.count()
    total_usuarios = Usuario.objects.count()
    total_postulaciones = Postulacion.objects.count()


    return render(request, 'administracion/panel_admin.html',{
    'total_usuarios': total_usuarios,
    'total_ofertas': total_ofertas,
    'total postulaciones': total_postulaciones,})

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
def seleccionar_tipo_usuario(request):
    return render(request, 'administracion/usuarios/seleccionar_tipo.html')

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
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == "POST":
        form = UsuarioAdminForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect("lista_usuarios")
    else:
        form = UsuarioAdminForm(instance=usuario)

    return render(request, "administracion/usuarios/usuario_forms.html", {"form": form})

# --- Eliminar usuario ---
@login_required
@user_passes_test(es_admin)
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    usuario.delete()

    messages.success(request, "Usuario eliminado correctamente.")

    return redirect('lista_usuarios')


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
#crear usuario
def crear_usuario(request):
    if request.method == "POST":
        form = UsuarioAdminForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password("123456")  
            usuario.save()

            messages.success(request, "Usuario creado exitosamente.")
            return redirect("usuarios_admin")
    else:
        form = UsuarioAdminForm()

    return render(request, "administracion/usuarios/usuario_forms.html", {"form": form})

#desactivar verificacion 
@login_required
def quitar_verificacion_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.verificado = False
    usuario.save()
    messages.success(request, f"Se ha quitado la verificación del usuario {usuario.username}.")
    return redirect('lista_usuarios')

#trabajo del area de ofertas

#lista de ofertas
@login_required
def admin_listar_ofertas(request):
    ofertas = OfertaLaboral.objects.all().order_by('-fecha_publicacion')
    total_ofertas = ofertas.count()
    paginator = Paginator(ofertas, 10)  # 10 ofertas por página
    page_number = request.GET.get('page')

    return render(request, "administracion/ofertas_admin.html", {
        "ofertas": ofertas,
        "total_ofertas": total_ofertas
    })
#ver oferta 
@login_required
def admin_ver_oferta(request, id):
    oferta = get_object_or_404(OfertaLaboral, id=id)
    return render(request, 'administracion/ofertas/oferta_detalle.html', {
        'oferta': oferta
    })
#activar oferta 
@login_required
def admin_activar_oferta(request, id):
    oferta = get_object_or_404(OfertaLaboral, id=id)
    oferta.estado = "activa"     
    oferta.save()
    messages.success(request, f"La oferta '{oferta.titulo}' ha sido activada.")
    return redirect("ofertas_admin")

#desactivar oferta 
@login_required
def admin_desactivar_oferta(request, id):
    oferta = get_object_or_404(OfertaLaboral, id=id)
    oferta.estado = "inactiva"   # usa el valor correcto según tu modelo
    oferta.save()
    messages.warning(request, f"La oferta '{oferta.titulo}' ha sido desactivada.")
    return redirect("ofertas_admin")
#eliminar ofertas 
@login_required
def admin_eliminar_oferta(request, id):
    oferta = get_object_or_404(OfertaLaboral, id=id)
    oferta.delete()
    messages.error(request, "Oferta eliminada correctamente.")
    return redirect("ofertas_admin")
#detalle de oferta 
def admin_detalle_oferta(request, id):
    oferta = get_object_or_404(OfertaLaboral, id=id)

    return render(request, "administracion/ofertas_detalle_admin.html", {
        "oferta": oferta
    })
                          
#trabajo con postulaciones 
@login_required
def postulaciones_admin(request):
    postulaciones = Postulacion.objects.select_related("candidato__usuario", "oferta").order_by("-fecha_postulacion")

    return render(request, "administracion/postulaciones_admin.html", {
        "postulaciones": postulaciones
    })
#detalles 
@login_required
def postulacion_detalle(request, id):
    p = get_object_or_404(Postulacion, id=id)

    return render(request, "administracion/postulacion_detalle.html", {
        "postulacion": p
    })
#eliminar postulacion 
@login_required
def eliminar_postulacion(request, id):
    p = get_object_or_404(Postulacion, id=id)
    p.delete()
    return redirect("postulaciones_admin")


