from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# VISTAS USADAS EN AMBAS RAMAS
from ofertas.views import lista_ofertas_publicas
from aplicaciones.views import diagnostico_correo   # HEAD lo usa
# frank2 tenía hola_mundo, pero no se usa y no afecta
# from aplicaciones.views import hola_mundo

urlpatterns = [
    path('admin/', admin.site.urls),

    # Página principal
    path('', lista_ofertas_publicas, name='pagina_principal'),

    # Rutas principales del proyecto
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),
    path('ofertas/', include('ofertas.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path("postulaciones/", include("postulaciones.urls")),

    # Agregado desde rama-de-prueba2
    path('diagnostico-secreto/', diagnostico_correo),

    # Agregado desde frank2
    path('mensajeria/', include('mensajeria.urls')),
    path('perfiles/', include('perfiles.urls')),
]

# Servir Media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
