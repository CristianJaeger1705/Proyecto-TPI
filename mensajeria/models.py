from django.db import models
from usuarios.models import Usuario
from ofertas.models import OfertaLaboral
from postulaciones.models import Postulacion

class Chat(models.Model):
    """
    Chat individual (uno a uno) o grupal (por oferta).
    """
    nombre = models.CharField(max_length=255, blank=True, null=True)
    es_grupal = models.BooleanField(default=False)
    oferta = models.ForeignKey(OfertaLaboral, on_delete=models.SET_NULL, null=True, blank=True)
    participantes = models.ManyToManyField(Usuario, related_name='chats')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre or f"Chat {self.id}"


class Mensaje(models.Model):
    """
    Mensajes enviados en un chat.
    """
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='mensajes')
    remitente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leido_por = models.ManyToManyField(Usuario, related_name='mensajes_leidos', blank=True)

    def __str__(self):
        return f"De {self.remitente.username} en {self.chat}"


class Notificacion(models.Model):
    """
    Notificaciones para los usuarios.
    """
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notif. {self.tipo} para {self.usuario.username}"
