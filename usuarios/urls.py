from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('register/', views.registro, name='register'),
    path('mi_perfil_candidato/', views.mi_perfil_candidato, name='mi_perfil_candidato'),
    path('mi_perfil_empresa/', views.mi_perfil_empresa, name='mi_perfil_empresa'),
    path('redirigir/', views.redirigir_segun_rol, name='redirigir_segun_rol'),

    # LOGIN correcto (solo este)
    path("login/", views.login_view, name="login"),

    # LOGOUT
    path("logout/", views.cerrar_sesion, name="logout"),

    path('verificar_codigo/', views.verificar_codigo, name='verificar_codigo'),
    path('recuperar_contrasena/', views.recuperar_contrasena, name='recuperar_contrasena'),
    path('verificar_codigo_recuperacion/', views.verificar_codigo_recuperacion, name='verificar_codigo_recuperacion'),
    path('nueva_contrasena_recuperacion/', views.nueva_contrasena_recuperacion, name='nueva_contrasena_recuperacion'),
]
