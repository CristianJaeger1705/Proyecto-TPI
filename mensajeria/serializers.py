from rest_framework import serializers
from .models import Chat, Mensaje, Notificacion
from usuarios.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'rol']

class MensajeSerializer(serializers.ModelSerializer):
    remitente = UsuarioSerializer(read_only=True)

    class Meta:
        model = Mensaje
        fields = ['id', 'chat', 'remitente', 'texto', 'fecha_envio', 'leido_por']

class ChatSerializer(serializers.ModelSerializer):
    participantes = UsuarioSerializer(many=True, read_only=True)
    mensajes = MensajeSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'nombre', 'es_grupal', 'oferta', 'participantes', 'mensajes']

class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = ['id', 'tipo', 'mensaje', 'leida', 'fecha']
