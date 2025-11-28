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
from aplicaciones.views import *
#from ofertas.views import obtener_datos_visualizacion
from ofertas.views import lista_ofertas_publicas
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', lista_ofertas_publicas, name='pagina_principal'), 
    path('', lista_ofertas_publicas, name='pagina_principal'),  # La página de prueba será nuestra página principal por ahora
    #quien haga el login tiene que cambiar el hola mundo por la del login
    #Urls necesaria para el funcionamiento del modulo ofertas
    path('ofertas/',include('ofertas.urls')),
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('django.contrib.auth.urls')), 
    path("postulaciones/", include("postulaciones.urls")),
    
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
