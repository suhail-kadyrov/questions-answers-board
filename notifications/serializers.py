from chat.serializers import *
from course.serializers import CourseSerializer
from profiles.serializers import ProfileSerializer
from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    receiver = ProfileSerializer()
    user = ProfileSerializer()
    course = CourseSerializer()
    message = MessageSerializer()

    class Meta:
        model = Notification
        fields = ['id', 'name', 'text', 'receiver', 'sent_at', 'user', 'course', 'message', 'is_seen']
