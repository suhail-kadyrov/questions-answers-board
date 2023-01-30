from admin_user.models import AutoAnswerSetting
from profiles.serializers import *
from rest_framework import serializers
from notifications.models import Notification

from .models import *


class RepliedMessageSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'text', 'sender',]


class MessageSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer(read_only=True)
    reply_to_message = RepliedMessageSerializer(read_only=True)
    is_edited = serializers.BooleanField(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'thread', 'text', 'sent_at', 'is_edited', 'sender', 'reply_to_message']


class MessageCreateSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer(read_only=True)
    sent_at = serializers.DateTimeField(read_only=True)
    is_edited = serializers.BooleanField(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'thread', 'text', 'sender', 'is_edited', 'reply_to_message', 'sent_at']


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
        else:
            Notification.objects.create(
                name='PROFESSOR_NEW_QUESTION',
                text=f'You have new question in {thread.course.name}',
                receiver=thread.course.professor,
                user=message.sender,
                course=thread.course,
                message=message
            )
        return thread
