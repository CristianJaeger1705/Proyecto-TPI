from django.urls import path
from . import views

urlpatterns = [
    path('', views.panel_admin, name='panel_admin'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('usuarios/', views.admin_usuarios, name='admin_usuarios'),
    path('empresas/', views.admin_empresas, name='admin_empresas'),
    path('ofertas/', views.admin_ofertas, name='admin_ofertas'),
    path('postulaciones/', views.admin_postulaciones, name='admin_postulaciones'),
]
