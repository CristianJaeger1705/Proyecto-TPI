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
from django.urls import path
from usuarios.views import *
app_name = 'usuarios'

urlpatterns = [
    # Autenticación (Módulo 1)
    path('register/', registro, name='register'),
    path("login/", CustomLoginView.as_view(template_name="registration/login.html"), name="login"),
    path('logout/', exit, name='exit'),
    path('verificar_codigo/', verificar_codigo, name='verificar_codigo'),
    path('recuperar_contrasena/', recuperar_contrasena, name='recuperar_contrasena'),
    path('verificar_codigo_recuperacion/', verificar_codigo_recuperacion, name='verificar_codigo_recuperacion'),
    path('nueva_contrasena_recuperacion/', nueva_contrasena_recuperacion, name='nueva_contrasena_recuperacion'),
    path("solicitar-empresa/", solicitar_empresa, name="solicitar_empresa"),
    path("registrar_empresa/<uuid:token>/", crear_cuenta_empresa, name="registrar_empresa"),
    # Redirección
    path('redirigir/', redirigir_según_rol, name='redirigir'),
    
    # Perfiles - Visualización (Módulo 2)
    path('mi_perfil_candidato/', mi_perfil_candidato, name='mi_perfil_candidato'),
    path('mi_perfil_empresa/', mi_perfil_empresa, name='mi_perfil_empresa'),
    
    # Perfiles - Completar (Módulo 2)
    path('completar-perfil-candidato/', completar_perfil_candidato, name='completar_perfil_candidato'),
    path('completar-perfil-empresa/', completar_perfil_empresa, name='completar_perfil_empresa'),
    
    # Perfiles - Editar (Módulo 2)
    path('editar-perfil-candidato/', editar_perfil_candidato, name='editar_perfil_candidato'),
    path('editar-perfil-empresa/', editar_perfil_empresa, name='editar_perfil_empresa'),
    
    # Experiencias Laborales - CRUD (Módulo 2)
    path('experiencia/agregar/', agregar_experiencia, name='agregar_experiencia'),
    path('experiencia/editar/<int:experiencia_id>/', editar_experiencia, name='editar_experiencia'),
    path('experiencia/eliminar/<int:experiencia_id>/', eliminar_experiencia, name='eliminar_experiencia'),
    
    # API - Municipios
    path('api/municipios/<str:departamento>/', obtener_municipios, name='obtener_municipios'),

    #para dejar reviews
    path("resenas/", listar_resenas, name="listar_resenas"),
    path("reseñas/nueva/", crear_review, name="crear_reseña"),
]
