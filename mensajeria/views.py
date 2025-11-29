from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.contrib.auth import get_user_model

from usuarios.models import Usuario
from ofertas.models import OfertaLaboral
from .models import Conversacion, Mensaje, Notificacion, GrupoConversacion, MensajeGrupo

User = get_user_model()


# ============================================================
#     PANEL COMPLETO DE CHAT — SOLO EMPRESAS
# ============================================================
@login_required
def lista_conversaciones(request):

    # 🚫 CANDIDATOS NO ENTRAN AQUÍ
    if request.user.rol == "candidato":
        return HttpResponseForbidden("No tienes permiso para acceder a esta área.")

    usuario = request.user

    # ----------------------------------------
    # SOLO EMPRESAS → ver postulantes propios
    # ----------------------------------------
    empresa = usuario.perfilempresa

    # Filtrar candidatos que postularon a ofertas de esta empresa
    usuarios_filtrados = Usuario.objects.filter(
        perfilcandidato__postulacion__oferta__empresa=empresa
    ).distinct()

    # Excluir al usuario actual
    usuarios_filtrados = usuarios_filtrados.exclude(id=usuario.id)

    # Conversaciones 1 a 1
    conversaciones = Conversacion.objects.filter(
        participantes=usuario
    ).distinct()

    # Conversaciones grupales de la empresa
    grupos = GrupoConversacion.objects.filter(
        empresa=usuario
    ).distinct()

    return render(request, 'mensajeria/chat_lista.html', {
        'conversaciones': conversaciones,
        'usuarios': usuarios_filtrados,  # ← YA FILTRADOS
        'grupos': grupos
    })


# ============================================================
#     CHAT INDIVIDUAL USADO POR CANDIDATO O EMPRESA
# ============================================================
@login_required
def chat_con_usuario(request, username):

    otro_usuario = get_object_or_404(Usuario, username=username)

    # Obtiene conversación privada de exactamente 2 usuarios
    conversacion = (
        Conversacion.objects
        .annotate(num=Count("participantes"))
        .filter(num=2, participantes=request.user)
        .filter(participantes=otro_usuario)
        .first()
    )

    if not conversacion:
        conversacion = Conversacion.objects.create()
        conversacion.participantes.add(request.user, otro_usuario)

    return render(request, "mensajeria/chat_room.html", {
        "otro_usuario": otro_usuario,
        "conversacion": conversacion,
    })


# ============================================================
#     AJAX ENVIAR MENSAJE PRIVADO
# ============================================================
@login_required
def ajax_enviar_mensaje(request, convo_id):

    if request.method != "POST":
        return JsonResponse({"status": "error", "msg": "Método no permitido"})

    texto = request.POST.get("texto", "").strip()
    if not texto:
        return JsonResponse({"status": "error", "msg": "Mensaje vacío"})

    conversacion = get_object_or_404(Conversacion, id=convo_id)

    destinatario = conversacion.participantes.exclude(id=request.user.id).first()

    if not destinatario:
        return JsonResponse({"status": "error", "msg": "Destinatario no encontrado"})

    mensaje = Mensaje.objects.create(
        conversacion=conversacion,
        remitente=request.user,
        destinatario=destinatario,
        texto=texto,
        fecha_envio=timezone.now()
    )

    return JsonResponse({
        "status": "ok",
        "mensaje": {
            "id": mensaje.id,
            "texto": mensaje.texto,
            "remitente": mensaje.remitente.username,
            "fecha": mensaje.fecha_envio.isoformat()
        }
    })


# ============================================================
#     AJAX OBTENER MENSAJES
# ============================================================
@login_required
def obtener_mensajes_ajax(request, convo_id):

    conversacion = get_object_or_404(Conversacion, id=convo_id)
    mensajes = conversacion.mensajes.order_by("fecha_envio")

    data = [{
        "id": m.id,
        "texto": m.texto,
        "remitente": m.remitente.username,
        "fecha": timezone.localtime(m.fecha_envio).isoformat()
    } for m in mensajes]

    return JsonResponse({"mensajes": data})


# ============================================================
#     NOTIFICACIONES
# ============================================================
@login_required
def obtener_notificaciones_ajax(request):

    notificaciones = Notificacion.obtener_no_leidas(request.user)

    data = [{
        "id": n.id,
        "tipo": n.tipo,
        "mensaje": n.mensaje,
        "fecha": timezone.localtime(n.fecha).strftime("%Y-%m-%d %H:%M:%S")
    } for n in notificaciones]

    return JsonResponse({"notificaciones": data})


@login_required
@csrf_exempt
def marcar_notificacion_leida(request, notif_id):

    notif = get_object_or_404(Notificacion, id=notif_id, usuario=request.user)
    notif.leida = True
    notif.save()

    return JsonResponse({"status": "ok"})


# ============================================================
#     CREACIÓN DE GRUPOS — SOLO EMPRESA
# ============================================================
@login_required
def crear_grupo(request):

    if request.user.rol != "empresa":
        return HttpResponseForbidden("Solo empresas pueden crear grupos.")

    postulantes = Usuario.objects.filter(rol="candidato")

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        seleccionados = request.POST.getlist("postulantes")

        if not seleccionados:
            messages.error(request, "Debes seleccionar al menos un postulante.")
            return redirect("mensajeria:crear_grupo")

        grupo = GrupoConversacion.objects.create(
            nombre=nombre,
            empresa=request.user
        )

        grupo.postulantes.add(*seleccionados)

        messages.success(request, "Grupo creado correctamente.")
        return redirect("mensajeria:lista_conversaciones")

    return render(request, "mensajeria/crear_grupo.html", {
        "postulantes": postulantes
    })


# ============================================================
#     CHAT DE GRUPO
# ============================================================
@login_required
def chat_grupo(request, grupo_id):

    grupo = get_object_or_404(GrupoConversacion, id=grupo_id)

    if request.user != grupo.empresa and request.user not in grupo.postulantes.all():
        return HttpResponseForbidden("No tienes acceso.")

    mensajes = MensajeGrupo.objects.filter(grupo=grupo).order_by("fecha_envio")

    if request.method == "POST":
        texto = request.POST.get("texto", "").strip()
        if texto:
            MensajeGrupo.objects.create(
                grupo=grupo,
                remitente=request.user,
                texto=texto
            )
            return redirect("mensajeria:chat_grupo", grupo_id=grupo.id)

    return render(request, "mensajeria/chat_grupo.html", {
        "grupo": grupo,
        "mensajes": mensajes,
        "miembros": grupo.postulantes.all(),
    })


# ============================================================
#     CONTACTAR EMPRESA DESDE UNA OFERTA
#     (PARA CANDIDATOS)
# ============================================================
@login_required
def contactar_empresa(request, oferta_id):

    oferta = get_object_or_404(OfertaLaboral, id=oferta_id)

    candidato = request.user
    empresa = oferta.empresa

    if candidato.rol != "candidato":
        return HttpResponseForbidden("Solo los candidatos pueden usar este chat directo.")

    # Crear o recuperar conversación
    conversacion = Conversacion.objects.get_or_create_individual(
        candidato, empresa
    )

    return redirect("mensajeria:chat_con_usuario", username=empresa.username)


@login_required
def ajax_enviar_mensaje_grupo(request, grupo_id):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    texto = request.POST.get("texto", "").strip()
    if not texto:
        return JsonResponse({"error": "Mensaje vacío"}, status=400)

    grupo = get_object_or_404(GrupoConversacion, id=grupo_id)

    # Verificación de permisos
    if request.user != grupo.empresa and request.user not in grupo.postulantes.all():
        return JsonResponse({"error": "No tienes acceso al grupo"}, status=403)

    mensaje = MensajeGrupo.objects.create(
        grupo=grupo,
        remitente=request.user,
        texto=texto,
    )

    return JsonResponse({
        "id": mensaje.id,
        "remitente": mensaje.remitente.username,
        "texto": mensaje.texto,
        "fecha": mensaje.fecha_envio.isoformat()
    })
@login_required
def ajax_mensajes_grupo(request, grupo_id):
    grupo = get_object_or_404(GrupoConversacion, id=grupo_id)

    if request.user != grupo.empresa and request.user not in grupo.postulantes.all():
        return JsonResponse({"error": "No tienes acceso"}, status=403)

    mensajes = MensajeGrupo.objects.filter(grupo=grupo).order_by("fecha_envio")

    data = [{
        "id": m.id,
        "remitente": m.remitente.username,
        "texto": m.texto,
        "fecha": m.fecha_envio.isoformat(),
    } for m in mensajes]

    return JsonResponse({"mensajes": data})

@login_required
def eliminar_grupo(request, grupo_id):
    grupo = get_object_or_404(GrupoConversacion, id=grupo_id)

    if request.user != grupo.empresa:
        return HttpResponseForbidden("No puedes eliminar este grupo.")

    grupo.delete()

    messages.success(request, "Grupo eliminado correctamente.")
    return redirect("mensajeria:lista_conversaciones")
@login_required
def api_nuevas(request):
    nuevas = Notificacion.obtener_no_leidas(request.user)

    data = [{
        "id": n.id,
        "tipo": n.tipo,
        "mensaje": n.mensaje,
        "fecha": n.fecha.isoformat()
    } for n in nuevas]

    return JsonResponse({"nuevas": data})
