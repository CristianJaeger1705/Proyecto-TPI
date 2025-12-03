from django.db import models
from usuarios.models import Usuario
from ofertas.models import OfertaLaboral


class Chat(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    es_grupal = models.BooleanField(default=False)
    oferta = models.ForeignKey(
        OfertaLaboral,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chats'
    )
    participantes = models.ManyToManyField('usuarios.Usuario', related_name='chats')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre or f"Chat {self.id}"


    @staticmethod
    def crear_o_actualizar_grupo_por_postulacion(postulacion):
        from .models import Notificacion  # evita import circular
        oferta = postulacion.oferta
        empresa = oferta.empresa.usuario

        grupo, creado = Chat.objects.get_or_create(
            es_grupal=True,
            oferta=oferta,
            defaults={'nombre': f'Grupo - {oferta.titulo}'}
        )

        grupo.participantes.add(postulacion.candidato.usuario, empresa)
        grupo.save()

        Notificacion.objects.create(
            usuario=postulacion.candidato.usuario,
            tipo='grupo',
            mensaje=f"Has sido agregado al grupo de la oferta '{oferta.titulo}'"
        )

        return grupo


class Mensaje(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='mensajes')
    remitente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensajes_enviados')
    texto = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leido_por = models.ManyToManyField(Usuario, related_name='mensajes_leidos', blank=True)

    def __str__(self):
        return f"De {self.remitente.username} a {self.destinatario.username}"


class Notificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notif. {self.tipo} para {self.usuario.username}"
