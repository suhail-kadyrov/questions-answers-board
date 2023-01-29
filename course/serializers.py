from uuid import uuid4

from authentication.models import *
from notifications.models import Notification
from profiles.serializers import ProfileSerializer
from rest_framework import serializers

from course.models import *


class CoursesListSerializers(serializers.ModelSerializer):
    name = serializers.CharField(max_length=150)
    professor = ProfileSerializer(read_only=True)
    semester = serializers.CharField(max_length=150)
    started_at = serializers.DateField()
    is_completed = serializers.BooleanField(default=False)
    students = serializers.SerializerMethodField()

    def get_students(self, obj):
        return obj.students.count()

    class Meta:
        model = Course
        fields = ['id', 'name', 'professor', 'semester', 'started_at', 'is_completed', 'students']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'semester', 'started_at', 'is_completed', 'students',]

    def create(self, validated_data):
        course = Course.objects.create(
            name = validated_data['name'],
            semester = validated_data['semester'],
            started_at = validated_data['started_at'],
            professor = self.context.get('user')
        )
        course.students.set(validated_data['students'])
        course.save()
        notification = list(map(
            lambda s: Notification(
                name='STUDENT_INVITED',
                text=f'{course.professor.full_name} has invited you to {course.name}',
                receiver=s,
                user=course.professor,
                course=course,
            ),
            validated_data['students']
        ))
        Notification.objects.bulk_create(notification)
        Notification.objects.create(
            name='ADMIN_NEW_COURSE',
            text=f'{course.professor.full_name} has created new course - {course.name}',
            receiver=CustomUser.objects.get(role='ADMIN'),
            user=course.professor,
            course=course,
        )
        return course
