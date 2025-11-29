# postulaciones/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import redirect, render, get_object_or_404

from ofertas.models import OfertaLaboral
from perfiles.models import PerfilCandidato, PerfilEmpresa
from postulaciones.models import Postulacion
from mensajeria.models import GrupoConversacion


# ------------------------------------------
# 1) POSTULAR → crea grupo si no existe
# ------------------------------------------
@login_required
def postular(request, oferta_id):
    oferta = get_object_or_404(OfertaLaboral, id=oferta_id)
    usuario = request.user

    # Validar rol
    if usuario.rol != "candidato":
        messages.error(request, "Solo los candidatos pueden postularse.")
        return redirect("ofertas:ofertas")

    perfil_candidato = PerfilCandidato.objects.filter(usuario=usuario).first()
    if not perfil_candidato:
        messages.error(request, "Debes crear tu perfil de candidato antes de postularte.")
        return redirect("perfiles:perfil_candidato")

    # Crear postulación
    Postulacion.objects.get_or_create(candidato=perfil_candidato, oferta=oferta)

    empresa_usuario = oferta.empresa.usuario

    # Crear o buscar grupo
    grupo, creado = GrupoConversacion.objects.get_or_create(
        oferta=oferta,
        defaults={
            "empresa": empresa_usuario,
            "nombre": f"Chat - {oferta.titulo}"
        }
    )

    # Asegurar que empresa está dentro del grupo
    if empresa_usuario not in grupo.postulantes.all():
        grupo.postulantes.add(empresa_usuario)

    # Asegurar que candidato está dentro del grupo
    if usuario not in grupo.postulantes.all():
        grupo.postulantes.add(usuario)

    messages.success(request, "Postulación realizada. Chat con la empresa disponible.")
    return redirect("mensajeria:chat_grupo", grupo_id=grupo.id)


# ------------------------------------------
# 2) VERSIÓN VIEJA (mantener para compatibilidad)
# ------------------------------------------
@login_required
def postular_con_id(request, id):
    oferta = get_object_or_404(OfertaLaboral, id=id)
    usuario = request.user

    if usuario.rol != "candidato":
        messages.error(request, "Solo los candidatos pueden postularse.")
        return redirect("ofertas:ofertas")

    perfil = PerfilCandidato.objects.filter(usuario=usuario).first()

    try:
        Postulacion.objects.create(oferta=oferta, candidato=perfil)
        messages.success(request, "Postulación creada.")
    except IntegrityError:
        messages.error(request, "Ya estás postulado a esta oferta.")

    return redirect("ofertas:ofertas")


# ------------------------------------------
# 3) CANCELAR POSTULACIÓN
# ------------------------------------------
@login_required
def cancelar_postulacion(request, id):
    usuario = request.user
    oferta = get_object_or_404(OfertaLaboral, id=id)

    perfil = PerfilCandidato.objects.filter(usuario=usuario).first()

    try:
        Postulacion.objects.get(oferta=oferta, candidato=perfil).delete()
        messages.success(request, "Postulación cancelada.")
    except Postulacion.DoesNotExist:
        messages.error(request, "No estabas postulado a esta oferta.")

    return redirect("ofertas:ofertas")


# ------------------------------------------
# 4) ACTUALIZAR POSTULACIÓN (solo empresa)
# ------------------------------------------
@login_required
def actualizar_postulacion(request, id):
    if request.method != "POST":
        return redirect("ofertas:ofertas")

    postulacion = get_object_or_404(Postulacion, id=id)

    usuario = request.user
    if usuario.rol != "empresa":
        messages.error(request, "No tienes permisos para esto.")
        return redirect("ofertas:ofertas")

    perfil_empresa = PerfilEmpresa.objects.filter(usuario=usuario).first()
    if postulacion.oferta.empresa != perfil_empresa:
        messages.error(request, "Esta postulación no pertenece a tu empresa.")
        return redirect("ofertas:ofertas")

    nuevo_estado = request.POST.get("estado")
    if nuevo_estado not in dict(Postulacion.ESTADOS):
        messages.error(request, "Estado inválido.")
        return redirect("ofertas:ofertas")

    postulacion.estado = nuevo_estado
    postulacion.save()

    messages.success(request, "Postulación actualizada.")
    return redirect("ofertas:ofertas")


# ------------------------------------------
# 5) SELECCIONAR PERFIL ANTES DE POSTULARSE
# ------------------------------------------
@login_required
def seleccionar_perfil(request, oferta_id):
    usuario = request.user

    if usuario.rol != "candidato":
        messages.error(request, "Solo los candidatos pueden postularse.")
        return redirect("ofertas:ofertas")

    perfiles = PerfilCandidato.objects.filter(usuario=usuario)  # <-- LISTA, no first()

    oferta = get_object_or_404(OfertaLaboral, id=oferta_id)

    return render(request, "seleccionar_perfil.html", {
        "perfiles": perfiles,   # <-- enviar la lista
        "oferta": oferta
    })
