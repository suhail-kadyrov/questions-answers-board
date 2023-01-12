from rest_framework import serializers
from .models import *


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    thread = ThreadSerializer()

    class Meta:
        model = Message
        fields = ['id', 'thread', 'text', 'sent_at', 'sender']