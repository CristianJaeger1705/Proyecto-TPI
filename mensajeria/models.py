from django.db import models
from django.utils import timezone
from usuarios.models import Usuario


# ============================================================
#  CONVERSACIONES INDIVIDUALES
# ============================================================
class ConversacionManager(models.Manager):
    def get_or_create_individual(self, usuario_a, usuario_b):
        usuarios = sorted([usuario_a, usuario_b], key=lambda u: u.id)

        conversacion = self.filter(
            participantes=usuarios[0]
        ).filter(
            participantes=usuarios[1]
        ).first()

        if conversacion:
            return conversacion, False

        nueva = self.create()
        nueva.participantes.add(usuarios[0], usuarios[1])
        return nueva, True


class Conversacion(models.Model):
    participantes = models.ManyToManyField(Usuario, related_name="conversaciones")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    objects = ConversacionManager()

    @property
    def mensajes(self):
        return self.mensaje_set.all()

    def __str__(self):
        return " - ".join([u.username for u in self.participantes.all()])


# Mensajes individuales
class Mensaje(models.Model):
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE)
    remitente = models.ForeignKey(Usuario, related_name="mensajes_enviados", on_delete=models.CASCADE)
    destinatario = models.ForeignKey(Usuario, related_name="mensajes_recibidos", on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_envio = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=20, default="enviado")

    def __str__(self):
        return f"{self.remitente} → {self.destinatario}: {self.texto[:20]}"


# ============================================================
#  NOTIFICACIONES
# ============================================================
class Notificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=30)
    mensaje = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)
    leida = models.BooleanField(default=False)

    @staticmethod
    def obtener_no_leidas(usuario):
        return Notificacion.objects.filter(usuario=usuario, leida=False)


# ============================================================
#  CHAT GRUPAL
# ============================================================
class GrupoConversacion(models.Model):
    empresa = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="grupos_empresa")
    postulantes = models.ManyToManyField(Usuario, related_name="grupos_postulantes")
    oferta = models.ForeignKey("ofertas.OfertaLaboral", on_delete=models.CASCADE, null=True, blank=True)

    nombre = models.CharField(max_length=200)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre}"


class MensajeGrupo(models.Model):
    grupo = models.ForeignKey(GrupoConversacion, on_delete=models.CASCADE, related_name="mensajes")
    remitente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_envio = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.remitente}: {self.texto[:20]}"
