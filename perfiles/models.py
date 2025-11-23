# Create your models here.
from django.db import models
from usuarios.models import Usuario

class PerfilCandidato(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    profesion = models.CharField(max_length=100, blank=True)
    habilidades = models.TextField(blank=True)
    experiencia = models.TextField(blank=True)
    departamento = models.CharField(max_length=50, blank=True)
    cv_url = models.TextField(blank=True, null=True)
    disponibilidad = models.BooleanField(default=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"

class PerfilEmpresa(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombre_empresa = models.CharField(max_length=150)
    rubro = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True)
    sitio_web = models.CharField(max_length=200, blank=True)
    contacto = models.CharField(max_length=100, blank=True)
    verificada = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_empresa
