from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from usuarios.models import SolicitudEmpresa
from aplicaciones.decorators import solo_admin
from usuarios.models import Review

def hola_mundo(request):
    return render(request, 'hola_mundo.html')


def dashboard_empresa(request):
    return render(request, 'dashboard_empresa.html')

@solo_admin
def dashboard_admin(request):
    if request.user.rol != "admin":
        return redirect("/")

    reseñas = Review.objects.all().order_by("-fecha")

    return render(request, "dashboard_admin.html", {
        "reseñas": reseñas
    })
#def dashboard_admin(request):
#   return render(request, 'dashboard_admin.html')

@solo_admin
def listar_solicitudes(request):
    solicitudes = SolicitudEmpresa.objects.filter(estado="pendiente")
    return render(request, "solicitudes.html", {"solicitudes": solicitudes})

@solo_admin
def historial_solicitudes(request):
    historial = SolicitudEmpresa.objects.exclude(estado="pendiente")
    return render(request, "historial _solicitudes_admin.html", {"historial": historial})

@solo_admin
def ver_solicitud(request, id):
    solicitud = get_object_or_404(SolicitudEmpresa, id=id)
    return render(request, "detalle_solicitud_empresa.html", {"solicitud": solicitud})

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


    return redirect("listar_solicitudes")

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
    return redirect("listar_solicitudes")

