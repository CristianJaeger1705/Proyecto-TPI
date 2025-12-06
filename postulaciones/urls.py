from django.urls import path
from postulaciones.views import *

urlpatterns = [
    path("<int:id>/", postular_con_id, name="postular_con_id"),
    path("cancelar/<int:id>/", cancelar_postulacion, name="cancelar_postulacion"),
    path("actualizar/<int:id>/", actualizar_postulacion, name="actualizar_postulacion"),
    path("postulaciones-empresa/", ver_postulaciones_pendientes, name="postulaciones_empresa"),
    path("postulaciones-empresa/<int:empresa_id>/", ver_postulaciones_pendientes, name="postulaciones_empresa"),
]
