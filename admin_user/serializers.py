from authentication.models import CustomUser
from course.models import Course
from pyexpat import model
from rest_framework import serializers


class UsersListSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()

    def get_courses(self, obj):
        if obj.role == 'STUDENT':
            return obj.enrolled_courses.count()
        return obj.courses.count()
    
    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'email', 'role', 'courses']


class AdminCourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'semester', 'professor', 'students', 'is_completed']
    