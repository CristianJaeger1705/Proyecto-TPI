from django.urls import path
from . import views

app_name = "mensajeria"

urlpatterns = [
    # Conversaciones individuales + grupos
    path('', views.lista_conversaciones, name='lista_conversaciones'),

    # Chat individual
    path('chat/<str:username>/', views.chat_con_usuario, name='chat_con_usuario'),

    # AJAX individual
    path('ajax/enviar/<int:convo_id>/', views.ajax_enviar_mensaje, name='ajax_enviar_mensaje'),
    path('ajax/mensajes/<int:convo_id>/', views.obtener_mensajes_ajax, name='ajax_mensajes'),

    # Notificaciones
    path('ajax/notificaciones/', views.obtener_notificaciones_ajax, name='ajax_notificaciones'),
    path('ajax/notificacion/leida/<int:notif_id>/', views.marcar_notificacion_leida, name='ajax_notificacion_leida'),

    # Chat grupal
    path('grupo/<int:grupo_id>/', views.chat_grupo, name='chat_grupo'),

    # AJAX chat grupal
    path('grupo/ajax/enviar/<int:grupo_id>/', views.ajax_enviar_mensaje_grupo, name='ajax_enviar_grupo'),
    path('grupo/ajax/mensajes/<int:grupo_id>/', views.ajax_mensajes_grupo, name='ajax_mensajes_grupo'),

    # Crear / eliminar grupo
    path('grupo/crear/', views.crear_grupo, name='crear_grupo'),
    path('grupo/eliminar/<int:grupo_id>/', views.eliminar_grupo, name='eliminar_grupo'),

    path('api/nuevas/', views.api_nuevas, name='api_nuevas'),
    path('contactar/<int:oferta_id>/', views.contactar_empresa, name="contactar_empresa"),
    

]
