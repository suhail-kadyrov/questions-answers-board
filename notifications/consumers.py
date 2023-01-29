import json

import jwt
from authentication.models import CustomUser
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings


class Consumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_user(self, user_id):
        return CustomUser.objects.get(id=user_id)

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )

    async def receive(self, text_data):
        try:
            payload = jwt.decode(text_data, settings.SECRET_KEY, algorithms='HS256')
            user = await self.get_user(payload['user_id'])
        except:
            self.close()
        else:
            self.group_name = f"{user.role}_{user.id}"

        await self.channel_layer.group_add(
           self.group_name, self.channel_name
        )

    async def chat_message(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))
