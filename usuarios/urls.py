from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Registro
    path('register/', views.registro, name='register'),

    # Login/Logout
    path("login/", views.login_view, name="login"),
    path("logout/", views.cerrar_sesion, name="logout"),

    # Recuperación y verificación de contraseñas
    path('verificar_codigo/', views.verificar_codigo, name='verificar_codigo'),
    path('recuperar_contrasena/', views.recuperar_contrasena, name='recuperar_contrasena'),
    path('verificar_codigo_recuperacion/', views.verificar_codigo_recuperacion, name='verificar_codigo_recuperacion'),
    path('nueva_contrasena_recuperacion/', views.nueva_contrasena_recuperacion, name='nueva_contrasena_recuperacion'),

    # Redirección según rol
    path('redirigir/', views.redirigir_segun_rol, name='redirigir'),

    # Perfiles - Visualización
    path('mi_perfil_candidato/', views.mi_perfil_candidato, name='mi_perfil_candidato'),
    path('mi_perfil_empresa/', views.mi_perfil_empresa, name='mi_perfil_empresa'),

    # Perfiles - Completar
    path('completar-perfil-candidato/', views.completar_perfil_candidato, name='completar_perfil_candidato'),
    path('completar-perfil-empresa/', views.completar_perfil_empresa, name='completar_perfil_empresa'),

    # Perfiles - Editar
    path('editar-perfil-candidato/', views.editar_perfil_candidato, name='editar_perfil_candidato'),
    path('editar-perfil-empresa/', views.editar_perfil_empresa, name='editar_perfil_empresa'),

    # Experiencias Laborales - CRUD
    path('experiencia/agregar/', views.agregar_experiencia, name='agregar_experiencia'),
    path('experiencia/editar/<int:experiencia_id>/', views.editar_experiencia, name='editar_experiencia'),
    path('experiencia/eliminar/<int:experiencia_id>/', views.eliminar_experiencia, name='eliminar_experiencia'),

    # API - Municipios
    path('api/municipios/<str:departamento>/', views.obtener_municipios, name='obtener_municipios'),
]
