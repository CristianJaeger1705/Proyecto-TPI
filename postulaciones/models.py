from django.db import models
from perfiles.models import PerfilCandidato
from ofertas.models import OfertaLaboral
from django.db.models.signals import post_save
from django.dispatch import receiver

class Postulacion(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    ]

    candidato = models.ForeignKey(PerfilCandidato, on_delete=models.CASCADE)
    oferta = models.ForeignKey(OfertaLaboral, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_postulacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('candidato', 'oferta')

    def __str__(self):
        return f"{self.candidato.usuario.username} → {self.oferta.titulo}"


@receiver(post_save, sender=Postulacion)
def crear_grupo_y_notificacion(sender, instance, created, **kwargs):
    if created:
        # Importamos aquí para evitar circular import
        from mensajeria.models import Chat
        Chat.crear_o_actualizar_grupo_por_postulacion(instance)
