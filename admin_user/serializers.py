from authentication.models import *
from course.models import Course
from pyexpat import model
from rest_framework import serializers
from profiles.serializers import ProfileSerializer


class UsersListSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()

    def get_courses(self, obj):
        if obj.role == 'STUDENT':
            return obj.enrolled_courses.count()
        return obj.courses.count()
    
    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'email', 'role', 'courses']


class LoginAttemptsSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    capture = serializers.ImageField(allow_empty_file=True, use_url=True, read_only=True)

    class Meta:
        model = LoginAttempt
        fields = ['id', 'user', 'time', 'capture',]


class AdminCourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'semester', 'professor', 'students', 'is_completed']
    