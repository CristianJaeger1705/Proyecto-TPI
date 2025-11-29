from django.urls import path
from . import views

app_name = 'ofertas'

urlpatterns=[

    path('listaofertas/', views.ofertas_List, name='ofertas'),
    path('eliminar/<int:id>/', views.eliminar, name="eliminar"),

    # URLs nuevas para modal
    path('obtener-formulario-creacion/', views.obtener_formulario_creacion, name='obtener_formulario_creacion'),
    path('obtener-formulario-edicion/<int:id>/', views.obtener_formulario_edicion, name='obtener_formulario_edicion'),
    path('guardar-creacion/', views.guardar_creacion_modal, name='guardar_creacion_modal'),
    path('guardar-edicion/<int:id>/', views.guardar_edicion_modal, name='guardar_edicion_modal'),
    path('', views.listado_ofertas, name='listado_ofertas'),  # Asegúrate de esto
    path('detalle/<int:oferta_id>/', views.detalle_oferta, name='detalle_oferta'),
]
