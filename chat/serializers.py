from admin_user.models import AutoAnswerSetting
from profiles.serializers import *
from rest_framework import serializers

from .models import *


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


class MessageCreateSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer(read_only=True)
    sent_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'thread', 'text', 'sender', 'reply_to_message', 'sent_at']


class MessageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text']


class ThreadSerializer(serializers.ModelSerializer):
    student = ProfileSerializer(read_only=True)
    title = serializers.SerializerMethodField()
    text = serializers.CharField(write_only=True)

    def get_title(self, obj):
        return obj.title.question

    class Meta:
        model = Thread
        fields = ['id', 'student', 'title', 'text', 'course']
    
    def create(self, validated_data):
        course = validated_data['course']
        question, created = Question.objects.get_or_create(question=validated_data['text'], professor=course.professor)
        thread = Thread.objects.create(
            title=question,
            course=course,
            student=self.context.get('user')
        )
        message = Message.objects.create(
            thread=thread,
            text=validated_data['text'],
            sender=self.context.get('user')
        )
        if not created and question.answer and not AutoAnswerSetting.objects.first().is_off:
            Message.objects.create(
                thread=message.thread,
                text=question.answer,
                sender=message.thread.course.professor,
                reply_to_message=message
            )
        return thread
