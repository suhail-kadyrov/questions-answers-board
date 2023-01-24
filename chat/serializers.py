from rest_framework import serializers
from .models import *
from profiles.serializers import *
from course.serializers import CoursesListSerializers


class RepliedMessageSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'text', 'sender',]


class MessageSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer(read_only=True)
    reply_to_message = RepliedMessageSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'thread', 'text', 'sent_at', 'sender', 'reply_to_message']


class ThreadSerializer(serializers.ModelSerializer):
    student = ProfileSerializer(read_only=True)
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.title.question

    class Meta:
        model = Thread
        fields = ['student', 'title']
