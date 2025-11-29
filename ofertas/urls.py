from django.urls import path
from . import views

app_name = 'ofertas'

urlpatterns = [
    # Listado de ofertas
    path('listaofertas/', views.ofertas_List, name='ofertas'),
    path('', views.listado_ofertas, name='listado_ofertas'),  # Ofertas públicas
    path('detalle/<int:oferta_id>/', views.detalle_oferta, name='detalle_oferta'),

    # CRUD y modales
    path('eliminar/<int:id>/', views.eliminar, name="eliminar"),
    path('obtener-formulario-creacion/', views.obtener_formulario_creacion, name='obtener_formulario_creacion'),
    path('obtener-formulario-edicion/<int:id>/', views.obtener_formulario_edicion, name='obtener_formulario_edicion'),
    path('guardar-creacion/', views.guardar_creacion_modal, name='guardar_creacion_modal'),
    path('guardar-edicion/<int:id>/', views.guardar_edicion_modal, name='guardar_edicion_modal'),
    path('obtener-visualizacion/<int:id>/', views.obtener_datos_visualizacion, name='obtener_visualizacion'),
]
