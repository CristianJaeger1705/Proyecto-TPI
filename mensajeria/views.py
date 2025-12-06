from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from rest_framework import generics, permissions
from .models import Chat, Mensaje, Notificacion
from usuarios.models import Usuario
from django.db.models import Q
from ofertas.models import OfertaLaboral
from .serializers import ChatSerializer, MensajeSerializer, NotificacionSerializer
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from perfiles.models import PerfilEmpresa
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import escape
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
import bleach

ALLOWED_TAGS = ['b', 'i', 'u', 'a']
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'target', 'rel']
}


User = get_user_model()

from mensajeria.signals import crear_o_actualizar_grupo_general


  # Función actualizada que evita duplicados


# =========================
# API REST para Chats
# =========================
class ChatListView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.rol == 'empresa':
            return Chat.objects.filter(
                participantes__in=Usuario.objects.filter(
                    chats__oferta__empresa=self.request.user.perfil_empresa
                )
            ).distinct().order_by('-fecha_creacion')

        return self.request.user.chats.all().order_by('-fecha_creacion')


class MensajeListView(generics.ListAPIView):
    serializer_class = MensajeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        chat = get_object_or_404(Chat, id=chat_id)
        if self.request.user in chat.participantes.all():
            return chat.mensajes.all().order_by('fecha_envio')
        return Mensaje.objects.none()


class MensajeCreateView(generics.CreateAPIView):
    serializer_class = MensajeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(remitente=self.request.user)


class NotificacionListView(generics.ListAPIView):
    serializer_class = NotificacionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notificacion.objects.filter(
            usuario=self.request.user
        ).order_by('-fecha')


# =========================
# PANEL EMPRESA
# =========================
@login_required
def panel_empresa(request):
    if request.user.rol != 'empresa':
        return redirect('/')

    perfil_empresa = request.user.perfil_empresa

    # Chats individuales
    chats_individuales = Chat.objects.filter(
        es_grupal=False,
        participantes=request.user,
        oferta__empresa=perfil_empresa
    ).distinct().order_by('-fecha_creacion')

    for c in chats_individuales:
        c.mensajes_no_vistos_count = c.mensajes.exclude(leido_por=request.user).count()

    chats_nuevos = sum(1 for c in chats_individuales if c.mensajes_no_vistos_count > 0)

    # Chats grupales
    grupos = Chat.objects.filter(
        es_grupal=True
    ).filter(
        Q(oferta__empresa=perfil_empresa) | Q(participantes=request.user)
    ).distinct().order_by('-fecha_creacion')

    # Marcar si cada grupo tiene admin
    for g in grupos:
        g.mensajes_no_vistos_count = g.mensajes.exclude(leido_por=request.user).count()
        g.tiene_admin = g.participantes.filter(rol='admin').exists()

    # Notificaciones recientes
    notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-fecha')[:5]

    return render(request, 'mensajeria/panel_empresa.html', {
        'chats_individuales': chats_individuales,
        'grupos': grupos,
        'notificaciones': notificaciones,
        'chats_nuevos': chats_nuevos,
    })

# =========================
# LISTADO DE CHATS EMPRESA
# =========================
@login_required
def chats_empresa(request):
    if request.user.rol != 'empresa':
        return redirect('/')

    perfil_empresa = request.user.perfil_empresa

    chats = Chat.objects.filter(
        es_grupal=False,
        participantes=request.user,
        oferta__empresa=perfil_empresa
    ).distinct().order_by('-fecha_creacion')

    return render(request, 'mensajeria/chats_empresa.html', {'chats': chats})


# =========================
# CRUD DE GRUPOS
# =========================
class GrupoForm(forms.ModelForm):
    participantes = forms.ModelMultipleChoiceField(
        queryset=Usuario.objects.none(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Chat
        fields = ['nombre', 'participantes']


@login_required
def grupos_empresa(request):
    if request.user.rol != 'empresa':
        return redirect('/')

    perfil_empresa = request.user.perfil_empresa

    grupos = Chat.objects.filter(
        es_grupal=True,
        oferta__empresa=perfil_empresa
    ).order_by('-fecha_creacion')

    if request.method == 'POST':
        form = GrupoForm(request.POST)
        form.fields['participantes'].queryset = Usuario.objects.filter(
            rol='candidato',
            chats__oferta__empresa=perfil_empresa
        ).distinct()

        if form.is_valid():
            grupo = form.save(commit=False)
            grupo.es_grupal = True
            grupo.save()

            # Guardar participantes desde los checkboxes
            participantes_ids = request.POST.getlist('participantes')
            grupo.participantes.set(Usuario.objects.filter(id__in=participantes_ids))

            messages.success(request, "Grupo creado correctamente.")
            return redirect('mensajeria:grupos-empresa')
    else:
        form = GrupoForm()
        form.fields['participantes'].queryset = Usuario.objects.filter(
            rol='candidato',
            chats__oferta__empresa=perfil_empresa
        ).distinct()

    return render(request, 'mensajeria/grupos_empresa.html', {
        'grupos': grupos,
        'form': form
    })


@login_required
def editar_grupo(request, grupo_id):
    if request.user.rol != 'empresa':
        return redirect('/')

    grupo = get_object_or_404(Chat, id=grupo_id, es_grupal=True)
    perfil_empresa = request.user.perfil_empresa

    if request.method == 'POST':
        form = GrupoForm(request.POST, instance=grupo)
        form.fields['participantes'].queryset = Usuario.objects.filter(
            rol='candidato',
            chats__oferta__empresa=perfil_empresa
        ).distinct()
        if form.is_valid():
            form.save()
            messages.success(request, "Grupo actualizado correctamente.")
            return redirect('mensajeria:grupos-empresa')

    else:
        form = GrupoForm(instance=grupo)
        form.fields['participantes'].queryset = Usuario.objects.filter(
            rol='candidato',
            chats__oferta__empresa=perfil_empresa
        ).distinct()

    return render(request, 'mensajeria/editar_grupo.html', {
        'form': form,
        'grupo': grupo
    })


@login_required
def eliminar_grupo(request, grupo_id):
    if request.user.rol != 'empresa':
        return redirect('/')

    grupo = get_object_or_404(Chat, id=grupo_id, es_grupal=True)
    grupo.delete()
    messages.success(request, "Grupo eliminado correctamente.")
    return redirect('mensajeria:grupos-empresa')


# =========================
# NOTIFICACIONES EMPRESA
# =========================
@login_required
def notificaciones_empresa(request):
    if request.user.rol != 'empresa':
        return redirect('/')

    notificaciones = Notificacion.objects.filter(
        usuario=request.user
    ).order_by('-fecha')

    return render(request, 'mensajeria/notificaciones_empresa.html', {
        'notificaciones': notificaciones
    })


@login_required
def marcar_notificacion_leida(request, notif_id):
    # Solo marcar como leída si la notificación pertenece al usuario
    notif = get_object_or_404(Notificacion, id=notif_id, usuario=request.user)
    notif.leida = True
    notif.save()
    messages.success(request, "Notificación marcada como leída.")
    # Redirigir a la página anterior, o al panel del usuario
    return redirect(request.META.get('HTTP_REFERER', 'mensajeria:panel-admin'))

# =========================
# PANEL CANDIDATO
# =========================
@login_required
def panel_candidato(request):
    if request.user.rol != 'candidato':
        return redirect('/')
    return render(request, 'mensajeria/panel_candidato.html')


# =========================
# INICIAR CHAT
# =========================
@login_required
def iniciar_chat(request, oferta_id):
    oferta = get_object_or_404(OfertaLaboral, id=oferta_id)
    empresa = oferta.empresa.usuario

    chat = Chat.objects.filter(
        es_grupal=False,
        participantes=request.user
    ).filter(
        participantes=empresa
    ).first()

    if not chat:
        chat = Chat.objects.create(
            es_grupal=False,
            nombre=f'Chat con {empresa.username}',
            oferta=oferta
        )
        chat.participantes.add(request.user, empresa)
        chat.save()

    return redirect('mensajeria:chat-detalle', chat.id)

@login_required
def iniciar_chat_con_postulante(request, oferta_id, postulante_id):
    if request.user.rol != 'empresa':
        return redirect('/')

    oferta = get_object_or_404(OfertaLaboral, id=oferta_id, empresa=request.user.perfil_empresa)
    empresa = oferta.empresa.usuario
    postulante = get_object_or_404(Usuario, id=postulante_id, rol='candidato')

    chat = Chat.objects.filter(
        es_grupal=False,
        oferta=oferta,
        participantes=postulante
    ).filter(
        participantes=empresa
    ).first()

    if not chat:
        chat = Chat.objects.create(
            es_grupal=False,
            nombre=f'Chat con {empresa.username}',
            oferta=oferta
        )
        chat.participantes.add(postulante, empresa)
        chat.save()

    return redirect('mensajeria:chat-detalle', chat.id)


# =========================
# DETALLE DE CHAT
# =========================



@login_required
def chat_detalle(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if request.user not in chat.participantes.all():
        if request.user.rol == 'admin':
            return redirect('mensajeria:panel-admin')
        elif request.user.rol == 'empresa':
            return redirect('mensajeria:panel-empresa')
        else:
            return redirect('mensajeria:panel-candidato')

    panel_url = {
        'admin': 'mensajeria:panel-admin',
        'empresa': 'mensajeria:panel-empresa',
        'candidato': 'mensajeria:panel-candidato'
    }.get(request.user.rol, 'mensajeria:panel-empresa')

    if not chat.mensajes.filter(es_automatico=True).exists() and request.user.rol == 'candidato':
        remitente_auto = chat.participantes.exclude(id=request.user.id).first()
        if remitente_auto:
            Mensaje.objects.create(
                chat=chat,
                remitente=remitente_auto,
                texto="Muchas gracias por comunicarte y por tu interés, te responderemos lo más pronto posible.",
                es_automatico=True
            )

    if request.method == 'POST':
        texto = request.POST.get('mensaje', '').strip()
        if texto:
            # Limpiar el mensaje antes de guardarlo
            texto_limpio = bleach.clean(
                texto,
                tags=ALLOWED_TAGS,
                attributes=ALLOWED_ATTRIBUTES,
                strip=True
            )
            # Evitar enlaces maliciosos con javascript:
            texto_limpio = bleach.linkify(texto_limpio)

            Mensaje.objects.create(
                chat=chat,
                remitente=request.user,
                texto=texto_limpio,
                es_automatico=False
            )
            return redirect('mensajeria:chat-detalle', chat.id)

    mensajes = chat.mensajes.all().order_by('fecha_envio')
    for m in mensajes:
        if request.user not in m.leido_por.all():
            m.leido_por.add(request.user)

    return render(request, 'mensajeria/chat_detalle.html', {
        'chat': chat,
        'mensajes': mensajes,
        'panel_url': panel_url
    })


# =========================
# EDITAR CHAT
# =========================
@login_required
def editar_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if request.user not in chat.participantes.all():
        return redirect('mensajeria:panel-empresa')

    if request.method == "POST":
        nuevo_nombre = request.POST.get("nombre", "").strip()
        if nuevo_nombre:
            chat.nombre = nuevo_nombre
            chat.save()
        return redirect('mensajeria:panel-empresa')

    return render(request, "mensajeria/editar_chat.html", {"chat": chat})


# =========================
# ELIMINAR CHAT
# =========================
@login_required
def eliminar_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if request.user not in chat.participantes.all():
        return redirect('mensajeria:panel-empresa')

    if request.method == "POST":
        chat.delete()
        return redirect('mensajeria:panel-empresa')

    return render(request, "mensajeria/eliminar_chat_confirm.html", {"chat": chat})


# =========================
# PANEL ADMINISTRADOR
# =========================
@login_required
def panel_admin(request):
    if not (request.user.rol == 'admin' or request.user.is_superuser):
        messages.error(request, "No tienes permisos para acceder al panel de administrador.")
        return redirect('/')

    # Sincronizar grupo general
    crear_o_actualizar_grupo_general()


    # Chats individuales del admin
    chats_individuales = Chat.objects.filter(
        es_grupal=False,
        participantes=request.user
    ).distinct().order_by('-fecha_creacion')

    for c in chats_individuales:
        c.mensajes_no_vistos_count = c.mensajes.exclude(leido_por=request.user).count()

    # Chats grupales del admin (incluye el grupo general)
    grupos = Chat.objects.filter(
        es_grupal=True,
        participantes=request.user
    ).distinct().order_by('-fecha_creacion')

    for g in grupos:
        g.mensajes_no_vistos_count = g.mensajes.exclude(leido_por=request.user).count()

    # Últimas 10 empresas
    empresas_recientes = PerfilEmpresa.objects.select_related('usuario').order_by('-fecha_creacion')[:10]

    # Últimas 10 notificaciones del admin
    notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-fecha')[:10]

    return render(request, 'mensajeria/panel_admin.html', {
        'chats_individuales': chats_individuales,
        'grupos': grupos,
        'empresas_recientes': empresas_recientes,
        'notificaciones': notificaciones,
    })


@login_required
@require_GET
def actualizar_notificaciones_admin(request):
    if request.user.rol != 'admin':
        return JsonResponse({'error': 'No autorizado'}, status=403)

    chats = Chat.objects.filter(participantes=request.user).distinct()
    data = [
        {'id': chat.id, 'mensajes_no_vistos_count': chat.mensajes.exclude(leido_por=request.user).count()}
        for chat in chats
    ]
    return JsonResponse({'chats': data})


# =========================
# LISTA DE CHATS PARA EMPRESA Y ADMIN
# =========================
@login_required
def lista_chats_panel(request):
    user = request.user

    if user.rol == 'empresa':
        perfil_empresa = user.perfil_empresa
        chats = Chat.objects.filter(
            participantes=user
        ).filter(
            Q(es_grupal=False, oferta__empresa=perfil_empresa) | Q(es_grupal=True, oferta__empresa=perfil_empresa)
        ).distinct().order_by('-fecha_creacion')

    elif user.rol == 'admin' or user.is_superuser:
        chats = Chat.objects.filter(
            participantes=user
        ).distinct().order_by('-fecha_creacion')

    else:
        messages.error(request, "No tienes permiso para acceder a este panel.")
        return redirect('/')

    for c in chats:
        c.mensajes_no_vistos_count = c.mensajes.exclude(leido_por=user).count()

    return render(request, 'mensajeria/panel_chats.html', {'chats': chats})


# =========================
# MENSAJE AUTOMÁTICO
# =========================
@login_required
def enviar_mensaje_automatico(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if request.user not in chat.participantes.all():
        return redirect('mensajeria:panel-empresa')

    if not chat.mensajes.filter(es_automatico=True).exists():
        Mensaje.objects.create(
            chat=chat,
            remitente=chat.participantes.exclude(id=request.user.id).first(),
            texto="Muchas gracias por comunicarte y por tu interés, te responderemos lo más pronto posible.",
            es_automatico=True
        )

    return redirect('mensajeria:chat-detalle', chat.id)


# ============================================
# SEÑAL: Crear grupo automático y notificación
# ============================================
@receiver(post_save, sender=PerfilEmpresa)
def crear_grupo_y_notificacion(sender, instance, created, **kwargs):
    if created:
        admins = User.objects.filter(rol='admin')
        nombre_grupo = f"Grupo {instance.nombre_empresa}"
        if not Chat.objects.filter(nombre=nombre_grupo, es_grupal=True).exists():
            grupo = Chat.objects.create(nombre=nombre_grupo, es_grupal=True)
            grupo.participantes.add(instance.usuario, *admins)
            for admin in admins:
                Notificacion.objects.create(
                    tipo="Nuevo Grupo Automático",
                    mensaje=f"Se creó un grupo automático para la empresa '{instance.nombre_empresa}'.",
                    usuario=admin
                )

@login_required
def eliminar_notificacion(request, notif_id):
    """
    Elimina una notificación y redirige al panel correspondiente
    según el rol del usuario.
    """
    notif = get_object_or_404(Notificacion, id=notif_id, usuario=request.user)
    notif.delete()
    messages.success(request, "Notificación eliminada correctamente.")

    # Redirigir según rol
    if request.user.rol == 'empresa':
        return redirect('mensajeria:notificaciones-empresa')
    elif request.user.rol == 'admin':
        return redirect('mensajeria:panel-admin')
    else:
        # Por si hay otros roles
        return redirect('mensajeria:panel-candidato')
    
   
@login_required
@require_GET
def obtener_mensajes_no_vistos(request):
    # Todos los chats del usuario
    chats = request.user.chats.all().distinct()
    data = []
    for chat in chats:
        no_vistos = chat.mensajes.exclude(leido_por=request.user).count()
        data.append({
            'chat_id': chat.id,
            'mensajes_no_vistos_count': no_vistos
        })
        
    return JsonResponse({'chats': data})



@login_required
@require_GET
def chat_mensajes_ajax(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user not in chat.participantes.all():
        return JsonResponse({'error': 'No autorizado'}, status=403)

    mensajes = chat.mensajes.all().order_by('fecha_envio')
    for m in mensajes:
        if request.user not in m.leido_por.all():
            m.leido_por.add(request.user)

    html = render_to_string("mensajeria/_mensajes.html", {'mensajes': mensajes, 'request': request})
    return JsonResponse({'html': html})
