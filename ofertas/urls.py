from django.urls import path
from . import views

urlpatterns=[
    
    path('ofertas',views.ofertas_List,name='ofertas'),
    path('ofertas/agregar',views.agregar_Campos,name="agregar"),
    path('ofertas/editar/<int:id>',views.editar_Campo,name="editar"),
]