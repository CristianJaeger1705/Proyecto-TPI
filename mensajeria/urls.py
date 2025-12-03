from django.urls import path
from .views import (
    ChatListView,
    MensajeListView,
    MensajeCreateView,
    NotificacionListView,
   
    panel_empresa,
    panel_candidato,
    chats_empresa,
    grupos_empresa,
    notificaciones_empresa,
    eliminar_grupo,
    iniciar_chat,
    editar_grupo,
    chat_detalle,
    marcar_notificacion_leida,
    editar_chat,
    eliminar_chat,
)

app_name = 'mensajeria'

urlpatterns = [
    # Chats y mensajes
    path('chats/', ChatListView.as_view(), name='chats-list'),
    path('chats/<int:chat_id>/mensajes/', MensajeListView.as_view(), name='mensajes-list'),
    path('chats/<int:chat_id>/mensajes/crear/', MensajeCreateView.as_view(), name='mensaje-crear'),
    
    # Notificaciones
    path('notificaciones/', NotificacionListView.as_view(), name='notificaciones-list'),

    # Paneles
    path('empresa/panel/', panel_empresa, name='panel-empresa'),
    path('panel-candidato/', panel_candidato, name='panel-candidato'),

    # Chats y grupos de empresa
    path('empresa/chats/', chats_empresa, name='chats-empresa'),
    path('empresa/grupos/', grupos_empresa, name='grupos-empresa'),
    path('iniciar-chat/<int:oferta_id>/', iniciar_chat, name='iniciar_chat'),

    path('empresa/notificaciones/', notificaciones_empresa, name='notificaciones-empresa'),

    # CRUD de grupos
    path('empresa/grupos/eliminar/<int:grupo_id>/', eliminar_grupo, name='eliminar-grupo'),
    path('empresa/grupos/editar/<int:grupo_id>/', editar_grupo, name='editar-grupo'),

    # Marcar notificación como leída
    path('empresa/notificaciones/marcar/<int:notif_id>/', marcar_notificacion_leida, name='marcar-notificacion'),
    path('chats/<int:chat_id>/', chat_detalle, name='chat-detalle'),

    path('chat/<int:chat_id>/editar/', editar_chat, name='editar-chat'),
    path('chat/<int:chat_id>/eliminar/', eliminar_chat, name='eliminar-chat'),

]
