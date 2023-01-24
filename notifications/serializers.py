from .models import Notification
from rest_framework import serializers
from profiles.serializers import ProfileSerializer
from course.serializers import CourseSerializer
from chat.serializers import *


class NotificationSerializer(serializers.ModelSerializer):
    receiver = ProfileSerializer()
    user = ProfileSerializer()
    course = CourseSerializer()
    message = MessageSerializer()

    class Meta:
        model = Notification
        fields = ['id', 'name', 'text', 'receiver', 'sent_at', 'user', 'course', 'message', 'is_seen']
