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

    # Chats individuales
    chats_individuales = Chat.objects.filter(
        es_grupal=False,
        participantes=request.user
    ).distinct()

    # Mensajes no vistos
    for c in chats_individuales:
        c.mensajes_no_vistos_count = c.mensajes.exclude(
            leido_por=request.user
        ).count()

    chats_nuevos = sum(
        1 for c in chats_individuales if c.mensajes_no_vistos_count > 0
    )

    perfil_empresa = request.user.perfil_empresa

    grupos = Chat.objects.filter(
        es_grupal=True
    ).filter(
        Q(oferta__empresa=perfil_empresa) | Q(participantes=request.user)
    ).distinct().order_by('-fecha_creacion')

    for g in grupos:
        g.mensajes_no_vistos_count = g.mensajes.exclude(
            leido_por=request.user
        ).count()

    notificaciones = Notificacion.objects.filter(
        usuario=request.user
    ).order_by('-fecha')[:5]

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

    form = GrupoForm()
    form.fields['participantes'].queryset = Usuario.objects.filter(
        rol='candidato',
        chats__oferta__empresa=perfil_empresa
    ).distinct()

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
            form.save_m2m()
            messages.success(request, "Grupo creado correctamente.")
            return redirect('mensajeria:grupos-empresa')

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
    if request.user.rol != 'empresa':
        return redirect('/')

    notif = get_object_or_404(Notificacion, id=notif_id)
    notif.leida = True
    notif.save()
    return redirect('mensajeria:notificaciones-empresa')


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


# =========================
# DETALLE DE CHAT
# =========================
@login_required
def chat_detalle(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if request.user not in chat.participantes.all():
        messages.error(request, "No tienes permiso para acceder a este chat.")
        if request.user.rol == 'empresa':
            return redirect('mensajeria:panel-empresa')
        return redirect('mensajeria:panel-candidato')

    if request.method == 'POST':
        texto = request.POST.get('mensaje', '').strip()
        if texto:
            Mensaje.objects.create(
                chat=chat,
                remitente=request.user,
                texto=texto
            )
            return redirect('mensajeria:chat-detalle', chat.id)

    mensajes = chat.mensajes.all().order_by('fecha_envio')

    for m in mensajes:
        if request.user not in m.leido_por.all():
            m.leido_por.add(request.user)

    return render(request, 'mensajeria/chat_detalle.html', {
        'chat': chat,
        'mensajes': mensajes
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
