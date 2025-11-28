# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ROLES = [
        ('admin', 'Administrador'),
        ('empresa', 'Empresa'),
        ('candidato', 'Candidato'),
    ]

    rol = models.CharField(max_length=20, choices=ROLES)
    verificado = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    codigo_verificacion = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.rol})"
    
import uuid
from django.db import models
from django.conf import settings

class SolicitudEmpresa(models.Model):
    estado = models.CharField(
        max_length=20,
        choices=[
            ("pendiente", "Pendiente"),
            ("aprobada", "Aprobada"),
            ("rechazada", "Rechazada"),
        ],
        default="pendiente"
    )
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    correo = models.EmailField()
    nombre_empresa = models.CharField(max_length=150)
   
    sitio_web = models.URLField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True)
    descripcion = models.TextField()
    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    token = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return self.nombre_empresa

