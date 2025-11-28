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



