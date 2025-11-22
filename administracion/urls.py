from django.urls import path
from . import views

urlpatterns = [
    path('', views.panel_admin, name='panel_admin'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('usuarios/', views.admin_usuarios, name='admin_usuarios'),
    path('empresas/', views.admin_empresas, name='admin_empresas'),
    path('ofertas/', views.admin_ofertas, name='admin_ofertas'),
    path('postulaciones/', views.admin_postulaciones, name='admin_postulaciones'),
    path('usuarios/', views.gestionar_usuarios, name='gestionar_usuarios'),
    path('usuarios/activar/<int:user_id>/', views.activar_usuario, name='activar_usuario'),
    path('usuarios/desactivar/<int:user_id>/', views.desactivar_usuario, name='desactivar_usuario'),
    path('usuarios/verificar/<int:user_id>/', views.verificar_usuario, name='verificar_usuario'),
]
