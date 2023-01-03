# chat/consumers.py
import json
from .models import Notification
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .serializers import NotificationSerializer
import pprint

class AdminConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "ADMIN"

        await self.channel_layer.group_add(
            self.group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        data = text_data_json["data"]

        await self.channel_layer.group_send(
            self.group_name, {"type": "chat_message", "message": data}
        )
    
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))


class ProfessorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        room_name = self.scope["url_route"]["kwargs"]["id"]
        self.group_name = "PROFESSOR_" + str(room_name)

        await self.channel_layer.group_add(
            self.group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.channel_layer.group_send(
            self.group_name, {"type": "chat_message", "message": message}
        )
    
    async def chat_message(self, event):
        is_message = event['is_message']
        data = event['data']
        print('event: ', event)

        # Send message to WebSocket
        await self.send(text_data=json.dumps(data))


class StudentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        room_name = self.scope["url_route"]["kwargs"]["id"]
        self.group_name = "STUDENT_" + str(room_name)

        await self.channel_layer.group_add(
            self.group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        data = text_data_json["data"]

        await self.channel_layer.group_send(
            '{}_{}'.format(data['receiver'], data['id']), {"type": "chat_message", "message": data}
        )
    
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))
