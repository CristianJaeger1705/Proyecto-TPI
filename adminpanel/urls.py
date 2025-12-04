"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
#from django.conf import settings
from django.conf.urls.static import static
from adminpanel.views import *
#from ofertas.views import obtener_datos_visualizacion
from ofertas.views import lista_ofertas_publicas
from django.conf import settings
#from aplicaciones.views import test_brevo, debug_smtp    

urlpatterns = [
    path('dashboard_admin', dashboard_admin, name='dashboard_admin'),

    #SOLICITUDES
    path("solicitudes/", listar_solicitudes, name="listar_solicitudes"),
    path("solicitudes/historial/", historial_solicitudes, name="historial_solicitudes"),
    path("solicitud/<int:id>/aprobar/", aprobar_solicitud, name="aprobar_solicitud"),
    path("solicitud/<int:id>/rechazar/", rechazar_solicitud, name="rechazar_solicitud"),
    path("solicitud/<int:id>/ver/", ver_solicitud, name="ver_solicitud"),

    #USUARIOS
    path('usuarios/crear/', crear_usuario, name='crear_usuario'),
    path('usuarios/detalle/<int:usuario_id>/', usuario_detalle, name='usuario_detalle'),
    path('usuarios/activar/<int:user_id>/', activar_usuario, name='activar_usuario'),
    path('usuarios/desactivar/<int:user_id>/', desactivar_usuario, name='desactivar_usuario'),
    path('usuarios/verificar/<int:user_id>/', verificar_usuario, name='verificar_usuario'),
    path('usuarios/<int:usuario_id>/quitar-verificacion/', quitar_verificacion_usuario, name='quitar_verificacion_usuario'),
    path("usuarios/candidatos/", listar_candidatos, name="listar_candidatos"),
    path("usuarios/empresas/", listar_empresas, name="listar_empresas"),

]