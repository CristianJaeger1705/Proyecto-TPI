from django.contrib import admin
from postulaciones.models import Postulacion

@admin.register(Postulacion)
class PostulacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'oferta', 'candidato', 'fecha_postulacion', 'estado')
    list_filter = ('estado', 'fecha_postulacion')
    search_fields = ('oferta__titulo', 'candidato__usuario__username')


