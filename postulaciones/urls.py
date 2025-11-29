from django.urls import path
from postulaciones import views

app_name = "postulaciones"

urlpatterns = [
    # Selección y postulación
    path("seleccionar-perfil/<int:oferta_id>/", views.seleccionar_perfil, name="seleccionar_perfil"),
    path("postular/<int:oferta_id>/", views.postular, name="postular"),

    # Postulaciones por ID
    path("<int:id>/", views.postular_con_id, name="postular_con_id"),
    path("cancelar/<int:id>/", views.cancelar_postulacion, name="cancelar_postulacion"),
    path("actualizar/<int:id>/", views.actualizar_postulacion, name="actualizar_postulacion"),
]
