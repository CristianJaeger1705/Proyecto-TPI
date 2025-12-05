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
    panel_admin,
    actualizar_notificaciones_admin,
    enviar_mensaje_automatico,
    eliminar_notificacion,
    obtener_mensajes_no_vistos,
    chat_mensajes_ajax,
)

app_name = 'mensajeria'

urlpatterns = [
    # -----------------------
    # API Chats y Mensajes
    # -----------------------
    path('chats/', ChatListView.as_view(), name='chats-list'),
    path('chats/<int:chat_id>/mensajes/', MensajeListView.as_view(), name='mensajes-list'),
    path('chats/<int:chat_id>/mensajes/crear/', MensajeCreateView.as_view(), name='mensaje-crear'),
    path('chat/<int:chat_id>/mensajes-json/', MensajeListView.as_view(), name='mensajes-json'),

    # -----------------------
    # Notificaciones
    # -----------------------
    path('notificaciones/', NotificacionListView.as_view(), name='notificaciones-list'),

    # -----------------------
    # Paneles
    # -----------------------
    path('empresa/panel/', panel_empresa, name='panel-empresa'),
    path('panel-candidato/', panel_candidato, name='panel-candidato'),
    path('admin/panel/', panel_admin, name='panel-admin'),

    # -----------------------
    # Chats y grupos empresa
    # -----------------------
    path('empresa/chats/', chats_empresa, name='chats-empresa'),
   # Para template de empresa
    path('iniciar-chat/<int:oferta_id>/', iniciar_chat, name='iniciar_chat'),
    path('empresa/grupos/', grupos_empresa, name='grupos-empresa'),
    path('empresa/grupos/eliminar/<int:grupo_id>/', eliminar_grupo, name='eliminar-grupo'),
    path('empresa/grupos/editar/<int:grupo_id>/', editar_grupo, name='editar-grupo'),

    # -----------------------
    # Notificaciones empresa
    # -----------------------
    path('empresa/notificaciones/', notificaciones_empresa, name='notificaciones-empresa'),
    # urls.py
    # Notificaciones empresa/admin
    path('notificaciones/marcar/<int:notif_id>/', marcar_notificacion_leida, name='marcar-notificacion-leida'),

    # Eliminar notificación admin
# Eliminar notificación empresa
    path('empresa/notificaciones/eliminar/<int:notif_id>/', eliminar_notificacion, name='eliminar-notificacion'),
    path('chat/<int:chat_id>/ajax/', chat_mensajes_ajax, name='chat_mensajes_ajax'),



    # -----------------------
    # Edición y eliminación de chats
    # -----------------------
    path('chats/<int:chat_id>/editar/', editar_chat, name='editar-chat'),
    path('empresa/chat/<int:chat_id>/eliminar/', eliminar_chat, name='eliminar-chat-empresa'),
    path('admin/chat/<int:chat_id>/eliminar/', eliminar_chat, name='eliminar-chat-admin'),

    # -----------------------
    # Panel y chats admin/empresa
    # -----------------------
    # Detalle de chat
   # urls.py
    path('chats/<int:chat_id>/', chat_detalle, name='chat-detalle'),

    path('chats/<int:chat_id>/mensaje-automatico/', enviar_mensaje_automatico, name='mensaje-automatico'),


    path('api/mensajes-no-vistos/', obtener_mensajes_no_vistos, name='api-mensajes-no-vistos'),



    # -----------------------
    # Notificaciones admin
    # -----------------------
    path('admin/actualizar-notificaciones/', actualizar_notificaciones_admin, name='actualizar-notificaciones-admin'),
]


