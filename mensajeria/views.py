from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Chat, Mensaje, Notificacion
from .serializers import ChatSerializer, MensajeSerializer, NotificacionSerializer

# Listar chats del usuario
class ChatListView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.chats.all().order_by('-fecha_creacion')

# Listar mensajes de un chat
class MensajeListView(generics.ListAPIView):
    serializer_class = MensajeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        chat = Chat.objects.get(id=chat_id)
        if self.request.user in chat.participantes.all():
            return chat.mensajes.all().order_by('fecha_envio')
        return Mensaje.objects.none()

# Crear mensaje (no en tiempo real, solo API REST)
class MensajeCreateView(generics.CreateAPIView):
    serializer_class = MensajeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(remitente=self.request.user)

# Listar notificaciones
class NotificacionListView(generics.ListAPIView):
    serializer_class = NotificacionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notificacion.objects.filter(usuario=self.request.user).order_by('-fecha')
