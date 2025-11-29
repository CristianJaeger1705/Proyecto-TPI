from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

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

    # ---------- NUEVOS CAMPOS ----------
    avatar = models.ImageField(upload_to="avatares/", blank=True, null=True)

    last_seen = models.DateTimeField(null=True, blank=True)

    # estado online
    @property
    def esta_en_linea(self):
        if not self.last_seen:
            return False
        return (timezone.now() - self.last_seen).seconds < 120  # 2 minutos

    def __str__(self):
        return f"{self.username} ({self.rol})"
