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
#from aplicaciones.views import hola_mundo
from ofertas.views import obtener_datos_visualizacion


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', obtener_datos_visualizacion, name='pagina_principal'), 
    #path('', hola_mundo, name='hola_mundo'),  # La página de prueba será nuestra página principal por ahora
    #quien haga el login tiene que cambiar el hola mundo por la del login
    #Urls necesaria para el funcionamiento del modulo ofertas
    path('ofertas/',include('ofertas.urls')),
    path('usuarios/',include('usuarios.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    path("postulaciones/", include("postulaciones.urls")),
]
