# Create your models here.
from django import forms
from django.db import models
from perfiles.models import PerfilEmpresa


class OfertaLaboral(models.Model):
    TIPOS = [
        ('formal', 'Formal'),
        ('temporal', 'Temporal'),
        ('freelance', 'Freelance'),
        ('pasantia', 'Pasantía'),
        ('primer_empleo', 'Primer Empleo'),
    ]
    
    empresa = models.ForeignKey(PerfilEmpresa, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=150)
    tipo_empleo = models.CharField(max_length=50, choices=TIPOS)
    descripcion = models.TextField()
    salario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ubicacion = models.CharField(max_length=100)
    fecha_publicacion = models.DateField(auto_now_add=True)
    fecha_expiracion = models.DateField(null=True, blank=True)  # ← NUEVO CAMPO
    estado = models.CharField(max_length=20, default='activa')

    def __str__(self):
        return f"{self.titulo} - {self.empresa.nombre_empresa}"
    
    # NUEVO: MODELO FAVORITO 

class Favorito(models.Model):
    usuario = models.ForeignKey(
        'usuarios.Usuario',           
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='favoritos'      
    )
    oferta = models.ForeignKey(
        'ofertas.OfertaLaboral',
        on_delete=models.CASCADE,
        related_name='favoritos_recibidos'
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'oferta', 'session_key')
        ordering = ['-fecha']

    def __str__(self):
        user = self.usuario.username if self.usuario else "Anónimo"
        return f"{user} → {self.oferta.titulo}"