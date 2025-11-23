from django.urls import path
from postulaciones.views import *

urlpatterns = [
    path("<int:id>/", postular_con_id, name="postular_con_id"),
    path("cancelar/<int:id>/", cancelar_postulacion, name="cancelar_postulacion"),
]
