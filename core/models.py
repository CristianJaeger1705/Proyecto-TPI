
# Create your models here.
# apps/core/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from postulaciones.models import Postulacion
from mensajeria.models import Notificacion

@receiver(post_save, sender=Postulacion)
def notificar_postulacion(sender, instance, created, **kwargs):
    if created:
        Notificacion.objects.create(
            usuario=instance.oferta.empresa.usuario,
            tipo='Nueva Postulación',
            mensaje=f"{instance.candidato.usuario.username} aplicó a tu oferta {instance.oferta.titulo}",
        )
