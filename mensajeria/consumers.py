import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat, Mensaje
from .serializers import MensajeSerializer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'

        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        mensaje_texto = data['mensaje']
        usuario_id = self.scope['user'].id

        mensaje = await self.guardar_mensaje(usuario_id, self.chat_id, mensaje_texto)

        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'mensaje': MensajeSerializer(mensaje).data
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['mensaje']))

    @database_sync_to_async
    def guardar_mensaje(self, usuario_id, chat_id, texto):
        chat = Chat.objects.get(id=chat_id)
        usuario = chat.participantes.get(id=usuario_id)
        mensaje = Mensaje.objects.create(chat=chat, remitente=usuario, texto=texto)
        return mensaje
