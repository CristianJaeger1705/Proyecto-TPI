from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from usuarios.models import SolicitudEmpresa,Usuario
from aplicaciones.decorators import solo_admin
from usuarios.models import Review
from aplicaciones.forms import UsuarioAdminForm
from django.contrib import messages
from django.urls import reverse

app_name = 'adminpanel'

@solo_admin
def dashboard_admin(request):
    if request.user.rol != "admin":
        return redirect("/")
    
    total_candidatos = Usuario.objects.filter(rol="candidato").count()
    total_empresas = Usuario.objects.filter(rol="empresa").count()
    total_solicitudes = SolicitudEmpresa.objects.filter(estado="pendiente").count()

    reseñas = Review.objects.all().order_by("-fecha")

    return render(request, "admin/dashboard_admin.html", {
        "reseñas": reseñas,
        'total_solicitudes' : total_solicitudes,
        'total_candidatos': total_candidatos,
        'total_empresas': total_empresas
    })
#def dashboard_admin(request):
#   return render(request, 'dashboard_admin.html')


#---------------------------------------------------------------------
#               SOLICITUDES
#--------------------------------------------------------------------
@solo_admin
def listar_solicitudes(request):
    solicitudes = SolicitudEmpresa.objects.filter(estado="pendiente")
    return render(request, "admin/solicitudes.html", {"solicitudes": solicitudes})

@solo_admin
def historial_solicitudes(request):
    historial = SolicitudEmpresa.objects.exclude(estado="pendiente")
    return render(request, "admin/historial _solicitudes_admin.html", {"historial": historial})

@solo_admin
def ver_solicitud(request, id):
    solicitud = get_object_or_404(SolicitudEmpresa, id=id)
    return render(request, "admin/detalle_solicitud_empresa.html", {"solicitud": solicitud})

@solo_admin
def aprobar_solicitud(request, id):
    solicitud = get_object_or_404(SolicitudEmpresa, id=id)
    solicitud.estado = "aprobada"
    solicitud.save()

    link = f"https://laburosv.com/usuarios/registrar_empresa/{solicitud.token}/"

    send_mail(
        subject="Solicitud aprobada - Crear cuenta",
        message=f"Su solicitud fue aprobada. Cree su cuenta aquí: {link}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[solicitud.correo],
    )


    return redirect("adminpanel:listar_solicitudes")

@solo_admin
def rechazar_solicitud(request, id):
    solicitud = get_object_or_404(SolicitudEmpresa, id=id)
    send_mail(
        subject="Solicitud rechazada",
         message="Lamentamos informarle que su solicitud ha sido rechazada.",
         from_email=settings.DEFAULT_FROM_EMAIL,
         recipient_list=[solicitud.correo],
    )
    solicitud.estado = "rechazada"
    solicitud.save()
    return redirect("adminpanel:listar_solicitudes")


#---------------------------------------------------------------------
#               USUARIOS
#--------------------------------------------------------------------
@solo_admin
def listar_candidatos(request):
    usuarios = Usuario.objects.filter(rol="candidato").order_by('id')
    return render(request, "admin/usuarios/lista_candidatos.html", {"usuarios": usuarios})

@solo_admin
def listar_empresas(request):
    usuarios = Usuario.objects.filter(rol="empresa").order_by('id')
    return render(request, "admin/usuarios/lista_empresas.html", {"usuarios": usuarios})

@solo_admin
def usuario_detalle(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    # Detectar a dónde debe regresar el botón "Volver"
    if usuario.rol == "candidato":
        volver_url = reverse("adminpanel:listar_candidatos")
    elif usuario.rol == "empresa":
        volver_url = reverse("adminpanel:listar_empresas")
    else:
        volver_url = reverse("adminpanel:dashboard_admin")  # fallback

    contexto = {
        "usuario": usuario,
        "volver_url": volver_url
    }

    return render(request, "admin/usuarios/usuario_detalle.html", contexto)


# --- Activar usuario ---
@solo_admin
def activar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    usuario.is_active = True
    usuario.save()
    messages.success(request, "Usuario activado correctamente.")

    next_url = request.GET.get("next")
    return redirect(next_url) if next_url else redirect("adminpanel:dashboard_admin")


# --- Desactivar usuario ---
@solo_admin
def desactivar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    usuario.is_active = False
    usuario.save()
    messages.error(request, "Usuario desactivado.")

    next_url = request.GET.get("next")
    return redirect(next_url) if next_url else redirect("adminpanel:dashboard_admin")


# --- Verificar usuario ---
@solo_admin
def verificar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    usuario.verificado = True
    usuario.save()
    messages.success(request, "Usuario marcado como verificado.")

    next_url = request.GET.get("next")
    return redirect(next_url) if next_url else redirect("adminpanel:dashboard_admin")


# --- Quitar verificación ---
@solo_admin
def quitar_verificacion_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.verificado = False
    usuario.save()
    messages.info(request, f"Se quitó la verificación del usuario {usuario.username}.")

    next_url = request.GET.get("next")
    return redirect(next_url) if next_url else redirect("adminpanel:dashboard_admin")


# --- Crear usuario ---
@solo_admin
def crear_usuario(request):
    if request.method == "POST":
        form = UsuarioAdminForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password("123456")  
            usuario.save()

            messages.success(request, "Usuario creado exitosamente.")

            next_url = request.GET.get("next")
            return redirect(next_url) if next_url else redirect("adminpanel:dashboard_admin")
    else:
        form = UsuarioAdminForm()

    return render(request, "admin/usuarios/usuario_forms.html", {"form": form})