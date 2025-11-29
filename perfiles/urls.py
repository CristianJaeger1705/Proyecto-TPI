from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'perfiles'

urlpatterns = [
    path('', views.perfil_inicio, name='inicio'),
    path('candidato/', views.perfil_candidato, name='perfil_candidato'),
    path('empresa/', views.perfil_empresa, name='perfil_empresa'),
    path('dashboard/candidato/', views.dashboard_candidato, name='dashboard_candidato'),
    path('dashboard/empresa/', views.dashboard_empresa, name='dashboard_empresa'),
]

# Solo en desarrollo, sirve los archivos media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
