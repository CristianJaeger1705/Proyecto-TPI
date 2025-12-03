from django.db.models.signals import post_save
from django.dispatch import receiver
from postulaciones.models import Postulacion
from .models import Chat, Notificacion

@receiver(post_save, sender=Postulacion)
def crear_chat_grupal_postulacion(sender, instance, created, **kwargs):
    """
    Cuando un candidato se postula a una oferta, crear chat grupal automáticamente
    para esa oferta si no existía, y agregar al candidato + empresa.
    """
    if created:
        oferta = instance.oferta
        candidato = instance.candidato.usuario
        empresa_usuario = oferta.empresa.usuario

        # Verificar si ya existe un chat grupal para esta oferta
        chat, created_chat = Chat.objects.get_or_create(
            es_grupal=True,
            oferta=oferta,
            defaults={'nombre': f"Grupo {oferta.titulo}"}
        )

        # Agregar participantes si no están
        chat.participantes.add(candidato)
        chat.participantes.add(empresa_usuario)
        chat.save()

        # Crear notificación para el candidato
        Notificacion.objects.create(
            usuario=candidato,
            tipo="Grupo de oferta",
            mensaje=f"Has sido agregado al grupo de la oferta '{oferta.titulo}'"
        )

        # Crear notificación para la empresa si el chat es nuevo
        if created_chat:
            Notificacion.objects.create(
                usuario=empresa_usuario,
                tipo="Nuevo grupo",
                mensaje=f"Se ha creado un grupo para la oferta '{oferta.titulo}'"
            )
