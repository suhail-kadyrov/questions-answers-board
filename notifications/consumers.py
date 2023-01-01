# chat/consumers.py
import json
from .models import Notification
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .serializers import NotificationSerializer
import pprint

class AdminConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_notifications(self):
        serializer = NotificationSerializer(Notification.objects.all(), many=True)
        return serializer.data

    async def connect(self):
        # room_name = self.scope["url_route"]["kwargs"]["id"]
        self.group_name = "admin"

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
        # message = event["message"]
        message = await self.get_notifications()

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))


class ProfessorConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_notifications(self):
        serializer = NotificationSerializer(Notification.objects.all(), many=True)
        return serializer.data

    async def connect(self):
        room_name = self.scope["url_route"]["kwargs"]["id"]
        self.group_name = "professor_" + str(room_name)

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
        # message = event["message"]
        message = await self.get_notifications()

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))


class StudentConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_notifications(self):
        serializer = NotificationSerializer(Notification.objects.all(), many=True)
        return serializer.data

    async def connect(self):
        room_name = self.scope["url_route"]["kwargs"]["id"]
        self.group_name = "student_" + str(room_name)

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
        # message = event["message"]
        message = await self.get_notifications()

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))
