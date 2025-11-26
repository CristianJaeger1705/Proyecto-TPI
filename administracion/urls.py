from django.urls import path
from . import views

urlpatterns = [
    path('', views.panel_admin, name='panel_admin'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('empresas/', views.admin_empresas, name='admin_empresas'),
    path('ofertas/', views.admin_ofertas, name='admin_ofertas'),
    path('postulaciones/', views.admin_postulaciones, name='admin_postulaciones'),
    path('usuarios/', views.gestionar_usuarios, name='gestionar_usuarios'),
    #path('usuarios/activar/<int:user_id>/', views.activar_usuario, name='activar_usuario'),
    #path('usuarios/desactivar/<int:user_id>/', views.desactivar_usuario, name='desactivar_usuario'),
    #path('usuarios/verificar/<int:user_id>/', views.verificar_usuario, name='verificar_usuario'),
    #path("usuarios/", views.lista_usuarios, name="lista_usuarios"),
    #path("usuarios/<int:usuario_id>/", views.usuario_detalle, name="usuario_detalle"),
    #path("usuarios/<int:usuario_id>/editar/", views.usuario_editar, name="usuario_editar"),
    #path("usuarios/<int:usuario_id>/eliminar/", views.usuario_eliminar, name="usuario_eliminar"),
     path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/activar/<int:user_id>/', views.activar_usuario, name='activar_usuario'),
    path('usuarios/desactivar/<int:user_id>/', views.desactivar_usuario, name='desactivar_usuario'),
    path('usuarios/verificar/<int:user_id>/', views.verificar_usuario, name='verificar_usuario'),
    path('crear/', views.crear_usuario, name='crear_usuario'),
]
