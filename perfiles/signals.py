from django.db.models.signals import post_save
from django.dispatch import receiver
from usuarios.models import Usuario
from .models import PerfilCandidato, PerfilEmpresa

@receiver(post_save, sender=Usuario)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        if instance.rol == "candidato":
            PerfilCandidato.objects.create(usuario=instance)
        elif instance.rol == "empresa":
            PerfilEmpresa.objects.create(usuario=instance)
