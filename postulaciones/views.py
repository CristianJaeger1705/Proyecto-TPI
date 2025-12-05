from django.contrib import messages
from django.contrib.auth.views import login_required
from django.db import IntegrityError
from django.shortcuts import redirect, render
from ofertas.models import OfertaLaboral
from perfiles.models import PerfilCandidato, PerfilEmpresa
from postulaciones.models import Postulacion

def postular_con_id(request, id):
    try:
        id = int(id)
    except ValueError:
        messages.error(request, "ID de vacante inválido.")
        return redirect("usuarios:redirigir")

    oferta = None
    try:
        oferta = OfertaLaboral.objects.get(id=id)
    except OfertaLaboral.DoesNotExist:
        oferta = None

    if oferta is None:
        messages.error(request, "La vacante no existe.")
        return redirect("usuarios:redirigir")

    user = request.user

    if not user.is_authenticated:
        return redirect("usuarios:redirigir")

    if user.rol != "candidato":
        messages.error(request, "Solo los candidatos pueden postularse a vacantes.")
        return redirect("usuarios:redirigir")

    perfil = PerfilCandidato.objects.filter(usuario_id=user.id).first()

    if perfil is None:
        messages.error(request, "No se encontró el perfil de candidato.")
        return redirect("usuarios:redirigir")

    try:
        Postulacion.objects.create(
            oferta=oferta,
            candidato=perfil,
            fecha_postulacion=None,
            estado="pendiente"
        )
    except IntegrityError:
        messages.error(request, "Postulación ya existente.")
        return redirect("usuarios:redirigir")
    except:
        messages.error(request, "Error al crear la postulación.")
        return redirect("usuarios:redirigir")

    messages.success(request, "Postulación creada exitosamente.")
    return redirect("ofertas:detalleoferta", oferta_id=oferta.id)

def cancelar_postulacion(request, id):
    try:
        id = int(id)
    except ValueError:
        messages.error(request, "ID de vacante inválido.")
        return redirect("usuarios:redirigir")

    oferta = None
    try:
        oferta = OfertaLaboral.objects.get(id=id)
    except OfertaLaboral.DoesNotExist:
        oferta = None

    if oferta is None:
        messages.error(request, "La vacante no existe.")
        return redirect("usuarios:redirigir")

    user = request.user

    if not user.is_authenticated:
        return redirect("usuarios:redirigir")

    if user.rol != "candidato":
        messages.error(request, "Solo los candidatos pueden postularse a vacantes.")
        return redirect("usuarios:redirigir")

    perfil = PerfilCandidato.objects.filter(usuario_id=user.id).first()

    if perfil is None:
        messages.error(request, "No se encontró el perfil de candidato.")
        return redirect("usuarios:redirigir")

    try:
        postulacion = Postulacion.objects.get(oferta=oferta, candidato=perfil)
        postulacion.delete()
    except Postulacion.DoesNotExist:
        messages.error(request, "No se encontró la postulación.")
        return redirect("usuarios:redirigir")
    except:
        messages.error(request, "Error al eliminar la postulación.")
        return redirect("usuarios:redirigir")

    messages.success(request, "Postulación cancelada exitosamente.")
    return redirect("ofertas:detalleoferta", oferta_id=oferta.id)

def obtener_postulantes_de_oferta(request, oferta_id):
    try:
        oferta_id = int(oferta_id)
    except ValueError:
        return None

    empresa = None
    if not request.user.is_authenticated or request.user.rol != "empresa":
        return None

    empresa = PerfilEmpresa.objects.filter(usuario_id=request.user.id).first()
    if empresa is None:
        return None

    oferta = None
    try:
        oferta = OfertaLaboral.objects.get(id=oferta_id, empresa=empresa)
    except OfertaLaboral.DoesNotExist:
        oferta = None

    if oferta is None:
        return None

    postulaciones = Postulacion.objects.filter(oferta=oferta).select_related('candidato__usuario')

    return postulaciones;


@login_required
def actualizar_postulacion(request, id):
    if (request.method != "POST"):
        return redirect("usuarios:redirigir")

    try:
        id = int(id)
    except ValueError:
        messages.error(request, "ID de postulación inválido.")
        return redirect("usuarios:redirigir")

    postulacion = None
    try:
        postulacion = Postulacion.objects.get(id=id)
    except Postulacion.DoesNotExist:
        postulacion = None

    if postulacion is None:
        messages.error(request, "La postulación no existe.")
        return redirect("usuarios:redirigir")

    if postulacion.estado != "pendiente":
        messages.error(request, "Solo se pueden actualizar postulaciones pendientes.")
        return redirect("usuarios:redirigir")

    nuevo_estado = request.POST.get("estado", "").strip()

    if nuevo_estado not in dict(Postulacion.ESTADOS).keys() or nuevo_estado == "pendiente":
        messages.error(request, "Estado de postulación inválido.")
        return redirect("usuarios:redirigir")

    user = request.user

    if not user.is_authenticated:
        return redirect("usuarios:redirigir")

    if user.rol != "empresa":
        messages.error(request, "Solo las empresas pueden actualizar postulaciones.")
        return redirect("usuarios:redirigir")

    perfil = PerfilEmpresa.objects.filter(usuario_id=user.id).first()

    if perfil is None:
        messages.error(request, "No se encontró el perfil de la empresa.")
        return redirect("usuarios:redirigir")

    if postulacion.oferta.empresa != perfil:
        messages.error(request, "No tienes permiso para actualizar esta postulación.")
        return redirect("usuarios:redirigir")

    try:
        postulacion.estado = nuevo_estado
        postulacion.save()
    except:
        messages.error(request, "Error al actualizar la postulación.")
        return redirect("usuarios:redirigir")

    messages.success(request, "Postulación actualizada exitosamente.")
    return render(request, 'hola_mundo.html')
