from rest_framework import serializers
from uuid import uuid4
from authentication.models import *
from course.models import *
from profiles.serializers import ProfileSerializer


class CoursesListSerializers(serializers.ModelSerializer):
    name = serializers.CharField(max_length=150)
    professor = ProfileSerializer(read_only=True)
    semester = serializers.CharField(max_length=150)
    started_at = serializers.DateField()
    is_completed = serializers.BooleanField(default=False)

    class Meta:
        model = Course
        fields = ['id', 'name', 'professor', 'semester', 'started_at', 'is_completed',]


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
        new_token = uuid4()
        while bool(Course.objects.filter(token=new_token)):
            new_token = uuid4()
        course.token = new_token
        course.students.set(validated_data['students'])
        course.save()
        return course

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.semester = validated_data.get('semester', instance.semester)
    #     instance.save()
    #     return instance
