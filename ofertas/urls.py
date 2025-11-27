from django.urls import path
from . import views

urlpatterns=[
    
    path('listaofertas',views.ofertas_List,name='ofertas'),
    path('eliminar/<int:id>',views.eliminar,name="eliminar"),
       # URLs nuevas para modal
    path('obtener-formulario-creacion/', views.obtener_formulario_creacion, name='obtener_formulario_creacion'),
    path('obtener-formulario-edicion/<int:id>/', views.obtener_formulario_edicion, name='obtener_formulario_edicion'),
    path('guardar-creacion/', views.guardar_creacion_modal, name='guardar_creacion_modal'),
    path('guardar-edicion/<int:id>/', views.guardar_edicion_modal, name='guardar_edicion_modal'),
    path('obtener-visualizacion/<int:id>/', views.obtener_datos_visualizacion, name='obtener_visualizacion'),
    path('', views.lista_ofertas_publicas, name='lista_ofertas_publicas'),
]